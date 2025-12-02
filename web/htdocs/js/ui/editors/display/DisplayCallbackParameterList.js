class DisplayCallbackParameterList extends ParameterList {

    #callbackNode = null;
    #hideParameterCallback = null;    // callback (param) => boolean

    constructor(controller, parser, callbackNode, hideParameterCallback = null) {
        super(controller, parser)
        this.#callbackNode = callbackNode;
        this.#hideParameterCallback = hideParameterCallback;
    }

    /**
     * Sets up parameters on the passed ParameterList instance, according to the type of display element.
     */
    async setup() {
        const that = this;
        if (!this.#callbackNode) return;
        
        // Get definition
        const definition = await this.parser.getCallbackDefinition(
            this.#callbackNode.name,
            this.#callbackNode.client
        );
        if (!definition) return;

        function getCallbackParameter(name) {
            const node = Tools.getArgument(that.#callbackNode, name);
            return node ? node.value : null;
        }

        function getCurrentValue(param) {
            let val = getCallbackParameter(param.name);
            if (!val) {
                val = param.meta.getDefaultValue();
            }
            
            return that.convertValue(param.meta.type(), val);
        }

        function setCurrentValue(param, value) {
            const defaultValue = param.meta.getDefaultValue();
            const valueConverted = that.unconvertValue(param.meta.type(), value);

            let node = Tools.getArgument(that.#callbackNode, param.name);
            if (!node) {
                that.#callbackNode.arguments.push(node = {
                    name: param.name
                })
            }

            if (valueConverted == defaultValue) {
                that.#callbackNode.arguments = that.#callbackNode.arguments.filter((entry) => (entry.name != param.name));                
            } else {
                node.value = valueConverted;
            }
        }

        // Add parameters
        console.log(definition)
        for(const param of definition.parameters) {
            if (this.#hideParameterCallback) {
                if (!(await this.#hideParameterCallback(param))) continue;
            }

            const type = param.meta.type();
            const listType = this.convertType(type);

            // Get current value or default if not set
            const currentValue = getCurrentValue(param);

            await this.createInput({
                type: listType,
                name: param.name,
                displayName: param.meta.getDisplayName(),
                comment: param.comment,
                value: currentValue,
                onChange: async function(value) {
                    setCurrentValue(param, value);
                }
            });
        }
    }
}