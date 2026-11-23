/**
 * Base class for the Fractal example tests. Provides access to the virtual Fractal client, switch LEDs
 * and the label texts of the running PySwitch instance.
 */
class FractalTestBase {

    // Default LED brightness values (config.py defaults)
    static BRIGHT = 0.3;
    static DIM = 0.02;

    // FC category colors (see pyswitch.clients.fractal)
    static COLOR_BANK = [255, 125, 0];
    static COLOR_PRESET = [0, 255, 0];
    static COLOR_SCENE = [255, 0, 0];
    static COLOR_EFFECT = [0, 255, 255];
    static COLOR_UTILITY = [0, 0, 255];

    runner = null;

    constructor(runner) {
        this.runner = runner;
    }

    /**
     * The virtual Fractal client (the configuration may use further clients)
     */
    get client() {
        return this.runner.runner.clients.fractal;
    }

    /**
     * Returns the hardware input for a mapping name (for example PA_MIDICAPTAIN_10_SWITCH_1)
     */
    input(name) {
        return this.runner.mapping(name);
    }

    /**
     * Performs ticks (100ms simulated time each). Between the ticks, the event loop is released so the
     * virtual client can process the messages sent by PySwitch.
     */
    async ticks(num = 10) {
        for (let i = 0; i < num; ++i) {
            await new Promise(r => setTimeout(r, 0));
            await this.runner.runner.tick();
        }
        await new Promise(r => setTimeout(r, 0));
    }

    /**
     * Presses and releases a switch, then waits for the communication. The push is detected by PySwitch
     * in the tick after pushing, so the hold time is simulated after that tick (ExampleTestRunner.simulateSwitchPress()
     * advances the time in the same tick which detects the push, so holding would not be detected).
     */
    async press(name, holdTimeMillis = 100) {
        const input = this.input(name);

        await this.runner.runner.tick();

        this.runner.setSwitch(input, true);
        await this.runner.runner.tick();
        await this.runner.runner.tick(holdTimeMillis);

        this.runner.setSwitch(input, false);
        await this.runner.runner.tick();

        await this.ticks();
    }

    /**
     * Holds a switch (longer than the hold time), then waits for the communication
     */
    async hold(name) {
        await this.press(name, 1000);
    }

    /**
     * Returns the LED color of a switch
     */
    led(name) {
        return this.runner.getSwitchColor(this.input(name));
    }

    /**
     * Returns the expected LED color for a color and state ("bright", "dim" or "off")
     */
    ledColor(color, state) {
        switch (state) {
            case "bright": return color.map((c) => Math.trunc(c * FractalTestBase.BRIGHT));
            case "dim": return color.map((c) => Math.trunc(c * FractalTestBase.DIM));
            case "off": return [0, 0, 0];
        }
        throw new Error("Invalid LED state: " + state);
    }

    /**
     * Expects a LED state
     */
    expectLed(name, color, state) {
        expect(this.led(name)).toEqual(this.ledColor(color, state), name + " should be " + state);
    }

    /**
     * Returns the label text of the first enabled action (with a label) of a switch
     */
    async label(name) {
        const port = this.input(name).data.model.port;

        return await this.#python(`
            _ret = None
            for _i in runner.controller.inputs:
                if not hasattr(_i, "pixels"):
                    continue
                if _i._SwitchController__switch.port != ` + port + `:
                    continue
                for _a in _i.actions:
                    if _a.enabled and _a.label and _ret == None:
                        _ret = _a.label.text
            _ret
        `);
    }

    /**
     * Returns the text of the display label which uses a callback of the passed class name
     */
    async displayText(callbackClassName) {
        return await this.#python(`
            _ret = None
            for _e in runner.controller.ui._UiController__current_splash_element.contents_flat():
                if getattr(_e, "callback", None) and type(_e.callback).__name__ == "` + callbackClassName + `":
                    _ret = _e.text
            _ret
        `);
    }

    /**
     * Returns if the tuner display is currently shown
     */
    async tunerShown() {
        return await this.#python(`
            type(runner.controller.ui._UiController__current_splash_element).__name__ == "TunerDisplay"
        `);
    }

    /**
     * Presses the pager switch until the page with the passed text is shown on its label
     */
    async selectPage(pagerName, pageText) {
        for (let i = 0; i < 10; ++i) {
            if ((await this.label(pagerName)) == pageText) return;
            await this.press(pagerName);
        }
        throw new Error("Page " + pageText + " not found");
    }

    /**
     * Loads a preset on the virtual client (like on the device) and waits for PySwitch to follow
     */
    async loadPreset(preset, scene = null) {
        this.client.presets.loadPreset(preset);
        if (scene !== null) this.client.presets.setScene(scene);
        await this.ticks();
    }

    /**
     * Runs python code in the emulator and returns the result
     */
    async #python(code) {
        return await this.runner.pyswitch.pyodide.runPython(code);
    }
}
