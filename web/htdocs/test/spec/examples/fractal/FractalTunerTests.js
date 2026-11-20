/**
 * Tests for the Fractal tuner (state derived from the tuner push data)
 */
class FractalTunerTests extends FractalTestBase {

    /**
     * Tuner switched on/off on the device
     */
    async testTriggeredFromClient() {
        await this.loadPreset(0);
        expect(await this.tunerShown()).toBe(false);

        this.client.tuner.setEnabled(true);
        await this.ticks();
        expect(await this.tunerShown()).toBe(true);

        // Push data stops: tuner display ends after the timeout (1.5 s)
        this.client.tuner.setEnabled(false);
        await this.ticks(25);
        expect(await this.tunerShown()).toBe(false);
    }

    /**
     * Tuner switched on by a switch (pressed or held), switched off by releasing any switch
     */
    async testFromSwitch(name, hold, offSwitchName) {
        await this.loadPreset(0);

        hold ? await this.hold(name) : await this.press(name);
        expect(this.client.tuner.enabled).toBe(true);
        expect(await this.tunerShown()).toBe(true);

        await this.press(offSwitchName);
        expect(this.client.tuner.enabled).toBe(false);
        expect(await this.tunerShown()).toBe(false);
    }
}
