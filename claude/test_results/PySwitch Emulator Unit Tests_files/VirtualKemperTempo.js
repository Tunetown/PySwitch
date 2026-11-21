class VirtualKemperTempo {
    
    #client = null;
    #period = null;
    #lastTap = null;

    #callbacks = [];

    #overrideTimeCallback = null;

    constructor(client, overrideTimeCallback) {
        this.#client = client;
        this.#overrideTimeCallback = overrideTimeCallback;

        this.set(120);
    }

    update() {
        if (!this.#period) return;

        if (this.#period.exceeded()) {
            const param = this.#client.parameters.get(new NRPNKey([124, 0]));
            param.setValue((param.value == 0) ? 1 : 0);
        }
    }

    /**
     * Returns the tempo in beats per minute (bpm)
     */
    bpm() {
        if (!this.#period) return null;

        return Math.round(30000 / this.#period.interval);
    }

    /**
     * Sets the tempo in bpm
     */
    set(bpm) {
        if (!bpm) {
            this.#period = null;

            for (const c of this.#callbacks) {
                c(this.bpm());
            }

            return;
        }

        this.#period = new PeriodCounter(30000 / Math.round(bpm), this.#overrideTimeCallback);

        for (const c of this.#callbacks) {
            c(this.bpm());
        }
    }

    /**
     * Tap tempo
     */
    tap(value) {
        if (value != 1) return;

        if (this.#lastTap === null) {
            this.#lastTap = Date.now();
            return;
        }

        const diff = Date.now() - this.#lastTap;
        this.#lastTap = Date.now();
        if (diff > 3000) {            
            return;
        }

        this.#period = new PeriodCounter(diff / 2, this.#overrideTimeCallback);

        for (const c of this.#callbacks) {
            c(this.bpm());
        }
    }

    /**
     * Adds a callback on change
     * 
     * callback(bpm) => void
     */
    addChangeCallback(callback) {
        this.#callbacks.push(callback);
    }

    destroy() {
        this.#callbacks = [];
    }
}