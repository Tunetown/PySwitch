/**
 * Traffic statistics of the virtual Fractal client (messages per second in both directions).
 */
class VirtualFractalStats {

    data = {
        receiveRate: 0,
        sendRate: 0,
        messagesSent: [],
        messagesReceived: []
    }

    #callbacks = [];

    #messagesSent = [];
    #messagesReceived = [];
    #lastTime = 0;
    #timeout = null;

    #interval = 1000; // Milliseconds

    constructor() {
        this.reset();
        this.#scheduleMeasurement();
    }

    reset() {
        this.#messagesSent = [];
        this.#messagesReceived = [];
        this.#lastTime = Date.now();
    }

    /**
     * Adds a callback on changing the stats: callback(data) => void
     */
    addChangeCallback(callback) {
        this.#callbacks.push(callback);
    }

    messageReceived(msg, hintText = "") {
        this.#messagesReceived.push({
            message: msg,
            hint: hintText
        });
    }

    messageSent(msg, hintText = "") {
        this.#messagesSent.push({
            message: msg,
            hint: hintText
        });
    }

    /**
     * Stops measuring
     */
    destroy() {
        clearTimeout(this.#timeout);
        this.#callbacks = [];
    }

    /**
     * Take stats measurement
     */
    #measure() {
        const seconds = Math.max((Date.now() - this.#lastTime) / 1000, 0.001);

        this.data = {
            receiveRate: Math.round(this.#messagesReceived.length / seconds),
            sendRate: Math.round(this.#messagesSent.length / seconds),
            messagesSent: this.#messagesSent,
            messagesReceived: this.#messagesReceived
        }

        for (const cb of this.#callbacks) {
            cb(this.data);
        }

        this.reset();
        this.#scheduleMeasurement();
    }

    #scheduleMeasurement() {
        const that = this;
        this.#timeout = setTimeout(function() {
            try {
                that.#measure();
            } catch (e) {
                console.error(e);
            }
        }, this.#interval);
    }
}
