/**
 * Parses incoming messages of the virtual Fractal client and builds the answers (3rd-party protocol,
 * claude/001 Fractal Support/FRACTAL.md 3). Like the real device, it only answers queries and never pushes state changes.
 *
 * Undocumented behaviour, chosen here:
 * - NAK error code for checksum errors: 0x01
 * - Bypass/channel queries for blocks not in the preset are not answered
 * - Malformed messages and out of range values are ignored
 * - Program changes are accepted on all MIDI channels
 */
class VirtualFractalProtocol {

    // Function codes
    static FN_BYPASS = 0x0a;
    static FN_CHANNEL = 0x0b;
    static FN_SCENE = 0x0c;
    static FN_PRESET_NAME = 0x0d;
    static FN_SCENE_NAME = 0x0e;
    static FN_LOOPER = 0x0f;
    static FN_TEMPO_TAP = 0x10;
    static FN_TUNER = 0x11;
    static FN_STATUS_DUMP = 0x13;
    static FN_TEMPO = 0x14;
    static FN_MULTIPURPOSE_RESPONSE = 0x64;

    // Query value
    static QUERY = 0x7f;

    // NAK error code for checksum errors (the real codes are undocumented)
    static ERROR_CHECKSUM = 0x01;

    // Length of names in answers
    static NAME_LENGTH = 32;

    // Function names for the MIDI monitor
    static FUNCTION_NAMES = {
        0x0a: "Bypass",
        0x0b: "Channel",
        0x0c: "Scene",
        0x0d: "Preset Name",
        0x0e: "Scene Name",
        0x0f: "Looper",
        0x10: "Tap Tempo",
        0x11: "Tuner",
        0x13: "Status Dump",
        0x14: "Tempo",
        0x64: "Multipurpose Response (NAK)"
    };

    #client = null;
    #bank = 0;                        // Last received CC0 value
    #warnedModels = new Set();        // Foreign model bytes already warned about

    constructor(client) {
        this.#client = client;
    }

    /**
     * Encodes a name to NAME_LENGTH ASCII bytes, padded with spaces
     */
    static encodeName(name) {
        const ret = [];
        for (let i = 0; i < VirtualFractalProtocol.NAME_LENGTH; ++i) {
            const c = (i < name.length) ? name.charCodeAt(i) : 0x20;
            ret.push((c >= 0x20 && c < 0x7f) ? c : 0x3f);   // Non-ASCII: "?"
        }
        return ret;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Parse raw message. Returns if the message has been processed.
     */
    parse(message) {
        if (this.#parseSysex(message)) return true;
        if (this.#parseControlChange(message)) return true;
        if (this.#parseProgramChange(message)) return true;

        return false;
    }

    /**
     * Tries to return a meaningful message name (for the MIDI monitor). Works for both directions.
     */
    getMessageProperties(message) {
        // Fractal SysEx
        if (message.length >= 7 && message[0] == 0xf0 && Tools.compareArrays(message.slice(1, 4), FractalClient.MANUFACTURER_ID)) {
            const func = message[5];
            let name = VirtualFractalProtocol.FUNCTION_NAMES[func] || ("Function " + func);

            // Push data has no checksum
            let data = message.slice(6, -2);
            if (func == VirtualFractalProtocol.FN_TEMPO_TAP && message.length == 7) {
                name = "Tempo Beat (push)";
                data = [];
            }
            if (func == VirtualFractalProtocol.FN_TUNER && message.length == 10) {
                name = "Tuner (push)";
                data = message.slice(6, -1);
            }

            const model = FractalClient.getModelId(message[4]);

            return {
                name: name + (model ? "" : " (unknown model " + message[4] + ")"),
                value: (data.length > VirtualFractalProtocol.NAME_LENGTH) ? Tools.data2string(data.slice(-VirtualFractalProtocol.NAME_LENGTH)).trim() : data
            };
        }

        // Bank select
        if ((message[0] & 0xf0) == 0xb0 && message[1] == 0) {
            return {
                name: "Bank (CC0, Channel " + ((message[0] & 0x0f) + 1) + ")",
                value: message[2]
            };
        }

        // Program change
        if ((message[0] & 0xf0) == 0xc0) {
            return {
                name: "Preset (PC, Channel " + ((message[0] & 0x0f) + 1) + ")",
                value: message[1]
            };
        }

        return null;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Bank select (CC0)
     */
    #parseControlChange(message) {
        if ((message[0] & 0xf0) != 0xb0 || message[1] != 0) return false;

        this.#bank = message[2];

        this.#client.stats.messageReceived(message, "Bank (CC0)");
        return true;
    }

    /**
     * Program change: loads preset 128 x bank + PC
     */
    #parseProgramChange(message) {
        if ((message[0] & 0xf0) != 0xc0) return false;

        this.#client.presets.loadPreset(128 * this.#bank + message[1]);

        this.#client.stats.messageReceived(message, "Preset (PC)");
        return true;
    }

    /**
     * Fractal SysEx messages
     */
    #parseSysex(message) {
        if (message.length < 7 || message[0] != 0xf0 || message[message.length - 1] != 0xf7) return false;
        if (!Tools.compareArrays(message.slice(1, 4), FractalClient.MANUFACTURER_ID)) return false;

        // The device ignores messages for other models
        const model = message[4];
        if (model != this.#client.model.modelByte) {
            this.#client.stats.messageReceived(message, "Ignored (model byte " + model + ")");

            if (!this.#warnedModels.has(model)) {
                this.#warnedModels.add(model);
                console.warn(this.#client.name + ": Ignoring messages with model byte " + model + " (current model: " + this.#client.model.name + ")");
            }
            return true;
        }

        if (message.length < 8) return false;

        const func = message[5];
        const data = message.slice(6, -2);
        const funcName = VirtualFractalProtocol.FUNCTION_NAMES[func] || ("Function " + func);

        // Checksum
        if (FractalClient.checksum(message.slice(0, -2)) != message[message.length - 2]) {
            this.#client.stats.messageReceived(message, "Checksum error");
            this.#answer(VirtualFractalProtocol.FN_MULTIPURPOSE_RESPONSE, [func, VirtualFractalProtocol.ERROR_CHECKSUM], "NAK");
            return true;
        }

        let handled = false;

        switch (func) {
            case VirtualFractalProtocol.FN_BYPASS:      handled = this.#bypass(data); break;
            case VirtualFractalProtocol.FN_CHANNEL:     handled = this.#channel(data); break;
            case VirtualFractalProtocol.FN_SCENE:       handled = this.#scene(data); break;
            case VirtualFractalProtocol.FN_PRESET_NAME: handled = this.#presetName(data); break;
            case VirtualFractalProtocol.FN_SCENE_NAME:  handled = this.#sceneName(data); break;
            case VirtualFractalProtocol.FN_LOOPER:      handled = this.#looper(data); break;
            case VirtualFractalProtocol.FN_TEMPO_TAP:   handled = this.#tap(data); break;
            case VirtualFractalProtocol.FN_TUNER:       handled = this.#tuner(data); break;
            case VirtualFractalProtocol.FN_STATUS_DUMP: handled = this.#statusDump(data); break;
            case VirtualFractalProtocol.FN_TEMPO:       handled = this.#tempo(data); break;
            default:
                return false;
        }

        this.#client.stats.messageReceived(message, funcName + (handled ? "" : " (ignored)"));
        return true;
    }

    /**
     * Set/get bypass: idL idH dd (dd: 0 = engaged, 1 = bypassed, 7F = query)
     */
    #bypass(data) {
        if (data.length != 3) return false;

        const id = FractalClient.decode14(data[0], data[1]);
        if (!this.#client.presets.hasBlock(id)) return false;

        if (data[2] != VirtualFractalProtocol.QUERY) {
            if (data[2] > 1) return false;
            this.#client.presets.setBypass(id, data[2] == 1);
        }

        this.#answer(
            VirtualFractalProtocol.FN_BYPASS,
            [data[0], data[1], this.#client.presets.getBlockState(id).bypassed ? 1 : 0],
            "Bypass " + VirtualFractalBlocks.getDisplayName(id)
        );
        return true;
    }

    /**
     * Set/get channel: idL idH dd (dd: channel, 7F = query)
     */
    #channel(data) {
        if (data.length != 3) return false;

        const id = FractalClient.decode14(data[0], data[1]);
        if (!this.#client.presets.hasBlock(id)) return false;

        if (data[2] != VirtualFractalProtocol.QUERY) {
            if (!this.#client.presets.setChannel(id, data[2])) return false;
        }

        this.#answer(
            VirtualFractalProtocol.FN_CHANNEL,
            [data[0], data[1], this.#client.presets.getBlockState(id).channel],
            "Channel " + VirtualFractalBlocks.getDisplayName(id)
        );
        return true;
    }

    /**
     * Set/get scene: dd (0-7, 7F = query)
     */
    #scene(data) {
        if (data.length != 1) return false;

        if (data[0] != VirtualFractalProtocol.QUERY) {
            if (!this.#client.presets.setScene(data[0])) return false;
        }

        this.#answer(VirtualFractalProtocol.FN_SCENE, [this.#client.presets.currentScene], "Scene");
        return true;
    }

    /**
     * Query preset name: nL nH (7F 7F = current). Answer: nL nH <32 chars>
     */
    #presetName(data) {
        if (data.length != 2) return false;

        const presets = this.#client.presets;
        const preset = (data[0] == VirtualFractalProtocol.QUERY && data[1] == VirtualFractalProtocol.QUERY) ? presets.currentPreset : FractalClient.decode14(data[0], data[1]);
        if (preset >= presets.numPresets()) return false;

        this.#answer(
            VirtualFractalProtocol.FN_PRESET_NAME,
            FractalClient.encode14(preset).concat(VirtualFractalProtocol.encodeName(presets.getPresetName(preset))),
            "Preset Name"
        );
        return true;
    }

    /**
     * Query scene name: dd (7F = current). Answer: nn <32 chars>
     */
    #sceneName(data) {
        if (data.length != 1) return false;

        const presets = this.#client.presets;
        const scene = (data[0] == VirtualFractalProtocol.QUERY) ? presets.currentScene : data[0];
        if (scene >= VirtualFractalPresets.NUM_SCENES) return false;

        this.#answer(
            VirtualFractalProtocol.FN_SCENE_NAME,
            [scene].concat(VirtualFractalProtocol.encodeName(presets.getSceneName(scene))),
            "Scene Name"
        );
        return true;
    }

    /**
     * Set/get looper: dd (button 0-5, 7F = query). Answer: state bit field
     */
    #looper(data) {
        if (data.length != 1) return false;

        if (data[0] != VirtualFractalProtocol.QUERY) {
            if (data[0] > 5) return false;
            this.#client.looper.press(data[0]);
        }

        this.#answer(VirtualFractalProtocol.FN_LOOPER, [this.#client.looper.state()], "Looper State");
        return true;
    }

    /**
     * Tap tempo (no answer)
     */
    #tap(data) {
        if (data.length != 0) return false;

        this.#client.tempo.tap();
        return true;
    }

    /**
     * Tuner on/off: dd (0 = off, 1 = on). No answer.
     */
    #tuner(data) {
        if (data.length != 1 || data[0] > 1) return false;

        this.#client.tuner.setEnabled(data[0] == 1);
        return true;
    }

    /**
     * Status dump of all blocks in the current preset
     */
    #statusDump(data) {
        if (data.length != 0) return false;

        this.#answer(VirtualFractalProtocol.FN_STATUS_DUMP, this.#client.presets.getStatusDump(), "Status Dump");
        return true;
    }

    /**
     * Set/get tempo: tL tH (7F 7F = query)
     */
    #tempo(data) {
        if (data.length != 2) return false;

        if (!(data[0] == VirtualFractalProtocol.QUERY && data[1] == VirtualFractalProtocol.QUERY)) {
            this.#client.tempo.set(FractalClient.decode14(data[0], data[1]));
        }

        this.#answer(VirtualFractalProtocol.FN_TEMPO, FractalClient.encode14(this.#client.tempo.bpm()), "Tempo");
        return true;
    }

    /**
     * Sends an answer with checksum
     */
    #answer(func, data, hintText) {
        this.#client.queueMessage(
            FractalClient.createSysex(this.#client.model.modelByte, func, data),
            hintText
        );
    }
}
