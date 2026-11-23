/**
 * Client implementation for the Fractal Audio AM4 (experimental). The AM4 uses the protocol of AM4-Edit, not the
 * 3rd-party protocol of the other Fractal devices. Spec: claude/001 Fractal Support/spec/am4/protocol.md
 */
class FractalAM4Client extends Client {

    // Fractal manufacturer ID and the AM4 model byte
    static MANUFACTURER_ID = [0x00, 0x01, 0x74];
    static MODEL_BYTE = 0x15;

    static NUM_PRESETS = 104;
    static NUM_SCENES = 4;
    static NUM_SLOTS = 4;

    // Block IDs and names (same order)
    static BLOCK_IDS = [0x2e, 0x32, 0x36, 0x3a, 0x42, 0x46, 0x4e, 0x52, 0x56, 0x5a, 0x5e, 0x66, 0x6a, 0x72, 0x76, 0x7a, 0x92];
    static BLOCK_NAMES = [
        "Compressor", "Graphic EQ", "Param EQ", "Amp", "Reverb", "Delay", "Chorus", "Flanger", "Rotary", "Phaser",
        "Wah", "Volume", "Tremolo", "Filter", "Drive", "Enhancer", "Gate"
    ];

    // Footswitch modes (argument of the mode select message)
    static MODES = { 0x48: "Presets", 0x49: "Scenes", 0x4a: "Effects", 0x58: "Amp", 0x18: "Tuner" };

    /**
     * Returns the block name for an ID, or null
     */
    static getBlockName(id) {
        const index = FractalAM4Client.BLOCK_IDS.indexOf(id);
        return (index >= 0) ? FractalAM4Client.BLOCK_NAMES[index] : null;
    }

    /**
     * Location text like on the AM4 ("A01".."Z04")
     */
    static locationText(location) {
        return String.fromCharCode(65 + Math.floor(location / 4)) + "0" + (location % 4 + 1);
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
     * Creates an AM4 SysEx message: F0 00 01 74 15 <function> <data...> <checksum> F7
     */
    static createSysex(func, data = []) {
        const msg = [0xf0].concat(FractalAM4Client.MANUFACTURER_ID, [FractalAM4Client.MODEL_BYTE, func], data);
        msg.push(FractalAM4Client.checksum(msg));
        msg.push(0xf7);
        return msg;
    }

    /**
     * Two septets of a 14-bit value (LS first)
     */
    static encode14(value) {
        return [value & 0x7f, (value >> 7) & 0x7f];
    }

    /**
     * Packs raw bytes into septets (8-to-7 sliding window, restarting every 7 bytes)
     */
    static pack(raw) {
        const ret = [];
        for (let start = 0; start < raw.length; start += 7) {
            const chunk = raw.slice(start, start + 7);
            let carry = 0;
            for (let i = 0; i < chunk.length; ++i) {
                const k = i + 1;
                ret.push(((chunk[i] >> k) & 0x7f) | carry);
                carry = ((~(0x7f << k) & chunk[i]) << (7 - k)) & 0x7f;
            }
            ret.push(carry);
        }
        return ret;
    }

    /**
     * Unpacks num raw bytes from septets packed by pack(), starting at index
     */
    static unpack(msg, index, num) {
        const ret = [];
        while (ret.length < num) {
            const n = Math.min(7, num - ret.length);
            for (let i = 0; i < n; ++i) {
                const k = i + 1;
                ret.push((((msg[index + i] & ((1 << (8 - k)) - 1)) << k) | (msg[index + i + 1] >> (7 - k))) & 0xff);
            }
            index += n + 1;
        }
        return ret;
    }

    /**
     * Encodes raw bytes as a continuous MSB-first bitstream of septets (name table answer)
     */
    static encodeBitstream(raw) {
        const ret = [];
        let acc = 0;
        let bits = 0;
        for (const b of raw) {
            acc = ((acc << 8) | b) & 0x7fff;
            bits += 8;
            while (bits >= 7) {
                bits -= 7;
                ret.push((acc >> bits) & 0x7f);
            }
        }
        if (bits) ret.push((acc << (7 - bits)) & 0x7f);
        return ret;
    }

    /**
     * Raw bytes of a float32 / uint32 (little endian) and back
     */
    static floatBytes(value) {
        const view = new DataView(new ArrayBuffer(4));
        view.setFloat32(0, value, true);
        return [0, 1, 2, 3].map((i) => view.getUint8(i));
    }

    static uintBytes(value) {
        return [value & 0xff, (value >> 8) & 0xff, (value >> 16) & 0xff, (value >>> 24) & 0xff];
    }

    static toFloat(raw) {
        const view = new DataView(new Uint8Array(raw).buffer);
        return view.getFloat32(0, true);
    }

    static toUint(raw) {
        return (raw[0] | (raw[1] << 8) | (raw[2] << 16) | (raw[3] << 24)) >>> 0;
    }

    /**
     * Name as 32 bytes (space padded, NUL terminated if shorter)
     */
    static nameBytes(name) {
        const ret = [];
        for (let i = 0; i < 32; ++i) {
            ret.push(i < name.length ? (name.charCodeAt(i) & 0x7f) : (i == name.length ? 0x00 : 0x20));
        }
        return ret;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Returns a display name for the client
     */
    getDisplayName() {
        return "Fractal AM4";
    }

    /**
     * Sort string among all clients available: after Fractal (Boomerang uses "YYY_", local actions "ZZZ...")
     */
    getSortString() {
        return "XXY_" + this.id;
    }

    /**
     * Returns a ClientDetector instance for the client
     */
    async getClientDetector() {
        return new FractalAM4ClientDetector();
    }

    /**
     * Returns a virtual AM4
     */
    async getVirtualClient(options) {
        return new VirtualFractalAM4Client(options || {});
    }
}
