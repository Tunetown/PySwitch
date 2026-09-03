/**
 * MIDI Settings tab
 */
class EmulatorSettings extends Tab {
    
    #monitorContainer = null;
    #controller = null;

    constructor(controller, tabName) {
        let monitorContainer = null;
        super(
            monitorContainer = $('<div class="emulator-settings-container" />'), 
            tabName
        );
        this.#monitorContainer = monitorContainer;
        this.#controller = controller;

        this.#initSettings();
    }

    /**
     * Rebuild the DOM
     */
    #initSettings() {
        this.#monitorContainer
            .empty()
            .append(
                $('<div class="emulator-settings" />').append(
                    this.#getConfigSettings(),
                    // this.#getCommSettings()
                )
            );
    }

    /**
     * Get MIDI comm settings
     */
    #getCommSettings() {
        const that = this;
        const inChannel = this.#controller.commSettings.getAttribute("inChannel");

        return $('<div class="box" />').append(
            $('<div class="title" />')
            .text("Communication Settings"),

            $('<div class="comment" />')
            .html("Global MIDI settings for the emulator. <br><br>NOTE: If you use the debug options, the output is printed to the JS console (F12 on Chrome)."),

            // Input channel
            $('<div class="label" />')
            .text("PySwitch Input Channel"),

            $('<input type="text" />')
            .val((inChannel != null) ? (inChannel + 1) : "All")
            .on('change', async function() {
                await that.#setCommFromInput($(this), "inChannel");
            }),

            // Output channel
            $('<div class="label" />')
            .text("PySwitch Output Channel"),

            $('<input type="text" />')
            .val(this.#controller.commSettings.getAttribute("outChannel") + 1)
            .on('change', async function() {
                await that.#setCommFromInput($(this), "outChannel");
            }),

            // Debug MIDI channels
            $('<div class="label" />')
            .text("Debug: MIDI channels"),

            $('<input type="checkbox" />')
            .prop('checked', !!this.#controller.commSettings.getAttribute("debug"))
            .on('change', async function() {
                await that.#setCommFromInput($(this), "debug");
            }),

            // Buttons
            $('<span class="setting-buttons" />').append(
                // Reset button
                $('<span class="button" />')
                .text('Reset')
                .on('click', async function() { 
                    await that.#resetCommSettings(); 
                }),

                // Apply
                $('<span class="button" />')
                .text('Apply')
                .on('click', async function() { 
                    await that.#restart(); 
                })
            )
        );
    }

    /**
     * Get config.py settings
     */
    #getConfigSettings() {
        const that = this;
        return $('<div class="box" />').append(
            $('<div class="title" />')
            .text("Configuration"),

            $('<div class="comment" />')
            .html("This controls the (global) config.py settings for the emulator. You can also download the resulting config.py file to be used on your controller. <br><br>NOTE: If you use the debug options, the output is printed to the JS console (F12 on Chrome)."),

            // Update interval
            $('<div class="label" />')
            .text("Update Interval (ms)"),

            $('<input type="number" min=1 />')
            .val(this.#controller.configFile.getAttribute("updateInterval"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "updateInterval");
            }),

            // Max. consecutive MIDI messages
            $('<div class="label" />')
            .text("Max. consecutive MIDI messages"),

            $('<input type="number" min=1 />')
            .val(this.#controller.configFile.getAttribute("maxConsecutiveMidiMessages"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "maxConsecutiveMidiMessages");
            }),

            // Clear Buffers
            $('<div class="label" />')
            .text("Clear MIDI Buffers at startup"),

            $('<input type="checkbox" />')
            .prop('checked', !!this.#controller.configFile.getAttribute("clearBuffers"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "clearBuffers");
            }),

            // Max. request lifetime (ms)
            $('<div class="label" />')
            .text("Max. consecutive MIDI messages"),

            $('<input type="number" min=1 />')
            .val(this.#controller.configFile.getAttribute("maxRequestLifetimeMillis"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "maxRequestLifetimeMillis");
            }),

            // memoryWarnLimitBytes
            $('<div class="label" />')
            .text("RAM limit before warning"),

            $('<input type="number" min=0 />')
            .val(this.#controller.configFile.getAttribute("memoryWarnLimitBytes"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "memoryWarnLimitBytes");
            }),

            // Display dim fators
            $('<div class="label" />')
            .text("Global display dim factor (On)"),

            $('<input type="number" min=0 max=1 step=0.01 />')
            .val(this.#controller.configFile.getAttribute("displayDimFactorOn"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "displayDimFactorOn");
            }),

            $('<div class="label" />')
            .text("Global display dim factor (Off)"),

            $('<input type="number" min=0 max=1 step=0.01 />')
            .val(this.#controller.configFile.getAttribute("displayDimFactorOff"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "displayDimFactorOff");
            }),

            // LED dim fators
            $('<div class="label" />')
            .text("Global LED brightness (On)"),

            $('<input type="number" min=0 max=1 step=0.01 />')
            .val(this.#controller.configFile.getAttribute("ledBrightnessOn"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "ledBrightnessOn");
            }),

            $('<div class="label" />')
            .text("Global LED brightness (Off)"),

            $('<input type="number" min=0 max=1 step=0.01 />')
            .val(this.#controller.configFile.getAttribute("ledBrightnessOff"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "ledBrightnessOff");
            }),

            // Explore mode
            $('<div class="label" />')
            .text("Explore Mode"),

            $('<input type="checkbox" />')
            .prop('checked', !!this.#controller.configFile.getAttribute("exploreMode"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "exploreMode");
            }),

            // Debug Stats
            $('<div class="label" />')
            .text("Debug: Statistics"),

            $('<input type="checkbox" />')
            .prop('checked', !!this.#controller.configFile.getAttribute("debugStats"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "debugStats");
            }),

            // debugStatsInterval
            $('<div class="label" />')
            .text("Debug Stats: Interval"),

            $('<input type="number" min=10 />')
            .val(this.#controller.configFile.getAttribute("debugStatsInterval"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "debugStatsInterval");
            }),

            // Debug protocol
            $('<div class="label" />')
            .text("Debug: Protocol"),

            $('<input type="checkbox" />')
            .prop('checked', !!this.#controller.configFile.getAttribute("debugBidirectionalProtocol"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "debugBidirectionalProtocol");
            }),

            // Debug unparsed messages
            $('<div class="label" />')
            .text("Debug: Unparsed messages"),

            $('<input type="checkbox" />')
            .prop('checked', !!this.#controller.configFile.getAttribute("debugUnparsedMessages"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "debugUnparsedMessages");
            }),

            // Debug sent messages
            $('<div class="label" />')
            .text("Debug: Sent messages"),

            $('<input type="checkbox" />')
            .prop('checked', !!this.#controller.configFile.getAttribute("debugSentMessages"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "debugSentMessages");
            }),

            // Debug client
            $('<div class="label" />')
            .text("Debug: Client statistics"),

            $('<input type="checkbox" />')
            .prop('checked', !!this.#controller.configFile.getAttribute("debugClientStats"))
            .on('change', async function() {
                await that.#setConfigFromInput($(this), "debugClientStats");
            }),


            // Buttons
            $('<span class="setting-buttons" />').append(
                // Reset button
                $('<span class="button" />')
                .text('Reset')
                .on('click', async function() { 
                    await that.#resetConfig(); 
                }),

                // Download config.py
                $('<span class="button" />')
                .text('Download')
                .on('click', async function() { 
                    await that.#downloadConfig(); 
                }),
                
                // Apply button
                $('<span class="button" />')
                .text('Apply')
                .on('click', async function() { 
                    await that.#restart(); 
                })
            )
        )
    }

    /**
     * Restart the emulator
     */
    async #restart() {            
        try {
            await this.#controller.restart({ message: "none" });
            this.#initSettings();

        } catch (e) {
            this.#controller.handle(e);
        }
    }

    /**
     * Reset config.py
     */
    async #resetConfig() {
        try {
            this.#controller.configFile.set({});
            this.#initSettings();
            await this.#restart();

        } catch (e) {
            this.#controller.handle(e);
        }
    }

    /**
     * Reset comm settings
     */
    async #resetCommSettings() {
        try {
            this.#controller.commSettings.set({});
            this.#initSettings();
            await this.#restart();

        } catch (e) {
            this.#controller.handle(e);
        }
    }

    /**
     * Sets a config.py value to the value of the passed input element
     */
    async #setConfigFromInput(input, name) {
        try {
            let value = null;
            switch (input.prop("type")) {
                case "checkbox":
                    value = !!input.prop('checked');
                    break;
                case "number":
                    if (input.prop("step").includes(".")) {
                        value = parseFloat(input.val());
                    } else {
                        value = parseInt(input.val());
                    }
                    break;
                default:
                    value = input.val();
                    break;
            }
            this.#controller.configFile.setAttribute(name, value);

        } catch (e) {
            this.#controller.handle(e);
        }
    }

    /**
     * Sets a comm setting value to the value of the passed input element
     */
    async #setCommFromInput(input, name) {
        try {
            if (input.prop('type') == "checkbox") {
                const value = !!input.prop('checked');
                this.#controller.commSettings.setAttribute(name, value);
            } else {
                const value = input.val();
                if (value == "All") {
                    this.#controller.commSettings.setAttribute(name, null);
                } else {
                    this.#controller.commSettings.setAttribute(name, parseInt(value) - 1);
                }
            }

        } catch (e) {
            this.#controller.handle(e);
        }
    }

    /**
     * Download as config.py
     */
    async #downloadConfig() {
        const data = await this.#controller.configFile.render();
        
        // Get the ZIP stream in a Blob (this function comes from the client-zip module)
        const blob = new Blob([data], {
            type: 'text/plain'
        });

        // Create an URL for the data blob
        const url = URL.createObjectURL(blob);

        window.saveAs(url, 'config.py');
    }
}