/**
 * Preset model of the virtual Fractal client.
 *
 * Stored presets are generated on demand with dummy content (names, blocks, per scene states).
 * Loading a preset copies it to a working buffer, like on the device: bypass and channel changes are
 * made in the working buffer (per scene) and are discarded on the next preset change.
 */
class VirtualFractalPresets {

    static NUM_SCENES = 8;

    // Change types passed to the change callbacks
    static CHANGE_PRESET = "preset";
    static CHANGE_SCENE = "scene";
    static CHANGE_BLOCKS = "blocks";
    static CHANGE_NAMES = "names";

    #client = null;
    #stored = new Map();       // Stored presets by number
    #working = null;           // Working buffer (copy of the current preset)
    #callbacks = [];

    currentPreset = 0;
    currentScene = 0;

    constructor(client) {
        this.#client = client;
        this.loadPreset(0);
    }

    /**
     * Resets all presets (used on model change)
     */
    reset() {
        this.#stored.clear();
        this.loadPreset(0);
    }

    /**
     * Adds a callback on change: callback(changeType) => void
     */
    addChangeCallback(callback) {
        this.#callbacks.push(callback);
    }

    destroy() {
        this.#callbacks = [];
    }

    /**
     * Number of presets of the current model
     */
    numPresets() {
        return this.#client.model.numPresets;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Loads a preset into the working buffer. Returns if successful.
     */
    loadPreset(preset) {
        if (preset < 0 || preset >= this.numPresets()) return false;

        this.#working = JSON.parse(JSON.stringify(this.#getStored(preset)));
        this.currentPreset = preset;
        this.currentScene = this.#working.defaultScene;

        this.#notify(VirtualFractalPresets.CHANGE_PRESET);
        return true;
    }

    /**
     * Returns the name of a preset (working buffer for the current one)
     */
    getPresetName(preset) {
        if (preset == this.currentPreset) return this.#working.name;
        return this.#getStored(preset).name;
    }

    /**
     * Renames a preset (stored and working buffer)
     */
    setPresetName(preset, name) {
        this.#getStored(preset).name = name;
        if (preset == this.currentPreset) this.#working.name = name;

        this.#notify(VirtualFractalPresets.CHANGE_NAMES);
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Selects a scene of the current preset. Returns if successful.
     */
    setScene(scene) {
        if (scene < 0 || scene >= VirtualFractalPresets.NUM_SCENES) return false;

        this.currentScene = scene;

        this.#notify(VirtualFractalPresets.CHANGE_SCENE);
        return true;
    }

    /**
     * Returns the name of a scene of the current preset
     */
    getSceneName(scene) {
        return this.#working.sceneNames[scene];
    }

    /**
     * Renames a scene of the current preset (stored and working buffer)
     */
    setSceneName(scene, name) {
        this.#getStored(this.currentPreset).sceneNames[scene] = name;
        this.#working.sceneNames[scene] = name;

        this.#notify(VirtualFractalPresets.CHANGE_NAMES);
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Returns the block IDs of the current preset, sorted by ID
     */
    getBlocks() {
        return this.#working.blocks;
    }

    /**
     * Returns if the current preset contains the block
     */
    hasBlock(id) {
        return this.#working.blocks.includes(id);
    }

    /**
     * Returns if the current preset contains a Looper block
     */
    hasLooper() {
        return this.hasBlock(VirtualFractalBlocks.idOf("LPR"));
    }

    /**
     * Returns the state of a block in the current scene: { bypassed, channel }, or null if not in the preset.
     */
    getBlockState(id) {
        if (!this.hasBlock(id)) return null;
        return this.#working.scenes[this.currentScene][id];
    }

    /**
     * Sets the bypass state of a block in the current scene. Returns if successful.
     */
    setBypass(id, bypassed) {
        const state = this.getBlockState(id);
        if (!state) return false;

        state.bypassed = !!bypassed;

        this.#notify(VirtualFractalPresets.CHANGE_BLOCKS);
        return true;
    }

    /**
     * Sets the channel of a block in the current scene. Returns if successful.
     */
    setChannel(id, channel) {
        const state = this.getBlockState(id);
        if (!state) return false;
        if (channel < 0 || channel >= VirtualFractalBlocks.get(id).channels) return false;

        state.channel = channel;

        this.#notify(VirtualFractalPresets.CHANGE_BLOCKS);
        return true;
    }

    /**
     * Adds a block to the current preset (engaged, channel A in all scenes)
     */
    addBlock(id) {
        if (this.hasBlock(id)) return;
        if (!VirtualFractalBlocks.isAvailable(id, this.#client.model.countIndex)) return;

        this.#working.blocks.push(id);
        this.#working.blocks.sort((a, b) => a - b);

        for (const scene of this.#working.scenes) {
            scene[id] = {
                bypassed: false,
                channel: 0
            };
        }

        this.#notify(VirtualFractalPresets.CHANGE_BLOCKS);
    }

    /**
     * Removes a block from the current preset
     */
    removeBlock(id) {
        if (!this.hasBlock(id)) return;

        this.#working.blocks = this.#working.blocks.filter((b) => b != id);

        for (const scene of this.#working.scenes) {
            delete scene[id];
        }

        this.#notify(VirtualFractalPresets.CHANGE_BLOCKS);
    }

    /**
     * Returns the status dump payload for the current scene: n x (idL idH dd), see FRACTAL.md 3.2
     */
    getStatusDump() {
        const ret = [];

        for (const id of this.#working.blocks) {
            const state = this.getBlockState(id);
            const info = VirtualFractalBlocks.get(id);

            ret.push(
                ...FractalClient.encode14(id),
                (state.bypassed ? 1 : 0) | ((state.channel & 0x07) << 1) | ((info.channels & 0x07) << 4)
            );
        }

        return ret;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Returns the stored preset, generating it if not yet existing
     */
    #getStored(preset) {
        if (!this.#stored.has(preset)) {
            this.#stored.set(preset, this.#generate(preset));
        }
        return this.#stored.get(preset);
    }

    /**
     * Generates deterministic dummy content for a preset
     */
    #generate(preset) {
        const amps = ["Plexi", "Deluxe", "Recto", "Class-A", "Brit 800", "5153", "Twin", "Bassguy"];
        const styles = ["Clean", "Crunch", "Rhythm", "Lead", "Ambient", "Blues", "Heavy", "Jazz"];
        const sceneNames = ["Clean", "Rhythm", "Crunch", "Lead", "Solo", "Ambient", "Verse", "Chorus"];

        // Blocks: base set in every preset, plus some depending on the preset number
        const abbrs = [["IN", 1], ["CMP", 1], ["DRV", 1], ["AMP", 1], ["CAB", 1], ["DLY", 1], ["REV", 1], ["OUT", 1]];
        if (preset % 2 == 0) abbrs.push(["DRV", 2]);
        if (preset % 2 == 1) abbrs.push(["WAH", 1]);
        if (preset % 3 == 0) abbrs.push(["CHO", 1]);
        if (preset % 3 == 1) abbrs.push(["PHA", 1]);
        if (preset % 4 == 0) abbrs.push(["LPR", 1]);
        if (preset % 5 == 0) abbrs.push(["PIT", 1]);

        const countIndex = this.#client.model.countIndex;
        const blocks = abbrs
            .map((a) => VirtualFractalBlocks.idOf(a[0], a[1]))
            .filter((id) => VirtualFractalBlocks.isAvailable(id, countIndex))
            .sort((a, b) => a - b);

        // Per scene states
        const alwaysOn = ["IN", "OUT", "AMP", "CAB"];
        const scenes = [];
        for (let s = 0; s < VirtualFractalPresets.NUM_SCENES; ++s) {
            const scene = {};

            for (let i = 0; i < blocks.length; ++i) {
                const info = VirtualFractalBlocks.get(blocks[i]);

                scene[blocks[i]] = {
                    bypassed: alwaysOn.includes(info.abbr) ? false : ((i + s + preset) % 3 == 2),
                    channel: (i + s + preset) % info.channels
                };
            }

            scenes.push(scene);
        }

        return {
            name: amps[preset % amps.length] + " " + styles[Math.floor(preset / amps.length) % styles.length],
            defaultScene: 0,
            sceneNames: sceneNames.map((n, s) => sceneNames[(s + preset) % sceneNames.length]),
            blocks: blocks,
            scenes: scenes
        };
    }

    /**
     * Notify listeners
     */
    #notify(changeType) {
        for (const cb of this.#callbacks) {
            cb(changeType);
        }
    }
}
