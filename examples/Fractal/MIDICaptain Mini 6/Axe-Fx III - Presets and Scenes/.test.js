/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Runs with the model of the example (Axe-Fx III, .test.config.json).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_MINI_SWITCH_" + name;

    expect(runner.runner.clients.fractal.getModelId()).toBe("AXEFX3");

    // Scenes
    await (new FractalSceneTests(runner)).testSceneSelect([S(1), S(2), S(3)]);

    // Presets
    const presetTests = new FractalPresetTests(runner);
    await presetTests.testPresetIncDec(S("A"), -1, true);
    await presetTests.testPresetIncDec(S("B"), 1, true);
    await presetTests.testNameDisplays();

    // Tap Tempo
    await (new FractalTempoTests(runner)).testTapTempo(S("C"));

    // Tuner
    const tunerTests = new FractalTunerTests(runner);
    await tunerTests.testTriggeredFromClient();
    await tunerTests.testFromSwitch(S("C"), true, S(1));
})
