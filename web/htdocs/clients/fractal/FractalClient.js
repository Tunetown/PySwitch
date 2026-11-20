/**
 * Client implementation for Fractal Audio devices (Axe-Fx III, FM9, FM3).
 * Protocol reference: claude/FRACTAL.md
 */
class FractalClient extends Client {

    // Fractal manufacturer ID
    static MANUFACTURER_ID = [0x00, 0x01, 0x74];

    // Supported models. countIndex is the column of the block instance counts in VirtualFractalBlocks.
    static MODELS = {
        FM3: {
            name: "FM3",
            modelByte: 0x11,
            numPresets: 512,
            countIndex: 2
        },
        FM9: {
            name: "FM9",
            modelByte: 0x12,
            numPresets: 512,
            countIndex: 1
        },
        AXEFX3: {
            name: "Axe-Fx III",
            modelByte: 0x10,
            numPresets: 1024,
            countIndex: 0
        }
    };

    // Default model (same as the default of the fractalModel option in config.py)
    static DEFAULT_MODEL = "FM3";

    /**
     * Returns the model ID (key of MODELS) for a model byte, or null if unknown.
     */
    static getModelId(modelByte) {
        for (const id in FractalClient.MODELS) {
            if (FractalClient.MODELS[id].modelByte == modelByte) return id;
        }
        return null;
    }

    /**
     * XOR checksum of all passed bytes, masked to 7 bits
     */
    static checksum(bytes) {
        let cs = 0;
        for (const b of bytes) {
            cs ^= b;
        }
        return cs & 0x7f;
    }

    /**
     * Creates a SysEx message: F0 00 01 74 <model> <function> <data...> [<checksum>] F7
     */
    static createSysex(modelByte, func, data = [], withChecksum = true) {
        const msg = [0xf0].concat(FractalClient.MANUFACTURER_ID, [modelByte, func], data);
        if (withChecksum) {
            msg.push(FractalClient.checksum(msg));
        }
        msg.push(0xf7);
        return msg;
    }

    /**
     * Encodes a 14 bit value to two 7-bit bytes, LS first
     */
    static encode14(value) {
        return [value & 0x7f, (value >> 7) & 0x7f];
    }

    /**
     * Decodes two 7-bit bytes (LS first) to a 14 bit value
     */
    static decode14(lsb, msb) {
        return lsb + 128 * msb;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Returns a display name for the client
     */
    getDisplayName() {
        return "Fractal Audio";
    }

    /**
     * Returns a ClientDetector instance for the client
     */
    async getClientDetector() {
        return new FractalClientDetector();
    }

    /**
     * Returns a virtual client. Without options (emulator UI), the model is taken from the emulator settings
     * (fractalModel in config.py), so the virtual device answers the messages of the emulated controller.
     * Callers passing options (tests) get the default model unless they pass one.
     */
    async getVirtualClient(options) {
        return new VirtualFractalClient(
            {
                ...{
                    model: options ? FractalClient.DEFAULT_MODEL : FractalClient.#getConfiguredModel(),
                    sendRealtimeSysex: true,             // Simulates Setup > MIDI/Remote > Send Realtime Sysex = ON
                    recordSecondPress: "overdub"         // Looper block config "Record 2nd Press": overdub, play or stop
                },
                ...options
            }
        );
    }

    /**
     * Returns the model ID configured in the emulator settings (config.py: fractalModel), or the default model.
     */
    static #getConfiguredModel() {
        try {
            const config = (new LocalState("global-settings")).get("config.py") || {};
            const id = FractalClient.getModelId(config.fractalModel);
            if (id) return id;

        } catch (e) {
            console.error(e);
        }

        return FractalClient.DEFAULT_MODEL;
    }

    /**
     * Can resolve tokens related to value ranges etc. in meta.json
     */
    async resolveValueToken(value) {
        // Ranges for the largest model (Axe-Fx III); the bank count depends on the bank size (config.py), down to 1.
        switch(value) {
            case "NUM_PRESETS": return 1024;
            case "MAX_PRESET": return 1023;
            case "NUM_BANKS": return 1024;
            case "NUM_SCENES": return 8;
        }

        return value;
    }

    /**
     * If the client has mapping implementations in __init__.py, this can return the class name for them.
     */
    getInitMappingsClassName() {
        return "FractalMappings";
    }
}
