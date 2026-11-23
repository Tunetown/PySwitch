/**
 * Client implementation for the Fractal Audio Axe-Fx II (Mark I/II, XL, XL+), experimental.
 * Spec: claude/001 Fractal Support/spec/axe_fx_ii/axe_fx_ii.md, protocol: spec/axe_fx_ii/protocol.md
 */
class FractalIIClient extends Client {

    // Fractal manufacturer ID
    static MANUFACTURER_ID = [0x00, 0x01, 0x74];

    // Supported models (model byte: data)
    static MODELS = {
        3: { name: "Axe-Fx II", numPresets: 384 },
        6: { name: "Axe-Fx II XL", numPresets: 768 },
        7: { name: "Axe-Fx II XL+", numPresets: 768 }
    };

    // Default model byte (same as the default of the fractalIIModel option in config.py)
    static DEFAULT_MODEL = 7;

    static NUM_SCENES = 8;

    // Blocks: effect ID => [name, abbreviation, instance] (switchable blocks, same as FractalIIBlock in Python)
    static BLOCKS = FractalIIClient.#createBlocks();

    static #createBlocks() {
        const types = [
            ["Compressor", "CPR", [100, 101]], ["Graphic EQ", "GEQ", [102, 103, 160, 161]], ["Param EQ", "PEQ", [104, 105, 162, 163]],
            ["Amp", "AMP", [106, 107]], ["Cab", "CAB", [108, 109]], ["Reverb", "REV", [110, 111]], ["Delay", "DLY", [112, 113]],
            ["MultiDly", "MTD", [114, 115]], ["Chorus", "CHO", [116, 117]], ["Flanger", "FLG", [118, 119]], ["Rotary", "ROT", [120, 121]],
            ["Phaser", "PHA", [122, 123]], ["Wah", "WAH", [124, 125]], ["Formant", "FRM", [126]], ["Volume", "VOL", [127, 166, 167, 168]],
            ["TremPan", "TRM", [128, 129]], ["Pitch", "PIT", [130, 153]], ["Filter", "FIL", [131, 132, 164, 165]], ["Drive", "DRV", [133, 134]],
            ["Enhancer", "ENH", [135]], ["FX Loop", "FXL", [136]], ["Mixer", "MIX", [137, 138]], ["Synth", "SYN", [144, 145]],
            ["Vocoder", "VOC", [146]], ["Megatap", "MGT", [147]], ["Crossover", "XVR", [148, 149]], ["Gate", "GTE", [150, 151]],
            ["Ring Mod", "RNG", [152]], ["MultiComp", "MBC", [154, 155]], ["QuadChorus", "QCH", [156, 157]], ["Resonator", "RES", [158, 159]],
            ["Looper", "LPR", [169]], ["Tone Match", "TMA", [170]]
        ];

        const ret = {};
        for (const [name, short, ids] of types) {
            ids.forEach((id, i) => ret[id] = [name, short, i + 1]);
        }
        return ret;
    }

    /**
     * Returns the block name for an effect ID ("Amp 1", short: "AMP1"), or null
     */
    static getBlockName(id, short = false) {
        const block = FractalIIClient.BLOCKS[id];
        if (!block) return null;
        return short ? (block[1] + block[2]) : (block[0] + " " + block[2]);
    }

    /**
     * Returns the model data for a model byte, or null if unknown
     */
    static getModel(modelByte) {
        return FractalIIClient.MODELS[modelByte] || null;
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
        const msg = [0xf0].concat(FractalIIClient.MANUFACTURER_ID, [modelByte, func], data);
        if (withChecksum) {
            msg.push(FractalIIClient.checksum(msg));
        }
        msg.push(0xf7);
        return msg;
    }

    /**
     * Name as 32 bytes (space padded)
     */
    static nameBytes(name) {
        const ret = [];
        for (let i = 0; i < 32; ++i) {
            ret.push(i < name.length ? (name.charCodeAt(i) & 0x7f) : 0x20);
        }
        return ret;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Returns a display name for the client
     */
    getDisplayName() {
        return "Fractal Axe-Fx II";
    }

    /**
     * Sort string among all clients available: after the AM4 (Boomerang uses "YYY_", local actions "ZZZ...")
     */
    getSortString() {
        return "XXZ_" + this.id;
    }

    /**
     * Returns a ClientDetector instance for the client
     */
    async getClientDetector() {
        return new FractalIIClientDetector();
    }

    /**
     * Returns a virtual Axe-Fx II. Without options (emulator UI), the model is taken from the emulator settings
     * (fractalIIModel in config.py); callers passing options (tests) get the model of options.config.fractalIIModel,
     * else the default model.
     */
    async getVirtualClient(options) {
        return new VirtualFractalIIClient(
            {
                ...{
                    model: FractalIIClient.#getModelFromConfig(options ? options.config : FractalIIClient.#getConfig()),
                    sendRealtimeSysex: true             // Simulates I/O > MIDI > SEND REALTIME SYSEX = ALL
                },
                ...(options || {})
            }
        );
    }

    /**
     * Returns the model byte for config.py options (fractalIIModel), or the default model
     */
    static #getModelFromConfig(config) {
        const model = config ? config.fractalIIModel : null;
        return FractalIIClient.getModel(model) ? model : FractalIIClient.DEFAULT_MODEL;
    }

    /**
     * Returns the config.py options of the emulator settings
     */
    static #getConfig() {
        try {
            return (new LocalState("global-settings")).get("config.py") || {};

        } catch (e) {
            console.error(e);
        }
        return {};
    }

    /**
     * Can resolve tokens related to value ranges etc. in meta.json
     */
    async resolveValueToken(value) {
        // Ranges for the largest models (XL, XL+)
        switch(value) {
            case "NUM_PRESETS": return 768;
            case "MAX_PRESET": return 767;
            case "NUM_BANKS": return 768;
            case "NUM_SCENES": return 8;
        }

        return value;
    }
}
