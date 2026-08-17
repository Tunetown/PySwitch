/**
 * Generates a parameter list for a DisplayNode
 */
class DisplayParameterList extends ParameterList {
    
    handler = null;  // DisplayNode instance
    #loaded = false;

    constructor(handler) {
        super(handler.editor.controller, handler.editor.getConfig().parser)
        this.handler = handler;
    }

    /**
     * Sets up the parameters
     */
    async setup() {
        await this.#setupNodeTypeParameter();
        await this.#setupOrderParameter();
        await this.#setupAssignParameter();

        // Others, depending on the type of node
        await this.setupTypeParameters();

        this.#loaded = true;

        this.update();
    }

    /**
     * Add type specific parameters in child classes
     */
    async setupTypeParameters() {        
    }

    /**
     * Update inputs from the data model
     */
    update() {
        if (!this.#loaded) return;
        
        this.setParameter('z', this.handler.getChildIndex());
        this.setParameter('assign', this.handler.node.assign);

        // Others, depending on the type of node
        this.updateTypeParameters();

        // Check
        this.check();
    }

    /**
     * Update type specific parameters in child classes
     */
    updateTypeParameters() {        
    }

    /**
     * Check messages
     */
    check() {
        this.inputs.forEach((input) => {
            input.log.clear();
        });

        const that = this;
        this.handler.getMessages().forEach((msg) => {
            if (!msg.input) return;
            that.getParameter(msg.input).log.message(msg.message, msg.type);
        });
    }

    ////////////////////////////////////////////////////////////////////////////////////////////

    async #setupNodeTypeParameter() {
        const that = this;

        async function setType(type) {
            await that.handler.setType(type);
            await that.handler.editor.parameters.select(that.handler.editor.selected);
        }

        let select = null;
        await this.createTextInput({
            name: "display_element_type",
            displayName: "Label Type",
            value: this.handler.node.name,
            additionalClasses: "wide",
            onChange: async function(value) {
                await setType(value);
            },
            additionalContent: [
                select = $('<select class="parameter-option" />')
                    .append(
                        $('<option />')
                            .prop('value', "")
                            .text('Select type...'),

                        $('<option />')
                            .prop('value', "DisplayLabel")
                            .text('DisplayLabel'),

                        $('<option />')
                            .prop('value', "TunerDisplay")
                            .text('TunerDisplay'),

                        $('<option />')
                            .prop('value', "BidirectionalProtocolState")
                            .text('BidirectionalProtocolState'),

                    )
                    .on('change', async function() {
                        try {
                            await setType(select.val());                            

                        } catch(e) {
                            that.handler.editor.controller.handle(e);
                        }
                    })
            ]
        });
    }

    /**
     * Add Z parameter
     */
    async #setupOrderParameter() {
        const that = this;

        await this.createNumericInput({
            name: "z",
            displayName: "Depth",
            //comment: "Z-Index (depth order index)",
            value: this.handler.getChildIndex(),
            additionalContent: [
                // Move up button
                $('<span class="button fas fa-chevron-up" data-toggle="tooltip" title="Move up in depth" />')
                .on('click', async function() {
                    try {
                        that.handler.moveUp();

                    } catch (e) {
                        that.controller.handle(e);
                    }
                }),

                // Move down button
                $('<span class="button fas fa-chevron-down" data-toggle="tooltip" title="Move down in depth" />')
                .on('click', async function() {
                    try {
                        that.handler.moveDown();

                    } catch (e) {
                        that.controller.handle(e);
                    }
                })
            ]
        });
    }

    /**
     * Add assignment parameter
     */
    async #setupAssignParameter() {
        const that = this;

        async function onChange(value, setValue) {
            // Strip unallowed chars
            let newValue = value.replace(/[^a-zA-Z0-9_]/g, '_');

            // Remove preceeding underscores
            while (newValue.startsWith('_')) newValue = newValue.slice(1);

            that.handler.node.assign = newValue;

            that.handler.editor.update();

            setValue(newValue);
        }

        await this.createTextInput({
            name: "assign",
            displayName: "Export as",
            comment: "If you assign a name here, the label can be used in the actions. (This creates an assignment for the label instance which can be exported)",
            value: this.handler.node.assign ? this.handler.node.assign : "",
            onChange: this.handler.isReferenced() ? null : onChange
        });
    }

    /**
     * Add x and y parameters
     */
    async setupPositionParameters() {
        const bounds = this.handler.getModelBounds();
        const that = this;

        await this.createNumericInput({
            name: "x",
            displayName: "X",
            //comment: "Vertical position",
            value: bounds.x,
            onChange: async function(value) {
                const bounds2 = that.handler.getModelBounds();
                bounds2.x = value;
                that.handler.setModelBounds(bounds2);
                
                that.handler.update();
            }
        });

        await this.createNumericInput({
            name: "y",
            displayName: "Y",
            //comment: "Horizontal position",
            value: bounds.y,
            onChange: async function(value) {
                const bounds2 = that.handler.getModelBounds();
                bounds2.y = value;
                that.handler.setModelBounds(bounds2);
                
                that.handler.update();
            }
        });
    }

    /**
     * Add width and height parameters
     */
    async setupSizeParameters() {
        const bounds = this.handler.getModelBounds();
        const that = this;

        await this.createNumericInput({
            name: "width",
            displayName: "Width",
            //comment: "Width",
            value: bounds.width,
            range: {
                min: 1
            },
            onChange: async function(value) {
                const bounds2 = that.handler.getModelBounds();
                bounds2.width = value;
                that.handler.setModelBounds(bounds2);
                
                that.handler.update();
            }
        });

        await this.createNumericInput({
            name: "height",
            displayName: "Height",
            //comment: "Height",
            value: bounds.height,
            range: {
                min: 1
            },
            onChange: async function(value) {
                const bounds2 = that.handler.getModelBounds();
                bounds2.height = value;
                that.handler.setModelBounds(bounds2);
                
                that.handler.update();
            }
        });
    }
}