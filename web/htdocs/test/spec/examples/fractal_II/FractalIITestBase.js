/**
 * Base class for the Axe-Fx II example tests: access to the virtual Axe-Fx II. The general helpers are in ExampleTestBase.
 */
class FractalIITestBase extends ExampleTestBase {

    /**
     * The virtual Axe-Fx II (the configuration may use further clients)
     */
    get client() {
        return this.runner.runner.clients.fractal_II;
    }

    /**
     * Loads a preset on the virtual Axe-Fx II (like on the device) and waits for PySwitch to follow
     */
    async loadPreset(preset, scene = null) {
        this.client.loadPreset(preset, scene);
        await this.ticks();
    }

    /**
     * Expects that PySwitch only sent messages of the spec
     */
    expectOnlyWhitelisted() {
        expect(this.client.rejected).withContext("Messages not in the spec").toEqual([]);
    }
}
