class VirtualKemperStats {

    data = {
        receiveRate: 0,
        sentRate: 0,
        messagesSent: [],
        messagesReceived: []
    }

    #callbacks = []

    #messagesSent = [];
    #messagesReceived = [];
    #lastTime = 0;

    #interval = 1000; // Milliseconds

    constructor() {
        this.#measure();
    }

    reset() {
        this.#messagesSent = [];
        this.#messagesReceived = [];
        this.#lastTime = Date.now();
    }

    /**
     * Adds a callback on changing the stats. (stats) => void
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
     * Take stats measurement
     */
    #measure() {
        const factor = ((Date.now() - this.#lastTime) / 1000);

        this.data = {
            receiveRate: Math.round(this.#messagesReceived.length * factor),
            sendRate: Math.round(this.#messagesSent.length * factor),
            messagesSent: this.#messagesSent,
            messagesReceived: this.#messagesReceived
        }
        
        for(const cb of this.#callbacks) {
            cb(this.data)
        }

        this.reset();

        const that = this;
        setTimeout(function() {
            that.#measure();
        }, this.#interval);
    }
}