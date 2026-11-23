// Default timeout for all specs. Several specs set their own (higher) timeout in beforeEach(), which stays set for 
// the following specs; the order of the specs is random. Pyodide is shared by all test classes and started by the
// first spec using it, so the default must cover the start of Pyodide.
jasmine.DEFAULT_TIMEOUT_INTERVAL = 60000;

class TestBase {

    // One PySwitchRunner (Pyodide) for all test classes, per coverage setting. Starting Pyodide takes several 
    // seconds, so it is not done for each test class. Spec: claude/001 Fractal Support/spec/emulator/integration.md
    static #runners = new Map();

    pyswitch = null;       // PySwitchRunner instance
    configRunner = null;   // Configuration runner

    /**
     * Must be called before any of the tests using pyswitch emulator can be run
     */
    async init(options = {}) {
        if (this.pyswitch) return;

        const coverage = !!options.coverage;

        if (!TestBase.#runners.has(coverage)) {
            const runner = new PySwitchRunner(
                {
                    domNamespace: "pyswitch",
                    updateIntervalMillis: 10,
                    coverage: coverage
                }, 
                "test-pyswitch"
            );

            // Store the promise, so test classes initializing at the same time share the runner, too
            TestBase.#runners.set(coverage, runner.init("../").then(() => runner));
        }

        this.pyswitch = await TestBase.#runners.get(coverage);

        this.runner = new ConfigRunner(this.pyswitch);
    }

    /**
     * Returns the URL parameter of the test page with the passed name, or null
     */
    static getUrlParameter(name) {
        return (new URLSearchParams(window.location.search)).get(name);
    }
}