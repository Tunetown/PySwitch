/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_MINI_SWITCH_" + name;
    const PAGER = S("C");

    // Presets page
    const presetTests = new FractalPresetTests(runner);
    await presetTests.selectPage(PAGER, "Presets");
    await presetTests.testSelectInBank([S(1), S(2), S(3), S("A"), S("B")]);
    await presetTests.testBankIncDecSelect(S("A"), S("B"), [S(1), S(2), S(3), S("A"), S("B")], true);
    await presetTests.testNameDisplays();

    // Scenes page
    const sceneTests = new FractalSceneTests(runner);
    await sceneTests.selectPage(PAGER, "Scenes");
    await sceneTests.testSceneSelect([S(1), S(2), S(3), S("A")]);
    await sceneTests.testSceneIncDec(S("B"));

    // Effects page
    const effectTests = new FractalEffectTests(runner);
    await effectTests.selectPage(PAGER, "Effects");
    await effectTests.testBypass(S(1), 118, "Drive 1");
    await effectTests.testBypass(S(2), 70, "Delay 1");
    await effectTests.testBypass(S(3), 66, "Reverb 1");
    await effectTests.testBypass(S("A"), 78, "Chorus 1");
    await effectTests.testBypass(S("B"), 46, "Compressor 1");

    // Looper page
    const looperTests = new FractalLooperTests(runner);
    await looperTests.selectPage(PAGER, "Looper");
    await looperTests.testLooper(S(1), S(2), S(3));

    // Tuner
    const tunerTests = new FractalTunerTests(runner);
    await tunerTests.testTriggeredFromClient();
    await tunerTests.testFromSwitch(PAGER, true, S(1));

    // Device offline
    await presetTests.selectPage(PAGER, "Presets");
    await presetTests.testOffline(S(1));
})
