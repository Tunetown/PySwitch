/**
 * Virtual Kemper.
 */
class VirtualKemperClient extends VirtualClient {
    
    #runIntervalHandler = null;
    #ui = null;

    options = null;
    protocol = null;
    parameters = null;
    tempo = null;
    tuner = null;
    morph = null;

    /**
     * {
     *      productType: 2            (Player),
     *      simulateMorphBug: true    Simulates the morph bug of the Kemper (as of 02/2025) causing morph state not 
     *                                being updated internally on morph button triggers. Remove the option when the bug is fixed.
     *      overrideTimeCallback:     Optional callback function replacing Date.now() for testing.
     * }
     */
    constructor(options) {
        super("Virtual Kemper");
        this.options = options || {};

        // Parameter storage
        this.parameters = new VirtualKemperParameters(this);

        // Bidirectional protocol
        this.protocol = new VirtualKemperProtocol(this, options.overrideTimeCallback);

        // Tempo handler
        this.tempo = new VirtualKemperTempo(this, options.overrideTimeCallback);

        // Virtual tuner
        this.tuner = new VirtualKemperTuner(this, options.overrideTimeCallback);

        // Morph state handler
        this.morph = new VirtualKemperMorph(this, options.overrideTimeCallback);

        // Statistics handler
        this.stats = new VirtualKemperStats();

        // Initialize the parameters with values and types
        (new VirtualKemperClientSetup(this)).setup();
        
        this.updateRig();
    }

    /**
     * Tries to return a meaningful message name
     */
    getMessageProperties(message) {
        let props = this.parameters.getMessageProperties(message);
        if (props) return {
            name: "Kemper: " + props.name,
            value: props.value
        }

        props = this.protocol.getMessageProperties(message)
        if (props) return {
            name: "Kemper: " + props.name,
            value: props.value
        }

        props = this.#determineMessageProperties(message);
        if (props) return {
            name: "Kemper: " + props.name,
            value: props.value
        }
    }

    /**
     * Start processing regular updates to send messages. If not set, the caller has to 
     * call update() regularly.
     */
    run(updateInterval) {
        const that = this;
        this.#runIntervalHandler = setInterval(
            function() {
                try {
                    that.update();

                } catch (e) {
                    console.error(e);
                }
            }, 
            updateInterval
        );
    }

    /**
     * When running, this is called regularly to update the protocol and other timed stuff
     */
    update() {
        this.protocol.update();

        this.tempo.update();
        this.tuner.update();
        this.morph.update();
    }

    /**
     * Updates everything to the current rig ID.
     */
    updateRig() {
        this.parameters.get(new NRPNKey([0, 1])).setValue(this.#generateRigName(this.getRigId()));
        this.parameters.get(new NRPNKey([0, 3])).setValue(this.generateRigDate());
    }

    /**
     * Generates dummy rig names
     */
    #generateRigName(rigId) {
        const bank = Math.floor(rigId / 5);
        const rig = rigId % 5;

        const tokens = [
            "Blue",
            "Yellow",
            "Red",
            "Green",
            "Purple"    
        ]

        let rigName = tokens[bank % tokens.length];

        switch(rig) {
            case 0: rigName += " Clean"; break;
            case 1: rigName += " Crunch"; break;
            case 2: rigName += " Overdrive"; break;
            case 3: rigName += " Lead"; break;
            case 4: rigName += " Acoustic"; break;
        }

        return rigName;
    }

    /**
     * Determine current rig ID
     */
    getRigId() {
        const rigId_cc32 = this.parameters.get(new CCKey(32)).value;
        const rigId_pc = this.parameters.get(new PCKey()).value;

        return 128 * rigId_cc32 + rigId_pc;
    }

    /**
     * Sets the rig ID
     */
    setRigId(rigId) {
        this.parameters.get(new CCKey(32)).setValue(Math.floor(rigId / 128));
        this.parameters.get(new PCKey()).setValue(rigId % 128);

        this.updateRig();
    }

    /**
     * Returns the current timestamp
     */
    generateRigDate() {
        return new Date().toLocaleString("de-DE", {
            timeZone: 'Europe/Berlin',
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
            fractionalSecondDigits: 3
        });
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Called by PySwitch when a message should be sent to the client. 
     * Naming is misleading here: this effectively receives data!
     */
    async doSend(message) {
        try {
            // Try to parse message: Protocol
            if (this.protocol.parse(message)) return;

            // Try to parse message: Parameters
            if (this.parameters.parse(message)) return;

            // Unparsed!
            this.stats.messageReceived(message, "Unparsed");
            console.warn(this.name + ": Unparsed message: ", message);

        } catch (e) {
            // We must catch here to get usable stack traces, as this is called by python code.
            console.error(e);
        }
    }

    /**
     * Add a raw message to the queue
     */
    queueMessage(message, hintText = "") {   
        // Stats
        this.stats.messageSent(message, hintText);

        // console.log(message)     
        this.messageQueue.push(message);
    }

    /**
     * Stop listening to the input
     */
    detach() {  
        clearInterval(this.#runIntervalHandler);

        this.parameters.destroy();
        this.tempo.destroy();
        this.tuner.destroy();
        this.morph.destroy();

        if (this.#ui) this.#ui.destroy();
    }

    /**
     * If supported, can create a user interface in the passed container DOM element
     */
    getUserInterface(container) {
        if (this.#ui) this.#ui.destroy();
        this.#ui = new VirtualKemperClientUI(container, this);
        return this.#ui;
    }

    /**
     * Logging with prefix
     */
    log() {
        [].unshift.call(arguments, this.name + ":");
        console.log.apply(null, arguments);
    }

    /**
     * Generic checking of a messages props
     */
    #determineMessageProperties(message) {
        // NRPN
        if (Tools.compareArrays(
            message.slice(0, 4),
            [240, 0, 32, 51]
        )) {
            if (message.length >= 8) {
                const fcode = message[6];

                const data = message.slice(8, -1)
                let value = data
    
                if (data.length == 2) {
                    // Most likely a number parameter
                    value = 128 * data[0] + data[1]
                }
                else if (data.length > 2) {
                    // Try as string
                    value = Tools.data2string(data);
                }

                return {
                    name: "NRPN Function " + fcode,
                    value: value
                }    
            } else {
                return {
                    name: "SysEx",
                    value: message.slice(4, -1)
                }    
            }
        }

        // Other types
        if (message[0] >= 176) {
            if (message[0] < 192) {
                return {
                    name: "CC " + message[1] + " (Channel " + (message[0] - 175) + ")",
                    value: message[2]
                }
            }
            else if (message[0] < 208) {
                return {
                    name: "PC (Channel " + (message[0] - 191) + ")",
                    value: message[1]
                }
            }
            else if (message[0] == 240) {
                return {
                    name: "SysEx",
                    value: message
                }
            }
        }

        return null;
    }
}