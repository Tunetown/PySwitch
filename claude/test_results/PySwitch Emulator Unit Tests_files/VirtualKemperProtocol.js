class VirtualKemperProtocol {

    static STATE_OFFLINE = 10;
    static STATE_CONNECTED = 20;

    state = null;

    #client = null;

    parameterSet = null;        // Currently active parameter set

    #timeLeaseCounter = null;   // PeriodCounter
    #keepAliveCounter = null;    // PeriodCounter
    #keepAliveStep = 0;

    #overrideTimeCallback = null;

    constructor(client, overrideTimeCallback = null) {
        this.#client = client;
        this.#overrideTimeCallback = overrideTimeCallback;

        this.state = VirtualKemperProtocol.STATE_OFFLINE;

        this.#keepAliveCounter = new PeriodCounter(500, this.#overrideTimeCallback);
    }

    /**
     * Tries to return a meaningful message name
     */
    getMessageProperties(message) {
        const keppAliveMsg = [240, 0, 32, 51, this.#client.options.productType, 127, 126, 0, 127]
        if (Tools.compareArrays(keppAliveMsg, message.slice(0, keppAliveMsg.length))) return {
            name: "Protocol KeepAlive",
            value: ""
        };

        if (this.parse(message, true)) return {
            name: "Protocol Init",
            value: ""
        };
    }

    /**
     * Called regularly when the client is running
     */
    update() {
        if (this.state == VirtualKemperProtocol.STATE_CONNECTED) {            
            // Connected state: Disable protocol after time lease exceeded
            if (this.#timeLeaseCounter.exceeded()) {
                this.state = VirtualKemperProtocol.STATE_OFFLINE;
            
                this.#keepAliveStep = 0;
                this.parameterSet = null;
            }

            // Send keep-alive messages every 500ms with increasing steps
            if (this.#keepAliveCounter.exceeded()) {
                this.#sendKeepAlive(this.#keepAliveStep++);

                if (this.#keepAliveStep >= 128) this.#keepAliveStep = 0;
            }
        }
    }

    /**
     * Sends a keep-alive message
     */
    #sendKeepAlive(cnt) {
        const msg = [240, 0, 32, 51, this.#client.options.productType, 127, 126, 0, 127, cnt, 247];

        this.#client.queueMessage(msg, "Protocol Keep-Alive");
    }    

    /**
     * Parse raw message. Must return if successful.
     */
    parse(message, simulate = false) {
        if (!Tools.compareArrays(
            message.slice(0, 9),
            [240, 0, 32, 51, this.#client.options.productType, 127].concat([126, 0, 64])
        )) return false;

        if (simulate) {
            return true;
        }

        // Decode 
        this.parameterSet = message[9];

        const flag_init     = !!(message[10] & 0b00000001);
        // const flag_sysex    = !!(message[10] & 0b00000010);   // Not supported
        // const flag_echo     = !!(message[10] & 0b00000100);   // Not supported
        // const flag_nofe     = !!(message[10] & 0b00001000);   // Not supported
        // const flag_noctr    = !!(message[10] & 0b00010000);   // Not supported
        // const flag_tunemode = !!(message[10] & 0b00100000);   // Not supported

        this.#timeLeaseCounter = new PeriodCounter(message[11] * 2000, this.#overrideTimeCallback);

        this.state = VirtualKemperProtocol.STATE_CONNECTED;

        // this.#client.log("Received bidirectional " + (flag_init ? "init" : "keep-alive") + " message");

        if (flag_init) {
            // Send initial set of parameters
            this.#sendParameterSet();
        }

        // Stats
        this.#client.stats.messageReceived(message, "Protocol");

        return true;
    }

    /**
     * Initially send all parameters of the set
     */
    #sendParameterSet() {
        const params = this.#client.parameters.getParameterSet(this.parameterSet);
        if (!params) {
            console.warn("Parameter set not supported by the virtual Kemper client: " + this.parameterSet);
        }

        for (const param of params) {
            param.send();
        }
    }
}