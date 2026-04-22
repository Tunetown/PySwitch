/**
 * Implements the parameter editor
 */
class ActionProperties {
    
    actionDefinition = null;
    inputs = null;
    parserFrontend = null;
    controller = null;
    oldProperties = null;

    #messages = null;
    #pagers = null;
    #internalRows = null;
    #encoderProps = null;
    #advancedRows = null;
    #advancedLevel = 0;

    constructor(controller, parserFrontend, actionDefinition, oldProperties = null, messages = []) {
        this.controller = controller;
        this.parserFrontend = parserFrontend;
        this.actionDefinition = actionDefinition;
        
        this.oldProperties = oldProperties;
        this.#messages = messages;
        
        this.#pagers = new PagerProperties(this);
        this.#internalRows = new ActionPropertiesInternal(this);
        this.#encoderProps = new ActionPropertiesEncoder(this);
    }

    /**
     * Initialize after adding to DOM
     */
    async init() {
        await this.#pagers.init();
        await this.update();
    }

    /**
     * Generate the DOM for the properties panel
     */
    async get() {
        this.#advancedRows = [];
        this.inputs = new Map();

        /**
         * Take over old values from the old props object, if different from the default
         */
        async function takeOverValues(input, param) {
            if (param.meta.type() == "text") return;
            if (!that.oldProperties) return;
                
            const oldParam = that.oldProperties.getParameterDefinition(param.name);
            const oldValue = that.oldProperties.getParameterValue(param.name);
            
            if (oldValue !== null && oldValue != oldParam.meta.getDefaultValue()) {
                await that.#setInputValue(input, param, oldValue);
            }
        }

        /**
         * Returns the passed element with the passed comment on hover
         */
        function withComment(el, param, comment) {
            if (param && param.meta.data.hideComment) return el;

            return Tools.withComment(el, comment)
        }

        const that = this;
        const parameters = await Promise.all(
            this.actionDefinition.parameters
            .sort(function(a, b) {
                return (a.meta.data.advanced ? a.meta.data.advanced : 0) - (b.meta.data.advanced ? b.meta.data.advanced : 0);
            })
            .map(
                async (param) => {
                    const input = await this.#createInput(param);

                    that.inputs.set(param.name, input);

                    // Take over old values from the old props object, if different from the default
                    await takeOverValues(input, param);

                    // Get messages for the parameter
                    const messages = that.#messages.filter((item) => item.parameter == param.name)
                    
                    // Build DOM for row
                    const row = withComment(
                        $('<tr class="selectable" />').append(
                            // Parameter Name                        
                            $('<td />').append(
                                $('<span />').text(param.meta.getDisplayName())
                            ),                     

                                
                            // Input
                            $('<td />')
                            .addClass(messages.length ? "has-messages" : null)
                            .append(
                                input,
                                ...(await that.#createAdditionalInputOptions(input, param))
                            )
                        ),
                        param,
                        await this.#getParameterComment(param)
                    );

                    if (!messages.length) {
                        // No messages: Hide if advanced
                        if (param.meta.data.advanced) {
                            that.registerAdvancedParameterRow(row, param);
                        }

                        return row;

                    } else {
                        // Messages: Also return additional rows. The result array (parameters) will be flattened later.
                        return [
                            // Main input row
                            row,

                            // Message rows
                            ...messages.map((item) => {
                                return $('<tr class="param-messages" />').append(
                                    $('<td />'),
    
                                    $('<td />').append(
                                        item.message
                                    )
                                )
                            })                            
                        ]
                    }
                }
            )
        );
        
        // Internal parameters (assign, hold etc.)
        const internalRows = [].concat(
            (await this.#internalRows.get()),
            (await this.#pagers.get())            
        )
        .map(
            (item) => {
                return item ? withComment(
                    item.element,
                    null,
                    item.comment
                ) : null;
            }
        );

        let tbody = null;
        const ret = $('<div class="action-properties" />').append(
            // Action name
            $('<div class="action-header" />')
            .text(this.actionDefinition.meta.getDisplayName()),
            
            // Comment
            $('<div class="action-comment" />')
            .html(this.#getActionComment()),

            // Parameters
            $('<div class="action-header" />')
            .text("Parameters:"),

            $('<div class="action-parameters" />').append(
                $('<table />').append(
                    tbody = $('<tbody />').append(
                        ...internalRows,

                        // Action parameters
                        parameters.flat()
                    )
                )
            ),

            // Pager buttons
            ...(await this.#pagers.getButtons())
        );

        await this.#internalRows.setup();
        await this.#pagers.setup();
        await this.#encoderProps.setup();

        // Advanced parameters: Show all button
        if (this.#advancedRows.length > 0) {
            let advRow = null;
            tbody.append(
                advRow = $('<tr />').append(
                    $('<td colspan="2" />').append(
                        $('<span class="show-advanced" />')
                        .text("more...")
                        .on('click', async function() {
                            try {
                                that.#advancedLevel++;
                                that.#updateAdvancedLevel(advRow);
                                
                            } catch (e) {
                                that.controller.handle(e);
                            }
                        })
                    )
                )
            )
        }

        return ret;
    }

    /**
     * Adds an advanced parameter row to an array to show them later (the array is 2 dimensional, grouped by advanced value)
     */
    registerAdvancedParameterRow(row, param) {
        row.hide();

        const level = param.meta.data.advanced;

        // Check if level exists
        while (this.#advancedRows.length < level) {
            this.#advancedRows.push([]);
        }

        this.#advancedRows[level - 1].push(
            {
                row: row,
                parameterName: param.name
            }
        );
    }

    /**
     * Update advanced parameter rows to the currend advancedLevel.
     */
    #updateAdvancedLevel(advRow) {
        if (this.#advancedRows.length < this.#advancedLevel) return;
                                
        for (const row of this.#advancedRows[this.#advancedLevel - 1]) {
            row.row.show();
        }

        if (this.#advancedRows.length == this.#advancedLevel + 1) {
            advRow.find('.show-advanced').text("all...");
        }

        if (this.#advancedRows.length == this.#advancedLevel) {
            // Last level
            advRow.hide();
        }
    }

    /**
     * Returns an action definition which can be added to the Configuration.
     */
    createActionDefinition() {
        const that = this;

        function getName() {
            if (that.actionDefinition.name == "PagerAction.proxy") {
                const pagerProxy = that.pagerProxy();
                
                if (pagerProxy) {
                    return that.actionDefinition.name.replace("PagerAction", pagerProxy)
                }
            }
            return that.actionDefinition.name;
        }

        return {
            name: getName(),
            assign: this.inputs.get('assign').val(),
            arguments: this.actionDefinition.parameters
                .filter((param) => {
                    const input = that.inputs.get(param.name);
                    if (!input) throw new Error("No input for param " + param.name + " found");
        
                    const value = that.#getInputValue(input, param);

                    return !param.hasOwnProperty("default") || (value != param.default);
                })
                .map((param) => {
                    const input = that.inputs.get(param.name);
                    if (!input) throw new Error("No input for param " + param.name + " found");
        
                    return {
                        name: param.name,
                        value: that.#getInputValue(input, param)
                    };
                })
        }
    }

    /**
     * Returns if the user selected hold or not (JS bool, no python value)
     */
    hold() {
        if (this.actionDefinition.meta.data.target == "AdafruitSwitch") {
            return !!this.inputs.get("hold").prop('checked');
        }
        return false;
    }

    /**
     * Sets the hold input
     */
    async setHold(hold) {
        if (this.actionDefinition.meta.data.target != "AdafruitSwitch") {
            return;
        }
        this.inputs.get("hold").prop('checked', !!hold)
        // await this.update();
    }

    /**
     * Returns the assign value if set
     */
    assign() {
        if (!this.inputs.has("assign")) return null;
        return this.inputs.get("assign").val();
    }

    /**
     * Sets the assign input
     */
    async setAssign(assign) {
        this.inputs.get("assign").val(assign);
        // await this.update();     
    }

    /**
     * Returns the pager proxy value if set
     */
    pagerProxy() {
        if (!this.inputs.has("pager")) return null;
        return this.inputs.get("pager").val();
    }

    /**
     * Sets the pager proxy input
     */
    async setPagerProxy(proxy) {
        this.inputs.get("pager").val(proxy);   
        // await this.update();
    }

    /**
     * Sets the input values to the passed arguments list's values
     */
    async setArguments(args) {
        await this.update();

        for (const arg of args) {
            await this.setArgument(arg.name, arg.value);
            
            // If not default value, show the row
            const param = this.getParameterDefinition(arg.name);
            const defaultValue = param.meta.getDefaultValue()
            if (defaultValue != arg.value) {
                this.showParameter(arg.name)
            }
        }

        await this.update();
    }

    /**
     * Set the value of a parameter input
     */
    async setArgument(name, value) {
        await this.update();

        // Get parameter definition first
        const param = this.getParameterDefinition(name);
        if (!param) throw new Error("Parameter " + name + " not found");

        const input = this.inputs.get(param.name);
        if (!input) throw new Error("No input for param " + param.name + " found");

        await this.#setInputValue(input, param, value);

        await this.update();
    }

    /**
     * Shows an advanced parameter
     */
    showParameter(name) {
        for (const level of this.#advancedRows) {
            for (const row of level) {
                if (row.parameterName == name) {
                    row.row.show();
                }
            }
        }
    }

    /**
     * Searches a parameter mode by name
     */
    getParameterDefinition(name) {
        for (const param of this.actionDefinition.parameters) {
            if (param.name == name) return param;
        }
        return null;
    }

    /**
     * Determine the comment for the action
     */
    #getActionComment() {
        if (!this.actionDefinition.comment) return "No information available";
        let comment = "" + this.actionDefinition.comment;

        //if (comment.slice(-1) != ".") comment += ".";

        return comment;
    }

    /**
     * Determine parameter comment
     */
    #getParameterComment(param) {
        if (param.meta.data.comment) return param.meta.data.comment;
        if (!param.comment) return "";
        return param.comment;
    }

    /**
     * Update the UI
     */
    async update() {
        await this.#pagers.update();
    }

    /**
     * Generates the DOM for one parameter
     */
    async #createInput(param) {
        const type = param.meta.type();

        const that = this;
        async function onChange() {            
            await that.update();
        }

        switch(type) {
            case "bool": {                             
                return $('<input type="checkbox" />')
                .prop('checked', param.meta.getDefaultValue() == "True")
                .on('change', onChange)
            }

            case "int": {
                return (await this.#getNumberInput(param))
                .on('change', onChange)
                .val(param.meta.getDefaultValue());
            }

            case 'select': {
                const values = await param.meta.getValues();
                if (values) {
                    return $('<select />').append(
                        values.map((option) => 
                            $('<option value="' + option.value + '" />')
                            .text(option.name)
                        )
                    )
                    .on('change', onChange)
                    .val(param.meta.getDefaultValue())
                }
                break;
            }

            case 'select-page': {
                return $('<select />')
                .on('change', onChange)
            }
                
            case 'pages': {
                // Dedicated type for the pager actions's "pages" parameter
                return this.#pagers.getPagesList(onChange);
            }

            case 'rig_map': {
                // Dedicated type for EFFECT_STATE_PER_RIG's rig_overrides parameter.
                // Renders a table where each row maps a Bank/Rig pair to an effect slot.
                return ActionProperties.#createRigMapInput(onChange);
            }
        }

        return $('<input type="text" />')
            .on('change', onChange)
            .val(param.meta.getDefaultValue())
    }

    /**
     * If the parameter is of type "color", this returns additional elements to add to the input. Also
     * other special types with additional inputs are created here. 
     * 
     * If not special, an empty array is returned.
     */
    async #createAdditionalInputOptions(input, param) {
        switch (param.meta.type()) {
            case "color": return this.#createAdditionalColorInputOptions(input, param);
            case "select-free": return this.#createAdditionalSelectFreeInputOptions(input, param);
        }
        
        return [];
    }

    async #createAdditionalSelectFreeInputOptions(input, param) {
        const that = this;
        return [
            $('<select class="parameter-option" />').append(
                (await param.meta.getValues())
                .concat([{
                    name: "Select..."
                }])
                .map((item) => 
                    $('<option value="' + item.name + '" />')
                    .text(item.name)
                )
            )
            .on('change', async function() {
                const value = $(this).val();
                if (value == "Select...") return;

                await that.setArgument(param.name, value);

                $(this).val("Select...")
            })
            .val("Select..."),
        ];
    }

    async #createAdditionalColorInputOptions(input, param) {
        let colorInput = null;
        const that = this;

        async function updateColorInput() {
            const color = await that.parserFrontend.parser.resolveColor(input.val());
            if (color) {
                colorInput.val(Tools.rgbToHex(color))
            }
        }

        const ret = [
            $('<select class="parameter-option" />').append(
                (await this.parserFrontend.parser.getAvailableColors())
                .concat([{
                    name: "Select color..."
                }])
                .map((item) => 
                    $('<option value="' + item.name + '" />')
                    .text(item.name)
                )
            )
            .on('change', async function() {
                const color = $(this).val();
                if (color == "Select color...") return;

                await that.setArgument(param.name, color);

                $(this).val("Select color...")

                await updateColorInput();
            })
            .val("Select color..."),

            colorInput = $('<input type="color" class="parameter-option parameter-link" />')
            .on('change', async function() {
                const rgb = Tools.hexToRgb($(this).val());

                await that.setArgument(param.name, "(" + rgb[0] + ", " + rgb[1] + ", " + rgb[2] + ")");
            })
        ];

        input.on('change', updateColorInput)
        await updateColorInput();

        return ret;
    }

    /**
     * Returns a parameter value by name
     */
    getParameterValue(name) {
        const param = this.getParameterDefinition(name);
        if (!param) return null;

        const input = this.inputs.get(param.name);
        if (!input) return null;

        return this.#getInputValue(input, param);        
    }

    /**
     * Converts the input values to action argument values
     */
    #getInputValue(input, param) {
        const type = param.meta.type();

        switch(type) {
            case "bool": return input.prop('checked') ? "True" : "False";
            case "pages": return this.#pagers.pages.get();
            case "rig_map": return ActionProperties.#getRigMapValue(input);
        }

        let value = input.val();
        if (value == "") value = param.meta.getDefaultValue();

        return param.meta.convertInput(value);
    }

    /**
     * Sets the input value according to an argumen/parameter value
     */
    async #setInputValue(input, param, value) {
        const type = param.meta.type();

        switch(type) {
            case "bool": 
                input.prop('checked', value == "True");
                input.trigger('change');
                break;

            case "pages":
                await this.#pagers.pages.set(value)
                break;

            case "rig_map":
                ActionProperties.#setRigMapValue(input, value, onChange);
                break;

            default:
                input.val(value.replaceAll('"', "'"));
                input.trigger('change');
        }
    }

    // -------------------------------------------------------------------------
    // rig_map type: per-rig slot override table for EFFECT_STATE_PER_RIG
    // -------------------------------------------------------------------------

    static #RIG_MAP_SLOTS = [
        { name: "Slot A",              value: "KemperEffectSlot.EFFECT_SLOT_ID_A" },
        { name: "Slot B",              value: "KemperEffectSlot.EFFECT_SLOT_ID_B" },
        { name: "Slot C",              value: "KemperEffectSlot.EFFECT_SLOT_ID_C" },
        { name: "Slot D",              value: "KemperEffectSlot.EFFECT_SLOT_ID_D" },
        { name: "Slot X",              value: "KemperEffectSlot.EFFECT_SLOT_ID_X" },
        { name: "Slot MOD",            value: "KemperEffectSlot.EFFECT_SLOT_ID_MOD" },
        { name: "Slot DLY (spillover)",value: "KemperEffectSlot.EFFECT_SLOT_ID_DLY" },
        { name: "Slot REV (spillover)",value: "KemperEffectSlot.EFFECT_SLOT_ID_REV" },
        { name: "Slot DLY (no spill)", value: "KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL" },
        { name: "Slot REV (no spill)", value: "KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL" },
    ];

    /**
     * Creates the rig_map table container element.
     * onChange is called whenever the user modifies a row.
     */
    static #createRigMapInput(onChange) {
        const container = $('<div class="rig-map-container" />');

        const table = $('<table class="rig-map-table" />').append(
            $('<thead />').append(
                $('<tr />').append(
                    $('<th />').text('Bank'),
                    $('<th />').text('Rig'),
                    $('<th />').text('Slot'),
                    $('<th />')
                )
            )
        );
        const tbody = $('<tbody />');
        table.append(tbody);
        container.append(table);

        const addBtn = $('<button type="button" class="rig-map-add" />').text('+ Add override');
        addBtn.on('click', function() {
            ActionProperties.#addRigMapRow(tbody, 1, 1, ActionProperties.#RIG_MAP_SLOTS[0].value, onChange);
            onChange();
        });
        container.append(addBtn);

        return container;
    }

    /**
     * Appends one row to the rig_map tbody.
     */
    static #addRigMapRow(tbody, bank, rig, slotValue, onChange) {
        const slotSelect = $('<select class="rig-slot" />').append(
            ActionProperties.#RIG_MAP_SLOTS.map(s =>
                $('<option />').val(s.value).text(s.name)
            )
        ).val(slotValue).on('change', onChange);

        const rigSelect = $('<select class="rig-rig" />').append(
            [1,2,3,4,5].map(n => $('<option />').val(n).text(n))
        ).val(rig).on('change', onChange);

        const bankInput = $('<input type="number" class="rig-bank" min="1" max="125" />')
            .val(bank).on('change', onChange);

        const removeBtn = $('<button type="button" class="rig-remove" />').text('X');
        const row = $('<tr />').append(
            $('<td />').append(bankInput),
            $('<td />').append(rigSelect),
            $('<td />').append(slotSelect),
            $('<td />').append(removeBtn)
        );
        removeBtn.on('click', function() {
            row.remove();
            onChange();
        });
        tbody.append(row);
    }

    /**
     * Reads the rig_map table and returns a Python dict string.
     * e.g. {2: KemperEffectSlot.EFFECT_SLOT_ID_C, 5: KemperEffectSlot.EFFECT_SLOT_ID_DLY}
     * Absolute rig ID = (bank - 1) * 5 + (rig - 1)
     */
    static #getRigMapValue(container) {
        const entries = [];
        container.find('tbody tr').each(function() {
            const bank = parseInt($(this).find('.rig-bank').val()) || 1;
            const rig  = parseInt($(this).find('.rig-rig').val())  || 1;
            const slot = $(this).find('.rig-slot').val() || ActionProperties.#RIG_MAP_SLOTS[0].value;
            const absRig = (bank - 1) * 5 + (rig - 1);
            entries.push(absRig + ': ' + slot);
        });
        return '{' + entries.join(', ') + '}';
    }

    /**
     * Parses a Python dict string and populates the rig_map table.
     * e.g. "{2: KemperEffectSlot.EFFECT_SLOT_ID_C, 5: KemperEffectSlot.EFFECT_SLOT_ID_DLY}"
     */
    static #setRigMapValue(container, value, onChange) {
        const tbody = container.find('tbody');
        tbody.empty();

        if (!value || value.trim() === '{}') return;

        // Strip braces and split by comma, handling potential spaces
        const inner = value.trim().replace(/^\{/, '').replace(/\}$/, '').trim();
        if (!inner) return;

        const pairs = inner.split(',').map(s => s.trim()).filter(s => s.length > 0);
        for (const pair of pairs) {
            const colonIdx = pair.indexOf(':');
            if (colonIdx < 0) continue;
            const absRigStr = pair.substring(0, colonIdx).trim();
            const slotStr   = pair.substring(colonIdx + 1).trim();
            const absRig = parseInt(absRigStr);
            if (isNaN(absRig)) continue;
            const bank = Math.floor(absRig / 5) + 1;
            const rig  = (absRig % 5) + 1;
            ActionProperties.#addRigMapRow(tbody, bank, rig, slotStr, onChange);
        }
    }

    /**
     * Create a numeric input (int)
     */
    async #getNumberInput(param) {
        const values = await param.meta.getValues();
        if (!values) {
            return $('<input type="number" />');
        }

        return $('<select />').append(
            values.map((option) => 
                $('<option value="' + option.value + '" />')
                .text(option.name)
            )
        ) 
    }
}