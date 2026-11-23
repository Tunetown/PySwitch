/**
 * Base class for the AM4 example tests: access to the virtual AM4. The general helpers are in ExampleTestBase.
 */
class FractalAM4TestBase extends ExampleTestBase {

    /**
     * The virtual AM4 (the configuration may use further clients)
     */
    get client() {
        return this.runner.runner.clients.fractal_am4;
    }

    /**
     * Loads a preset on the virtual AM4 (like on the device) and waits for PySwitch to follow
     */
    async loadPreset(location, scene = null) {
        this.client.loadPreset(location);
        if (scene !== null) this.client.setScene(scene);
        await this.ticks();
    }

    /**
     * Expects that PySwitch only sent whitelisted messages (the real AM4 might freeze on others)
     */
    expectOnlyWhitelisted() {
        expect(this.client.rejected).withContext("Messages not whitelisted").toEqual([]);
    }
}
