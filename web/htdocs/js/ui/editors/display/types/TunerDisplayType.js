class TunerDisplayType extends DisplayNodeType {

    // layout = null;    // TunerDisplayTypeLayout instance

    constructor(handler) {
        super(handler);

        // this.layout = new TunerDisplayTypeLayout(handler)
    }

    /**
     * Sets up the preview DOM element
     */
    setupPreviewElement(element) {
        element.addClass('display-tuner')
    }

    /**
     * Is the node editable?
     */
    editable() {
        return true;
    }

    /**
     * Returns if the node is resizable
     */
    resizable() {
        return true;
    }

    /**
     * Returns the display text for the node (for all others than the preview)
     */
    getName() {
        if (this.handler.node.hasOwnProperty("assign")) return this.handler.node.assign;

        const callback = Tools.getArgument(this.handler.node, "callback");
        if (callback) return callback.value.name;
        
        return super.getName();
    }

    // /**
    //  * Background color for preview or null for no specific color is wanted
    //  */
    // getPreviewBackColor() {
    //     return this.layout.getParameter('backColor');
    // }

    // /**
    //  * Text color for preview or null for no specific color is wanted
    //  */
    // getPreviewTextColor() {
    //     return this.layout.getParameter('textColor');
    // }

    /**
     * Gets a data node list for the default arguments of the type.
     */
    getDefaultArguments() {
        return [
            // {
            //     name: "layout",
            //     value: {
            //         arguments: [
            //             {
            //                 name: "font",
            //                 value: '"/fonts/H20.pcf"'
            //             },
            //             {
            //                 name: "backColor",
            //                 value: 'DEFAULT_LABEL_COLOR'
            //             },
            //             {
            //                 name: "stroke",
            //                 value: '1'
            //             }
            //         ]
            //     }
            // }
        ];
    }

    /**
     * Returns DOM for parameter lists
     */
    async getParameterLists() {
        return [
            new TunerDisplayTypeParameterList(this)
        ]
    }
}