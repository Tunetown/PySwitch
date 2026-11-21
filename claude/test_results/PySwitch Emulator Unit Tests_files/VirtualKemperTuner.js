class VirtualKemperTuner {
    
    #client = null;
    #period = null;
    
    running = false;
    
    constructor(client, overrideTimeCallback) {
        this.#client = client;

        this.#period = new PeriodCounter(20, overrideTimeCallback);
    }

    update() {
        if (this.running && this.#period.exceeded()) {
            this.#sendState();
        }
    }

    #sendState() {
        // Note
        this.#client.parameters.get(new NRPNKey([125, 84])).send();

        // Deviance
        this.#client.parameters.get(new NRPNKey([124, 15])).send();
    }

    destroy() {        
    }
}