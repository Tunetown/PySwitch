/**
 * Tests for the Fractal tap tempo action
 */
class FractalTempoTests extends FractalTestBase {

    /**
     * TAP_TEMPO with label BPM: tapping changes the tempo of the device, the label follows
     */
    async testTapTempo(name) {
        const tempo = this.client.tempo;

        tempo.set(120);
        await this.ticks();
        expect(await this.label(name)).toBe("120 bpm");

        // Taps 900ms apart (the device starts a new tap series after 2.5 s), then wait for the label
        for (let i = 0; i < 4; ++i) {
            await this.press(name, 100, 5);
        }
        await this.ticks();

        expect(tempo.bpm()).not.toBe(120);
        expect(await this.label(name)).toBe(tempo.bpm() + " bpm");

        tempo.set(120);
        await this.ticks();
    }
}
