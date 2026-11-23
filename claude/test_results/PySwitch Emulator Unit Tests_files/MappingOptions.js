class MappingOptions {

    // Number of values offered for parameters with too many values (ranges without a value list)
    static #NUM_VALUES_LARGE_RANGE = 10;

    /**
     * Generates the mapping list for input. Mappings with the same name in several clients are distinguished by
     * the client: the value uses the qualified name <CLIENT>_<NAME> (see claude/spec/emulator/parser.md), the 
     * name shows the client.
     */
    async generate(parser, addNone = false) {
        const clients = await parser.getAvailableMappings();

        // Number of clients per mapping name
        const numClients = new Map();
        for (const client of clients) {
            for (const mapping of client.mappings) {
                numClients.set(mapping.name, (numClients.get(mapping.name) || 0) + 1);
            }
        }

        async function getMappingVariants(mapping, clientId) {
            const ambiguous = (numClients.get(mapping.name) > 1) && !mapping.name.includes(".");
            const codeName = ambiguous ? (clientId.toUpperCase() + "_" + mapping.name) : mapping.name;
            const displaySuffix = ambiguous ? (" (" + ClientFactory.getInstance(clientId).getDisplayName() + ")") : "";

            if (mapping.parameters.length == 0) {
                return [
                    {
                        name: mapping.name + "()" + displaySuffix,
                        value: codeName + "()"
                    }
                ]
            }

            // We only resolve the first parameter here
            const param = mapping.parameters[0];

            function addValues(values) {
                for(const value of values) {
                    const argStr = param.name + " = " + value.value

                    ret.push({
                        name: mapping.name + "(" + argStr + ")" + displaySuffix,
                        value: codeName + "(" + argStr + ")"
                    });
                }
            }

            const ret = [];
            if (param.meta && param.meta.range()) {
                const range = param.meta.range();
                const values = await range.getValues();

                // Too many values: only the first ones are offered (all others can be entered in the code)
                addValues(values ? values : (await MappingOptions.#getFirstValues(range)));

            } else if (param.meta && param.meta.data.values) {
                addValues(param.meta.data.values);
                
            } else {
                throw new Error("No parameter values for parameter " + param.name + " of mapping " + mapping.name + " found in meta.json (client " + param.meta?.client + ")")
            }

            return ret;
        }

        let ret = addNone ? [
             {
                name: "None",
                value: "None"
            }
        ] : [];

        for (const client of clients) {
            for(const mapping of client.mappings) {
                const vars = await getMappingVariants(mapping, client.client);
                
                ret = ret.concat(vars)
            }
        }

        return ret.sort((a, b) => (a.name > b.name) ? 1 : -1);
    }

    /**
     * Returns the first values of a range (for ranges with too many values)
     */
    static async #getFirstValues(range) {
        const min = parseInt(await range.min());
        const max = parseInt(await range.max());

        const ret = [];
        for (let i = min; i <= max && ret.length < MappingOptions.#NUM_VALUES_LARGE_RANGE; ++i) {
            ret.push({
                name: "" + i,
                value: i
            });
        }
        return ret;
    }
}