/**
 * Tests for configurations controlling several clients: detection of the clients, protocol client and the
 * combined MIDI wrapper. Spec: claude/spec/emulator/multi_client.md
 */
class MultiClientTests extends TestBase {

    static INPUTS_KEMPER = "from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO\n";
    static INPUTS_FRACTAL = "from pyswitch.clients.fractal.actions.scene import SCENE_SELECT\n";
    static INPUTS_LOCAL = "from pyswitch.clients.local.actions.binary_switch import BINARY_SWITCH\n";

    /**
     * Detection of all clients used by a configuration (inputs.py and display.py)
     */
    async estimateClients() {
        expect(await this.#clients(MultiClientTests.INPUTS_KEMPER, "")).toEqual(["kemper"]);
        expect(await this.#clients(MultiClientTests.INPUTS_FRACTAL, "")).toEqual(["fractal"]);
        expect(await this.#clients(MultiClientTests.INPUTS_FRACTAL + MultiClientTests.INPUTS_KEMPER, "")).toEqual(["kemper", "fractal"]);
        expect(await this.#clients(MultiClientTests.INPUTS_FRACTAL, "from pyswitch.clients.kemper import KemperRigNameCallback\n")).toEqual(["kemper", "fractal"]);

        // No client: default
        expect(await this.#clients(MultiClientTests.INPUTS_LOCAL, "")).toEqual(["kemper"]);
    }

    /**
     * The protocol is taken from the client which has one
     */
    async protocolClient() {
        expect((await ClientFactory.getProtocolClient(new MockConfiguration(MultiClientTests.INPUTS_FRACTAL, ""))).id).toBe("fractal");
        expect((await ClientFactory.getProtocolClient(new MockConfiguration(MultiClientTests.INPUTS_KEMPER, ""))).id).toBe("kemper");
        expect((await ClientFactory.getProtocolClient(new MockConfiguration(MultiClientTests.INPUTS_FRACTAL + MultiClientTests.INPUTS_KEMPER, ""))).id).toBe("kemper");
    }

    /**
     * Combined MIDI wrapper: sends to all wrappers, receives from all wrappers
     */
    async combinedMidiWrapper() {
        class MockWrapper {
            messageQueue = [];
            sent = [];
            updates = 0;
            detached = false;

            async send(message) {
                this.sent.push(message.toJs());
            }

            update() {
                this.updates++;
            }

            detach() {
                this.detached = true;
            }
        }

        const w1 = new MockWrapper();
        const w2 = new MockWrapper();
        const combined = new CombinedMidiWrapper([w1, w2]);

        // Send
        await combined.send({ toJs: () => [0xb0, 1, 2] });
        expect(w1.sent).toEqual([[0xb0, 1, 2]]);
        expect(w2.sent).toEqual([[0xb0, 1, 2]]);

        // Receive
        w1.messageQueue.push([1]);
        w2.messageQueue.push([2]);
        expect(combined.messageQueue).toEqual([[1], [2]]);

        // Update
        combined.update();
        expect(w1.updates).toBe(1);
        expect(w2.updates).toBe(1);

        // Detach
        combined.detach();
        expect(w1.detached).toBe(true);
        expect(w2.detached).toBe(true);
    }

    /**
     * A configuration with two clients runs with both virtual clients
     */
    async runTwoClients() {
        await this.init();

        const config = new MockConfiguration(
            "from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *\n" +
            "from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO as KEMPER_TAP_TEMPO\n" +
            "from pyswitch.clients.fractal.actions.tap_tempo import TAP_TEMPO as FRACTAL_TAP_TEMPO\n" +
            "\n" +
            "Inputs = [\n" +
            "    {\n" +
            "        \"assignment\": PA_MIDICAPTAIN_NANO_SWITCH_1,\n" +
            "        \"actions\": [\n" +
            "            KEMPER_TAP_TEMPO(),\n" +
            "            FRACTAL_TAP_TEMPO(),\n" +
            "        ]\n" +
            "    }\n" +
            "]\n",

            "from pyswitch.ui.ui import DisplayElement\n" +
            "from pyswitch.clients.local.callbacks.splashes import SplashesCallback\n" +
            "\n" +
            "Splashes = SplashesCallback(\n" +
            "    splashes = DisplayElement(\n" +
            "        children = []\n" +
            "    )\n" +
            ")\n"
        );

        await this.runner.run(config);

        expect(Object.keys(this.runner.clients)).toEqual(["kemper", "fractal"]);
        expect(this.runner.clients.kemper).toBeInstanceOf(VirtualKemperClient);
        expect(this.runner.clients.fractal).toBeInstanceOf(VirtualFractalClient);
        expect(this.runner.client).toBeInstanceOf(CombinedMidiWrapper);
    }

    ///////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Returns the clients detected for the passed sources
     */
    async #clients(inputs_py, display_py) {
        return await ClientFactory.estimateClients(new MockConfiguration(inputs_py, display_py));
    }
}
