class KeycodeParserTests extends FunctionParserTestBase {

    async getAvailableKeycodes() {
        await this.init();
        
        const basePath = "../";
        const that = this;

        async function fromClass(options) {
            const extractor = new ClassItemExtractor(that.pyswitch);
            return await extractor.get(options);
        }                 

        await this.checkDefinitions(
            "keycodes.json",

            // Load from buffer file
            async function() {
                return JSON.parse(await Tools.fetch(basePath + "definitions/keycodes.json"));
            },

            // Generate from scratch
            async function() {
                const keycodes = await fromClass({
                    file: "adafruit_hid/keycode.py",
                    className: "Keycode",
                    attributes: true
                })                  

                return keycodes;
            }
        )
    }
}