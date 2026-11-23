/**
 * User interface for the virtual Fractal AM4: preset, scene, names, the blocks of the 4 slots and their bypass states
 * in the current scene. Everything can be changed "on the device".
 */
class VirtualFractalAM4ClientUI {

    #container = null;
    #client = null;
    #content = null;

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
        const client = this.#client;
        const that = this;

        this.#container.empty();

        // Preset and scene
        const presetOptions = [];
        for (let p = 0; p < FractalAM4Client.NUM_PRESETS; ++p) {
            presetOptions.push([p, FractalAM4Client.locationText(p) + " " + client.presets[p].name]);
        }

        const sceneOptions = [];
        for (let s = 0; s < FractalAM4Client.NUM_SCENES; ++s) {
            sceneOptions.push([s, "Scene " + (s + 1)]);
        }

        this.#createBox("Preset", [
            $('<div class="label" />').text("Preset"),
            this.#createSelect(presetOptions, client.location)
            .on('change', function() { that.#call(() => client.loadPreset(parseInt($(this).val()))); }),

            $('<div class="label" />').text("Preset Name"),
            $('<input type="text" class="longtext" autocomplete="off">')
            .val(client.preset.name)
            .on('change', function() { that.#call(() => client.setName($(this).val())); }),

            $('<div class="label" />').text("Scene"),
            this.#createSelect(sceneOptions, client.scene)
            .on('change', function() { that.#call(() => client.setScene(parseInt($(this).val()))); }),

            $('<div class="label" />').text("Scene Name"),
            $('<input type="text" class="longtext" autocomplete="off">')
            .val(client.preset.scenes[client.scene])
            .on('change', function() { that.#call(() => client.setName($(this).val(), client.scene)); }),

            $('<div class="label" />').text("Footswitch Mode"),
            $('<div class="value" />').text(client.mode !== null ? FractalAM4Client.MODES[client.mode] : "-")
        ]);

        // Slots
        const blockOptions = [[0, "(empty)"]].concat(FractalAM4Client.BLOCK_IDS.map((id) => [id, FractalAM4Client.getBlockName(id)]));
        const slots = [];

        for (let slot = 0; slot < FractalAM4Client.NUM_SLOTS; ++slot) {
            slots.push(
                $('<div class="label" />').text("Slot " + (slot + 1)),

                this.#createSelect(blockOptions, client.preset.blocks[slot])
                .on('change', function() { that.#call(() => client.setBlock(slot, parseInt($(this).val()))); }),

                $('<label />').append(
                    $('<input type="checkbox" />')
                    .prop('checked', !client.getBypass(slot))
                    .on('change', function() { that.#call(() => client.setBypass(slot, !$(this).prop('checked'))); }),
                    $('<span />').text(" engaged (scene " + (client.scene + 1) + ")")
                )
            );
        }

        this.#createBox("Slots", slots);

        if (client.rejected.length) {
            this.#createBox("Rejected messages", [
                $('<div class="value" />').text(client.rejected.length + " messages were not whitelisted (see console)")
            ]);
        }
    }

    #call(func) {
        try {
            func();
        } catch (e) {
            console.error(e);
        }
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
