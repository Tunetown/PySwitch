/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_10_SWITCH_" + name;
    const PAGER = S("UP");

    // Presets page
    const presetTests = new FractalPresetTests(runner);
    await presetTests.selectPage(PAGER, "Presets");
    await presetTests.testSelectInBank([S(1), S(2), S(3), S(4), S("A")]);
    await presetTests.testBankIncDecDisplay(S("B"), -1);
    await presetTests.testBankIncDecDisplay(S("C"), 1);
    await presetTests.testBankIncDecSelect(S("B"), S("C"), [S(1), S(2), S(3), S(4), S("A")]);
    await presetTests.testPresetIncDec(S("D"), 1);
    await presetTests.testNameDisplays();

    // Scenes page
    const sceneTests = new FractalSceneTests(runner);
    await sceneTests.selectPage(PAGER, "Scenes");
    await sceneTests.testSceneSelect([S(1), S(2), S(3), S(4), S("A"), S("B"), S("C"), S("D")]);

    // Effects page
    const effectTests = new FractalEffectTests(runner);
    await effectTests.selectPage(PAGER, "Effects");
    await effectTests.testBypass(S(1), 118, "Drive 1");
    await effectTests.testBypass(S(2), 70, "Delay 1");
    await effectTests.testBypass(S(3), 66, "Reverb 1");
    await effectTests.testBypass(S(4), 78, "Chorus 1");
    await effectTests.testBypass(S("A"), 46, "Compressor 1");
    await effectTests.testBypass(S("B"), 90, "Phaser 1");
    await effectTests.testBypass(S("C"), 110, "Pitch 1");
    await effectTests.testBypass(S("D"), 94, "Wah 1");

    // Channels page
    await effectTests.selectPage(PAGER, "Channels");
    await effectTests.testChannelSelect([S(1), S(2), S(3), S(4)], 58, "AMP1");
    await effectTests.testChannelToggle(S("A"), 118, "DRV1");
    await effectTests.testChannelToggle(S("B"), 119, "DRV2");
    await effectTests.testChannelIncDec(S("C"), 70, "DLY1");
    await effectTests.testChannelIncDec(S("D"), 66, "REV1");

    // Looper page
    const looperTests = new FractalLooperTests(runner);
    await looperTests.selectPage(PAGER, "Looper");
    await looperTests.testLooper(S(1), S(2), S(3));
    await (new FractalTempoTests(runner)).testTapTempo(S("D"));

    // Tuner
    const tunerTests = new FractalTunerTests(runner);
    await tunerTests.testTriggeredFromClient();
    await tunerTests.testFromSwitch(S("DOWN"), true, S(1));

    // Device offline
    await presetTests.selectPage(PAGER, "Presets");
    await presetTests.testOffline(S(1));
})
