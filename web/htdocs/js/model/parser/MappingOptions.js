class MappingOptions {

    /**
     * Generates the mapping list for input
     */
    async generate(parser, addNone = false) {
        async function getMappingVariants(mapping) {
            if (mapping.parameters.length == 0) {
                return [
                    {
                        name: mapping.name + "()",
                        value: mapping.name + "()"
                    }
                ]
            }

            // We only resolve the first parameter here (mappings never have more)
            const param = mapping.parameters[0];

            function addValues(values) {
                for(const value of values) {
                    const argStr = (mapping.parameters.length > 1) ? (param.name + " = ") : "";

                    ret.push({
                        name: mapping.name + "(" + argStr + value.value + ")",
                        value: mapping.name + "(" + argStr + value.value + ")"
                    });
                }
            }

            const ret = [];
            if (param.meta && param.meta.range()) {
                const values = await param.meta.range().getValues();
                addValues(values);

            } else if (param.meta && param.meta.data.values) {
                addValues(param.meta.data.values);
                
            } else {
                throw new Error("No parameter values for parameter " + param.name + " of mapping " + mapping.name + " found in meta.json")
            }
            return ret;
        }

        const clients = await parser.getAvailableMappings();

        let ret = addNone ? [
             {
                name: "None",
                value: "None"
            }
        ] : [];

        for (const client of clients) {
            for(const mapping of client.mappings) {
                ret = ret.concat(await getMappingVariants(mapping))
            }
        }

        return ret.sort((a, b) => (a.name > b.name) ? 1 : -1);
    }
}