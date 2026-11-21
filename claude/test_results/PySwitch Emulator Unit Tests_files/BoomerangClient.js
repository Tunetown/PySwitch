/**
 * Client implementation for the Boomerang III Phrase Sampler
 */
class BoomerangClient extends Client {
    
    /**
     * Factory for FunctionMeta instances
     */
    async createFunctionMeta(parser, meta, funcDef) {
        return new BoomerangFunctionMeta(parser, this, meta, funcDef);
    }
    
    /**
     * Returns a display name for the client
     */
    getDisplayName() {
        return "Boomerang";
    }

    /**
     * Sort string among all clients available
     */
    getSortString() {
        return "YYY_" + this.id;
    }
}