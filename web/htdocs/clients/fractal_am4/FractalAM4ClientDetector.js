/**
 * Detects if a Fractal AM4 is listening: sends the (confirmed) preset number request and waits for the answer.
 */
class FractalAM4ClientDetector extends ClientDetector {

    /**
     * Tests if an AM4 is listening. Returns the listener generated (has to be detached!)
     */
    async test(midiHandler, input, output, resolve) {
        let listener = null;

        midiHandler.addListener(
            listener = new MidiListener(
                input.name,
                async function(data) {
                    if (data[0] != 0xf0 || data[data.length - 1] != 0xf7) return;

                    const msg = Array.from(data);

                    if (!Tools.compareArrays(msg.slice(1, 4), FractalAM4Client.MANUFACTURER_ID)) return;
                    if (msg[4] != FractalAM4Client.MODEL_BYTE) return;
                    if (msg[5] != 0x14) return;                                     // Preset number answer

                    resolve();
                }
            )
        );

        await output.send(FractalAM4Client.createSysex(0x14));

        return listener;
    }
}
