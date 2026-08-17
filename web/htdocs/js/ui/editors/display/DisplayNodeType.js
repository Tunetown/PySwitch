/**
 * Implements type specific stuff for DisplayNode
 */
class DisplayNodeType {
   
    handler = null;   // DisplayNode instance

    /**
     * Factory
     */
    static getInstance(handler) {
        switch(handler.node.name) {
            case "DisplayLabel":
                return new DisplayLabelType(handler);
            case "BidirectionalProtocolState": 
                return new BidirectionalProtocolStateType(handler);
            case "TunerDisplay":
                return new TunerDisplayType(handler);
            default:
                return new DisplayNodeType(handler);
        }
    }

    constructor(handler) {
        this.handler = handler;
    }
    
    /**
     * Called to set up the node handler
     */
    async setup() {        
    }

    /**
     * Sets up the preview DOM element
     */
    setupPreviewElement(element) {
    }

    /**
     * Is the node editable?
     */
    editable() {
        return false;
    }

    /**
     * Returns if the node is resizable
     */
    resizable() {
        return false;
    }

    /**
     * Determines the bounds node from the data model.
     */
    getBoundsNode() {
        const ret = Tools.getArgument(this.handler.node, "bounds");
        if (ret) return ret.value;

        if (this.handler.node.arguments.length == 1) {
            if (this.handler.node.arguments[0].value && 
                this.handler.node.arguments[0].value.name == "DisplayBounds") {
                    
                return this.handler.node.arguments[0].value;
            }
        }
        return null;
    }

    /**
     * Returns the display text for the node preview element
     */
    getPreviewText() {
        return this.getName();
    }

    /**
     * Returns the display text for the node (for all others than the preview)
     */
    getName() {
        return this.handler.node.name;  
    }

    /**
     * Background color for preview or null for no specific color is wanted
     */
    getPreviewBackColor() {
        return null;
    }

    /**
     * Text color for preview or null for no specific color is wanted
     */
    getPreviewTextColor() {
        return null;
    }

    /**
     * Gets a data node list for the default arguments of the type.
     */
    getDefaultArguments() {
        return [];
    }

    /**
     * Returns DOM for parameter lists
     */
    async getParameterLists() {
        return [
            new DisplayParameterList(this.handler)
        ]
    }
}