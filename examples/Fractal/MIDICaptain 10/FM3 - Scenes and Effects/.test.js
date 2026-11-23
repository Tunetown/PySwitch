/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Runs with the model of the example (FM3, .test.config.json).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_10_SWITCH_" + name;

    expect(runner.runner.clients.fractal.getModelId()).toBe("FM3");

    // Scenes
    await (new FractalSceneTests(runner)).testSceneSelect([S(1), S(2), S(3), S(4)]);

    // Effects
    const effectTests = new FractalEffectTests(runner);
    await effectTests.testBypass(S("A"), 118, "Drive 1");
    await effectTests.testBypass(S("B"), 70, "Delay 1");
    await effectTests.testBypass(S("C"), 66, "Reverb 1");
    await effectTests.testBypass(S("D"), 78, "Chorus 1");

    // Presets (Up/Down have no label)
    const presetTests = new FractalPresetTests(runner);
    const presets = runner.runner.clients.fractal.presets;

    await presetTests.loadPreset(7);
    await presetTests.press(S("UP"));
    expect(presets.currentPreset).toBe(8);

    await presetTests.press(S("DOWN"));
    await presetTests.press(S("DOWN"));
    expect(presets.currentPreset).toBe(6);

    await presetTests.testNameDisplays();

    // Tuner
    const tunerTests = new FractalTunerTests(runner);
    await tunerTests.testTriggeredFromClient();
    await tunerTests.testFromSwitch(S("DOWN"), true, S(1));
})
