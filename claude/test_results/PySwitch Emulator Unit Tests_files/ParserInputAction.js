class ParserInputAction extends ParserTreeElement {

    input = null;          // Reference to the parent input handler

    name = null;
    client = null;
    assign = null;
    definitionName = null; // Name of the action definition, if different from the name
    
    #id = null;
    #arguments = null;

    constructor(parser, input, data) {
        super(parser, data);

        this.#id = Tools.uuid();
        this.input = input;
        
        this.name = data.name;
        this.client = data.client;
        this.assign = data.assign;
        this.definitionName = this.#determineDefinitionName(); 
    }

    /**
     * Determine the proxy name (e.g. PagerAction.proxy)
     */
    #determineDefinitionName() {
        if (!this.name || !this.name.includes(".")) return null;

        const splt = this.name.split(".");
        if (splt.length != 2) return null;

        const assign = splt[0];     // _pager
        const funcName = splt[1];   // proxy

        const assignment = this.parser.getAssignment("inputs_py", assign);
        if (!assignment) return null;

        return assignment.name + "." + funcName;  // PagerAction.proxy
    }

    /**
     * Unique ID for the action to retrieve it in lists etc.
     */
    id() {
        return this.#id;
    }

    /**
     * Returns the name of the pager of the action, if it is assigned to one
     */
    pager() {
        this.checkValid()

        const ec = this.argument("enable_callback");
        if (!ec || ec == "None") return null;
        
        const id = this.argument("id");
        if (!id || id == "None")  return null;
        
        const splt = ec.split(".");
        if (splt.length != 2) return null;
        
        return splt[0];
    }

    /**
     * Returns the page (id) of the action, if it is assigned to a pager
     */
    page() {        
        if (!this.pager()) return null;
        return this.argument("id");
    }

    /**
     * Returns the arguments of the action
     */
    arguments() {
        this.checkValid()

        if (this.#arguments) return this.#arguments;
        if (!this.data.arguments) return [];

        const that = this;
        this.#arguments = this.data.arguments.map((arg) => {
            if (this.name == "PagerAction" && arg.name == "pages") {
                return {
                    name: arg.name ? arg.name : null,
                    value: that.#decodePages(arg)
                }
            }
            
            return {
                name: arg.name ? arg.name : null,
                value: this.parser.codeForNode(arg.value)
            }
        });

        return this.#arguments;
    }

    /**
     * Returns the value of a specific argument of the action.
     */
    argument(name) {
        this.checkValid()

        const args = this.arguments();

        for (const arg of args) {
            if (arg.name == name) return arg.value;
        }

        return null;
    }

    /**
     * Converts the nternal parser raw format to the pages array format used in the UI
     */
    #decodePages(arg) {
        return arg.value.map((page) => {
            function getPageArg(name) {
                for (const a of page.arguments) {
                    if (a.name == name) {
                        return a.value
                    }
                }
            }

            return {
                id: getPageArg("id"),
                color: getPageArg("color"),
                text: getPageArg("text")
            }
        })
    }
}