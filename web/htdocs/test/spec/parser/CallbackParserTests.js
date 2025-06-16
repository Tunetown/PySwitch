class CallbackParserTests extends FunctionParserTestBase {

    async getAvailableDisplayLabelCallbacks() {
        await this.init();
        
        const basePath = "../";
        const that = this;

        async function fromClass(options) {
            const extractor = new ClassItemExtractor(that.pyswitch);
            return await extractor.get(options);
        }                 

        await this.checkDefinitions(
            "callbacks.json",

            // Load from buffer file
            async function() {
                return JSON.parse(await Tools.fetch(basePath + "definitions/callbacks.json"));
            },

            // Generate from scratch
            async function() {
                const extractor = new ClassNamesExtractor(that.pyswitch);
        
                const clients = await Client.getAvailable(basePath);

                const ret = [];
                for (const client of clients) {
                    let classes = await extractor.get({
                        tocPath: basePath + "circuitpy/lib/pyswitch/clients/toc.php",
                        subPath: client.id + "/callbacks",
                        targetPath: "pyswitch/clients/" + client.id + "/callbacks"
                    });

                    // // Add callbacks from __init__.py
                    // if (client.getInitActionsClassName()) {
                    //     actions = actions.concat(await fromClass({
                    //         file: "pyswitch/clients/" + client.id + "/__init__.py",
                    //         importPath: "pyswitch.clients." + client.id,
                    //         className: client.getInitActionsClassName(),
                    //         functions: true
                    //     }))
                    // }

                    ret.push({
                        client: client.id,
                        callbacks: classes
                    })
                }

            //     // Add general actions, not coming from the clients folder
            //     let actionsGeneral = (
            //             await fromClass({
            //                 file: "pyswitch/controller/actions/AnalogAction.py",
            //                 importPath: "pyswitch.controller.actions.AnalogAction",
            //                 className: "AnalogAction",
            //                 includeUnderscore: true,
            //                 functions: true
            //             })
            //         )
            //         .filter((item) => item.name == "AnalogAction");

            //     actionsGeneral = actionsGeneral.concat(
            //         (
            //             await fromClass({
            //                 file: "pyswitch/controller/actions/EncoderAction.py",
            //                 importPath: "pyswitch.controller.actions.EncoderAction",
            //                 className: "EncoderAction",
            //                 includeUnderscore: true,
            //                 functions: true
            //             })
            //         )
            //         .filter((item) => item.name == "EncoderAction"),

            //         (
            //             await fromClass({
            //                 file: "pyswitch/clients/local/actions/pager.py",
            //                 importPath: "pyswitch.clients.local.actions.pager",
            //                 className: "PagerAction",
            //                 includeUnderscore: true,
            //                 functions: true
            //             })
            //         )
            //         .filter((item) => item.name == "PagerAction" || item.name == "PagerAction.proxy")
            //     );

            //     ret.push({
            //         client: "local",
            //         actions: actionsGeneral
            //     })

                return ret;
            }
        )
    }

    /**
     * Check metadata
     */
    // async getAvailableActionsMeta() {
    //     await this.init();
        
    //     const config = new MockConfiguration("", "");
    //     await config.init(this.pyswitch, "../");
    //     const parser = config.parser;
        
    //     const clients = await parser.getAvailableActions();

    //     for(const client of clients) {
    //         for (const action of client.actions) {
    //             expect(action.meta).toBeInstanceOf(FunctionMeta);
                
    //             expect(action.meta.getDisplayName().length).toBeGreaterThan(0)
    //             expect(action.meta.getShortDisplayName().length).toBeGreaterThan(0)

    //             expect(action.meta.data.category.length).toBeGreaterThan(0)
    //             expect(action.meta.data.target.length).toBeGreaterThan(0)
    //         }
    //     }
    // }
}