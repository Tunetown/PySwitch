const KEMPER_MANUFACTURER_ID = [0x00, 0x20, 0x33];

const NRPN_PRODUCT_TYPE_PROFILER_PLAYER = 0x02;
const NRPN_PRODUCT_TYPE = NRPN_PRODUCT_TYPE_PROFILER_PLAYER;

/**
 * Detects if a Kemper device is listening
 */
class KemperClientDetector extends ClientDetector {
    
    /**
     * Tests if a Kemper device is listening. Returns the listener generated (has to detached!)
     */
    async test(midiHandler, input, output, resolve) {
        let listener = null;

        // Listen to the requested parameter
        midiHandler.addListener(
            listener = new MidiListener(
                input.name,
                async function(data) {
                    // Check if its a sysex message
                    if (data[0] != 0xf0 || data[data.length - 1] != 0xf7) {
                        return;
                    }
                    
                    const manufacturerId = Array.from(data).slice(1, 4);
                    const msgData = Array.from(data).slice(4, data.length - 1);

                    if (JSON.stringify(manufacturerId) != JSON.stringify(KEMPER_MANUFACTURER_ID)) return;
                    
                    if (JSON.stringify(msgData.slice(2, 6)) != JSON.stringify([
                        0x01,                 // Response: Single parameter
                        0x00,                 // Device ID (always 0)
                        0x04,                 // Address page: Rig parameters
                        0x01                  // Parameter: Rig volume
                    ])) return;

                    resolve();
                }
            )
        );

        // Send a request for rig volume which the Kemper has to answer
        const msg = [
            0xf0                      // Sysex status
        ].concat(
            KEMPER_MANUFACTURER_ID,   
            [
                NRPN_PRODUCT_TYPE,
                0x7f,                 // Device ID: Omni
                0x41,                 // Request single parameter
                0x00,                 // Device ID (always 0)
                0x04,                 // Address page: Rig parameters
                0x01,                 // Parameter: Rig volume
                0xf7                  // End of Sysex
            ]
        );
        
        await output.send(msg);

        return listener;
    }
}