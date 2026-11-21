/**
 * Metadata for functions (Boomerang overrides)
 */
class BoomerangFunctionMeta extends FunctionMeta {

    /**
     * Returns the display name for specific actions
     */
    getShortDisplayName(actionCallProxy = null) {
        return super.getShortDisplayName(actionCallProxy)
            .replace("Boomerang ", "");
    }   
}