/**
 * Tests for the Fractal scene actions
 */
class FractalSceneTests extends FractalTestBase {

    /**
     * SCENE_SELECT switches (scenes 1..n): labels (scene names), LEDs, selecting a scene
     */
    async testSceneSelect(names) {
        const presets = this.client.presets;

        await this.loadPreset(4, 1);

        for (let s = 0; s < names.length; ++s) {
            expect(await this.label(names[s])).toBe(presets.getSceneName(s));
            this.expectLed(names[s], FractalTestBase.COLOR_SCENE, (s == 1) ? "bright" : "dim");
        }

        // Select the first scene
        await this.press(names[0]);
        expect(presets.currentScene).toBe(0);
        this.expectLed(names[0], FractalTestBase.COLOR_SCENE, "bright");
        this.expectLed(names[1], FractalTestBase.COLOR_SCENE, "dim");

        // Scene change on the device
        presets.setScene(names.length - 1);
        await this.ticks();
        this.expectLed(names[names.length - 1], FractalTestBase.COLOR_SCENE, "bright");
        this.expectLed(names[0], FractalTestBase.COLOR_SCENE, "dim");

        // Other preset: other scene names
        await this.loadPreset(5);
        expect(await this.label(names[0])).toBe(presets.getSceneName(0));
    }

    /**
     * SCENE_INC_DEC (step +1, label ACTION or DESTINATION_NAME)
     */
    async testSceneIncDec(name, destinationName = false) {
        const presets = this.client.presets;

        await this.loadPreset(4, 6);
        this.expectLed(name, FractalTestBase.COLOR_SCENE, "dim");

        if (destinationName) {
            expect(await this.label(name)).toBe(presets.getSceneName(7));
        } else {
            expect(await this.label(name)).toBe("Scene +1");
        }

        await this.press(name);
        expect(presets.currentScene).toBe(7);

        // Wrap
        await this.press(name);
        expect(presets.currentScene).toBe(0);
    }
}
