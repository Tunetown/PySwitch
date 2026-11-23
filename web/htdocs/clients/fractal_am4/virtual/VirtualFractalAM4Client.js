/**
 * Virtual Fractal AM4. Answers exactly the messages used by PySwitch (spec/am4/protocol.md 4); every other message
 * is rejected with a NAK (0x64 <fn> 05) and logged as warning, because the real AM4 can freeze on unknown messages.
 * The AM4 sends nothing by itself.
 */
class VirtualFractalAM4Client extends VirtualClient {

    #ui = null;
    #callbacks = [];

    options = null;
    presets = [];               // { name, scenes: [4 names], blocks: [4 block IDs], bypass: [scene][slot] }
    location = 0;               // Current preset (0..103)
    scene = 0;                  // Current scene (0..3)
    mode = null;                // Last footswitch mode selected (argument of the mode select message)
    rejected = [];              // Messages rejected (not whitelisted), for the tests
    cc = {};                    // Last values of the received control changes (CC number: value), for the tests. The
                                // function of a CC is a setting on the device (for example the tuner, see the examples)

    /**
     * options: none used (overrideTimeCallback is accepted for compatibility)
     */
    constructor(options) {
        super("Virtual AM4");
        this.options = options || {};

        this.#setup();
    }

    /**
     * Adds a callback on changes: callback() => void
     */
    addChangeCallback(callback) {
        this.#callbacks.push(callback);
    }

    /**
     * Current preset data
     */
    get preset() {
        return this.presets[this.location];
    }

    /**
     * Loads a preset (like on the device): scene 1
     */
    loadPreset(location) {
        if (location < 0 || location >= FractalAM4Client.NUM_PRESETS) return false;
        this.location = location;
        this.scene = 0;
        this.#changed();
        return true;
    }

    /**
     * Selects a scene of the current preset
     */
    setScene(scene) {
        if (scene < 0 || scene >= FractalAM4Client.NUM_SCENES) return false;
        this.scene = scene;
        this.#changed();
        return true;
    }

    /**
     * Sets the block of a slot (0 = empty) of the current preset
     */
    setBlock(slot, block) {
        this.preset.blocks[slot] = block;
        this.#changed();
    }

    /**
     * Returns / sets the bypass state of a slot in the current scene
     */
    getBypass(slot) {
        return this.preset.bypass[this.scene][slot];
    }

    setBypass(slot, bypassed) {
        this.preset.bypass[this.scene][slot] = !!bypassed;
        this.#changed();
    }

    /**
     * Sets names of the current preset (scene = null: preset name)
     */
    setName(name, scene = null) {
        if (scene === null) {
            this.preset.name = name;
        } else {
            this.preset.scenes[scene] = name;
        }
        this.#changed();
    }

    /**
     * Tries to return a meaningful message name
     */
    getMessageProperties(message) {
        const msg = Array.from(message);
        if (msg[0] != 0xf0 || msg[4] != FractalAM4Client.MODEL_BYTE) return null;

        switch (msg[5]) {
            case 0x14: return { name: "AM4: Preset" };
            case 0x12: return { name: "AM4: Mode", value: FractalAM4Client.MODES[msg[6]] };
            case 0x64: return { name: "AM4: Response", value: msg.slice(6, 8) };
            case 0x01: {
                const pidLow = msg[6] + 128 * msg[7];
                const pidHigh = msg[8] + 128 * msg[9];
                const action = msg[10] + 128 * msg[11];

                if (pidLow == 0xce && action == 0x1f) return { name: "AM4: Name Table" };
                if (pidLow == 0xce && pidHigh == 0x0a) return { name: "AM4: Preset Select" };
                if (pidLow == 0xce && pidHigh == 0x0d) return { name: "AM4: Scene Select" };
                if (pidLow == 0xce && pidHigh == 0x0b) return { name: "AM4: Preset Name" };
                if (pidHigh == 0x03) return { name: "AM4: Bypass " + (FractalAM4Client.getBlockName(pidLow) || pidLow) };
                return { name: "AM4: Parameter" };
            }
        }
        return null;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Called by PySwitch when a message is sent to the device
     */
    async doSend(message) {
        try {
            const msg = Array.from(message);

            // Program change (if "Receive MIDI PC" is on)
            if ((msg[0] & 0xf0) == 0xc0 && msg.length == 2) {
                this.loadPreset(msg[1]);
                return;
            }

            // Control change: only remembered
            if ((msg[0] & 0xf0) == 0xb0 && msg.length == 3) {
                this.cc[msg[1]] = msg[2];
                return;
            }

            if (msg[0] != 0xf0) return;                     // Others: ignored
            if (msg[4] != FractalAM4Client.MODEL_BYTE) return;

            if (!this.#parse(msg)) {
                this.rejected.push(msg);
                console.warn(this.name + ": Message not whitelisted (the real AM4 might freeze): ", msg);
                this.#queue(FractalAM4Client.createSysex(0x64, [msg[5], 0x05]));
            }

        } catch (e) {
            console.error(e);
        }
    }

    /**
     * Parses a whitelisted message and answers it. Returns false if the message is not whitelisted.
     */
    #parse(msg) {
        const func = msg[5];

        if (func == 0x14 && msg.length == 8) {
            this.#queue(FractalAM4Client.createSysex(0x14, FractalAM4Client.encode14(this.location)));
            return true;
        }

        if (func == 0x12 && msg.length == 9 && FractalAM4Client.MODES[msg[6]]) {
            this.mode = msg[6];
            this.#changed();
            this.#queue(FractalAM4Client.createSysex(0x64, [0x12, 0x00]));
            return true;
        }

        if (func != 0x01 || msg.length < 18) return false;

        const pidLow = msg[6] + 128 * msg[7];
        const pidHigh = msg[8] + 128 * msg[9];
        const action = msg[10] + 128 * msg[11];
        const length = msg[14] + 128 * msg[15];
        const header = msg.slice(6, 12);

        // Name table
        if (pidLow == 0xce && pidHigh == 0 && action == 0x1f && length == 0) {
            this.#queue(FractalAM4Client.createSysex(0x01, header.concat([0, 0, 0x40, 0x01], FractalAM4Client.encodeBitstream(this.#nameTable()))));
            return true;
        }

        const slot = this.preset.blocks.indexOf(pidLow);

        // Bypass read (long read)
        if (pidHigh == 0x03 && action == 0x0d && length == 0 && FractalAM4Client.getBlockName(pidLow)) {
            const payload = new Array(46).fill(0x11);
            payload[22 - 16] = (slot >= 0 && this.getBypass(slot)) ? 0x01 : 0x00;
            this.#queue(FractalAM4Client.createSysex(0x01, header.concat([0, 0, 0x28, 0x00], payload)));
            return true;
        }

        // Writes (4 raw bytes)
        if (action == 0x01 && length == 4 && msg.length == 23) {
            const raw = FractalAM4Client.unpack(msg, 16, 4);

            if (pidHigh == 0x03 && FractalAM4Client.getBlockName(pidLow)) {
                if (slot >= 0) this.setBypass(slot, FractalAM4Client.toFloat(raw) >= 0.5);
                this.#writeEcho(header);
                return true;
            }

            if (pidLow == 0xce && pidHigh == 0x0d) {
                this.setScene(FractalAM4Client.toUint(raw));
                this.#writeEcho(header);
                return true;
            }

            if (pidLow == 0xce && pidHigh == 0x0a) {
                this.loadPreset(Math.round(FractalAM4Client.toFloat(raw)));
                this.#writeEcho(header);
                return true;
            }

            return false;
        }

        // Preset name of any location
        if (pidLow == 0xce && pidHigh == 0x0b && action == 0x12 && length == 4 && msg.length == 23) {
            const location = FractalAM4Client.toUint(FractalAM4Client.unpack(msg, 16, 4));
            if (location >= FractalAM4Client.NUM_PRESETS) return false;

            const name = this.presets[location].name || "<EMPTY>";
            this.#queue(FractalAM4Client.createSysex(0x01, header.concat([0, 0, 0x20, 0x00], FractalAM4Client.pack(FractalAM4Client.nameBytes(name)))));
            return true;
        }

        return false;
    }

    /**
     * Raw bytes of the name table answer (192 bytes)
     */
    #nameTable() {
        const raw = new Array(192).fill(0);
        const preset = this.preset;

        FractalAM4Client.uintBytes(this.location % 3).forEach((b, i) => raw[0x00 + i] = b);
        FractalAM4Client.uintBytes(this.scene).forEach((b, i) => raw[0x08 + i] = b);
        FractalAM4Client.floatBytes(70 + Math.random() * 5).forEach((b, i) => raw[0x0c + i] = b);     // Level meter

        FractalAM4Client.nameBytes(preset.name).forEach((b, i) => raw[0x10 + i] = b);
        for (let s = 0; s < FractalAM4Client.NUM_SCENES; ++s) {
            FractalAM4Client.nameBytes(preset.scenes[s]).forEach((b, i) => raw[0x30 + 0x20 * s + i] = b);
        }
        for (let slot = 0; slot < FractalAM4Client.NUM_SLOTS; ++slot) {
            FractalAM4Client.uintBytes(preset.blocks[slot]).forEach((b, i) => raw[0xb0 + 4 * slot + i] = b);
        }
        return raw;
    }

    /**
     * Answers a write with a 64-byte write echo (content not used by PySwitch)
     */
    #writeEcho(header) {
        this.#queue(FractalAM4Client.createSysex(0x01, header.concat([0, 0, 0x28, 0x00], new Array(46).fill(0x22))));
    }

    #queue(message) {
        this.messageQueue.push(message);
    }

    #changed() {
        for (const cb of this.#callbacks) {
            cb();
        }
    }

    /**
     * Default presets: names, scene names and blocks
     */
    #setup() {
        const amps = ["Clean", "Plexi", "Recto", "Deluxe", "AC30", "5153", "JCM800", "Twin"];
        const scenes = ["Clean", "Crunch", "Lead", ""];
        const chains = [
            [0x76, 0x3a, 0x46, 0x42],       // Drive, Amp, Delay, Reverb
            [0x2e, 0x3a, 0x4e, 0x42],       // Compressor, Amp, Chorus, Reverb
            [0x5e, 0x76, 0x3a, 0x46],       // Wah, Drive, Amp, Delay
            [0x3a, 0x42, 0x00, 0x00]        // Amp, Reverb, empty, empty
        ];

        for (let p = 0; p < FractalAM4Client.NUM_PRESETS; ++p) {
            const bypass = [];
            for (let s = 0; s < FractalAM4Client.NUM_SCENES; ++s) {
                bypass.push([s == 0, false, s < 2, false]);
            }

            this.presets.push({
                name: (p >= 100) ? "" : (amps[p % amps.length] + " " + (Math.floor(p / amps.length) + 1)),     // Last bank empty
                scenes: scenes.slice(),
                blocks: chains[p % chains.length].slice(),
                bypass: bypass
            });
        }
    }

    /**
     * Stop listening, remove the UI
     */
    detach() {
        this.#callbacks = [];
        if (this.#ui) this.#ui.destroy();
    }

    /**
     * User interface in the passed container DOM element
     */
    getUserInterface(container) {
        if (this.#ui) this.#ui.destroy();
        this.#ui = new VirtualFractalAM4ClientUI(container, this);
        return this.#ui;
    }
}
