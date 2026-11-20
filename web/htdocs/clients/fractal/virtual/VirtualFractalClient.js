/**
 * Virtual Fractal device (Axe-Fx III, FM9, FM3). Behaves like a real device connected via DIN MIDI with
 * Send Realtime Sysex = ON: answers queries, never pushes state changes, only tempo beat and tuner data
 * are pushed. Spec: claude/spec/emulator/virtual_client.md
 */
class VirtualFractalClient extends VirtualClient {

    #runIntervalHandler = null;
    #ui = null;
    #modelId = null;
    #modelCallbacks = [];

    options = null;
    model = null;           // Current model (entry of FractalClient.MODELS)
    stats = null;
    protocol = null;
    presets = null;
    tempo = null;
    tuner = null;
    looper = null;

    /**
     * {
     *      model:                 Model ID (key of FractalClient.MODELS)
     *      sendRealtimeSysex:     Push tempo beat and tuner data
     *      recordSecondPress:     Looper "Record 2nd Press": "overdub", "play" or "stop"
     *      overrideTimeCallback:  Optional callback function replacing Date.now() for testing
     * }
     */
    constructor(options) {
        super("Virtual Fractal");
        this.options = options || {};

        this.#setModelData(this.options.model || FractalClient.DEFAULT_MODEL);

        this.stats = new VirtualFractalStats();
        this.protocol = new VirtualFractalProtocol(this);
        this.presets = new VirtualFractalPresets(this);
        this.tempo = new VirtualFractalTempo(this, this.options.overrideTimeCallback);
        this.tuner = new VirtualFractalTuner(this, this.options.overrideTimeCallback);
        this.looper = new VirtualFractalLooper(this);
    }

    /**
     * Returns the current model ID (key of FractalClient.MODELS)
     */
    getModelId() {
        return this.#modelId;
    }

    /**
     * Changes the model. This resets all presets and the looper.
     */
    setModel(modelId) {
        this.#setModelData(modelId);

        this.presets.reset();
        this.looper.reset();
        this.tuner.setEnabled(false);

        for (const cb of this.#modelCallbacks) {
            cb(this.#modelId);
        }
    }

    /**
     * Adds a callback on model change: callback(modelId) => void
     */
    addModelChangeCallback(callback) {
        this.#modelCallbacks.push(callback);
    }

    /**
     * Returns the current timestamp in milliseconds
     */
    now() {
        if (this.options.overrideTimeCallback) {
            return this.options.overrideTimeCallback();
        }
        return Date.now();
    }

    /**
     * Tries to return a meaningful message name
     */
    getMessageProperties(message) {
        const props = this.protocol.getMessageProperties(message);
        if (!props) return null;

        return {
            name: "Fractal: " + props.name,
            value: props.value
        };
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
     * When running, this is called regularly to update timed stuff
     */
    update() {
        this.tempo.update();
        this.tuner.update();
        this.looper.update();
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Called by PySwitch when a message should be sent to the client.
     * Naming is misleading here: this effectively receives data!
     */
    async doSend(message) {
        try {
            if (this.protocol.parse(message)) return;

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
        this.stats.messageSent(message, hintText);
        this.messageQueue.push(message);
    }

    /**
     * Stop listening to the input
     */
    detach() {
        clearInterval(this.#runIntervalHandler);

        this.presets.destroy();
        this.tempo.destroy();
        this.tuner.destroy();
        this.looper.destroy();
        this.stats.destroy();
        this.#modelCallbacks = [];

        if (this.#ui) this.#ui.destroy();
    }

    /**
     * If supported, can create a user interface in the passed container DOM element
     */
    getUserInterface(container) {
        if (this.#ui) this.#ui.destroy();
        this.#ui = new VirtualFractalClientUI(container, this);
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
     * Sets model ID and data
     */
    #setModelData(modelId) {
        if (!FractalClient.MODELS[modelId]) {
            throw new Error("Unknown Fractal model: " + modelId);
        }

        this.#modelId = modelId;
        this.model = FractalClient.MODELS[modelId];
    }
}
