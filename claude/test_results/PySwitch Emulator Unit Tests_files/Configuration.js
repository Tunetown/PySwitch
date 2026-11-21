/**
 * Represents a configuration, consisting of the files inputs.py and display.py.
 * Child classes must provide the more specific loading implementations.
 */
class Configuration {

    #data = null;
    #name = null;
    #dirty = false;
    
    parser = null;
    controller = null;

    globalConfiguration = {}
    
    constructor(controller, name = "") {
        this.controller = controller;
        this.#name = name;
    }

    async destroy() {        
    }

    /**
     * Init the parser
     */
    async init(runner, basePath = "") {
        await this.get();
        
        this.parser = new Parser(this, runner, basePath);
    }

    /**
     * Returns an object containing all config code. Normally this is:
     * {
     *      inputs_py: "Code",
     *      display_py: "Code"
     * }
     */
    async get() {
        if (!this.loaded()) {
            this.#data = await this.load();
            this.resetDirtyState();
        }
        
        return this.#data;
    }

    /**
     * Set new data.
     */
    set(data) {
        this.setDirty();
        this.#data = data;
    }

    /**
     * Returns if the config has been loaded
     */
    loaded() {
        return !!this.#data;
    }

    /**
     * Returns the text for the head line
     */
    async name() {
        return this.#name;
    }

    ///////////////////////////////////////////////////////////////////

    /**
     * Save the data to the location of the configuration
     */
    async save() {
        await this.doSave();
        this.resetDirtyState();
    }

    /**
     * Returns if the config has unsaved changes
     */
    isDirty() {
        return this.#dirty;
    }

    /**
     * Set the config dirty
     */
    setDirty() {
        this.#dirty = true;
        this.controller.ui.setDirty();
    }

    /**
     * Reset the dirty state
     */
    resetDirtyState() {
        this.#dirty = false;
        this.controller.ui.resetDirtyState();
    }

    ///////////////////////////////////////////////////////////////////

    /**
     * Must load data and return it (only called internally!)
     */
    async load() {
        throw new Error("Must be implemented in child classes");
    }

    /**
     * Can the config be saved?
     */
    canBeSaved() {
        return false;
    }

    /**
     * Save the data to the location of the configuration
     */
    async doSave() {
        throw new Error("Saving not supported for this type of configuration");
    }
}