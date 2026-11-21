class TestBase {

    pyswitch = null;       // PySwitchRunner instance
    configRunner = null;   // Configuration runner

    /**
     * Must be called before any of the tests using pyswitch emulator can be run
     */
    async init(options = {}) {
        if (this.pyswitch) return;

        this.pyswitch = new PySwitchRunner(
            {
                domNamespace: "pyswitch",
                updateIntervalMillis: 10,
                coverage: !!options.coverage
            }, 
            "test-pyswitch"
        );

        await this.pyswitch.init("../");

        this.runner = new ConfigRunner(this.pyswitch);
    }
}