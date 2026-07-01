/**
 * Parser base class. Implements the basic parsing (using python helpers a lot), while the
 * child class(es) add client specific information.
 */
class Parser {

    config = null;                   // Configuration instance
    runner = null;                   // PySwitchRunner instance
    basePath = null;                 // Base path for fetching data via HTTP
    checks = null;                   // Checks handler

    #pySwitchParser = null;          // Proxy to the python PySwitchParser instance

    #availableActions = null;        // Buffer
    #availableMappings = null;       // Buffer
    #availableKeycodes = null;       // Buffer
    #availableFonts = null;          // Buffer
    #bufferHardwareInfo = null;      // Buffer
    #availableCallbacks = null; // Buffer
    #colors = null;                  // Buffer
    #inputs = null;                  // Buffer for input instances

    #trees = null;                   // Raw parsed data

    constructor(config, runner, basePath = "") {
        this.config = config;
        this.runner = runner;
        this.basePath = basePath;

        this.checks = new ParserChecks(this);

        this.#bufferHardwareInfo = new Map();        
        this.reset();
    }

    /**
     * Creates the python libcst parser. Must be called at least once before 
     * the parser is actually used. Expects the PySwitchRunner.
     */
    async init() {
        const device = await this.device();

        if (this.#pySwitchParser && (this.#pySwitchParser.hw_import_path == device.getHardwareImportPath())) {
            this.#initTrees();
            return;
        }
        
        const clients = (await Client.getAvailable(this.basePath)).map((item) => item.id);

        this.#pySwitchParser = await this.runner.pyodide.runPython(`         
            from parser.PySwitchParser import PySwitchParser
            PySwitchParser(
                hw_import_path         = "` + device.getHardwareImportPath() + `",
                available_clients_json = '` + JSON.stringify(clients) + `',
            )
        `);

        //this.#pySwitchParser.init(this);

        const inputs_py = (await this.config.get()).inputs_py;
        const display_py = (await this.config.get()).display_py;

        await this.#pySwitchParser.from_source(inputs_py, display_py);        

        this.#initTrees();
    }

    /**
     * Load trees if not yet done
     */
    #initTrees() {
        const that = this;
        function createTree(fileId, createDataCallback) {   
            if (that.#trees.has(fileId)) return
            
            const data = createDataCallback();
            if (data) {
                that.#trees.set(fileId, JSON.parse(data));
            }
        }

        createTree("inputs_py", () => this.#pySwitchParser.inputs())
        createTree("display_py", () => this.#pySwitchParser.splashes())
    }

    /**
     * Reset trees and checks
     */
    reset() {
        this.checks.reset();

        this.#trees = new Map();
        this.#inputs = new Map();
    }

    /**
     * From the tree for fileId, this searches recursively for the passed assignment 
     * name and returns its definition node.
     */
    getAssignment(fileId, name) {
        this.#initTrees();
        
        function crawl(node) {
            if (Array.isArray(node)) {
                for (const item of node) {
                    const ret = crawl(item);
                    if (ret) return ret;
                }
            }

            if (typeof node == "object") {
                if (node.assign == name) return node;
                if (node.value) return crawl(node.value);
                if (node.arguments) return crawl(node.arguments);
            }

            return null;
        }

        return crawl(this.#trees.get(fileId));
    }

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * For a raw tree node, this returns the source code
     */
    codeForNode(node) {
        return this.#pySwitchParser.code_for_data_node(node)
    }

    /**
     * Returns the inputs raw tree
     */
    inputs() {
        if (!this.#pySwitchParser) throw new Error("Parser not initialized")
        this.#initTrees();
        return this.#trees.get("inputs_py");
    }

    /**
     * Returns a (proxy) instance of Input.py, which handles all operations on the input.
     * modelName must be the model name as defined in the hardware definitions.
     */
    async input(modelName, createIfNotExistent = false) {
        if (this.#inputs.has(modelName)) return this.#inputs.get(modelName);
        
        await this.init();

        const hw = await this.getHardwareInfo();

        function getAssignmentForModel() {
            const filteredHw = hw.filter((item) => item.data.name == modelName);
            if (!filteredHw.length) return null;
         
            return filteredHw[0];
        }
        
        const assignment = getAssignmentForModel();
        const inputData = this.inputData(assignment.name);

        if (!inputData) {
            if (!createIfNotExistent) return null;

            // Create new input
            const newInput = {
                arguments: [
                    {
                        name: "assignment",
                        value: assignment.name
                    }
                ]
            }

            this.#trees.get("inputs_py").push(newInput);

            this.updateConfig();
            
            return this.input(modelName);
        }
        
        const ret = new ParserInput(this, inputData, assignment);
        this.#inputs.set(modelName, ret);

        return ret;
    }

    /**
     * Returns raw input data for a assignmentName input, or null
     */
    inputData(assignmentName) {
        if (!this.#pySwitchParser) throw new Error("Parser not initialized")
            
        function getArgument(node, name) {
            if (!node.arguments) return null;

            const filteredArgs = node.arguments.filter((arg) => arg.name == name);
            if (!filteredArgs.length) return null;

            return filteredArgs[0].value;
        }

        const inputs_py = this.#trees.get("inputs_py");
        if (!inputs_py) return null;

        const filtered = inputs_py.filter((inputData) => 
            getArgument(inputData, "assignment") == assignmentName
        );

        if (!filtered.length) return null;
        return filtered[0];
    }

    /**
     * Returns the splashes raw tree
     */
    splashes() {
        if (!this.#pySwitchParser) throw new Error("Parser not initialized")
        this.#initTrees();
        return this.#trees.get("display_py");
    }

    /**
     * Sets a new splashes definition
     */
    async setSplashes(splashes) {
        await this.init();
        this.#trees.set("display_py", splashes);
        this.updateConfig();
    }

    /**
     * Updates the underlying config from the current CSTs. Called by python code after updates to the trees.
     */
    updateConfig() {
        if (!this.#pySwitchParser) throw new Error("Parser not initialized")

        this.#initTrees();
        this.#pySwitchParser.set_inputs(this.#trees.get("inputs_py"));
        this.#pySwitchParser.set_splashes(this.#trees.get("display_py"));

        const src = this.#pySwitchParser.to_source().toJs();
        
        this.config.set({
            inputs_py: src.get("inputs_py"),
            display_py: src.get("display_py")
        });

        this.reset();
    }

    /**
     * Update the config with new code for a single file and reset the parser
     */
    async updateFromSource(fileName, code) {
        await this.init();

        const data = await this.config.get();
        data[fileName] = code;

        await this.updateFromData(data);

        this.reset();    
    }

    /**
     * Update the config with new code for all files and reset the parser
     */
    async updateFromData(data) {
        await this.init();

        this.config.set(data);
        
        await this.#pySwitchParser.from_source(data.inputs_py, data.display_py);
        
        this.reset();
    }    

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Returns a device handler for the configuration (a config can only have one device)
     */
    async device() {
        return Device.getInstance(this.config);
    }

    /**
     * Returns hardware info (available inputs) for the given config (buffered)
     */
    async getHardwareInfo() {        
        const device = await this.device();
    
        if (this.#bufferHardwareInfo.has(device.getHardwareImportPath())) return this.#bufferHardwareInfo.get(device.getHardwareImportPath());

        const hardwareJson = await this.runner.pyodide.runPython(`
            import json
            from parser.PySwitchHardware import PySwitchHardware
            pySwitchHardware = PySwitchHardware()
            json.dumps(pySwitchHardware.get("` + device.getHardwareImportPath() + `"))
        `);

        this.#bufferHardwareInfo.set(device.getHardwareImportPath(), JSON.parse(hardwareJson));
        return this.#bufferHardwareInfo.get(device.getHardwareImportPath());
    }

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Returns all actions with the given name
     */
    async actions(name) {
        const hw = await this.getHardwareInfo();
        
        const ret = [];
        for (const inputDefinition of hw) {
            const input = await this.input(inputDefinition.data.name);
            if (!input) continue;

            const actions = input.actions(false).concat(input.actions(true));

            for (const action of actions) {
                if (action.name != name) continue;

                ret.push(action);
            }
        }
        return ret;
    }

    /**
     * Returns a PagerAction proxy by assign target name
     */
    async getPagerAction(name) {
        const pagers = await this.actions("PagerAction");
        for (const pager of pagers) {
            if (pager.assign == name) {
                return pager;
            }
        }
        return null;
    }

    /**
     * Resolve a color string. (r, g, b) will be passed through, Colors.XXX will be resolved.
     */
    async resolveColor(colorValue) {
        if (colorValue.startsWith('Colors')) {
            const colors = await this.getAvailableColors();
            
            for (const color of colors) {
                if (color.name == colorValue) {
                    return color.value;
                }
            }
        }

        return colorValue;
    }

    /**
     * Returns all available colors (buffered)
     */
    async getAvailableColors() {
        if (this.#colors) return this.#colors;

        const extractor = new ClassItemExtractor(this.runner);
        this.#colors = await extractor.get({
            file: "pyswitch/colors.py",
            importPath: "pyswitch.colors",
            className: "Colors",
            attributes: true
        });

        return this.#colors;
    }

    /**
     * Returns all available display labels
     */
    async getAvailableDisplays() {
        await this.init();
        
        const displays = JSON.parse(this.#pySwitchParser.displays());

        return displays.filter((item) => item != "Splashes");
    }

    /**
     * Returns all available key codes
     */
    async getAvailableKeycodes() {
        if (this.#availableKeycodes) return this.#availableKeycodes;

        this.#availableKeycodes = JSON.parse(await Tools.fetch(this.basePath + "definitions/keycodes.json"));

        return this.#availableKeycodes;
    }

    /**
     * Returns a list of available fonts
     */
    async getAvailableFonts() {
    if (this.#availableFonts) return this.#availableFonts;

        function getSortCriteria(item) {
            return parseInt(item.replace(/[^0-9]/g, ''));
        }

        this.#availableFonts = JSON.parse(await Tools.fetch(this.basePath + "definitions/fonts.json"))
            .sort((a, b) => getSortCriteria(a) - getSortCriteria(b));

        return this.#availableFonts;
    }

    /**
     * Returns a list of all available actions, with mixed in meta information
     */
    async getAvailableActions() {
        if (this.#availableActions) return this.#availableActions;

        // This just loads the buffered version. To create the list, see the parser tests.
        this.#availableActions = JSON.parse(await Tools.fetch(this.basePath + "definitions/actions.json"));
        
        // Put in meta info where exists
        for (const client of this.#availableActions) {
            await this.#mixInMetaInformation(client.actions, ClientFactory.getInstance(client.client));
        }
        
        return this.#availableActions;
    }

    /**
     * Returns an actions definition by name/clientId or null if not found
     *
    async getActionDefinition(name, clientId = null) {
        const clients = await this.getAvailableActions();

        for (const client of clients) {
            if (clientId && client.client != clientId) continue;

            for (const action of client.actions) {
                if (action.name == name) {
                    return action
                }
            }    
        }
        return null;
    }

    /**
     * Returns a list of all available callbacks, with mixed in meta information
     */
    async getAvailableCallbacks() {
        if (this.#availableCallbacks) return this.#availableCallbacks;

        // This just loads the buffered version. To create the list, see the parser tests.
        this.#availableCallbacks = JSON.parse(await Tools.fetch(this.basePath + "definitions/callbacks.json"));
        
        // Put in meta info where exists
        for (const client of this.#availableCallbacks) {
            await this.#mixInMetaInformation(client.callbacks, ClientFactory.getInstance(client.client));
        }
        
        return this.#availableCallbacks;
    }

    /**
     * Returns the definition for a callback, or null if not found
     */
    async getCallbackDefinition(name, clientId) {
        const clients = await this.getAvailableCallbacks();

        for (const client of clients) {
            if (clientId && client.client != clientId) continue;

            for (const callback of client.callbacks) {
                if (callback.name == name) {
                    return callback
                }
            }    
        }
        return null;
    }

    /**
     * Returns a list of all available actions, with mixed in meta information
     */
    async getAvailableMappings() {
        if (this.#availableMappings) return this.#availableMappings;

        // This just loads the buffered version. To create the list, see the parser tests.
        this.#availableMappings = JSON.parse(await Tools.fetch(this.basePath + "definitions/mappings.json"));

        // Put in meta info where exists
        for (const client of this.#availableMappings) {
            await this.#mixInMetaInformation(client.mappings, ClientFactory.getInstance(client.client));
        }

        return this.#availableMappings;
    }

    /**
     * For a list of function descriptors, this adds meta descriptor information (unbuffered)
     */
    async #mixInMetaInformation(data, client) {
        const that = this;
        const meta = JSON.parse(await Tools.fetch(this.basePath + "definitions/meta.json"));

        /**
         * Searches a function meta definition for the given function name.
         * No default resolving here.
         */
        function searchFunctionDefinition(funcName) {
            for (const clientDef of meta) {
                if (clientDef.client != client.id) continue;

                for (const definition of clientDef.entities) {
                    if (definition.entityName == funcName) {
                        return definition;
                    }
                }    
            }
            return null;
        }

        /**
         * Searches a parameter meta definition for the given function name and parameter name. 
         * No default resolving here.
         */
        function searchParameterDefinition(funcName, paramName) {
            const definition = searchFunctionDefinition(funcName);
            if (!definition) return null;

            for (const param of definition.parameters || []) {
                if (param.name == paramName) {                            
                    return param;
                }
            }                    

            return null;
        }

        /**
         * Returns function metadata
         */
        async function getFunctionMeta(func) {
            // Search for specific definition first
            let def = searchFunctionDefinition(func.name);

            // Strip parameters (waste of memory)
            if (def) {
                def = structuredClone(def);
                delete def.entityName;    
                delete def.parameters; 
                delete def.comment;    
            }

            return client.createFunctionMeta(that, def, func);
        }

        /**
         * Tries to find meta info for a parameter, resolving to default if not found
         */
        async function getParameterMeta(func, param) {
            // Search for specific definition first
            let def = searchParameterDefinition(func.name, param.name);

            if (!def) {
                // Search for default
                def = searchParameterDefinition("default", param.name);
            }

            return client.createParameterMeta(that, def, param);
        }

        // Scan function definitions
        for (const entry of data) {
            for (const param of entry.parameters || []) {
                param.meta = await getParameterMeta(entry, param);
            }

            entry.meta = await getFunctionMeta(entry);
        }
    }
}