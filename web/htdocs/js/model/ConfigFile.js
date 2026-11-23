/**
 * Handles global configuration (config.py)
 */
class ConfigFile {

    #controller = null;
    #state = null;
    #defaults = null;

    constructor(controller) {
        this.#controller = controller;

        this.#state = new LocalState("global-settings");
        this.#defaults = {
            maxConsecutiveMidiMessages: 10,
            clearBuffers: true,
            maxRequestLifetimeMillis: 2000,
            memoryWarnLimitBytes: 1024 * 15,
            updateInterval: 400,
            displayDimFactorOn: 1,
            displayDimFactorOff: 0.2,
            ledBrightnessOn: 0.3,
            ledBrightnessOff: 0.02,
            fractalModel: 17,
            fractalBankSize: 5,
            fractalPresetDisplayOffset: 0,
            exploreMode: false,
            debugStats: false,
            debugStatsInterval: 2000,
            debugBidirectionalProtocol: false,
            debugUnparsedMessages: false,
            debugSentMessages: false,
            debugClientStats: false
        }
    }

    /**
     * Get the configuration
     */
    get() {
        return this.#state.get("config.py") || {}
    }

    /**
     * Set the configuration
     */
    set(data) {
        this.#state.set("config.py", data || {})
    }

    /**
     * Returns a single value
     */
    getAttribute(name) {
        const data = this.get();

        if (data.hasOwnProperty(name)) return data[name];

        if (!this.#defaults.hasOwnProperty(name)) return null;
        return this.#defaults[name];
    }

    /**
     * Sets a single value
     */
    setAttribute(name, value) {
        const data = this.get();

        data[name] = value;
        
        this.set(data);
    }
    
    /**
     * Returns config.py code
     */
    async render() {
        // Load template
        let template = await Tools.fetch("templates/config-template.py");

        const that = this;
        const done = new Map();

        /**
         * Is value a known default?
         */
        function isDefault(parameter, value) {
            if (!that.#defaults.hasOwnProperty(parameter)) return false;
            return that.#defaults[parameter] == value;
        }

        /**
         * Convert to python
         */
        function convertValue(value) {
            if (value === false) return "False";
            if (value === true) return "True";
            return value;
        }

        /**
         * Replace one token
         */
        function replaceToken(parameter) {
            const valueUnconverted = that.getAttribute(parameter);
            const value = convertValue(valueUnconverted);
            const valueStr = '"' + parameter + '": ' + value;
            done.set(parameter, true);
            template = template.replace('%' + parameter + '%', isDefault(parameter, valueUnconverted) ? ("#" + valueStr) : valueStr)
        }

        // Get data
        const data = this.get();

        // Set all fields of the data
        Object.keys(data).forEach(function(key) {
            replaceToken(key)
        });

        // Set all defaults where no value has been set
        Object.keys(this.#defaults).forEach(function(key) {
            if (done.has(key) && done.get(key)) return;
            replaceToken(key)
        });

        return template;
    }
}