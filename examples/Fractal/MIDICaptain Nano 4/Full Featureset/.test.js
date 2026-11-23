/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const PAGER = S("B");

    // Presets page
    const presetTests = new FractalPresetTests(runner);
    await presetTests.selectPage(PAGER, "Presets");
    await presetTests.testPresetIncDec(S(1), -1, true);
    await presetTests.testPresetIncDec(S(2), 1, true);
    await presetTests.testBankIncDecLoadFirst(S(1), S(2));
    await (new FractalTempoTests(runner)).testTapTempo(S("A"));
    await presetTests.testNameDisplays();

    // Scenes page
    const sceneTests = new FractalSceneTests(runner);
    await sceneTests.selectPage(PAGER, "Scenes");
    await sceneTests.testSceneSelect([S(1), S(2)]);
    await sceneTests.testSceneIncDec(S("A"), true);

    // Effects page
    const effectTests = new FractalEffectTests(runner);
    await effectTests.selectPage(PAGER, "Effects");
    await effectTests.testBypass(S(1), 118, "Drive 1");
    await effectTests.testBypass(S(2), 70, "Delay 1");
    await effectTests.testBypass(S("A"), 66, "Reverb 1");

    // Channels page
    await effectTests.selectPage(PAGER, "Channels");
    await effectTests.testChannelToggle(S(1), 58, "AMP1");
    await effectTests.testChannelIncDec(S(2), 118, "DRV1");
    await effectTests.testChannelSelectSmartBypass(S("A"), 70, 1);

    // Tuner
    const tunerTests = new FractalTunerTests(runner);
    await tunerTests.testTriggeredFromClient();
    await tunerTests.testFromSwitch(PAGER, true, S(1));

    // Device offline
    await presetTests.selectPage(PAGER, "Presets");
    await presetTests.testOffline(S(1));
})
