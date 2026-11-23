/**
 * Base class for the Kemper example tests: access to the virtual Kemper client, bank colors.
 * The general helpers (pressing switches, ticks, LEDs, labels) are in ExampleTestBase.
 */
class KemperTestBase extends ExampleTestBase {
    
    #infoProvider = null;

    /**
     * The virtual Kemper client (the configuration may use further clients)
     */
    get client() {
        return this.runner.runner.clients.kemper;
    }

    /**
     * Sets the rig ID on the virtual client (like on the device) and waits for PySwitch to follow
     */
    async setRigId(rigId) {
        this.client.setRigId(rigId);
        await this.ticks();
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

    /**
     * Starts recording the MIDI messages sent by PySwitch to the virtual Kemper (as arrays of bytes)
     */
    startRecording() {
        const client = this.client;
        if (!client.recordedMessages) {
            const doSend = client.doSend.bind(client);
            client.doSend = function(message) {
                client.recordedMessages.push(Array.from(message));
                return doSend(message);
            };
        }
        client.recordedMessages = [];
    }

    /**
     * Returns the values of the CC messages with the passed control number recorded since startRecording()
     */
    recordedCC(control) {
        return this.client.recordedMessages
            .filter((m) => m.length == 3 && (m[0] & 0xf0) == 0xb0 && m[1] == control)
            .map((m) => m[2]);
    }

    /**
     * Returns all CC messages ([control, value]) recorded since startRecording() or the last call, and clears them.
     * PySwitch polls with SysEx messages, so CC messages are only sent by the actions (NRPN: CC 99, 98, 6, 38).
     */
    takeCCs() {
        const ret = this.client.recordedMessages
            .filter((m) => m.length == 3 && (m[0] & 0xf0) == 0xb0)
            .map((m) => [m[1], m[2]]);

        this.client.recordedMessages = [];
        return ret;
    }

    /**
     * Returns the value of a parameter of the virtual Kemper (key: NRPNKey, CCKey, ...)
     */
    param(key) {
        return this.client.parameters.get(key).value;
    }

    /**
     * Expects the LED color of a switch and optionally the color of a display pixel (label)
     */
    expectColors(name, ledColor, labelTestCoordinates = null, labelColor = null) {
        expect(this.led(name)).toEqual(ledColor);
        if (labelTestCoordinates) expect(this.runner.getDisplayColorAt(labelTestCoordinates)).toEqual(labelColor);
    }
}
