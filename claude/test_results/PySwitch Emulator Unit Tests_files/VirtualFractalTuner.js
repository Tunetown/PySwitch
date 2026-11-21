/**
 * Tuner of the virtual Fractal client. While on, it pushes tuner data continuously
 * (if Send Realtime Sysex is on): F0 00 01 74 <model> 11 nn ss cc F7 (no checksum).
 */
class VirtualFractalTuner {

    static PUSH_INTERVAL_MILLIS = 50;

    // Notes of the open strings, low E first
    static OPEN_STRINGS = [4, 9, 2, 7, 11, 4];

    // Range of the cents input (offset binary on the wire: 63 = 0)
    static MAX_CENTS = 50;

    #client = null;
    #period = null;
    #callbacks = [];

    enabled = false;
    note = 9;            // 0-11 (0 = C)
    cents = 0;           // -50..50

    constructor(client, overrideTimeCallback = null) {
        this.#client = client;
        this.#period = new PeriodCounter(VirtualFractalTuner.PUSH_INTERVAL_MILLIS, overrideTimeCallback);
    }

    /**
     * Called regularly: sends the push data while the tuner is on
     */
    update() {
        if (!this.enabled || !this.#client.options.sendRealtimeSysex) return;
        if (!this.#period.exceeded()) return;

        this.#client.queueMessage(
            FractalClient.createSysex(
                this.#client.model.modelByte,
                VirtualFractalProtocol.FN_TUNER,
                [this.note, this.string(), 63 + this.cents],
                false
            ),
            "Tuner Data"
        );
    }

    /**
     * Returns the string (0-5, 0 = low E) for the current note: the first open string with the same note, else 0.
     */
    string() {
        const ind = VirtualFractalTuner.OPEN_STRINGS.indexOf(this.note);
        return (ind >= 0) ? ind : 0;
    }

    /**
     * Switches the tuner on or off
     */
    setEnabled(enabled) {
        this.enabled = !!enabled;
        this.#notify();
    }

    /**
     * Sets the note (0-11)
     */
    setNote(note) {
        this.note = ((Math.round(note) % 12) + 12) % 12;
        this.#notify();
    }

    /**
     * Sets the cents deviation
     */
    setCents(cents) {
        this.cents = Math.min(Math.max(Math.round(cents), -VirtualFractalTuner.MAX_CENTS), VirtualFractalTuner.MAX_CENTS);
        this.#notify();
    }

    /**
     * Adds a callback on change: callback() => void
     */
    addChangeCallback(callback) {
        this.#callbacks.push(callback);
    }

    destroy() {
        this.#callbacks = [];
    }

    #notify() {
        for (const cb of this.#callbacks) {
            cb();
        }
    }
}
