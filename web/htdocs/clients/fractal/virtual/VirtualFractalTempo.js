/**
 * Tempo of the virtual Fractal client: BPM, tap tempo and beat push data.
 */
class VirtualFractalTempo {

    static MIN_BPM = 24;
    static MAX_BPM = 250;

    // The device averages across ten taps by default (Setup: Global: Config: Tap Tempo)
    static MAX_TAPS = 10;

    // A tap after this time starts a new tap series
    static TAP_TIMEOUT_MILLIS = 2500;

    #client = null;
    #bpm = null;
    #period = null;             // PeriodCounter for the beats
    #taps = [];                 // Timestamps of the current tap series
    #callbacks = [];
    #beatCallbacks = [];

    #overrideTimeCallback = null;

    constructor(client, overrideTimeCallback = null) {
        this.#client = client;
        this.#overrideTimeCallback = overrideTimeCallback;

        this.set(120);
    }

    /**
     * Called regularly: sends the beat push data
     */
    update() {
        if (!this.#period.exceeded()) return;

        if (this.#client.options.sendRealtimeSysex) {
            this.#client.queueMessage(
                FractalClient.createSysex(this.#client.model.modelByte, VirtualFractalProtocol.FN_TEMPO_TAP, [], false),
                "Tempo Beat"
            );
        }

        for (const cb of this.#beatCallbacks) {
            cb();
        }
    }

    /**
     * Returns the tempo in BPM
     */
    bpm() {
        return this.#bpm;
    }

    /**
     * Sets the tempo in BPM (clamped to the device range)
     */
    set(bpm) {
        bpm = Math.round(bpm);
        if (!bpm) return;

        this.#bpm = Math.min(Math.max(bpm, VirtualFractalTempo.MIN_BPM), VirtualFractalTempo.MAX_BPM);
        this.#period = new PeriodCounter(60000 / this.#bpm, this.#overrideTimeCallback);

        for (const cb of this.#callbacks) {
            cb(this.#bpm);
        }
    }

    /**
     * Tap tempo: averages the intervals of the current tap series
     */
    tap() {
        const now = this.#client.now();

        if (this.#taps.length > 0 && now - this.#taps[this.#taps.length - 1] > VirtualFractalTempo.TAP_TIMEOUT_MILLIS) {
            this.#taps = [];
        }

        this.#taps.push(now);
        if (this.#taps.length > VirtualFractalTempo.MAX_TAPS) {
            this.#taps.shift();
        }

        if (this.#taps.length < 2) return;

        const avgInterval = (this.#taps[this.#taps.length - 1] - this.#taps[0]) / (this.#taps.length - 1);
        if (avgInterval <= 0) return;

        this.set(60000 / avgInterval);
    }

    /**
     * Adds a callback on tempo change: callback(bpm) => void
     */
    addChangeCallback(callback) {
        this.#callbacks.push(callback);
    }

    /**
     * Adds a callback on every beat: callback() => void
     */
    addBeatCallback(callback) {
        this.#beatCallbacks.push(callback);
    }

    destroy() {
        this.#callbacks = [];
        this.#beatCallbacks = [];
    }
}
