/**
 * Base class for the Fractal example tests: access to the virtual Fractal client, FC colors, presets.
 * The general helpers are in ExampleTestBase.
 */
class FractalTestBase extends ExampleTestBase {

    // FC category colors (see pyswitch.clients.fractal)
    static COLOR_BANK = [255, 125, 0];
    static COLOR_PRESET = [0, 255, 0];
    static COLOR_SCENE = [255, 0, 0];
    static COLOR_EFFECT = [0, 255, 255];
    static COLOR_UTILITY = [0, 0, 255];

    /**
     * The virtual Fractal client (the configuration may use further clients)
     */
    get client() {
        return this.runner.runner.clients.fractal;
    }

    /**
     * Loads a preset on the virtual client (like on the device) and waits for PySwitch to follow
     */
    async loadPreset(preset, scene = null) {
        this.client.presets.loadPreset(preset);
        if (scene !== null) this.client.presets.setScene(scene);
        await this.ticks();
    }
}
