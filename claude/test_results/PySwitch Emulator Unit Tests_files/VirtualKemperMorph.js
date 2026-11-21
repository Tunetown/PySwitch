class VirtualKemperMorph {
    
    #client = null;
    #period = null;

    #fadeStep = null;
    #fadeTarget = null;

    rigBtnMorph = true;
    
    constructor(client, overrideTimeCallback = null) {
        this.#client = client;

        this.#period = new PeriodCounter(100, overrideTimeCallback);

        this.setFadeSpeed(4);
    }

    /**
     * Set fade speed in seconds
     */
    setFadeSpeed(secs) {
        this.#fadeStep = 16384 / ((secs * 1000) / this.#period.interval);
    }

    update() {
        if (this.#fadeTarget !== null) {
            const state = this.#client.parameters.get(new NRPNKey([0, 11])).value;

            if (state == this.#fadeTarget) {
                this.#fadeTarget = null;
            } else {
                const diff = this.#fadeTarget - state;
                
                let value;
                if (Math.abs(diff) < this.#fadeStep) {
                    value = this.#fadeTarget;
                } else {
                    value = Math.round(state + ((diff > 0) ? this.#fadeStep : -this.#fadeStep));
                }
                
                this.#client.parameters.get(new NRPNKey([0, 11])).setValue(value);
            }
        }

        if (this.running && this.#period.exceeded()) {
            this.#sendState();
        }
    }

    /**
     * Triggered when morph button is pushed.
     */
    triggerButton() {
        if (this.#client.options.simulateMorphBug) return;

        const state = this.#client.parameters.get(new NRPNKey([0, 11])).value;        

        if (state > 8191) {
            this.#fadeTarget = 0;
        } else {
            this.#fadeTarget = 16383;
        }
    }

    #sendState() {
        this.#client.parameters.get(new NRPNKey([0, 11])).send();
    }

    destroy() {        
    }
}