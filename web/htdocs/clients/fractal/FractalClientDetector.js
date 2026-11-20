/**
 * Detects if a Fractal device is listening. The model cannot be queried, so a scene query
 * is sent with the model byte of each supported model; any valid answer identifies the device.
 */
class FractalClientDetector extends ClientDetector {

    /**
     * Tests if a Fractal device is listening. Returns the listener generated (has to be detached!)
     */
    async test(midiHandler, input, output, resolve) {
        let listener = null;

        midiHandler.addListener(
            listener = new MidiListener(
                input.name,
                async function(data) {
                    // Check if its a sysex message
                    if (data[0] != 0xf0 || data[data.length - 1] != 0xf7) {
                        return;
                    }

                    const msg = Array.from(data);

                    if (!Tools.compareArrays(msg.slice(1, 4), FractalClient.MANUFACTURER_ID)) return;
                    if (msg[5] != 0x0c) return;                                     // Scene answer
                    if (FractalClient.getModelId(msg[4]) === null) return;

                    resolve();
                }
            )
        );

        // Query the current scene with every known model byte
        for (const id in FractalClient.MODELS) {
            await output.send(
                FractalClient.createSysex(FractalClient.MODELS[id].modelByte, 0x0c, [0x7f])
            );
        }

        return listener;
    }
}
