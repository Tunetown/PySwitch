/**
 * Tests for the client aware imports of the parser: actions and mappings of different clients can have the same
 * name. They are imported by client, and with an alias (<CLIENT>_<NAME>) if several clients' functions with the same
 * name are used in one file. Spec: claude/spec/emulator/parser.md
 */
class ClientImportsTests extends TestBase {

    static IMPORT_KEMPER_TAP_TEMPO = "from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO";
    static IMPORT_FRACTAL_TAP_TEMPO = "from pyswitch.clients.fractal.actions.tap_tempo import TAP_TEMPO";

    /**
     * Only one client uses the name: plain import from that client
     */
    async singleClient() {
        for (const client of ["kemper", "fractal"]) {
            const config = await this.#config([], []);
            const src = await this.#setActions(config, [["TAP_TEMPO", client]]);

            expect(src).toContain(client == "kemper" ? ClientImportsTests.IMPORT_KEMPER_TAP_TEMPO + "\n" : ClientImportsTests.IMPORT_FRACTAL_TAP_TEMPO + "\n");
            expect(src).not.toContain(client == "kemper" ? "pyswitch.clients.fractal" : "pyswitch.clients.kemper");
            expect(src).not.toContain(" as ");

            await this.#expectActions(config, [["TAP_TEMPO", client]]);
        }
    }

    /**
     * Two clients use the same name: both are imported with an alias, reading resolves name and client
     */
    async twoClients() {
        const config = await this.#config([], []);
        const src = await this.#setActions(config, [["TAP_TEMPO", "fractal"], ["TAP_TEMPO", "kemper"], ["BANK_SELECT", "kemper"]]);

        expect(src).toContain(ClientImportsTests.IMPORT_FRACTAL_TAP_TEMPO + " as FRACTAL_TAP_TEMPO\n");
        expect(src).toContain(ClientImportsTests.IMPORT_KEMPER_TAP_TEMPO + " as KEMPER_TAP_TEMPO\n");
        expect(src).toContain("FRACTAL_TAP_TEMPO()");
        expect(src).toContain("KEMPER_TAP_TEMPO()");

        // BANK_SELECT is only used by one client here: no alias
        expect(src).toContain("from pyswitch.clients.kemper.actions.bank_select import BANK_SELECT\n");

        await this.#expectActions(config, [["TAP_TEMPO", "fractal"], ["TAP_TEMPO", "kemper"], ["BANK_SELECT", "kemper"]]);
    }

    /**
     * The client which is already imported without alias keeps the plain name
     */
    async existingPlainImport() {
        const config = await this.#config(
            [ClientImportsTests.IMPORT_KEMPER_TAP_TEMPO],
            ["TAP_TEMPO()"]
        );
        await this.#expectActions(config, [["TAP_TEMPO", "kemper"]]);

        const src = await this.#setActions(config, [["TAP_TEMPO", "kemper"], ["TAP_TEMPO", "fractal"]]);

        expect(src).toContain(ClientImportsTests.IMPORT_KEMPER_TAP_TEMPO + "\n");
        expect(src).toContain(ClientImportsTests.IMPORT_FRACTAL_TAP_TEMPO + " as FRACTAL_TAP_TEMPO\n");
        expect(src).toContain("            TAP_TEMPO(),");
        expect(src).toContain("FRACTAL_TAP_TEMPO()");

        await this.#expectActions(config, [["TAP_TEMPO", "kemper"], ["TAP_TEMPO", "fractal"]]);
    }

    /**
     * Changing the client of an action replaces the import
     */
    async changeClient() {
        const config = await this.#config(
            [ClientImportsTests.IMPORT_KEMPER_TAP_TEMPO],
            ["TAP_TEMPO()"]
        );

        const src = await this.#setActions(config, [["TAP_TEMPO", "fractal"]]);

        expect(src).toContain(ClientImportsTests.IMPORT_FRACTAL_TAP_TEMPO + "\n");
        expect(src).not.toContain("pyswitch.clients.kemper");

        await this.#expectActions(config, [["TAP_TEMPO", "fractal"]]);
    }

    /**
     * When only one of the aliased clients is left, its alias is removed again
     */
    async removeAlias() {
        const config = await this.#config(
            [
                ClientImportsTests.IMPORT_FRACTAL_TAP_TEMPO + " as FRACTAL_TAP_TEMPO",
                ClientImportsTests.IMPORT_KEMPER_TAP_TEMPO + " as KEMPER_TAP_TEMPO"
            ],
            ["FRACTAL_TAP_TEMPO()", "KEMPER_TAP_TEMPO()"]
        );
        await this.#expectActions(config, [["TAP_TEMPO", "fractal"], ["TAP_TEMPO", "kemper"]]);

        const src = await this.#setActions(config, [["TAP_TEMPO", "fractal"]]);

        expect(src).toContain(ClientImportsTests.IMPORT_FRACTAL_TAP_TEMPO + "\n");
        expect(src).not.toContain(" as ");
        expect(src).not.toContain("pyswitch.clients.kemper");

        await this.#expectActions(config, [["TAP_TEMPO", "fractal"]]);
    }

    /**
     * Updating a configuration without changes keeps the client of all actions, regardless of the order of
     * the clients in the definitions
     */
    async unchanged() {
        for (const imp of [ClientImportsTests.IMPORT_KEMPER_TAP_TEMPO, ClientImportsTests.IMPORT_FRACTAL_TAP_TEMPO]) {
            const config = await this.#config([imp], ["TAP_TEMPO()"]);
            const client = imp.includes("kemper") ? "kemper" : "fractal";

            await config.parser.input("1");
            config.parser.updateConfig();

            const src = (await config.get()).inputs_py;
            expect(src).toContain(imp + "\n");
            expect(src).not.toContain(client == "kemper" ? "pyswitch.clients.fractal" : "pyswitch.clients.kemper");

            await this.#expectActions(config, [["TAP_TEMPO", client]]);
        }
    }

    /**
     * Client functions in code strings (for example mappings selected in the UI) are imported from the
     * clients used in the file first
     */
    async codeStrings() {
        for (const client of ["kemper", "fractal"]) {
            const config = await this.#config([], []);
            const input = await config.parser.input("1");

            input.setActions([
                {
                    name: "TAP_TEMPO",
                    client: client,
                    arguments: []
                },
                {
                    name: "BINARY_SWITCH",
                    client: "local",
                    arguments: [
                        {
                            name: "mapping",
                            value: "MAPPING_TEMPO_BPM()"
                        }
                    ]
                }
            ]);

            const src = (await config.get()).inputs_py;
            expect(src).toContain(
                (client == "kemper")
                    ? "from pyswitch.clients.kemper.mappings.tempo_bpm import MAPPING_TEMPO_BPM\n"
                    : "from pyswitch.clients.fractal.mappings.tempo import MAPPING_TEMPO_BPM\n"
            );
        }
    }

    /**
     * Same-named actions of two clients in one configuration also work in PySwitch
     */
    async runTwoClients() {
        const config = await this.#config([], []);
        await this.#setActions(config, [["TAP_TEMPO", "fractal"], ["TAP_TEMPO", "kemper"]]);

        await this.runner.run(config);

        expect(1).toBe(1);
    }

    ///////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Creates a configuration (MIDICaptain Nano 4) with the passed import lines and action code lines on switch 1
     */
    async #config(imports, actions) {
        await this.init();

        const inputs_py =
            imports.map((line) => line + "\n").join("") +
            "from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *\n" +
            "\n" +
            "Inputs = [\n" +
            "    {\n" +
            "        \"assignment\": PA_MIDICAPTAIN_NANO_SWITCH_1,\n" +
            "        \"actions\": [\n" +
            actions.map((line) => "            " + line + ",\n").join("") +
            "        ]\n" +
            "    }\n" +
            "]\n";

        const display_py = 
            "from pyswitch.ui.ui import DisplayElement\n" +
            "from pyswitch.clients.local.callbacks.splashes import SplashesCallback\n" +
            "\n" +
            "Splashes = SplashesCallback(\n" +
            "    splashes = DisplayElement(\n" +
            "        children = []\n" +
            "    )\n" +
            ")\n";

        const config = new MockConfiguration(inputs_py, display_py);
        await config.init(this.pyswitch, "../");

        return config;
    }

    /**
     * Sets the actions of switch 1: [[name, client], ...]. Returns the new inputs.py
     */
    async #setActions(config, actions) {
        const input = await config.parser.input("1");

        input.setActions(
            actions.map((item) => {
                return {
                    name: item[0],
                    client: item[1],
                    arguments: []
                }
            })
        );

        return (await config.get()).inputs_py;
    }

    /**
     * Expects the actions of switch 1 (read by the parser): [[name, client], ...]
     */
    async #expectActions(config, expected) {
        const input = await config.parser.input("1");
        const actions = await input.actions();

        expect(actions.map((item) => [item.name, item.client])).toEqual(expected);
    }
}
