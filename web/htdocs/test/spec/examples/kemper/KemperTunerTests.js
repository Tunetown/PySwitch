/**
 * Tests for the Kemper tuner
 */
class KemperTunerTests extends KemperTestBase {

    /**
     * Tuner switched on/off on the device: all switch LEDs off and the tuner display shown, then the tuner display
     * is hidden again. The LEDs are not checked after the tuner: the Kemper client leaves them dark (or in a wrong
     * color after a rig change) when the tuner is switched off (claude/001 Fractal Support/TODO.md).
     */
    async testTriggeredFromClient() {
        const that = this;

        function getSwitchColors() {
            return that.runner.hardware
                .filter((input) => input.data.pixels && input.data.pixels.length)
                .map((input) => that.runner.getSwitchColor(input));
        }

        // Remember old colors
        const oldSwitchColors = getSwitchColors();
        expect(await this.tunerShown()).toBe(false);
            
        // Enable tuner
        this.client.parameters.get(new NRPNKey([127, 126])).setValue(1);
        await this.ticks();

        expect(getSwitchColors()).toEqual(oldSwitchColors.map(() => [0, 0, 0]));
        expect(await this.tunerShown()).toBe(true);

        // Disable tuner
        this.client.parameters.get(new NRPNKey([127, 126])).setValue(3);
        await this.ticks();

        expect(await this.tunerShown()).toBe(false);
    }
}
