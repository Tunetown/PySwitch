/**
 * Implements the input options editor
 */
class InputSettings extends ParameterList {
    
    #definition = null;
    #input = null;

    constructor(controller, definition, input) {
        super(controller)
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

        switch (this.#definition.data.model.type) {
            case "AdafruitSwitch": 
                await getSwitchOptions();
                break;
        }
    }
}