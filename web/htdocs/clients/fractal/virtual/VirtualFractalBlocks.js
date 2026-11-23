/**
 * Block (effect) definitions of the gen-3 Fractal devices for the virtual Fractal client.
 *
 * IDs: 3rd-party spec rev 1.4, Appendix 1 (claude/001 Fractal Support/FRACTAL.md 4).
 * Names, abbreviations and instances per model: Fractal Audio Blocks Guide, "Product Comparison".
 * Instance counts are [ Axe-Fx III, FM9, FM3 ] (see FractalClient.MODELS countIndex).
 * Channel counts of blocks without channels (1) are assumptions.
 */
class VirtualFractalBlocks {

    // First ID of the regular blocks, 4 IDs per block type
    static FIRST_REGULAR_ID = 46;
    static IDS_PER_TYPE = 4;

    // Regular block types in enum order: [ name, abbreviation, instance counts, channels ]
    static TYPES = [
        ["Compressor",     "CMP", [4, 2, 2], 4],     // COMP
        ["Graphic EQ",     "GEQ", [4, 4, 2], 4],     // GRAPHEQ
        ["Parametric EQ",  "PEQ", [4, 4, 2], 4],     // PARAEQ
        ["Amp",            "AMP", [2, 2, 1], 4],     // DISTORT
        ["Cab",            "CAB", [2, 2, 1], 4],     // CAB
        ["Reverb",         "REV", [2, 2, 1], 4],     // REVERB
        ["Delay",          "DLY", [4, 2, 2], 4],     // DELAY
        ["Multi-Delay",    "MTD", [2, 2, 1], 4],     // MULTITAP
        ["Chorus",         "CHO", [2, 2, 2], 4],     // CHORUS
        ["Flanger",        "FLG", [2, 2, 2], 4],     // FLANGER
        ["Rotary",         "ROT", [2, 2, 2], 4],     // ROTARY
        ["Phaser",         "PHA", [2, 2, 2], 4],     // PHASER
        ["Wah",            "WAH", [2, 2, 2], 4],     // WAH
        ["Formant",        "FRM", [2, 2, 2], 4],     // FORMANT
        ["Volume/Pan",     "VOL", [4, 4, 2], 4],     // VOLUME
        ["Tremolo",        "TRM", [2, 2, 2], 4],     // TREMOLO
        ["Pitch Shift",    "PIT", [2, 1, 1], 4],     // PITCH
        ["Filter",         "FIL", [4, 4, 4], 4],     // FILTER
        ["Drive",          "DRV", [4, 3, 2], 4],     // FUZZ
        ["Enhancer",       "ENH", [2, 2, 2], 4],     // ENHANCER
        ["Mixer",          "MIX", [4, 4, 4], 4],     // MIXER
        ["Synth",          "SYN", [2, 1, 1], 4],     // SYNTH
        ["Vocoder",        "VOC", [1, 0, 0], 4],     // VOCODER
        ["Megatap",        "MGT", [2, 2, 1], 4],     // MEGATAP
        ["Crossover",      "XVR", [2, 2, 0], 4],     // CROSSOVER
        ["Gate/Expander",  "GTE", [4, 4, 2], 4],     // GATE
        ["Ring Mod",       "RNG", [1, 1, 1], 4],     // RINGMOD
        ["Multiband Comp", "MBC", [2, 2, 1], 4],     // MULTICOMP
        ["Ten-Tap Delay",  "TTD", [2, 2, 1], 4],     // TENTAP
        ["Resonator",      "RES", [2, 2, 2], 4],     // RESONATOR
        ["Looper",         "LPR", [1, 1, 1], 1],     // LOOPER
        ["Tone Match",     "TMA", [1, 0, 0], 1],     // TONEMATCH
        ["RTA",            "RTA", [1, 0, 0], 1],     // RTA
        ["Plex Delay",     "PLX", [2, 1, 1], 4],     // PLEX
        ["Send",           "SND", [2, 2, 2], 1],     // FBSEND
        ["Return",         "RTN", [2, 2, 2], 1]      // FBRETURN
    ];

    // Special blocks: [ first ID, name, abbreviation, instance counts, channels ]
    static SPECIAL = [
        [37,  "Input",       "IN",   [5, 4, 2], 1],
        [42,  "Output",      "OUT",  [4, 3, 2], 1],
        [190, "Scene MIDI",  "MIDI", [1, 1, 1], 1],
        [191, "Multiplexer", "MUX",  [2, 2, 2], 6],
        [195, "IR Player",   "IRP",  [2, 0, 0], 4]
    ];

    /**
     * Returns info about a block ID, or null if unknown:
     * {
     *     id:        Effect ID
     *     name:      Long name ("Drive")
     *     abbr:      Abbreviation ("DRV")
     *     instance:  Instance (1-based)
     *     counts:    Instance counts per model
     *     channels:  Number of channels
     * }
     */
    static get(id) {
        const first = VirtualFractalBlocks.FIRST_REGULAR_ID;
        const perType = VirtualFractalBlocks.IDS_PER_TYPE;

        if (id >= first && id < first + perType * VirtualFractalBlocks.TYPES.length) {
            const type = VirtualFractalBlocks.TYPES[Math.floor((id - first) / perType)];
            return {
                id: id,
                name: type[0],
                abbr: type[1],
                instance: (id - first) % perType + 1,
                counts: type[2],
                channels: type[3]
            };
        }

        for (const special of VirtualFractalBlocks.SPECIAL) {
            const instance = id - special[0] + 1;
            if (instance < 1 || instance > Math.max(...special[3])) continue;

            return {
                id: id,
                name: special[1],
                abbr: special[2],
                instance: instance,
                counts: special[3],
                channels: special[4]
            };
        }

        return null;
    }

    /**
     * Returns the effect ID for an abbreviation and instance, or null if not found.
     */
    static idOf(abbr, instance = 1) {
        for (let i = 0; i < VirtualFractalBlocks.TYPES.length; ++i) {
            if (VirtualFractalBlocks.TYPES[i][1] != abbr) continue;
            return VirtualFractalBlocks.FIRST_REGULAR_ID + VirtualFractalBlocks.IDS_PER_TYPE * i + instance - 1;
        }

        for (const special of VirtualFractalBlocks.SPECIAL) {
            if (special[2] != abbr) continue;
            return special[0] + instance - 1;
        }

        return null;
    }

    /**
     * Returns if the block ID is available on the model with the given count index
     */
    static isAvailable(id, countIndex) {
        const info = VirtualFractalBlocks.get(id);
        if (!info) return false;

        return info.instance <= info.counts[countIndex];
    }

    /**
     * Returns all block IDs available on the model with the given count index, sorted by ID.
     */
    static getAvailable(countIndex) {
        const ret = [];

        for (const special of VirtualFractalBlocks.SPECIAL) {
            for (let i = 0; i < special[3][countIndex]; ++i) {
                ret.push(special[0] + i);
            }
        }

        for (let t = 0; t < VirtualFractalBlocks.TYPES.length; ++t) {
            for (let i = 0; i < VirtualFractalBlocks.TYPES[t][2][countIndex]; ++i) {
                ret.push(VirtualFractalBlocks.FIRST_REGULAR_ID + VirtualFractalBlocks.IDS_PER_TYPE * t + i);
            }
        }

        return ret.sort((a, b) => a - b);
    }

    /**
     * Returns a display name for the block ID, e.g. "Drive 1"
     */
    static getDisplayName(id) {
        const info = VirtualFractalBlocks.get(id);
        if (!info) return "Unknown (" + id + ")";

        return info.name + " " + info.instance;
    }
}
