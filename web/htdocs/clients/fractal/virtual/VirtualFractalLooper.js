/**
 * Looper state machine of the virtual Fractal client (Fractal Audio Blocks Guide, Looper block).
 * Only works while the current preset contains a Looper block, like on the device.
 */
class VirtualFractalLooper {

    // Buttons (3rd-party command 0F)
    static BUTTON_RECORD = 0;
    static BUTTON_PLAY = 1;
    static BUTTON_UNDO = 2;
    static BUTTON_ONCE = 3;
    static BUTTON_REVERSE = 4;
    static BUTTON_HALF = 5;

    // State bits
    static BIT_RECORD = 0x01;
    static BIT_PLAY = 0x02;
    static BIT_OVERDUB = 0x04;
    static BIT_ONCE = 0x08;
    static BIT_REVERSE = 0x10;
    static BIT_HALF = 0x20;

    #client = null;
    #callbacks = [];

    recording = false;
    playing = false;
    overdub = false;
    once = false;
    reverse = false;
    half = false;

    loopLength = 0;             // Milliseconds, 0 = no loop recorded
    layers = 0;                 // Number of recorded layers
    #undoneLayers = 0;          // Layers which can be restored by Undo

    #recordStart = 0;
    #playStart = 0;
    #onceEnd = 0;

    constructor(client) {
        this.#client = client;
    }

    /**
     * Resets the looper (erases the loop)
     */
    reset() {
        this.recording = false;
        this.playing = false;
        this.overdub = false;
        this.once = false;
        this.reverse = false;
        this.half = false;

        this.#erase();
        this.#notify();
    }

    /**
     * Called regularly: stops "once" playback at the end of the loop
     */
    update() {
        if (!this.playing || !this.once) return;
        if (this.#client.now() < this.#onceEnd) return;

        if (this.overdub) this.#endOverdub();

        this.playing = false;
        this.once = false;

        this.#notify();
    }

    /**
     * Returns the state bit field as sent to the controller (0 when the preset has no Looper block)
     */
    state() {
        if (!this.#client.presets.hasLooper()) return 0;

        return (this.recording ? VirtualFractalLooper.BIT_RECORD : 0)
            | (this.playing ? VirtualFractalLooper.BIT_PLAY : 0)
            | (this.overdub ? VirtualFractalLooper.BIT_OVERDUB : 0)
            | (this.once ? VirtualFractalLooper.BIT_ONCE : 0)
            | (this.reverse ? VirtualFractalLooper.BIT_REVERSE : 0)
            | (this.half ? VirtualFractalLooper.BIT_HALF : 0);
    }

    /**
     * Press a looper button. Returns if the press had any effect.
     */
    press(button) {
        if (!this.#client.presets.hasLooper()) return false;

        switch (button) {
            case VirtualFractalLooper.BUTTON_RECORD: this.#record(); break;
            case VirtualFractalLooper.BUTTON_PLAY: this.#play(); break;
            case VirtualFractalLooper.BUTTON_UNDO: this.#undo(); break;
            case VirtualFractalLooper.BUTTON_ONCE: this.#once(); break;
            case VirtualFractalLooper.BUTTON_REVERSE: this.reverse = !this.reverse; break;
            case VirtualFractalLooper.BUTTON_HALF: this.half = !this.half; break;
            default: return false;
        }

        this.#notify();
        return true;
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

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Record: starts recording when stopped, toggles overdub while playing. While recording,
     * the option recordSecondPress (overdub, play, stop) decides.
     */
    #record() {
        if (this.recording) {
            this.#endRecording();

            switch (this.#client.options.recordSecondPress) {
                case "play":
                    this.#startPlayback();
                    break;

                case "stop":
                    break;

                default:
                    this.#startPlayback();
                    this.overdub = true;
            }
            return;
        }

        if (this.playing) {
            if (this.overdub) {
                this.#endOverdub();
            } else {
                this.overdub = true;
            }
            return;
        }

        // Stopped: record a new loop
        this.#erase();
        this.recording = true;
        this.#recordStart = this.#client.now();
    }

    /**
     * Play: ends recording/overdub (playback continues), else starts/stops playback
     */
    #play() {
        if (this.recording) {
            this.#endRecording();
            this.#startPlayback();
            return;
        }

        if (this.overdub) {
            this.#endOverdub();
            return;
        }

        if (this.playing) {
            this.playing = false;
            this.once = false;
            return;
        }

        if (this.loopLength > 0) {
            this.#startPlayback();
        }
    }

    /**
     * Undo: erases when stopped, undoes/restores the last layer while playing
     */
    #undo() {
        if (this.recording) {
            this.recording = false;
            this.#erase();
            return;
        }

        if (!this.playing) {
            this.#erase();
            return;
        }

        if (this.overdub) {
            // Discard the current overdub pass
            this.overdub = false;
            return;
        }

        if (this.#undoneLayers > 0) {
            this.#undoneLayers--;
            this.layers++;
            return;
        }

        if (this.layers > 1) {
            this.layers--;
            this.#undoneLayers++;
        }
    }

    /**
     * Once: stops at the end of the loop; retriggers when pressed again; stops a recording
     */
    #once() {
        if (this.recording) {
            this.#endRecording();
            return;
        }

        if (this.playing) {
            if (this.once) {
                // Retrigger
                this.#playStart = this.#client.now();
                this.#onceEnd = this.#playStart + this.#effectiveLength();
            } else {
                this.once = true;

                const elapsed = this.#client.now() - this.#playStart;
                const cycles = Math.max(1, Math.ceil(elapsed / this.#effectiveLength()));
                this.#onceEnd = this.#playStart + cycles * this.#effectiveLength();
            }
            return;
        }

        if (this.loopLength > 0) {
            this.#startPlayback();
            this.once = true;
            this.#onceEnd = this.#playStart + this.#effectiveLength();
        }
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    #endRecording() {
        this.recording = false;
        this.loopLength = Math.max(1, this.#client.now() - this.#recordStart);
        this.layers = 1;
        this.#undoneLayers = 0;
    }

    #endOverdub() {
        this.overdub = false;
        this.layers++;
        this.#undoneLayers = 0;
    }

    #startPlayback() {
        this.playing = true;
        this.#playStart = this.#client.now();
    }

    #erase() {
        this.loopLength = 0;
        this.layers = 0;
        this.#undoneLayers = 0;
        this.playing = false;
        this.overdub = false;
        this.once = false;
    }

    /**
     * Loop length regarding half speed
     */
    #effectiveLength() {
        return this.loopLength * (this.half ? 2 : 1);
    }

    #notify() {
        for (const cb of this.#callbacks) {
            cb();
        }
    }
}
