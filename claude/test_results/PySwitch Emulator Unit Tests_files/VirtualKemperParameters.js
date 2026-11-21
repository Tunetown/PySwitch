class VirtualKemperParameters {

    #client = null;
    #data = null;
    #defaults = [];
    #callbacks = [];

    constructor(client) {
        this.#client = client;
        this.#data = new Map();
    }

    /**
     * Tries to return a meaningful message name
     */
    getMessageProperties(message) {
        for (const [key, entry] of this.#data) {
            // Try to parse the message
            let parseResult = entry.parse(message, true)
            if (parseResult) {
                return parseResult;
            }

            // Check if the message could be sent from the parameter
            parseResult = entry.parseSendMessage(message);
            if (parseResult) {
                return parseResult;
            }
        }

        return null;
    }

    /**
     * Adds a callback after init()
     * 
     * callback(param) => void
     */
    addInitCallback(callback) {
        this.#callbacks.push(callback);
    }

    /**
     * Try to parse all parameters. Returns if successful.
     */
    parse(message) {
        // Try all parameters
        for (const [key, entry] of this.#data) {
            if (entry.parse(message)) {
                // Stats
                this.#client.stats.messageReceived(message, entry.getDisplayName());

                return true;
            }
        }

        // Not parsed: Try defaults
        for (const def of this.#defaults) {
            if (def.parse(message)) {
                // Stats
                this.#client.stats.messageReceived(message, def.getDisplayName());

                return true;
            }
        }

        return false;
    }
    
    /**
     * Returns the value for the key, or 0 if not found
     */
    value(key) {
        const jsonKey = key.getId();
        if (!this.#data.has(jsonKey)) return 0;

        const entry = this.#data.get(jsonKey);
        return entry.value;
    }

    /**
     * Returns the entry of the parameter (if known). Will be created if not present.
     */
    get(key) {
        const jsonKey = key.getId();

        if (!this.#data.has(jsonKey)) {
            return this.init({ 
                keys: new VirtualKemperParameterKeys({ send: key }), 
                value: 0,
                // initiator: "auto"
            });
        }

        return this.#data.get(jsonKey);
    }

    /**
     * Initializes a parameter value.
     */
    init(options) {
        const jsonKey = options.keys.getId();
        
        if (this.#data.has(jsonKey)) {
            throw new Error("Redundant parameter definition: " + jsonKey);
        }

        const param = new VirtualKemperParameter(
            this.#client, 
            options
        );

        this.#data.set(
            jsonKey, 
            param
        );

        for (const cb of this.#callbacks) {
            cb(param);
        }

        return param;
    }

    /**
     * Initializes a default for a value type.
     */
    initDefault(options) {
        this.#defaults.push(
            new VirtualKemperParameterDefault(
                this.#client, 
                options
            )
        );
    }

    /**
     * Returns all parameters of a parameter set as array
     */
    getParameterSet(parameterSet) {
        const ret = [];
        for (const [key, entry] of this.#data) {
            if (entry.options.parameterSets && entry.options.parameterSets.includes(parameterSet)) {
                ret.push(entry);
            }
        }
        return ret;
    }

    destroy() {
        this.#data = new Map();
    }
}