class CallbackParserTests extends FunctionParserTestBase {

    async getAvailableDisplayLabelCallbacks() {
        await this.init();
        
        const basePath = "../";
        const that = this;

        const clients = await Client.getAvailable(basePath);

        function hasParentClass(cls, name) {
            return cls.extends.filter((item) => (item == name)).length > 0;
        }

        function hasMethod(cls, items, name) {
            return items.filter((item) => (item.name == cls.name + "." + name)).length > 0;
        }

        function determineTarget(cls, items) {
            // Some parents are known directly
            if (hasParentClass(cls, "ParameterDisplayCallback")) return "DisplayLabel";

            // Splashes root
            if (hasMethod(cls, items, "get_root")) return "Splashes";

            // DisplayLabel callback
            if (hasMethod(cls, items, "update_label")) return "DisplayLabel";

            // No known callback
            return null;
        }
        
        async function loadClasses(classes, init = false) {
            const itemExtractor = new ClassItemExtractor(that.pyswitch);        
        
            const ret = [];
            for (const cls of classes) {
                const items = await itemExtractor.get({
                    file: cls.importPath.replaceAll('.', '/') + (init ? "/__init__" : "") + ".py",
                    className: cls.name,
                    importPath: cls.importPath,
                    functions: true,
                    includeUnderscore: true
                });

                const target = determineTarget(cls, items);
                if (!target) continue;

                for (const item of items) {
                    if (item.name != cls.name) continue;  // __init__

                    cls.parameters = item.parameters;
                    cls.target = target;

                    ret.push(cls);
                    break;
                }
            }
            return ret;
        }

        async function getFolderCallbacks(client) {
            const extractor = new ClassNamesExtractor(that.pyswitch);
            
            const classes = await extractor.get({
                tocPath: basePath + "circuitpy/lib/pyswitch/clients/toc.php",
                subPath: client.id + "/callbacks",
                targetPath: "pyswitch/clients/" + client.id + "/callbacks"
            });

            return loadClasses(classes, false);
        }

        async function getInitCallbacks(client) {
            const extractor = new ClassNameExtractor(that.pyswitch);

            const classes = await extractor.get({
                file: "pyswitch/clients/" + client.id + "/__init__.py",
                importPath: "pyswitch.clients." + client.id,
                includeUnderscore: false
            });

            return loadClasses(classes, true);
        }

        await this.checkDefinitions(
            "callbacks.json",

            // Load from buffer file
            async function() {
                return JSON.parse(await Tools.fetch(basePath + "definitions/callbacks.json"));
            },

            // Generate from scratch
            async function() {
                const ret = [];
                for (const client of clients) {
                    ret.push({
                        client: client.id,
                        callbacks: [].concat(
                            await getFolderCallbacks(client),
                            await getInitCallbacks(client)
                        )
                    })
                }

                return ret;
            }
        )
    }
}