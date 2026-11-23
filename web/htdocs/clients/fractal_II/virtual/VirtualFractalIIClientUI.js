/**
 * User interface for the virtual Axe-Fx II: preset, scene, preset name, the blocks of the preset with their states in
 * the current scene, tuner and tempo. Everything can be changed "on the device".
 */
class VirtualFractalIIClientUI {

    #container = null;
    #client = null;
    #building = false;

    constructor(container, client) {
        this.#container = container;
        this.#client = client;

        const that = this;
        this.#client.addChangeCallback(function() {
            try {
                that.#build();
            } catch (e) {
                console.error(e);
            }
        });

        this.#build();
    }

    /**
     * Destroy the UI
     */
    destroy() {
        this.#container.empty();
    }

    #build() {
        // Do not rebuild while an input of the UI is being processed
        if (this.#building) return;

        const client = this.#client;
        const that = this;

        this.#container.empty();

        // Preset and scene
        const presetOptions = [];
        for (let p = 0; p < client.model.numPresets; ++p) {
            presetOptions.push([p, String(p + 1).padStart(3, "0") + " " + client.presets[p].name]);
        }

        const sceneOptions = [];
        for (let s = 0; s < FractalIIClient.NUM_SCENES; ++s) {
            sceneOptions.push([s, "Scene " + (s + 1)]);
        }

        this.#createBox(client.model.name, [
            $('<div class="label" />').text("Preset"),
            this.#createSelect(presetOptions, client.preset)
            .on('change', function() { that.#call(() => client.loadPreset(parseInt($(this).val()))); }),

            $('<div class="label" />').text("Preset Name"),
            $('<input type="text" class="longtext" autocomplete="off">')
            .val(client.current.name)
            .on('change', function() { that.#call(() => client.setName($(this).val())); }),

            $('<div class="label" />').text("Scene"),
            this.#createSelect(sceneOptions, client.scene)
            .on('change', function() { that.#call(() => client.setScene(parseInt($(this).val()))); })
        ]);

        // Blocks
        const blocks = [];
        for (const id of client.current.blocks) {
            const state = client.getBlock(id);

            blocks.push(
                $('<div class="label" />').text(FractalIIClient.getBlockName(id)),

                $('<label />').append(
                    $('<input type="checkbox" />')
                    .prop('checked', state.engaged)
                    .on('change', function() { that.#call(() => client.setEngaged(id, $(this).prop('checked'))); }),
                    $('<span />').text(" engaged "),

                    this.#createSelect([[1, "X"], [0, "Y"]], state.x ? 1 : 0)
                    .on('change', function() { that.#call(() => client.setX(id, $(this).val() == "1")); })
                )
            );
        }

        this.#createBox("Blocks (scene " + (client.scene + 1) + ")", blocks);

        // Tuner and tempo
        this.#createBox("Tuner / Tempo", [
            $('<div class="label" />').text("Tuner (CC " + VirtualFractalIIClient.TUNER_CC + ")"),
            $('<input type="checkbox" />')
            .prop('checked', client.tuner)
            .on('change', function() { that.#call(() => client.setTuner($(this).prop('checked'))); }),

            $('<div class="label" />').text("Tuner Note"),
            this.#createSelect(
                ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"].map((n, i) => [i, n]),
                client.tunerNote
            )
            .on('change', function() { that.#call(() => client.setTunerData(parseInt($(this).val()), client.tunerCents)); }),

            $('<div class="label" />').text("Tuner Cents"),
            $('<input type="number" min=-50 max=50 />')
            .val(client.tunerCents)
            .on('change', function() { that.#call(() => client.setTunerData(client.tunerNote, parseInt($(this).val()))); }),

            $('<div class="label" />').text("Tempo (BPM, tap: CC " + VirtualFractalIIClient.TAP_TEMPO_CC + ")"),
            $('<input type="number" min=24 max=250 />')
            .val(client.bpm)
            .on('change', function() { that.#call(() => client.setBpm(parseInt($(this).val()))); })
        ]);

        if (client.rejected.length) {
            this.#createBox("Rejected messages", [
                $('<div class="value" />').text(client.rejected.length + " messages are not in the spec (see console)")
            ]);
        }
    }

    #call(func) {
        this.#building = true;
        try {
            func();
        } catch (e) {
            console.error(e);
        }
        this.#building = false;
        this.#build();
    }

    /**
     * Creates a select element. options: [ [value, text], ... ]
     */
    #createSelect(options, value) {
        const select = $('<select autocomplete="off" />');

        for (const option of options) {
            select.append(
                $('<option />')
                .attr("value", option[0])
                .text(option[1])
            );
        }

        if (value !== null) select.val(value);
        return select;
    }

    /**
     * Creates a box with title
     */
    #createBox(title, content) {
        const box = $('<div class="box" />').append(
            $('<div class="title" />').text(title),
            content
        );
        this.#container.append(box);
        return box;
    }
}
