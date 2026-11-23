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
            case "fractal_am4": return new FractalAM4Client(clientId);
            case "fractal_II": return new FractalIIClient(clientId);
            case "local": return new Client(clientId);
        }
        return null;
    }

    // Clients which can be detected in a configuration, in order of precedence (the first one is the
    // main client, for example for the protocol)
    static #DETECTABLE_CLIENTS = ["kemper", "boomerang", "fractal", "fractal_am4", "fractal_II"];

    /**
     * Determines all clients used by a configuration (imports of pyswitch.clients.<client> in inputs.py or
     * display.py). Returns an array of client IDs (at least one).
     */
    static async estimateClients(config) {
        const data = await config.get();
        const code = data.inputs_py + "\n" + (data.display_py ? data.display_py : "");

        const ret = ClientFactory.#DETECTABLE_CLIENTS.filter(
            (clientId) => (new RegExp("pyswitch\\.clients\\." + clientId + "\\b")).test(code)
        );

        if (ret.length > 0) return ret;

        console.warn("Unknown client type, defaulting to Kemper");
        return ["kemper"];
    }

    /**
     * Returns the client handler of the client whose protocol is used by the configuration (at most one
     * bidirectional protocol per configuration), or the main client if no client has a protocol.
     */
    static async getProtocolClient(config) {
        const clients = (await ClientFactory.estimateClients(config)).map((clientId) => ClientFactory.getInstance(clientId));

        for (const client of clients) {
            if (client.getProtocolCode()) return client;
        }

        return clients[0];
    }
}