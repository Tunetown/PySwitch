class KemperTestBase {
    
    runner = null;
    #infoProvider = null;

    constructor(runner) {
        this.runner = runner;
    }

    /**
     * Returns a bank color with optional scaling
     */
    bankColor(bank, factor) {
        const col = this.#infoProvider.data.bankColors[bank % this.#infoProvider.data.numRigsPerBank]
        return [
            Math.floor(col[0] * factor),
            Math.floor(col[1] * factor),
            Math.floor(col[2] * factor)
        ]
    }

    /**
     * Returns an object providing basic client info, derived from PyScript directly.
     */
    async loadInfo() {
        if (this.#infoProvider) return this.#infoProvider.data;

        this.#infoProvider = new KemperInfoProvider(this.runner);
        await this.#infoProvider.init();
        
        return this.#infoProvider.data;
    }
}