class ParserTreeElement {

    data = null;
    parser = null;
    
    #parentInputs = null;

    constructor(parser, data) {
        this.parser = parser;
        this.data = data;
        
        this.setValid();
    }

    /**
     * Set the current data reference valid
     */
    setValid() {
        this.#parentInputs = this.parser.inputs();
    }

    /**
     * Checks if the data reference is still valid. Throws if not.
     */
    checkValid() {
        if (this.parser.inputs() === this.#parentInputs) return;
        throw new Error("This handler is not valid anymore", this.data);
    }

    /**
     * Gets the value of a specific argument, or null.
     */
    getArgument(name) {
        this.checkValid()
        
        for (const arg of this.data.arguments) {
            if (arg.name == name) return arg;
        }
        return null;
    }

    /**
     * Sets a specific argument. If not found, it will be added.
     */
    setArgument(name, value) {
        this.checkValid()

        for (const arg of this.data.arguments) {
            if (arg.name == name) {
                arg.value = value;
                return;
            }
        }

        // Add new
        this.data.arguments.push(
            {
                name: name,
                value: value
            }
        )
    }
}