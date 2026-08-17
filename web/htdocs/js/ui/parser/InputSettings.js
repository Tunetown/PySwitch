/**
 * Implements the input options editor
 */
class InputSettings extends ParameterList {
    
    #definition = null;
    #input = null;

    constructor(controller, definition, input, parser = null) {
        super(controller, parser)
        this.#definition = definition;
        this.#input = input;
    }

    /**
     * Must return the headline
     */
    async getHeadline() {
        return "These options apply to all actions of " + this.#definition.displayName + ":"
    }

    /**
     * Set up inputs
     */
    async setup() {
        const that = this;

        async function getSwitchOptions() {
            const holdTimeMillis = that.#input ? that.#input.holdTimeMillis() : 0
    
            await that.createBooleanInput({
                name: "Hold Repeat",
                comment: "This option keeps repeating the hold actions again and again as long as the switch is held.",
                value: that.#input ? that.#input.holdRepeat() : false,
                onChange: async function(value) {
                    that.#input.setHoldRepeat(value);

                    await that.controller.restart({
                        message: "none"
                    });
                }
            });
                    
            await that.createNumericInput({
                name: "Hold Time", 
                comment: "Amount of time you have to press the switch for the hold actions to be triggered (Milliseconds).",
                value: holdTimeMillis ? holdTimeMillis : 600,
                range: {
                    min: 0
                },
                onChange: async function(value) {
                    that.#input.setHoldTimeMillis(value);

                    await that.controller.restart({
                        message: "none"
                    });
                }
            });
        }

        async function getLedOptions() {
            await that.createColorInput({
                name: "color",
                displayName: "LED Color",
                comment: "Color of the switch LEDs when no action controls them. Leave empty to use the firmware default (white).",
                value: that.#input ? (that.#input.color() || "") : "",
                onChange: async function(value) {
                    that.#input.setColor(value || null);

                    await that.controller.restart({
                        message: "none"
                    });
                }
            });

            await that.createNumericInput({
                name: "brightness",
                displayName: "LED Brightness",
                comment: "Brightness of the switch LEDs when no action controls them. Range: [0..1]. Leave empty to use the firmware default (off).",
                value: that.#input ? (that.#input.brightness() !== null ? that.#input.brightness() : "") : "",
                range: {
                    min: 0,
                    max: 1,
                    step: 0.01
                },
                validate: function(value) {
                    if (value === "") return null;
                    const n = parseFloat(value);
                    if (isNaN(n) || n < 0 || n > 1) return "Must be between 0 and 1";
                    return null;
                },
                onChange: async function(value) {
                    const parsed = value !== "" ? parseFloat(value) : null;
                    that.#input.setBrightness(parsed);

                    await that.controller.restart({
                        message: "none"
                    });
                }
            });
        }

        switch (this.#definition.data.model.type) {
            case "AdafruitSwitch":
                await getSwitchOptions();
                await getLedOptions();
                break;
        }
    }
}