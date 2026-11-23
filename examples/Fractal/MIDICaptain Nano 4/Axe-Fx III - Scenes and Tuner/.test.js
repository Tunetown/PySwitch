/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Runs with the model of the example (Axe-Fx III, .test.config.json).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;

    expect(runner.runner.clients.fractal.getModelId()).toBe("AXEFX3");

    // Scenes
    const sceneTests = new FractalSceneTests(runner);
    await sceneTests.testSceneSelect([S(1), S(2), S("A"), S("B")]);

    // Preset and scene name displays
    await (new FractalPresetTests(runner)).testNameDisplays();

    // Tuner
    const tunerTests = new FractalTunerTests(runner);
    await tunerTests.testTriggeredFromClient();
    await tunerTests.testFromSwitch(S("B"), true, S(1));
})
