/**
 * Factory for client handlers
 */
class ClientFactory {

    /**
     * Factory for client handlers
     */
    static getInstance(clientId) {
        switch (clientId) {
            case "kemper": return new KemperClient(clientId);
            case "boomerang": return new BoomerangClient(clientId);
            case "fractal": return new FractalClient(clientId);
            case "local": return new Client(clientId);
        }
        return null;
    }

    /**
     * Tries to determine which client a configuration uses the most. Returns a client ID.
     */
    static async estimateClient(config) {
        const data = await config.get();

        if (data.inputs_py.includes("pyswitch.clients.kemper")) {
            return "kemper";
        }

        if (data.inputs_py.includes("pyswitch.clients.boomerang")) {
            return "boomerang";
        }

        if (data.inputs_py.includes("pyswitch.clients.fractal")) {
            return "fractal";
        }

        console.warn("Unknown client type, defaulting to Kemper");
        return "kemper";
    }
}