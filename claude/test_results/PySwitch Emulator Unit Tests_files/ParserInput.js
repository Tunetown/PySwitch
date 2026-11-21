class ParserInput extends ParserTreeElement {

    assignment = null;

    #actions = null;
    #actionsHold = null;

    constructor(parser, data, assignment) {
        super(parser, data);

        this.assignment = assignment;
    }

    /**
     * If invalid, replace the data by searching for the input again
     */
    checkValid() {
        try {
            super.checkValid();

        } catch (e) {
            // Try to find the current version of the input data
            this.data = this.parser.inputData(this.assignment.name);
            
            if (!this.data) {
                throw new Error("The input is invalid and cannot be reactivated again: " + this.assignment.name);
            }

            this.setValid();
            super.checkValid();
        }
    }

    /**
     * Display name for the input
     */
    displayName() {
        return this.assignment.displayName;
    }

    /**
     * Returns the hold time in milliseconds
     */
    holdTimeMillis() {
        this.checkValid()

        const arg = this.getArgument("holdTimeMillis");
        return (arg && arg.value) ? parseInt(Tools.stripQuotes(arg.value)) : null;
    }

    /**
     * Sets the hold time in milliseconds
     */
    setHoldTimeMillis(htm) {
        this.checkValid()

        this.setArgument("holdTimeMillis", "" + parseInt(htm));
        this.parser.updateConfig();
    }

    /**
     * Returns if the holdRepeat optionis enabled
     */
    holdRepeat() {
        this.checkValid()

        const arg = this.getArgument("holdRepeat");
        return (arg && arg.value) ? (arg.value == "True") : null;
    }

    /**
     * Sets the holdRepeat option
     */
    setHoldRepeat(hr) {
        this.checkValid()
        
        this.setArgument("holdRepeat", hr ? "True" : "False");
        this.parser.updateConfig();
    }

    /**
     * Returns the actions of the input as arrays of ParserInputActions
     */
    actions(hold = false) {
        this.checkValid()

        if (!hold && this.#actions) return this.#actions;
        if (hold && this.#actionsHold) return this.#actionsHold;

        const actions = this.getArgument(hold ? "actionsHold" : "actions");
        if (!actions) return []

        const ret = actions.value
            .filter((item) => item != "None")
            .map((item) => new ParserInputAction(this.parser, this, item));

        if (hold) {
            this.#actionsHold = ret;
        } else {
            this.#actions = ret;
        }

        return ret;
    }

    /**
     * Sets the actions of the input by an array of objects describing the actions
     */
    setActions(actions, hold = false, noUpdate = false) {
        this.checkValid()

        const that = this;
        const prepped = actions.map((item) => { 
            return {
                name: item.name,
                assign: item.assign,
                arguments: item.arguments.map((arg) => {
                    if (item.name == "PagerAction" && arg.name == "pages") {
                        return {
                            name: arg.name,
                            value: arg.value.map((page) => {
                                return {
                                    arguments: that.#encodePage(page)
                                }
                            })
                        }    
                    }

                    return {
                        name: arg.name,
                        value: arg.value,
                        assign: arg.assign ? arg.assign : null
                    }
                })
            }
        })
        
        this.#actions = null;
        this.setArgument(hold ? "actionsHold" : "actions", prepped);

        if (!noUpdate) {
            this.parser.updateConfig();
        }
    }

    /**
     * Encodes a page deifinition like used in the UI and returns it as raw parser definition
     */
    #encodePage(page) {
        const ret = [
            {
                name: "id",
                value: page.id
            }
        ]

        if (page.color) {
            ret.push(
                {
                    name: "color",
                    value: page.color
                }
            )
        }
            
        if (page.text) {
            ret.push(
                {
                    name: "text",
                    value: page.text
                }
            )
        }

        return ret;
    }
}