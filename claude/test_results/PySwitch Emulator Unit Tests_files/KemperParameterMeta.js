class KemperParameterMeta extends ParameterMeta {
    
    /**
     * Returns the display name for the parameter
     */
    getDisplayName() {
        switch (this.parameter.name) {
            case "process_overridden_actions": return "Process Actions";
        }

        return super.getDisplayName();
    }
}