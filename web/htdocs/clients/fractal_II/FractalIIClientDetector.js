/**
 * Detects if a Fractal Axe-Fx II is listening: sends the preset number request (protocol.md 4.1) with the model byte of
 * every supported model and waits for an answer.
 */
class FractalIIClientDetector extends ClientDetector {

    /**
     * Tests if an Axe-Fx II is listening. Returns the listener generated (has to be detached!)
     */
    async test(midiHandler, input, output, resolve) {
        let listener = null;

        midiHandler.addListener(
            listener = new MidiListener(
                input.name,
                async function(data) {
                    if (data[0] != 0xf0 || data[data.length - 1] != 0xf7) return;

                    const msg = Array.from(data);

                    if (!Tools.compareArrays(msg.slice(1, 4), FractalIIClient.MANUFACTURER_ID)) return;
                    if (!FractalIIClient.getModel(msg[4])) return;
                    if (msg[5] != 0x14 || msg.length != 10) return;                 // Preset number answer

                    resolve();
                }
            )
        );

        for (const model in FractalIIClient.MODELS) {
            await output.send(FractalIIClient.createSysex(parseInt(model), 0x14));
        }

        return listener;
    }
}
