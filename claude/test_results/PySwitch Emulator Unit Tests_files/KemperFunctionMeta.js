/**
 * Metadata for functions (kemper overrides)
 */
class KemperFunctionMeta extends FunctionMeta {

    /**
     * Returns the display name for specific actions
     */
    getDisplayName(actionCallProxy = null) {
        switch (this.functionDefinition.name) {
            case "RIG_SELECT_AND_MORPH_STATE": return this.client.getDisplayName() + ": " + this.#getDisplayNameRigSelectAndMorphState(actionCallProxy);
            case "LOOPER_REC_PLAY_OVERDUB": return this.client.getDisplayName() + ": " + super.getShortDisplayName(actionCallProxy);
        }

        return this.client.getDisplayName() + ": " + this.getShortDisplayName(actionCallProxy);
    }

    /**
     * Returns the display name for specific actions
     */
    getShortDisplayName(actionCallProxy = null) {
        switch (this.functionDefinition.name) {
            case "RIG_SELECT": return this.#getDisplayNameRigSelect(actionCallProxy);
            case "RIG_SELECT_AND_MORPH_STATE": return this.#getDisplayNameRigSelectAndMorphStateShort(actionCallProxy);
            case "BANK_SELECT": return this.#getDisplayNameBankSelect(actionCallProxy);
            case "EFFECT_BUTTON": return this.#getDisplayNameEffectButton(actionCallProxy);
            case "EFFECT_STATE": return this.#getDisplayNameEffectState(actionCallProxy);
            case "EFFECT_STATE_EXT": return this.#getDisplayNameEffectStateExt(actionCallProxy);
            case "FIXED_EFFECT_STATE": return this.#getDisplayNameFixedEffectState(actionCallProxy);
            case "LOOPER_REC_PLAY_OVERDUB": return "Looper Rec|Play|OD";
            case "ENCODER_BPM": return "Tempo (BPM)";
            case "ENCODER_RIG_TRANSPOSE": return "Rig Transpose";
            case "ENCODER_BANK_SELECT": return "Bank Select";
        }

        return super.getShortDisplayName(actionCallProxy);
    }

    /**
     * Returns a sort string for the passed action definition
     */
    async getSortString() {
        const category = this.functionDefinition.meta.getCategory();
        
        switch (category) {
            case "rig": return "a" + this.functionDefinition.meta.getDisplayName();
            case "bank": return "b" + this.functionDefinition.meta.getDisplayName();
            case "effects": return "e";
            case "tuner": return "f";
            case "none": return "m";
            case "looper": return "w";
        }    
            
        return category;
    }

    ///////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Special implementation for rig select
     */
    #getDisplayNameRigSelect(actionCallProxy = null) {
        const rig = this.getArgument(actionCallProxy, "rig");
        const rig_off = this.getArgument(actionCallProxy, "rig_off");
        
        if (actionCallProxy && !(rig_off == null || rig_off.value == "None")) {
            return this.#replaceParameterTokens(actionCallProxy, "Toggle Rigs {rig}/{rig_off}");
        }
        else if (actionCallProxy && !(rig == null || rig.value != "None")) {
            return "Select Current Rig";
        }

        if (!actionCallProxy) {
            return "Select Rig";  
        }

        return this.#replaceParameterTokens(actionCallProxy, "Select Rig {rig}");
    }

    /**
     * Special implementation for rig select and morph state
     */
    #getDisplayNameRigSelectAndMorphState(actionCallProxy = null) {
        const rig_off = this.getArgument(actionCallProxy, "rig_off");

        if (actionCallProxy && !(rig_off == null || rig_off.value == "None")) {
            return this.#replaceParameterTokens(actionCallProxy, "Toggle Rigs {rig}/{rig_off} & Morph Display");
        }

        if (!actionCallProxy) {
            return "Select Rig & Morph Display";  
        }

        return this.#replaceParameterTokens(actionCallProxy, "Select Rig {rig} & Morph Display");
    }

    /**
     * Special implementation for rig select and morph state (short version)
     */
    #getDisplayNameRigSelectAndMorphStateShort(actionCallProxy = null) {
        const rig_off = this.getArgument(actionCallProxy, "rig_off");
        
        if (actionCallProxy && !(rig_off == null || rig_off.value == "None")) {
            return this.#replaceParameterTokens(actionCallProxy, "Rigs {rig}/{rig_off} & Morph");
        }

        if (!actionCallProxy) {
            return "Rig & Morph";
        }

        return this.#replaceParameterTokens(actionCallProxy, "Rig {rig} & Morph");
    }

    /**
     * Special implementation for bank select
     */
    #getDisplayNameBankSelect(actionCallProxy = null) {
        const bank_off = this.getArgument(actionCallProxy, "bank_off");
        const preselect = this.getArgument(actionCallProxy, "preselect");
        
        if (!actionCallProxy) {
            return "Select Bank";  
        }

        if (!(bank_off == null || bank_off.value == "None")) {
            return this.#replaceParameterTokens(actionCallProxy, "Toggle Banks {bank}/{bank_off}");
        }

        if (preselect && (preselect.value == "True")) {
            return this.#replaceParameterTokens(actionCallProxy, "Preselect Bank {bank}");
        }

        return this.#replaceParameterTokens(actionCallProxy, "Select Bank {bank}");
    }

    /**
     * Special implementation for effect buttons
     */
    #getDisplayNameEffectButton(actionCallProxy = null) {
        const num = this.getArgument(actionCallProxy, "num");
        if (actionCallProxy && num) {
            return this.#replaceParameterTokens(actionCallProxy, "Effect Button {num}");
        }

        return "Effect Button";
    }

    /**
     * Special implementation for effect state
     */
    #getDisplayNameEffectState(actionCallProxy = null) {
        const slot_id = this.getArgument(actionCallProxy, "slot_id");
        if (actionCallProxy && slot_id) {
            function getSlotName(id) {
                switch (id) {
                    case "KemperEffectSlot.EFFECT_SLOT_ID_A": return "A";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_B": return "B";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_C": return "C";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_D": return "D";

                    case "KemperEffectSlot.EFFECT_SLOT_ID_X": return "X";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_MOD": return "MOD";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_DLY": return "DLY";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_REV": return "REV";

                    case "KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL": return "DLY";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL": return "REV";
                }
                return "?";
            }

            return "Effect State " + getSlotName(slot_id.value);
        }

        return "Effect State";
    }

    /**
     * Special implementation for effect state (fixed fx)
     */
    #getDisplayNameFixedEffectState(actionCallProxy = null) {
        const slot_id = this.getArgument(actionCallProxy, "slot");
        if (actionCallProxy && slot_id) {
            switch (slot_id.value) {
                case "FIXED_SLOT_ID_TRANSPOSE": return "Transpose";
                case "FIXED_SLOT_ID_GATE": return "Gate (fixed)";
                case "FIXED_SLOT_ID_COMP": return "Compressor (fixed)";
                case "FIXED_SLOT_ID_BOOST": return "Booster (fixed)";
                case "FIXED_SLOT_ID_WAH": return "Wah (fixed)";
                case "FIXED_SLOT_ID_CHORUS": return "Chorus (fixed)";

                case "FIXED_SLOT_ID_AIR": return "Air Chorus (fixed)";
                case "FIXED_SLOT_ID_DBL_TRACKER": return "Doubler (fixed)";
            }
        }

        return "Fixed Effect State";
    }

    /**
     * Special implementation for effect state
     */
    #getDisplayNameEffectStateExt(actionCallProxy = null) {
        const slot_id = this.getArgument(actionCallProxy, "slot_id");
        if (actionCallProxy && slot_id) {
            function getSlotName(id) {
                switch (id) {
                    case "KemperEffectSlot.EFFECT_SLOT_ID_A": return "A";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_B": return "B";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_C": return "C";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_D": return "D";

                    case "KemperEffectSlot.EFFECT_SLOT_ID_X": return "X";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_MOD": return "MOD";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_DLY": return "DLY";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_REV": return "REV";

                    case "KemperEffectSlot.EFFECT_SLOT_ID_DLY_NO_SPILL": return "DLY";
                    case "KemperEffectSlot.EFFECT_SLOT_ID_REV_NO_SPILL": return "REV";
                }
                return "?";
            }

            return "Effect State " + getSlotName(slot_id.value);
        }

        return "Effect State (Ext.)";
    }

    /////////////////////////////////////////////////////////////////////////////////////////////////

    /**
     * Replaces all tokens for parameters
     */
    #replaceParameterTokens(actionCallProxy = null, str) {
        function getReplaceValue(param) {
            for (const def of (actionCallProxy ? actionCallProxy.arguments() : [])) {
                if (def.name == param.name) {
                    return def.value;
                }
            }

            return param.meta.getDefaultValue();
        }

        function replaceToken(str, token, value) {
            return str.replace("{" + token + "}", "" + value);
        }

        for (const param of this.functionDefinition.parameters) {
            str = replaceToken(str, param.name, getReplaceValue(param))
        }

        return str;
    }
}