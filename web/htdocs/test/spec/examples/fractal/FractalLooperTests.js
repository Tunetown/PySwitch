/**
 * Tests for the Fractal looper actions
 */
class FractalLooperTests extends FractalTestBase {

    static LOOPER_BLOCK_ID = 166;

    static COLOR_RECORD = [255, 0, 0];
    static COLOR_OVERDUB = [255, 255, 0];
    static COLOR_PLAY = [0, 255, 0];
    static COLOR_UNDO = [180, 0, 120];

    /**
     * Record, Play/Stop and Undo switches
     */
    async testLooper(recordName, playName, undoName) {
        const presets = this.client.presets;
        const looper = this.client.looper;

        await this.loadPreset(0);
        presets.addBlock(FractalLooperTests.LOOPER_BLOCK_ID);
        looper.reset();
        await this.ticks();

        expect(await this.label(recordName)).toBe("Record");
        expect(await this.label(playName)).toBe("Play");
        this.expectLed(recordName, FractalLooperTests.COLOR_RECORD, "dim");
        this.expectLed(playName, FractalLooperTests.COLOR_PLAY, "dim");
        this.expectLed(undoName, FractalLooperTests.COLOR_UNDO, "dim");

        // Record
        await this.press(recordName);
        expect(looper.recording).toBe(true);
        this.expectLed(recordName, FractalLooperTests.COLOR_RECORD, "bright");

        // Record again: overdub (Record 2nd Press default)
        await this.press(recordName);
        expect(looper.overdub).toBe(true);
        expect(await this.label(recordName)).toBe("Overdub");
        this.expectLed(recordName, FractalLooperTests.COLOR_OVERDUB, "bright");
        this.expectLed(playName, FractalLooperTests.COLOR_PLAY, "bright");
        expect(await this.label(playName)).toBe("Stop");

        // Play: ends overdub, playback continues
        await this.press(playName);
        expect(looper.overdub).toBe(false);
        expect(looper.playing).toBe(true);
        this.expectLed(recordName, FractalLooperTests.COLOR_RECORD, "dim");

        // Stop
        await this.press(playName);
        expect(looper.playing).toBe(false);
        this.expectLed(playName, FractalLooperTests.COLOR_PLAY, "dim");

        // Undo when stopped: erase
        await this.press(undoName);
        expect(looper.loopLength).toBe(0);

        // No Looper block in the preset: LEDs off
        presets.removeBlock(FractalLooperTests.LOOPER_BLOCK_ID);
        await this.ticks();
        this.expectLed(recordName, FractalLooperTests.COLOR_RECORD, "off");
        this.expectLed(playName, FractalLooperTests.COLOR_PLAY, "off");

        presets.addBlock(FractalLooperTests.LOOPER_BLOCK_ID);
        await this.ticks();
    }
}
