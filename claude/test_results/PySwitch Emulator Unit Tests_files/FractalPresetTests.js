/**
 * Tests for the Fractal preset and bank actions (bank size 5, the default)
 */
class FractalPresetTests extends FractalTestBase {

    static BANK_SIZE = 5;

    /**
     * PRESET_SELECT_IN_BANK switches (positions 1..n): labels, LEDs, selecting a preset
     */
    async testSelectInBank(names) {
        const presets = this.client.presets;

        // Preset 7: bank 2 (presets 5-9), position 3
        await this.loadPreset(7);

        for (let p = 0; p < names.length; ++p) {
            expect(await this.label(names[p])).toBe(presets.getPresetName(5 + p));
            this.expectLed(names[p], FractalTestBase.COLOR_PRESET, (p == 2) ? "bright" : "dim");
        }

        // Select position 1
        await this.press(names[0]);

        expect(presets.currentPreset).toBe(5);
        this.expectLed(names[0], FractalTestBase.COLOR_PRESET, "bright");
        this.expectLed(names[2], FractalTestBase.COLOR_PRESET, "dim");

        // Preset changed on the device (position 5)
        await this.loadPreset(9);
        this.expectLed(names[0], FractalTestBase.COLOR_PRESET, "dim");
        if (names.length > 4) {
            this.expectLed(names[4], FractalTestBase.COLOR_PRESET, "bright");
        }
    }

    /**
     * BANK_INC_DEC switches with preset_load NONE: only the bank is selected, the in bank switches follow
     */
    async testBankIncDecSelect(downName, upName, inBankNames, hold = false) {
        const presets = this.client.presets;

        await this.loadPreset(7);

        // Bank up: no preset is loaded
        hold ? await this.hold(upName) : await this.press(upName);
        expect(presets.currentPreset).toBe(7);

        for (let p = 0; p < inBankNames.length; ++p) {
            expect(await this.label(inBankNames[p])).toBe(presets.getPresetName(10 + p));
            this.expectLed(inBankNames[p], FractalTestBase.COLOR_PRESET, "dim");
        }

        // Selecting a preset loads it from the selected bank
        await this.press(inBankNames[1]);
        expect(presets.currentPreset).toBe(11);
        this.expectLed(inBankNames[1], FractalTestBase.COLOR_PRESET, "bright");

        // Bank down twice: bank 1
        hold ? await this.hold(downName) : await this.press(downName);
        hold ? await this.hold(downName) : await this.press(downName);
        expect(presets.currentPreset).toBe(11);
        expect(await this.label(inBankNames[0])).toBe(presets.getPresetName(0));

        // Wrap around to the last bank (presets 510, 511)
        hold ? await this.hold(downName) : await this.press(downName);
        expect(await this.label(inBankNames[0])).toBe(presets.getPresetName(510));
        expect(await this.label(inBankNames[2])).toBe("");

        // A preset change on the device resets the selection
        await this.loadPreset(3);
        expect(await this.label(inBankNames[0])).toBe(presets.getPresetName(0));
    }

    /**
     * BANK_INC_DEC (hold functions) with preset_load FIRST
     */
    async testBankIncDecLoadFirst(downName, upName) {
        const presets = this.client.presets;

        await this.loadPreset(7);

        await this.hold(upName);
        expect(presets.currentPreset).toBe(10);

        await this.hold(downName);
        await this.hold(downName);
        expect(presets.currentPreset).toBe(0);
    }

    /**
     * BANK_INC_DEC labels and LEDs
     */
    async testBankIncDecDisplay(name, step) {
        await this.loadPreset(7);

        expect(await this.label(name)).toBe("Bank " + (step > 0 ? "+" : "") + step);
        this.expectLed(name, FractalTestBase.COLOR_BANK, "dim");
    }

    /**
     * PRESET_INC_DEC: steps through the presets (label: ACTION or DESTINATION_NAME)
     */
    async testPresetIncDec(name, step, destinationName = false) {
        const presets = this.client.presets;

        await this.loadPreset(7);
        this.expectLed(name, FractalTestBase.COLOR_PRESET, "dim");

        if (destinationName) {
            expect(await this.label(name)).toBe(presets.getPresetName(7 + step));
        } else {
            expect(await this.label(name)).toBe("Preset " + (step > 0 ? "+" : "") + step);
        }

        await this.press(name);
        expect(presets.currentPreset).toBe(7 + step);

        if (destinationName) {
            expect(await this.label(name)).toBe(presets.getPresetName(7 + 2 * step));
        }
    }

    /**
     * Preset and scene name displays (both with numbers)
     */
    async testNameDisplays() {
        const presets = this.client.presets;

        await this.loadPreset(12, 3);

        expect(await this.displayText("FractalPresetNameCallback")).toBe("012 " + presets.getPresetName(12));
        expect(await this.displayText("FractalSceneNameCallback")).toBe("4 " + presets.getSceneName(3));

        // Renamed on the device: the name follows (preset name is polled)
        presets.setPresetName(12, "Renamed");
        await this.ticks();
        expect(await this.displayText("FractalPresetNameCallback")).toBe("012 Renamed");

        // Scene change on the device
        presets.setScene(5);
        await this.ticks();
        expect(await this.displayText("FractalSceneNameCallback")).toBe("6 " + presets.getSceneName(5));
    }

    /**
     * Device offline (simulated by a model change of the virtual device: it ignores the messages):
     * the values expire, LEDs go off. Afterwards, the device is reset to the FM3 (preset 0).
     */
    async testOffline(presetSwitchName) {
        await this.loadPreset(2);
        expect(this.led(presetSwitchName)).not.toEqual([0, 0, 0]);

        this.client.setModel("FM9");
        await this.ticks(40);

        this.expectLed(presetSwitchName, FractalTestBase.COLOR_PRESET, "off");
        expect(await this.displayText("FractalPresetNameCallback")).toBe("");

        this.client.setModel("FM3");
        await this.ticks();

        expect(await this.displayText("FractalPresetNameCallback")).toBe("000 " + this.client.presets.getPresetName(0));
    }
}
