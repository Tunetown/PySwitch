/**
 * Metadata for functions
 */
class FunctionMeta {

    data = null;                   // Function metadata
    functionDefinition = null;     // Function descriptor
    client = null;

    constructor(parser, client, meta, functionDefinition) {
        this.client = client;
        this.data = meta || {};
        this.functionDefinition = functionDefinition;
    }   

    getCategory() {
        return this.data.category ? this.data.category : "none";
    }

    /**
     * Returns the display name for specific actions. If an action call proxy is passed, the 
     * argument values can be used to show more specific names.
     */
    getDisplayName(actionCallProxy = null) {
        switch (this.functionDefinition.name) {
            case "HID_KEYBOARD": return this.#getDisplayNameHidKeyboard(actionCallProxy);
        }
        return ((this.client.id != "local") ? (this.client.getDisplayName() + ": ") : "") + this.getShortDisplayName(actionCallProxy);
    }

    /**
     * Returns the display name for specific actions. If an action call proxy is passed, the 
     * argument values can be used to show more specific names.
     */
    getShortDisplayName(actionCallProxy = null) {
        switch (this.functionDefinition.name) {
            case "PagerAction": return this.#getDisplayNamePager(actionCallProxy);
            case "PagerAction.proxy": return this.#getDisplayNamePagerProxy(actionCallProxy);
            case "AnalogAction": return this.#getDisplayNameAnalogAction(actionCallProxy);
            case "EncoderAction": return this.#getDisplayNameEncoderAction(actionCallProxy);
            case "BINARY_SWITCH": return this.#getDisplayNameBinarySwitch(actionCallProxy);
            case "HID_KEYBOARD": return this.#getDisplayNameHidKeyboardShort(actionCallProxy);
            case "ENCODER_BUTTON": return this.#getDisplayNameEncoderButtonShort(actionCallProxy);
            case "PARAMETER_UP_DOWN": return this.#getDisplayNameChangeParam(actionCallProxy);
            case "CUSTOM_MESSAGE": return this.#getDisplayNameCustomMessage(actionCallProxy);
            case "ROTATING_MESSAGES": return this.#getDisplayNameRotatingMessage(actionCallProxy);            
        }
        return this.underscoreToDisplayName(this.functionDefinition.name);
    }

    /**
     * Returns a sort string for the action definition
     */
    async getSortString() {
        if (this.functionDefinition.name.startsWith("PagerAction")) return "ZZZZZ_900_" + this.functionDefinition.name;

        if (this.functionDefinition.name == "BINARY_SWITCH")        return "ZZZZZ_010";
        if (this.functionDefinition.name == "EncoderAction")        return "ZZZZZ_010";
        if (this.functionDefinition.name == "AnalogAction")         return "ZZZZZ_010";

        if (this.functionDefinition.name == "PARAMETER_UP_DOWN")    return "ZZZZZ_020";
        if (this.functionDefinition.name == "HID_KEYBOARD")         return "ZZZZZ_040";
        if (this.functionDefinition.name == "ENCODER_BUTTON")       return "ZZZZZ_050";
        if (this.functionDefinition.name == "CUSTOM_MESSAGE")       return "ZZZZZ_100";
        if (this.functionDefinition.name == "ROTATING_MESSAGES")    return "ZZZZZ_110";
        
        return this.functionDefinition.name;
    }

    /**
     * Converts underscore names to more readable ones
     */
     underscoreToDisplayName(str) {
        const splt = str.split("_");
        return splt.map((token) => token.charAt(0).toUpperCase() + token.substring(1).toLowerCase()).join(" ");
    }

    /**
     * Special implementation for AnalogAction
     */
    #getDisplayNameAnalogAction(actionCallProxy = null) {
        if (!actionCallProxy) return "Other Parameter";
        
        const mapping = this.getArgument(actionCallProxy, "mapping");

        if (!(mapping == null || mapping.value == "None")) {
            return this.underscoreToDisplayName(
                mapping.value
                .replaceAll("MAPPING_", "")
                .replaceAll("KemperMappings.", "")
                .replaceAll(/\((.+?)*\)/g, "")
            );
        }

        return "Other Parameter";
    }

    /**
     * Special implementation for PagerAction
     */
    #getDisplayNamePager(actionCallProxy = null) {
        if (!actionCallProxy) return "Pager";
        
        const select_page = this.getArgument(actionCallProxy, "select_page");

        if (!(select_page == null || select_page.value == "None")) {
            return "Select " + actionCallProxy.assign + "|" + select_page.value;
        }

        return "Rotate " + actionCallProxy.assign;
    }   

    

    /**
     * Special implementation for PagerAction.proxy
     */
    #getDisplayNamePagerProxy(actionCallProxy = null) {
        if (!actionCallProxy) return "Select Page";
        
        const page_id = this.getArgument(actionCallProxy, "page_id");
        const pager = this.#extractPager(actionCallProxy.name);

        if (!(page_id == null || page_id.value == "None")) {
            return "Select " + pager + "|" + page_id.value;
        }

        return "Select Page";
    }   

    /**
     * Extracts the pager name from _pager.xxx
     */
    #extractPager(name) {
        const splt = name.split(".");
        if (!splt.length == 2) return null;

        return splt[0];
    }

    #stripMappingName(mapping) {
        return this.underscoreToDisplayName(
            mapping.value
            .replace("MAPPING_", "")
            .replace("KemperMappings.", "")
            .replace(/\((.+?)*\)/g, "")
        );
    }

    /**
     * Special implementation for EncoderAction
     */
    #getDisplayNameEncoderAction(actionCallProxy = null) {
        if (!actionCallProxy) return "Other Parameter";
        
        const mapping = this.getArgument(actionCallProxy, "mapping");

        if (!(mapping == null || mapping.value == "None")) {
            return this.#stripMappingName(mapping)
        }

        return "Other Parameter";
    }

    /**
     * Special implementation for Binary Switch action
     */
    #getDisplayNameBinarySwitch(actionCallProxy = null) {
        if (!actionCallProxy) return "Other Parameter (w.FB)";

        const mapping = this.getArgument(actionCallProxy, "mapping");

        if (!(mapping == null || mapping.value == "None")) {
            return this.#stripMappingName(mapping)
        }

        return "Other Parameter (w.FB)";
    }

    #getDisplayNameChangeParam(actionCallProxy = null) {
        if (!actionCallProxy) return "Parameter Up/Down";

        const mapping = this.getArgument(actionCallProxy, "mapping");
        const offset = this.getArgument(actionCallProxy, "offset");

        if (!(mapping == null || mapping.value == "None")) {
            if (!(offset == null || offset.value == "None")) {
                const offsetInt = parseInt(offset.value)
                return this.#stripMappingName(mapping) + ((offsetInt > 0) ? " Up": " Down");
            } else {
                return this.#stripMappingName(mapping);
            }            
        }

        return "Parameter Up/Down";
    }

    #getDisplayNameCustomMessage(actionCallProxy = null) {
        const text = this.getArgument(actionCallProxy, "text");
        if (!(text == null || text.value == "None" || text.value == "''")) {
            return Tools.stripQuotes(text.value);
        }

        return "Custom MIDI Message";
    }

    #getDisplayNameRotatingMessage(actionCallProxy = null) {
        return "Rotating MIDI Messages";
    }

    #getDisplayNameHidKeyboard(actionCallProxy = null) {
        if (!actionCallProxy) return "USB Keyboard (HID)";

        const keycodes = this.getArgument(actionCallProxy, "keycodes");

        if (!(keycodes == null || keycodes.value == "None")) {
            return "USB Key " + this.#formatKeycodes(keycodes.value)
        }

        return "USB Keyboard (HID)";
    }

    #getDisplayNameHidKeyboardShort(actionCallProxy = null) {
        if (!actionCallProxy) return "USB Key";

        const keycodes = this.getArgument(actionCallProxy, "keycodes");

        if (!(keycodes == null || keycodes.value == "None")) {
            return "USB Key " + this.#formatKeycodes(keycodes.value)
                
        }

        return "USB Key";
    }

    #getDisplayNameEncoderButtonShort(actionCallProxy = null) {
        return "Encoder Button";
    }

    #formatKeycodes(codes) {
        return codes.replaceAll("Keycode.", "")
            .replaceAll("[", "")
            .replaceAll("]", "")
            .replaceAll("(", "")
            .replaceAll(")", "")
    }

    /**
     * Gets the name of a argument in the given definition
     */
    getArgument(actionCallProxy = null, name) {
        if (!actionCallProxy) return null;
        
        const args = actionCallProxy.arguments();
        
        for (const arg of args) {
            if (arg.name == name) return arg;
        }
        return null;
    }
}