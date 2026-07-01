class ExampleTestRunner extends TestBase {

    client = null;
    hardware = null;

    #examplesPath = null;
    
    constructor(path) {
        super();
        this.#examplesPath = path;
    }

    /**
     * Process the tests. This loads a TOC of all tests and executes one after another, 
     * with behavioural mocks testing the functionality.
     */
    async process() {
        await this.init({
            coverage: true
        });

        // Test all examples
        await this.#testExamples();

        // Show a basic coverage report in the console
        await this.coverage();        
    }

    /**
     * Show a coverage report in the console
     */
    async coverage() {
        const cov = (await this.pyswitch.pyodide.runPython(`
            import coverage
            coverage.Coverage()
        `));
        
        cov.load();
        cov.report();
    }

    /**
     * Scans examples using the popup classes, and tests each one of the callable ones
     */
    async #testExamples() {
        const toc = await (new ExamplesProvider(null, this.#examplesPath + "/toc.php")).getToc();
        
        const that = this;
        async function crawl(entry) {
            if (entry.isCallable()) {
                await that.#testExample(entry);
                return;
            }

            for (const child of entry.children || []) {
                await crawl(child);
            }
        }

        await crawl(toc);
    }

    /**
     * Tests one BrowserEntry which contains an example
     */
    async #testExample(entry) {
        if (!entry.data.callPath) {
            console.warn("Skip example without callPath: ", entry);
            return;
        };

        // console.log("Testing example " + entry.data.callPath)

        const config = new WebConfiguration(new MockController(), this.#examplesPath + entry.data.callPath);
        
        const that = this;        
        await this.runner.run(config, async function() {
            // Do some further initial ticks to get the bidirectional protocol connected
            let i = 0;
            while(i++ < 100) {
                await that.runner.tick();
            }

            // Check if there is a test script. If so, execute it.
            function getTestScript() {
                for(const file of entry.data.toc ? entry.data.toc.children : []) {
                    if (file.name == ".test.js") {
                        return that.#examplesPath + entry.data.callPath + "/" + file.name;
                    }                    
                }
                return null;
            }

            const testScriptUrl = getTestScript();

            await new Promise(r => setTimeout(r, 5));  // Some break to make the canvas visible

            if (testScriptUrl) {
                await that.#runExampleTest(config, await Tools.fetch(testScriptUrl));
            }
        });

        expect(1).toBe(1);
    }

    /**
     * Performs each example's test case (eval)
     */
    async #runExampleTest(config, testScript) {
        // Get hardware info first
        await config.init(this.pyswitch);
        const parser = config.parser;
        this.hardware = await parser.getHardwareInfo();

        // Get the testing function and run it
        const test = eval(testScript);
        await test(this);
    }

    // Functions to be used by the test scripts ///////////////////////////////////////////////////////////////////////

    /**
     * Returns a hardware mapping by name. Only usable after (or during) #runExampleTest has been called
     */
    mapping(mappingName) {
        for(const input of this.hardware) {
            if (input.name == mappingName) {
                return input;
            }
        }
        throw new Error("Mapping for input " + mappingName + " not found");
    }

    /**
     * Sets the rig ID incl. a tick afterwards.
     */
    async setRigId(id) {
        this.runner.client.setRigId(id);
        await this.runner.tick();
    }

    /**
     * Simulates that a switch is pushed and released again, with ticks in between.
     */
    async simulateSwitchPress(input, holdTime = 100) {
        await this.runner.tick();
        
        this.setSwitch(input, true);
        await this.runner.tick(holdTime);

        this.setSwitch(input, false);
        await this.runner.tick();
    }

    /**
     * Sets a switches state
     */
    setSwitch(input, pushed) {
        const inputElement = this.#getInputElement(input);
        inputElement[0].dataset.pushed = pushed ? "true" : null;
    }

    /**
     * Gets a switch state
     */
    switchPushed(input) {
        const inputElement = this.#getInputElement(input);
        return inputElement[0].dataset.pushed == "true";
    }    

    /**
     * Gets the color of a switch. If the switch has multiple colors, this 
     * will throw. Use getSwitchColors() instead for those.
     */
    getSwitchColor(input) {
        const ledElements = this.#getLedElements(input);

        let color = null;
        for(const ledElement of ledElements) {
            const rgb = JSON.parse(ledElement[0].dataset.color);
            
            if (color === null) {
                color = rgb;
            } else {
                if (!Tools.compareArrays(color, rgb)) throw new Error("Switch has multiple colors, but is expected to only have one");
            }            
        }

        return color;
    }

    /**
     * Returns the display color at the given pixel. position must be an array with [x, y]
     */
    getDisplayColorAt(position) {
        const canvas = $("#pyswitch-display");
        if (!canvas) throw new Error("Display not found");

        const ctx = canvas[0].getContext('2d');
        const p = ctx.getImageData(position[0], position[1], 1, 1).data; 
        
        return [p[0], p[1], p[2]];
    }

    /**
     * Returns the switch element for a switch ID as defined in the mappings.
     */
    #getInputElement(input) {
        const port = input.data.model.port;
        const inputElement = $("#pyswitch-switch-gp" + port);
        if (inputElement.attr('id') != "pyswitch-switch-gp" + port) throw new Error("Switch " + port + " not found");
        return inputElement;
    }

    /**
     * Returns the LED element for a pixel ID as defined in the mappings.
     */
    #getLedElements(input) {
        const ret = [];
        for (const led of input.data.pixels) {
            const ledElement = $("#pyswitch-led-" + led);
            if (ledElement.attr('id') != "pyswitch-led-" + led) throw new Error("LED " + led + " not found");
            ret.push(ledElement);
        }
        return ret;
    }
}