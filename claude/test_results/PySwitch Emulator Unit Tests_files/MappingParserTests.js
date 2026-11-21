class MappingParserTests extends FunctionParserTestBase {

    async getAvailableMappings() {
        await this.init();
        
        const basePath = "../";
        const that = this;

        async function fromClass(options) {
            const extractor = new ClassItemExtractor(that.pyswitch);
            return await extractor.get(options);
        }   

        await this.checkDefinitions(
            "mappings.json",

            // Load from buffer file
            async function() {
                return JSON.parse(await Tools.fetch(basePath + "definitions/mappings.json"));
            },

            // Generate from scratch
            async function() {
                const extractor = new FunctionExtractor(that.pyswitch);

                const clients = await Client.getAvailable(basePath);

                const ret = [];
                for (const client of clients) {
                    let mappings = await extractor.get({
                        tocPath: basePath + "circuitpy/lib/pyswitch/clients/toc.php",
                        subPath: client.id + "/mappings",
                        targetPath: "pyswitch/clients/" + client.id + "/mappings"
                    })

                    // Add mappings from __init__.py
                    if (client.getInitMappingsClassName()) {
                        mappings = mappings.concat(await fromClass({
                            file: "pyswitch/clients/" + client.id + "/__init__.py",
                            importPath: "pyswitch.clients." + client.id,
                            className: client.getInitMappingsClassName(),
                            functions: true
                        }))
                        .filter((item) => !item.name.startsWith('convert_'))
                    }
                    
                    ret.push({
                        client: client.id,
                        mappings: mappings
                    })
                }
                return ret;
            }
        )
    }
}