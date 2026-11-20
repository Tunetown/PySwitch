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

        for (let i = 0; i < 4; ++i) {
            await this.press(name);
        }

        expect(tempo.bpm()).not.toBe(120);
        expect(await this.label(name)).toBe(tempo.bpm() + " bpm");

        tempo.set(120);
        await this.ticks();
    }
}
