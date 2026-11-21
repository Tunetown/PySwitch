class ConfigRunner {
    
    pyswitch = null;
    timeMillis = 0;
    client = null;
    frontend = null;

    constructor(pyswitch) {
        this.pyswitch = pyswitch;        
    }

    /**
     * Runs the config in PySwitch. 
     * 
     * async performTestsCallback() => void
     */
    async run(config, performTestsCallback = null) {
        this.client = null;

        // Create a temporary container element for pyswitch
        const el = $('<div id="test-pyswitch-example" />').hide();
        $('body').append(el);

        const globals = $('<span />').hide();
        $('body').append(globals);

        // Set up frontend
        this.frontend = new PySwitchFrontend(null, el, { 
            domNamespace: "pyswitch",
            globalContainer: globals
        });
        await config.init(this.pyswitch, "../");
        await this.frontend.apply(config.parser);

        // Reset virtual simulation time
        this.timeMillis = 0;

        // Set up virtual client
        const that = this;
        const clientId = await ClientFactory.estimateClient(config);
        const client = ClientFactory.getInstance(clientId);
        
        this.client = await client.getVirtualClient({
            overrideTimeCallback: function() {
                return that.timeMillis;
            }
        });

        // Set client as MIDI wrapper to connect it to PySwitch
        this.pyswitch.setMidiWrapper(this.client);
        
        // Override current time
        this.pyswitch.setTimeCallback(function() {
            return that.timeMillis / 1000;
        });

        // Run without ticking
        await this.pyswitch.run(config, true);

        // Do the tests
        if (performTestsCallback) {
            await performTestsCallback();
        } else {
            // Do some few initial ticks to check everything is up and running
            let i = 0;
            while(i++ < 5) {
                await this.tick();
            }
        }    

        // Remove the test element from the body again
        el.remove();
        globals.remove();
    }

    /**
     * Execute one tick for a given amount of milliseconds (default is one second).
     */
    async tick(stepMillis = 100) {
        this.timeMillis += stepMillis;

        await this.pyswitch.tick();

        if (this.client) {
            await this.client.update();
        }
    }
}