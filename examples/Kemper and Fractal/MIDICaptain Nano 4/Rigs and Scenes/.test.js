/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Kemper and Fractal in one configuration: both virtual clients are connected, one switch taps the tempo of both.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;

    const kemper = runner.runner.clients.kemper;
    const fractal = runner.runner.clients.fractal;

    expect(kemper).toBeInstanceOf(VirtualKemperClient);
    expect(fractal).toBeInstanceOf(VirtualFractalClient);

    const fractalTests = new FractalSceneTests(runner);
    const kemperTests = new KemperTestBase(runner);

    // Fractal scene toggle (switch A): scene 1, again: scene 2
    await fractalTests.loadPreset(4, 5);
    await fractalTests.press(S("A"));
    expect(fractal.presets.currentScene).toBe(0);
    await fractalTests.press(S("A"));
    expect(fractal.presets.currentScene).toBe(1);
    expect(await fractalTests.displayText("FractalSceneNameCallback")).toBe("2 " + fractal.presets.getSceneName(1));

    // Kemper rigs (switches 1 and 2)
    await fractalTests.press(S(2));
    expect(kemper.getRigId()).toBe(1);

    await fractalTests.press(S(1));
    expect(kemper.getRigId()).toBe(0);

    // Selecting a Kemper rig does not change the Fractal scene
    expect(fractal.presets.currentScene).toBe(1);

    // Tap tempo on both devices (switch B): the Fractal tempo follows (label: BPM), the Kemper receives the taps (CC 30)
    kemperTests.startRecording();
    await (new FractalTempoTests(runner)).testTapTempo(S("B"));
    expect(kemperTests.takeCCs().filter((m) => m[0] == 30 && m[1] == 1).length).toBe(4);
})
