class PeriodCounter {

    interval = null;

    #lastReset = 0;
    #overrideTimeCallback = null;

    constructor(intervalMillis, overrideTimeCallback = null) {
        this.interval = intervalMillis;
        this.#overrideTimeCallback = overrideTimeCallback;

        this.reset();
    }
    
    /**
     * Resets the period counter to the current time
     */
    reset() {
        this.#lastReset = this.#getCurrentTimestamp();
    }

    /**
     * Returns the amount of milliseconds passed since the last reset
     */
    passed() {
        return this.#getCurrentTimestamp() - this.#lastReset;
    }

    /**
     * Returns if the period has been exceeded. If yes, it lso resets 
     * the period to the current time.
     */
    exceeded() {
        const currentTime = this.#getCurrentTimestamp();
        if (this.#lastReset + this.interval < currentTime) {
            this.#lastReset = currentTime;
            return true;
        }
        return false;
    }

    /**
     * Returns current unix timestamp
     */
    #getCurrentTimestamp() {
        if (this.#overrideTimeCallback) {
            return this.#overrideTimeCallback();
        }
        return Date.now();
    }
}