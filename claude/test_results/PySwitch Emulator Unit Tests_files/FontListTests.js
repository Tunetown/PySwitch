class FontListTests extends FunctionParserTestBase {

    async getAvailableFonts() {
        await this.init();
        
        const basePath = "../";

        const that = this;
        await this.checkDefinitions(
            "fonts.json",

            // Load from buffer file
            async function() {
                return JSON.parse(await Tools.fetch(basePath + "definitions/fonts.json"));
            },

            // Generate from scratch
            async function() {
                const fonts = JSON.parse(await Tools.fetch(basePath + "circuitpy/fonts/toc.php"))                
                return that.#convert(fonts);
            }
        )
    }

    /**
     * Convert TOC to the (flat) fonts list
     */
    #convert(fonts) {
        const ret = [];
        
        function crawl(node, prefix) {
            switch (node.type) {
                case 'file':
                    if (node.name.toLowerCase().endsWith('.pcf')) {
                        ret.push(prefix + node.name)
                    }
                    break;

                case 'dir':
                    for (const child of node.children) {
                        crawl(child, prefix + node.name + "/");
                    }
                    break;
            }
        }

        crawl(fonts, "/fonts");

        ret.sort();

        return ret;
    }
}