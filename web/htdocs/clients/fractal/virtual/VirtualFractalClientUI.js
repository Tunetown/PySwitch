/**
 * User interface for the virtual Fractal client
 */
class VirtualFractalClientUI {

    static CHANNEL_NAMES = ["A", "B", "C", "D", "E", "F"];
    static NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];

    #container = null;
    #client = null;

    #blocksBox = null;

    constructor(container, client) {
        this.#container = container;
        this.#client = client;

        this.#build();
    }

    /**
     * Destroy the UI
     */
    destroy() {
        this.#container.empty();
    }

    #build() {
        this.#container.empty();

        this.#buildGeneral();
        this.#buildPreset();
        this.#buildBlocks();
        this.#buildTuner();
        this.#buildLooper();
    }

    /**
     * Model, tempo, traffic
     */
    #buildGeneral() {
        const that = this;

        let modelSelect = null;
        let tempoInput = null;
        let beatIndicator = null;
        let trafficInIndicator = null;
        let trafficOutIndicator = null;

        function formatMessages(messages, prefix) {
            let ret = prefix + "in the last second:\n\n";

            for (const msg of messages) {
                ret += msg.hint + ": " + Array.from(msg.message).map((b) => b.toString(16).padStart(2, "0")).join(" ") + "\n";
            }

            return ret;
        }

        this.#createBox(
            "General",
            [
                // Model
                $('<div class="label" />')
                .text("Model"),

                modelSelect = this.#createSelect(
                    Object.keys(FractalClient.MODELS).map((id) => [id, FractalClient.MODELS[id].name]),
                    this.#client.getModelId()
                )
                .on('change', function() {
                    try {
                        that.#client.setModel($(this).val());
                    } catch (e) {
                        console.error(e);
                    }
                }),

                // Send Realtime Sysex
                $('<div class="label" />')
                .text("Send Realtime Sysex"),

                $('<input type="checkbox" autocomplete="off">')
                .prop("checked", !!this.#client.options.sendRealtimeSysex)
                .on('change', function() {
                    try {
                        that.#client.options.sendRealtimeSysex = this.checked;
                    } catch (e) {
                        console.error(e);
                    }
                }),

                // Tempo
                $('<div class="label" />')
                .text("Tempo (BPM)"),

                tempoInput = $('<input type="text" autocomplete="off">')
                .val(this.#client.tempo.bpm())
                .on('change', function() {
                    try {
                        that.#client.tempo.set(parseInt($(this).val()));
                        tempoInput.val(that.#client.tempo.bpm());
                    } catch (e) {
                        console.error(e);
                    }
                }),

                $('<div class="label" />')
                .text("Beat"),

                beatIndicator = $('<div class="value-output" />')
                .text("○"),

                // MIDI Traffic indicators
                $('<div class="label" />')
                .text("MIDI In:")
                .on('click', async function() {
                    alert(formatMessages(that.#client.stats.data.messagesReceived, "Received messages "));
                }),

                trafficInIndicator = $('<div class="value-output" />'),

                $('<div class="label" />')
                .text("MIDI Out:")
                .on('click', async function() {
                    alert(formatMessages(that.#client.stats.data.messagesSent, "Sent messages "));
                }),

                trafficOutIndicator = $('<div class="value-output" />')
            ]
        );

        this.#client.addModelChangeCallback(function(modelId) {
            modelSelect.val(modelId);
        });

        this.#client.tempo.addChangeCallback(function(bpm) {
            tempoInput.val(bpm);
        });

        let beatToggle = false;
        this.#client.tempo.addBeatCallback(function() {
            beatToggle = !beatToggle;
            beatIndicator.text(beatToggle ? "●" : "○");
        });

        this.#client.stats.addChangeCallback(function(stats) {
            trafficInIndicator.text(stats.receiveRate + "/s");
            trafficOutIndicator.text(stats.sendRate + "/s");
        });
    }

    /**
     * Preset and scene
     */
    #buildPreset() {
        const that = this;
        const presets = this.#client.presets;

        let presetInput = null;
        let presetNameInput = null;
        let sceneSelect = null;
        let sceneNameInput = null;

        const sceneOptions = [];
        for (let s = 0; s < VirtualFractalPresets.NUM_SCENES; ++s) {
            sceneOptions.push([s, "Scene " + (s + 1)]);
        }

        this.#createBox(
            "Preset",
            [
                // Preset number (0-based, like the device with Display Offset 0)
                $('<div class="label" />')
                .text("Preset"),

                presetInput = $('<input type="text" autocomplete="off">')
                .val(presets.currentPreset)
                .on('change', function() {
                    try {
                        if (!presets.loadPreset(parseInt($(this).val()))) {
                            presetInput.val(presets.currentPreset);
                        }
                    } catch (e) {
                        console.error(e);
                    }
                }),

                // Preset name
                $('<div class="label" />')
                .text("Preset Name"),

                presetNameInput = $('<input type="text" class="longtext" autocomplete="off">')
                .val(presets.getPresetName(presets.currentPreset))
                .on('change', function() {
                    try {
                        presets.setPresetName(presets.currentPreset, $(this).val());
                    } catch (e) {
                        console.error(e);
                    }
                }),

                // Scene
                $('<div class="label" />')
                .text("Scene"),

                sceneSelect = this.#createSelect(sceneOptions, presets.currentScene)
                .on('change', function() {
                    try {
                        presets.setScene(parseInt($(this).val()));
                    } catch (e) {
                        console.error(e);
                    }
                }),

                // Scene name
                $('<div class="label" />')
                .text("Scene Name"),

                sceneNameInput = $('<input type="text" class="longtext" autocomplete="off">')
                .val(presets.getSceneName(presets.currentScene))
                .on('change', function() {
                    try {
                        presets.setSceneName(presets.currentScene, $(this).val());
                    } catch (e) {
                        console.error(e);
                    }
                })
            ]
        );

        presets.addChangeCallback(function(changeType) {
            if (changeType == VirtualFractalPresets.CHANGE_BLOCKS) return;

            presetInput.val(presets.currentPreset);
            presetNameInput.val(presets.getPresetName(presets.currentPreset));
            sceneSelect.val(presets.currentScene);
            sceneNameInput.val(presets.getSceneName(presets.currentScene));
        });
    }

    /**
     * Blocks of the current preset (rebuilt on every change)
     */
    #buildBlocks() {
        const that = this;

        this.#blocksBox = this.#createBox("Blocks (current scene)", []);
        this.#updateBlocks();

        this.#client.presets.addChangeCallback(function(changeType) {
            if (changeType == VirtualFractalPresets.CHANGE_NAMES) return;
            that.#updateBlocks();
        });
    }

    /**
     * Refills the blocks box
     */
    #updateBlocks() {
        const presets = this.#client.presets;
        const content = [];

        for (const id of presets.getBlocks()) {
            const info = VirtualFractalBlocks.get(id);
            const state = presets.getBlockState(id);

            const channelOptions = VirtualFractalClientUI.CHANNEL_NAMES
                .slice(0, info.channels)
                .map((name, index) => [index, name]);

            content.push(
                $('<div class="label" />')
                .text(VirtualFractalBlocks.getDisplayName(id) + " [" + id + "]"),

                $('<div />').append([
                    // Engaged
                    $('<input type="checkbox" autocomplete="off" title="Engaged">')
                    .prop("checked", !state.bypassed)
                    .on('change', function() {
                        try {
                            presets.setBypass(id, !this.checked);
                        } catch (e) {
                            console.error(e);
                        }
                    }),

                    // Channel
                    (info.channels > 1) ? (
                        this.#createSelect(channelOptions, state.channel)
                        .attr("title", "Channel")
                        .on('change', function() {
                            try {
                                presets.setChannel(id, parseInt($(this).val()));
                            } catch (e) {
                                console.error(e);
                            }
                        })
                    ) : null,

                    // Remove
                    $('<button type="button" title="Remove block from preset" />')
                    .text("✕")
                    .on('click', function() {
                        try {
                            presets.removeBlock(id);
                        } catch (e) {
                            console.error(e);
                        }
                    })
                ].filter((el) => el !== null))
            );
        }

        // Add a block
        const addOptions = VirtualFractalBlocks.getAvailable(this.#client.model.countIndex)
            .filter((id) => !presets.hasBlock(id))
            .map((id) => [id, VirtualFractalBlocks.getDisplayName(id) + " [" + id + "]"]);

        let addSelect = null;

        content.push(
            $('<div class="label" />')
            .text("Add Block"),

            $('<div />').append(
                addSelect = this.#createSelect(addOptions, null),

                $('<button type="button" />')
                .text("Add")
                .on('click', function() {
                    try {
                        presets.addBlock(parseInt(addSelect.val()));
                    } catch (e) {
                        console.error(e);
                    }
                })
            )
        );

        this.#blocksBox.children().not('.title').remove();
        this.#blocksBox.append(content);
    }

    /**
     * Tuner
     */
    #buildTuner() {
        const that = this;
        const tuner = this.#client.tuner;

        let enableInput = null;
        let noteSelect = null;
        let centsInput = null;
        let centsOutput = null;
        let stringOutput = null;

        this.#createBox(
            "Tuner",
            [
                $('<div class="label" />')
                .text("Enable"),

                enableInput = $('<input type="checkbox" autocomplete="off">')
                .prop("checked", tuner.enabled)
                .on('change', function() {
                    try {
                        tuner.setEnabled(this.checked);
                    } catch (e) {
                        console.error(e);
                    }
                }),

                $('<div class="label" />')
                .text("Note"),

                noteSelect = this.#createSelect(
                    VirtualFractalClientUI.NOTE_NAMES.map((name, index) => [index, name]),
                    tuner.note
                )
                .on('change', function() {
                    try {
                        tuner.setNote(parseInt($(this).val()));
                    } catch (e) {
                        console.error(e);
                    }
                }),

                $('<div class="label" />')
                .text("String"),

                stringOutput = $('<div class="value-output" />'),

                $('<div class="label" />')
                .text("Cents"),

                centsInput = $('<input type="range" min="' + (-VirtualFractalTuner.MAX_CENTS) + '" max="' + VirtualFractalTuner.MAX_CENTS + '">')
                .val(tuner.cents)
                .on('input', function() {
                    try {
                        tuner.setCents(parseInt($(this).val()));
                    } catch (e) {
                        console.error(e);
                    }
                }),

                $('<div class="label" />'),

                centsOutput = $('<div class="value-output" />')
            ]
        );

        function update() {
            enableInput.prop("checked", tuner.enabled);
            noteSelect.val(tuner.note);
            centsInput.val(tuner.cents);
            centsOutput.text((tuner.cents > 0 ? "+" : "") + tuner.cents);
            stringOutput.text((tuner.string() + 1) + " (" + ["low E", "A", "D", "G", "B", "high E"][tuner.string()] + ")");
        }

        tuner.addChangeCallback(update);
        update();
    }

    /**
     * Looper
     */
    #buildLooper() {
        const that = this;
        const looper = this.#client.looper;

        let stateOutput = null;
        let infoOutput = null;

        const buttons = [
            [VirtualFractalLooper.BUTTON_RECORD, "Record"],
            [VirtualFractalLooper.BUTTON_PLAY, "Play"],
            [VirtualFractalLooper.BUTTON_UNDO, "Undo"],
            [VirtualFractalLooper.BUTTON_ONCE, "Once"],
            [VirtualFractalLooper.BUTTON_REVERSE, "Reverse"],
            [VirtualFractalLooper.BUTTON_HALF, "Half"]
        ];

        this.#createBox(
            "Looper",
            [
                $('<div class="label" />')
                .text("Buttons"),

                $('<div />').append(
                    buttons.map((b) =>
                        $('<button type="button" />')
                        .text(b[1])
                        .on('click', function() {
                            try {
                                looper.press(b[0]);
                            } catch (e) {
                                console.error(e);
                            }
                        })
                    )
                ),

                $('<div class="label" />')
                .text("State"),

                stateOutput = $('<div class="value-output" />'),

                $('<div class="label" />')
                .text("Loop"),

                infoOutput = $('<div class="value-output" />'),

                $('<div class="label" />')
                .text("Record 2nd Press"),

                this.#createSelect(
                    [["overdub", "Overdub"], ["play", "Play"], ["stop", "Stop"]],
                    this.#client.options.recordSecondPress
                )
                .on('change', function() {
                    try {
                        that.#client.options.recordSecondPress = $(this).val();
                    } catch (e) {
                        console.error(e);
                    }
                })
            ]
        );

        function update() {
            if (!that.#client.presets.hasLooper()) {
                stateOutput.text("No Looper block in preset");
            } else {
                const states = [];
                if (looper.recording) states.push("Record");
                if (looper.playing) states.push("Play");
                if (looper.overdub) states.push("Overdub");
                if (looper.once) states.push("Once");
                if (looper.reverse) states.push("Reverse");
                if (looper.half) states.push("Half");

                stateOutput.text(states.length ? states.join(", ") : "Stopped");
            }

            infoOutput.text(looper.loopLength ? ((looper.loopLength / 1000).toFixed(1) + "s, " + looper.layers + " layer(s)") : "Empty");
        }

        looper.addChangeCallback(update);
        this.#client.presets.addChangeCallback(update);
        update();
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

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
     * Used by all parts to create their boxes.
     */
    #createBox(title, content) {
        const box = $('<div class="box" />').append(
            $('<div class="title" />')
            .text(title),

            content
        );
        this.#container.append(box);
        return box;
    }
}
