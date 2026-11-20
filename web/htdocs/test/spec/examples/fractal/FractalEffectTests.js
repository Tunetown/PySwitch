/**
 * Tests for the Fractal effect actions (block bypass and channels). Block IDs: claude/FRACTAL.md 4.
 */
class FractalEffectTests extends FractalTestBase {

    /**
     * EFFECT_BYPASS: LED states (engaged, bypassed, not in preset), label, switching
     */
    async testBypass(name, id, labelText) {
        const presets = this.client.presets;

        await this.loadPreset(0);
        presets.addBlock(id);
        presets.setBypass(id, false);
        await this.ticks();

        expect(await this.label(name)).toBe(labelText);
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "bright");

        // Bypass from the switch
        await this.press(name);
        expect(presets.getBlockState(id).bypassed).toBe(true);
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "dim");

        // Engage on the device
        presets.setBypass(id, false);
        await this.ticks();
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "bright");

        // Not in the preset: LED off, label stays, pressing does nothing
        presets.removeBlock(id);
        await this.ticks();
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "off");
        expect(await this.label(name)).toBe(labelText);

        await this.press(name);
        expect(presets.hasBlock(id)).toBe(false);

        presets.addBlock(id);
        await this.ticks();
    }

    /**
     * EFFECT_CHANNEL_SELECT switches for channels A, B, ...: LEDs, labels, selecting
     */
    async testChannelSelect(names, id, abbreviation) {
        const presets = this.client.presets;
        const channels = ["A", "B", "C", "D"];

        await this.loadPreset(0);
        presets.addBlock(id);
        presets.setBypass(id, false);
        presets.setChannel(id, 0);
        await this.ticks();

        for (let c = 0; c < names.length; ++c) {
            expect(await this.label(names[c])).toBe(abbreviation + " " + channels[c]);
            this.expectLed(names[c], FractalTestBase.COLOR_EFFECT, (c == 0) ? "bright" : "dim");
        }

        await this.press(names[names.length - 1]);
        expect(presets.getBlockState(id).channel).toBe(names.length - 1);
        this.expectLed(names[names.length - 1], FractalTestBase.COLOR_EFFECT, "bright");
        this.expectLed(names[0], FractalTestBase.COLOR_EFFECT, "dim");

        // Bypassed: all off
        presets.setBypass(id, true);
        await this.ticks();
        for (const name of names) {
            this.expectLed(name, FractalTestBase.COLOR_EFFECT, "off");
        }

        presets.setBypass(id, false);
        await this.ticks();
    }

    /**
     * EFFECT_CHANNEL_SELECT with second_press = SMART_BYPASS
     */
    async testChannelSelectSmartBypass(name, id, channel) {
        const presets = this.client.presets;

        await this.loadPreset(0);
        presets.addBlock(id);
        presets.setBypass(id, false);
        presets.setChannel(id, 0);
        await this.ticks();

        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "dim");

        // Select the channel
        await this.press(name);
        expect(presets.getBlockState(id).channel).toBe(channel);
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "bright");

        // Second press: bypass, third press: engage
        await this.press(name);
        expect(presets.getBlockState(id).bypassed).toBe(true);
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "dim");

        await this.press(name);
        expect(presets.getBlockState(id).bypassed).toBe(false);
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "bright");
    }

    /**
     * EFFECT_CHANNEL_TOGGLE between A and B (label BOTH_CHANNELS)
     */
    async testChannelToggle(name, id, abbreviation) {
        const presets = this.client.presets;

        await this.loadPreset(0);
        presets.addBlock(id);
        presets.setChannel(id, 0);
        await this.ticks();

        expect(await this.label(name)).toBe(abbreviation + " [A]B");
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "bright");

        await this.press(name);
        expect(presets.getBlockState(id).channel).toBe(1);
        expect(await this.label(name)).toBe(abbreviation + " A[B]");
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "dim");

        // Other channel on the device
        presets.setChannel(id, 2);
        await this.ticks();
        expect(await this.label(name)).toBe(abbreviation + " A/B");
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "off");

        await this.press(name);
        expect(presets.getBlockState(id).channel).toBe(0);
    }

    /**
     * EFFECT_CHANNEL_INC_DEC (step +1, label CURRENT_CHANNEL)
     */
    async testChannelIncDec(name, id, abbreviation) {
        const presets = this.client.presets;

        await this.loadPreset(0);
        presets.addBlock(id);
        presets.setChannel(id, 2);
        await this.ticks();

        expect(await this.label(name)).toBe(abbreviation + " C");
        this.expectLed(name, FractalTestBase.COLOR_EFFECT, "dim");

        await this.press(name);
        expect(presets.getBlockState(id).channel).toBe(3);
        expect(await this.label(name)).toBe(abbreviation + " D");

        // Wrap (4 channels)
        await this.press(name);
        expect(presets.getBlockState(id).channel).toBe(0);
    }
}
