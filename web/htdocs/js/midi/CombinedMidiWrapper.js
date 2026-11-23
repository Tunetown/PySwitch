/**
 * MIDI wrapper combining several MIDI wrappers (virtual clients and/or PythonMidiWrapper instances for real
 * devices), used when a configuration controls several clients. Like the MIDI routing on the controller, every
 * message sent by PySwitch is sent to all wrappers, and the messages of all wrappers are received.
 * Spec: claude/001 Fractal Support/spec/emulator/multi_client.md
 */
class CombinedMidiWrapper {

    messageQueue = [];   // Queue of raw MIDI bytes, shared with all wrappers (they push their incoming messages here)
    wrappers = null;     // Combined wrappers

    constructor(wrappers) {
        this.wrappers = wrappers;

        // All wrappers push their incoming messages into the shared queue
        for (const wrapper of this.wrappers) {
            wrapper.messageQueue = this.messageQueue;
        }
    }

    /**
     * Send a MIDI message to all wrappers. Expects a byte array of raw data (python proxy).
     */
    async send(message) {
        // Convert once: the python proxy may not be valid anymore after the first await
        const data = message.toJs();
        const proxy = {
            toJs: function() {
                return data;
            }
        };

        await Promise.all(
            this.wrappers.map((wrapper) => wrapper.send(proxy))
        );
    }

    /**
     * Start processing regular updates of all wrappers which support this (virtual clients)
     */
    run(updateInterval) {
        for (const wrapper of this.wrappers) {
            if (wrapper.run) wrapper.run(updateInterval);
        }
    }

    /**
     * Updates all wrappers which support this (virtual clients)
     */
    update() {
        for (const wrapper of this.wrappers) {
            if (wrapper.update) wrapper.update();
        }
    }

    /**
     * Stop listening on all wrappers
     */
    detach() {
        for (const wrapper of this.wrappers) {
            wrapper.detach();
        }
    }

    /**
     * Tries to return a meaningful message name (first wrapper which knows the message)
     */
    getMessageProperties(message) {
        for (const wrapper of this.wrappers) {
            if (!wrapper.getMessageProperties) continue;

            const props = wrapper.getMessageProperties(message);
            if (props) return props;
        }
        return null;
    }
}
