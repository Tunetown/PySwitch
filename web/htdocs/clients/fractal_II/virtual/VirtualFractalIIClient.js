/**
 * Virtual Fractal Axe-Fx II (Mark I/II, XL, XL+). Answers exactly the messages used by PySwitch
 * (spec/axe_fx_ii/protocol.md 4); every other message is answered with the status message "not recognized"
 * (64 <fn> 05) like the real device, and logged in "rejected" (the tests check that PySwitch only sends messages of
 * the spec). Like the real device with I/O > MIDI > SEND REALTIME SYSEX = ALL, it pushes tuner data while the tuner is
 * on and a message on every beat. Changes made "on the device" (UI, tests) push the preset number, scene and X/Y.
 */
class VirtualFractalIIClient extends VirtualClient {

    static TUNER_CC = 15;                   // Default of I/O > CTRL > Tuner
    static TAP_TEMPO_CC = 14;               // Default of I/O > CTRL > Tap Tempo
    static TUNER_PUSH_MILLIS = 50;
    static MIN_BPM = 24;
    static MAX_BPM = 250;
    static TAP_TIMEOUT_MILLIS = 2500;       // A tap after this time starts a new tap series

    #ui = null;
    #callbacks = [];
    #runIntervalHandler = null;
    #tunerPeriod = null;
    #beatPeriod = null;
    #taps = [];

    options = null;
    modelByte = null;
    model = null;               // Entry of FractalIIClient.MODELS
    presets = [];               // { name, blocks: [effect IDs], engaged: [scene][block index], x: [scene][block index] }
    preset = 0;                 // Current preset number (0-based)
    scene = 0;                  // Current scene (0..7)
    tuner = false;              // Tuner on
    tunerNote = 9;              // Tuner note (0 = C, like PySwitch)
    tunerCents = 0;             // -50..50
    bpm = 120;
    beats = 0;                  // Number of beats sent
    rejected = [];              // Messages not in the spec, for the tests
    cc = {};                    // Last values of the received control changes (CC number: value), for the tests

    /**
     * {
     *      model:                 Model byte (3, 6, 7)
     *      sendRealtimeSysex:     Push tuner data and tempo beats
     *      overrideTimeCallback:  Optional callback function replacing Date.now() for testing
     * }
     */
    constructor(options) {
        super("Virtual Axe-Fx II");
        this.options = options || {};

        this.modelByte = this.options.model || FractalIIClient.DEFAULT_MODEL;
        this.model = FractalIIClient.getModel(this.modelByte);
        if (!this.model) throw new Error("Unknown Axe-Fx II model: " + this.modelByte);

        this.#tunerPeriod = new PeriodCounter(VirtualFractalIIClient.TUNER_PUSH_MILLIS, this.options.overrideTimeCallback);
        this.#setBpm(120);
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
    get current() {
        return this.presets[this.preset];
    }

    /**
     * Returns the current timestamp in milliseconds
     */
    now() {
        return this.options.overrideTimeCallback ? this.options.overrideTimeCallback() : Date.now();
    }

    /**
     * Loads a preset on the device (pushes the preset number like the real device)
     */
    loadPreset(preset, scene = null) {
        if (!this.#loadPreset(preset)) return false;
        if (scene !== null) this.scene = scene;
        this.#queue(FractalIIClient.createSysex(this.modelByte, 0x14, [preset >> 7, preset & 0x7f]));
        this.#changed();
        return true;
    }

    /**
     * Selects a scene on the device (pushes the scene)
     */
    setScene(scene) {
        if (scene < 0 || scene >= FractalIIClient.NUM_SCENES) return false;
        this.scene = scene;
        this.#queue(FractalIIClient.createSysex(this.modelByte, 0x29, [scene]));
        this.#changed();
        return true;
    }

    /**
     * Returns the block state in the current scene: { engaged, x }, or null if the block is not in the preset
     */
    getBlock(id) {
        const index = this.current.blocks.indexOf(id);
        if (index < 0) return null;
        return {
            engaged: this.current.engaged[this.scene][index],
            x: this.current.x[this.scene][index]
        };
    }

    /**
     * Engages / bypasses a block in the current scene on the device
     */
    setEngaged(id, engaged) {
        const index = this.current.blocks.indexOf(id);
        if (index < 0) return false;
        this.current.engaged[this.scene][index] = !!engaged;
        this.#changed();
        return true;
    }

    /**
     * Selects X (true) or Y (false) of a block in the current scene on the device (pushes the X/Y state)
     */
    setX(id, x) {
        if (!this.#setX(id, x)) return false;
        this.#queue(FractalIIClient.createSysex(this.modelByte, 0x11, [id & 0x7f, id >> 7, x ? 0 : 1]));
        this.#changed();
        return true;
    }

    /**
     * Sets the blocks of the current preset (effect IDs). New blocks are engaged on X in all scenes.
     */
    setBlocks(ids) {
        const preset = this.current;
        const old = preset.blocks;

        preset.engaged = preset.engaged.map((scene) => ids.map((id) => old.indexOf(id) >= 0 ? scene[old.indexOf(id)] : true));
        preset.x = preset.x.map((scene) => ids.map((id) => old.indexOf(id) >= 0 ? scene[old.indexOf(id)] : true));
        preset.blocks = ids.slice();

        this.#changed();
    }

    /**
     * Sets the name of the current preset
     */
    setName(name) {
        this.current.name = name;
        this.#changed();
    }

    /**
     * Switches the tuner on/off on the device
     */
    setTuner(on) {
        this.tuner = !!on;
        this.#changed();
    }

    /**
     * Sets the tuner note (0-11, 0 = C) and deviation (cents)
     */
    setTunerData(note, cents) {
        this.tunerNote = ((Math.round(note) % 12) + 12) % 12;
        this.tunerCents = Math.min(Math.max(Math.round(cents), -50), 50);
        this.#changed();
    }

    /**
     * Sets the tempo (BPM) on the device
     */
    setBpm(bpm) {
        this.#setBpm(bpm);
        this.#changed();
    }

    /**
     * Tries to return a meaningful message name
     */
    getMessageProperties(message) {
        const msg = Array.from(message);
        if (msg[0] != 0xf0 || !FractalIIClient.getModel(msg[4])) return null;

        const id = msg[6] + 128 * msg[7];

        switch (msg[5]) {
            case 0x14: return { name: "Axe-Fx II: Preset" };
            case 0x3c: return { name: "Axe-Fx II: Preset Select", value: 128 * msg[6] + msg[7] };
            case 0x0f: return { name: "Axe-Fx II: Preset Name" };
            case 0x15: return { name: "Axe-Fx II: Preset Name by Number", value: 128 * msg[6] + msg[7] };
            case 0x29: return { name: "Axe-Fx II: Scene", value: msg[6] };
            case 0x0e: return { name: "Axe-Fx II: Block States" };
            case 0x02: return { name: "Axe-Fx II: Bypass " + (FractalIIClient.getBlockName(id) || id) };
            case 0x11: return { name: "Axe-Fx II: X/Y " + (FractalIIClient.getBlockName(id) || id) };
            case 0x0d: return { name: "Axe-Fx II: Tuner Data" };
            case 0x10: return { name: "Axe-Fx II: Tempo Beat" };
            case 0x2f: return { name: "Axe-Fx II: Tempo BPM" };
            case 0x64: return { name: "Axe-Fx II: Status", value: msg.slice(6, 8) };
        }
        return null;
    }

    /**
     * Start processing regular updates to send messages. If not set, the caller has to call update() regularly.
     */
    run(updateInterval) {
        const that = this;
        this.#runIntervalHandler = setInterval(
            function() {
                try {
                    that.update();
                } catch (e) {
                    console.error(e);
                }
            },
            updateInterval
        );
    }

    /**
     * Called regularly: tuner data and tempo beats
     */
    update() {
        if (this.tuner && this.options.sendRealtimeSysex && this.#tunerPeriod.exceeded()) {
            const string = [4, 9, 2, 7, 11, 4].indexOf(this.tunerNote);
            this.#queue(FractalIIClient.createSysex(
                this.modelByte,
                0x0d,
                [(this.tunerNote + 3) % 12, string >= 0 ? string : 0, 63 + this.tunerCents],     // The device counts the notes from A
                false
            ));
        }

        if (this.#beatPeriod.exceeded()) {
            ++this.beats;
            if (this.options.sendRealtimeSysex) {
                this.#queue(FractalIIClient.createSysex(this.modelByte, 0x10, [], false));
            }
        }
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Called by PySwitch when a message is sent to the device
     */
    async doSend(message) {
        try {
            const msg = Array.from(message);

            // Control change: tuner and tap tempo CCs (MIDI channel 1), others are only remembered
            if (msg[0] == 0xb0 && msg.length == 3) {
                this.cc[msg[1]] = msg[2];

                if (msg[1] == VirtualFractalIIClient.TUNER_CC) {
                    this.setTuner(msg[2] >= 64);
                } else if (msg[1] == VirtualFractalIIClient.TAP_TEMPO_CC && msg[2] > 0) {
                    this.#tap();
                }
                return;
            }

            if (msg[0] != 0xf0 || !Tools.compareArrays(msg.slice(1, 4), FractalIIClient.MANUFACTURER_ID)) return;   // Others: ignored

            // Wrong model byte: the real device answers "wrong model number" (or ignores it, protocol.md 8)
            if (msg[4] != this.modelByte) {
                this.#reject(msg, 0x03);
                return;
            }

            if (msg[msg.length - 2] != FractalIIClient.checksum(msg.slice(0, msg.length - 2))) {
                this.#reject(msg, 0x01);                            // Bad checksum
                return;
            }

            if (!this.#parse(msg)) {
                this.#reject(msg, 0x05);
            }

        } catch (e) {
            console.error(e);
        }
    }

    /**
     * Parses a message of the spec and answers it. Returns false if the message is not in the spec.
     */
    #parse(msg) {
        const func = msg[5];
        const len = msg.length;
        const model = this.modelByte;

        // Current preset
        if (func == 0x14 && len == 8) {
            this.#queue(FractalIIClient.createSysex(model, 0x14, [this.preset >> 7, this.preset & 0x7f]));
            return true;
        }

        // Preset select
        if (func == 0x3c && len == 10) {
            if (!this.#loadPreset(128 * msg[6] + msg[7])) return false;
            this.#queue(FractalIIClient.createSysex(model, 0x64, [0x3c, 0x00]));
            this.#changed();
            return true;
        }

        // Current preset name
        if (func == 0x0f && len == 8) {
            this.#queue(FractalIIClient.createSysex(model, 0x0f, FractalIIClient.nameBytes(this.current.name)));
            return true;
        }

        // Preset name by number (never 7F 7F)
        if (func == 0x15 && len == 10) {
            const preset = 128 * msg[6] + msg[7];
            if (preset >= this.model.numPresets) return false;

            this.#queue(FractalIIClient.createSysex(model, 0x15, [msg[6], msg[7]].concat(FractalIIClient.nameBytes(this.presets[preset].name))));
            return true;
        }

        // Scene query / select (no answer on select)
        if (func == 0x29 && len == 9) {
            if (msg[6] == 0x7f) {
                this.#queue(FractalIIClient.createSysex(model, 0x29, [this.scene]));
                return true;
            }
            if (msg[6] >= FractalIIClient.NUM_SCENES) return false;

            this.scene = msg[6];
            this.#changed();
            return true;
        }

        // Block states (no checksum)
        if (func == 0x0e && len == 8) {
            this.#queue(FractalIIClient.createSysex(model, 0x0e, this.#blockStates(), false));
            return true;
        }

        // Bypass: parameter 255 of a block, value 0 = engage, 1 = bypass, set (01)
        if (func == 0x02 && len == 16 && msg[8] == 0x7f && msg[9] == 0x01 && msg[11] == 0 && msg[12] == 0 && msg[13] == 0x01 && msg[10] <= 1) {
            const id = msg[6] + 128 * msg[7];
            if (!FractalIIClient.getBlockName(id)) return false;

            // The real device answers with the new value and its text; PySwitch does not use the answer
            if (this.setEngaged(id, msg[10] == 0)) {
                this.#queue(FractalIIClient.createSysex(model, 0x64, [0x02, 0x00]));
            } else {
                this.#queue(FractalIIClient.createSysex(model, 0x64, [0x02, 0x08]));     // Block not in the preset
            }
            return true;
        }

        // X/Y select
        if (func == 0x11 && len == 12 && msg[9] == 0x01 && msg[8] <= 1) {
            const id = msg[6] + 128 * msg[7];
            if (!FractalIIClient.getBlockName(id)) return false;

            if (this.#setX(id, msg[8] == 0)) {
                this.#queue(FractalIIClient.createSysex(model, 0x11, [msg[6], msg[7], msg[8]]));
                this.#changed();
            } else {
                this.#queue(FractalIIClient.createSysex(model, 0x64, [0x11, 0x08]));
            }
            return true;
        }

        // Tempo query
        if (func == 0x2f && len == 8) {
            this.#queue(FractalIIClient.createSysex(model, 0x2f, [this.bpm & 0x7f, this.bpm >> 7]));
            return true;
        }

        return false;
    }

    /**
     * Block state records (5 septets per block, LS first: effect ID << 24 | X/Y CC << 16 | bypass CC << 8 | flags).
     * Includes the input and output blocks like the real device.
     */
    #blockStates() {
        const ret = [];
        const preset = this.current;
        const blocks = [[139, true, true]].concat(
            preset.blocks.map((id, i) => [id, preset.engaged[this.scene][i], preset.x[this.scene][i]]),
            [[140, true, true]]
        );

        for (const [id, engaged, x] of blocks) {
            const cc = 37 + (id % 64);              // Some CC numbers (not used by PySwitch)
            const word = ((id << 24) | ((cc + 1) << 16) | (cc << 8) | (engaged ? 1 : 0) | (x ? 2 : 0)) >>> 0;

            for (let i = 0; i < 5; ++i) {
                ret.push(Math.floor(word / Math.pow(2, 7 * i)) & 0x7f);
            }
        }
        return ret;
    }

    #loadPreset(preset) {
        if (preset < 0 || preset >= this.model.numPresets) return false;
        this.preset = preset;
        this.scene = 0;
        return true;
    }

    #setX(id, x) {
        const index = this.current.blocks.indexOf(id);
        if (index < 0) return false;
        this.current.x[this.scene][index] = !!x;
        return true;
    }

    #setBpm(bpm) {
        bpm = Math.round(bpm);
        if (!bpm) return;

        this.bpm = Math.min(Math.max(bpm, VirtualFractalIIClient.MIN_BPM), VirtualFractalIIClient.MAX_BPM);
        this.#beatPeriod = new PeriodCounter(60000 / this.bpm, this.options.overrideTimeCallback);
    }

    /**
     * Tap tempo: averages the intervals of the current tap series
     */
    #tap() {
        const now = this.now();

        if (this.#taps.length > 0 && now - this.#taps[this.#taps.length - 1] > VirtualFractalIIClient.TAP_TIMEOUT_MILLIS) {
            this.#taps = [];
        }

        this.#taps.push(now);
        if (this.#taps.length > 10) this.#taps.shift();
        if (this.#taps.length < 2) return;

        const avgInterval = (this.#taps[this.#taps.length - 1] - this.#taps[0]) / (this.#taps.length - 1);
        if (avgInterval > 0) this.setBpm(60000 / avgInterval);
    }

    #reject(msg, code) {
        this.rejected.push(msg);
        console.warn(this.name + ": Message not in the spec: ", msg);
        this.#queue(FractalIIClient.createSysex(this.modelByte, 0x64, [msg[5], code]));
        this.#changed();
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
     * Default presets: names and blocks. Scene n engages the blocks differently, scenes 5-8 use Y for the amp.
     */
    #setup() {
        const amps = ["Clean", "Plexi", "Recto", "Deluxe", "AC30", "5153", "JCM800", "Twin"];
        const chains = [
            [133, 106, 108, 112, 110],              // Drive 1, Amp 1, Cab 1, Delay 1, Reverb 1
            [100, 106, 108, 116, 110],              // Compressor 1, Amp 1, Cab 1, Chorus 1, Reverb 1
            [124, 133, 106, 107, 108, 112],         // Wah 1, Drive 1, Amp 1, Amp 2, Cab 1, Delay 1
            [106, 108, 110]                         // Amp 1, Cab 1, Reverb 1
        ];

        for (let p = 0; p < this.model.numPresets; ++p) {
            const blocks = chains[p % chains.length];
            const engaged = [];
            const x = [];

            for (let s = 0; s < FractalIIClient.NUM_SCENES; ++s) {
                engaged.push(blocks.map((id) => (id == 106 || id == 108) ? true : ((s + blocks.indexOf(id)) % 2 == 0)));
                x.push(blocks.map((id) => !(s >= 4 && id == 106)));
            }

            this.presets.push({
                name: amps[p % amps.length] + " " + (Math.floor(p / amps.length) + 1),
                blocks: blocks.slice(),
                engaged: engaged,
                x: x
            });
        }
    }

    /**
     * Stop listening, remove the UI
     */
    detach() {
        clearInterval(this.#runIntervalHandler);
        this.#callbacks = [];
        if (this.#ui) this.#ui.destroy();
    }

    /**
     * User interface in the passed container DOM element
     */
    getUserInterface(container) {
        if (this.#ui) this.#ui.destroy();
        this.#ui = new VirtualFractalIIClientUI(container, this);
        return this.#ui;
    }
}
