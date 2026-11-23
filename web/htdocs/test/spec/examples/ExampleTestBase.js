/**
 * Base class for the example tests (all clients): switches, switch LEDs, label and display texts of the running
 * PySwitch instance, ticks with simulated time. Spec: claude/001 Fractal Support/spec/emulator/integration.md
 */
class ExampleTestBase {

    // Default LED brightness values (config.py defaults)
    static BRIGHT = 0.3;
    static DIM = 0.02;

    // Default number of ticks (100ms each) to wait for the communication: 2 seconds = 5 update intervals of 400ms.
    // After a preset change, names need up to 3 intervals (detect the preset, request the names, show them).
    static DEFAULT_TICKS = 20;

    runner = null;

    constructor(runner) {
        this.runner = runner;
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
    async ticks(num = ExampleTestBase.DEFAULT_TICKS) {
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
     * waitTicks: ticks to wait for the communication afterwards.
     */
    async press(name, holdTimeMillis = 100, waitTicks = ExampleTestBase.DEFAULT_TICKS) {
        const input = this.input(name);

        await this.runner.runner.tick();

        this.runner.setSwitch(input, true);
        await this.runner.runner.tick();
        await this.runner.runner.tick(holdTimeMillis);

        this.runner.setSwitch(input, false);
        await this.runner.runner.tick();

        await this.ticks(waitTicks);
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
     * Returns the colors of all LEDs (segments) of a switch
     */
    leds(name) {
        return this.input(name).data.pixels.map((led) => JSON.parse($("#pyswitch-led-" + led)[0].dataset.color));
    }

    /**
     * Returns the expected LED color for a color and state ("bright", "dim" or "off")
     */
    ledColor(color, state) {
        switch (state) {
            case "bright": return color.map((c) => Math.trunc(c * ExampleTestBase.BRIGHT));
            case "dim": return color.map((c) => Math.trunc(c * ExampleTestBase.DIM));
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

        return await this.python(`
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
     * Returns the state of an action of a switch: { label, state, enabled } (the LED color: led()).
     * index: index of the action in the actions (or hold actions) list; null: the first enabled action.
     * Returns null if no action is found.
     */
    async action(name, index = null, hold = false) {
        const port = this.input(name).data.model.port;

        const json = await this.python(`
            import json as _json
            _ret = None
            for _i in runner.controller.inputs:
                if not hasattr(_i, "pixels") or _i._SwitchController__switch.port != ` + port + `:
                    continue
                _acts = _i._SwitchController__actions` + (hold ? "_hold" : "") + `
                _sel = ` + ((index === null) ? "[_a for _a in _acts if _a.enabled]" : ("_acts[" + index + ":" + (index + 1) + "]")) + `
                if _sel:
                    _a = _sel[0]
                    _ret = {
                        "label": _a.label.text if _a.label else None,
                        "state": getattr(_a, "state", None),
                        "enabled": _a.enabled
                    }
            _json.dumps(_ret)
        `);

        return JSON.parse(json);
    }

    /**
     * Logs the LEDs and labels of the passed switches and the values of the passed checks to the console, as one 
     * line "DUMP <json>". Used to write tests: tools/dump_to_test.py converts the dumps of an exploration script
     * into expectations (expectSwitch(), expect(<check>).toEqual(<value>)).
     * checks: { "<JavaScript expression>": <current value>, ... }
     */
    async dump(title, names, checks = {}) {
        const switches = {};
        for (const name of names) {
            const action = await this.action(name);
            switches[name] = {
                leds: this.leds(name),
                label: action ? action.label : null
            };
        }
        console.log("DUMP " + JSON.stringify({ title: title, switches: switches, checks: checks }));
    }

    /**
     * Expects the LED colors (all segments) and/or the label text of the first enabled action of a switch
     * expected: { leds: [[r, g, b], ...], label: "..." }
     */
    async expectSwitch(name, expected) {
        if (expected.leds) {
            expect(this.leds(name)).withContext(name + " LEDs").toEqual(expected.leds);
        }
        if (expected.hasOwnProperty("label")) {
            const action = await this.action(name);
            expect(action ? action.label : null).withContext(name + " label").toEqual(expected.label);
        }
    }

    /**
     * Returns the text of the display label which uses a callback of the passed class name
     */
    async displayText(callbackClassName) {
        return await this.python(`
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
        return await this.python(`
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
     * Runs python code in the emulator and returns the result
     */
    async python(code) {
        return await this.runner.pyswitch.pyodide.runPython(code);
    }
}
