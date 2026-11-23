/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Axe-Fx II: all pages.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_10_SWITCH_" + name;
    const t = new FractalIITestBase(runner);
    const all = [S(1), S(2), S(3), S(4), S("A"), S("B"), S("C"), S("D"), S("UP"), S("DOWN")];
    const axe = t.client;
    const presetText = () => t.displayText("FractalIIPresetNameCallback");
    const sceneText = () => t.displayText("FractalIISceneNameCallback");
    const blocks = () => axe.current.blocks.map((id) => FractalIIClient.getBlockName(id, true) + ":" + (axe.getBlock(id).engaged ? "on" : "off") + (axe.getBlock(id).x ? "X" : "Y")).join(" ");
    const tunerNote = () => t.python(`
        _s = runner.controller.ui._UiController__current_splash_element
        _s.label_note.text if type(_s).__name__ == "TunerDisplay" else None
    `);
    const c = async () => ({
        "axe.preset": axe.preset,
        "axe.scene": axe.scene,
        "blocks()": blocks(),
        "axe.tuner": axe.tuner,
        "await tunerNote()": await tunerNote(),
        "axe.bpm": axe.bpm,
        "await presetText()": await presetText(),
        "await sceneText()": await sceneText()
    });

    await t.loadPreset(12, 1);
    await t.selectPage(S("UP"), "Presets");
    // Presets page, preset 013, scene 2
    expect(axe.preset).withContext("axe.preset").toEqual(12);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:offX AMP1:onX CAB1:onX DLY1:onX REV1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("013 AC30 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 2" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 4" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.press(S("A"));
    // Press A: 015
    expect(axe.preset).withContext("axe.preset").toEqual(14);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("015 JCM800 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Recto 2" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Deluxe 2" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "AC30 2" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "5153 2" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "JCM800 2" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 2" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 4" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.press(S("B"));
    // Press B: previous bank (no preset loaded)
    expect(axe.preset).withContext("axe.preset").toEqual(14);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("015 JCM800 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "5153 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 1" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 1" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Clean 2" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 2" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 1" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 3" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.press(S(1));
    // Press 1: 006
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("006 5153 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "5153 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 1" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 1" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Clean 2" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 2" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 1" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 3" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 1" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.press(S("D"));
    // Press D: next preset 007
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "5153 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "JCM800 1" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 1" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Clean 2" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 2" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 1" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 3" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 1" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.selectPage(S("UP"), "Scenes");
    await t.press(S("D"));
    // Scenes page, press D: scene 8
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(7);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:offX DRV1:onX AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 8");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 5" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 6" });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 7" });
    await t.expectSwitch(S("D"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 8" });
    await t.expectSwitch(S("UP"), { leds: [[38, 0, 0], [38, 0, 0], [38, 0, 0]], label: "Scenes" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.selectPage(S("UP"), "Effects");
    await t.press(S(2));
    await t.press(S("D"));
    // Effects page (preset 007: wah, drive, amp 1 + 2, cab, delay), press 2 and D
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(7);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:onX AMP1:onY AMP2:offX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 8");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Compressor 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Wah 1" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive 1" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp 1" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Chorus 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Effects" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.selectPage(S("UP"), "Channels");
    await t.press(S("D"));
    // Channels page, press D: amp 2 Y (bypassed: LED dim)
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(7);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:onX AMP1:onY AMP2:offY CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 8");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DRV1 [X]Y" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "CAB1 [X]Y" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "REV1 X/Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "CHO1 X/Y" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP2 X" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP2 Y" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Channels" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.press(S("D"));
    // Press D again (smart bypass): amp 2 engaged
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(7);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:onX AMP1:onY AMP2:onY CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 8");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DRV1 [X]Y" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "CAB1 [X]Y" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "REV1 X/Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "CHO1 X/Y" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP2 X" });
    await t.expectSwitch(S("D"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "AMP2 Y" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Channels" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.press(S("C"));
    // Press C: amp 2 X
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(7);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:onX AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 8");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DRV1 [X]Y" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "CAB1 [X]Y" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "REV1 X/Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "CHO1 X/Y" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "AMP2 X" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP2 Y" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Channels" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.press(S("DOWN"), 100, 5);
    await t.press(S("DOWN"), 100, 5);
    await t.press(S("DOWN"), 100, 5);
    // Tap Down three times (500 ms)
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(7);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:onX AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(67);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 8");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DRV1 [X]Y" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "CAB1 [X]Y" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "REV1 X/Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "CHO1 X/Y" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "AMP2 X" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP2 Y" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Channels" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.hold(S("DOWN"));
    // Hold Down: tuner on (CC 15 = 127)
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(7);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:onX AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(true);
    expect(await tunerNote()).withContext("await tunerNote()").toEqual("A");
    expect(axe.bpm).withContext("axe.bpm").toEqual(67);
    await t.expectSwitch(S("1"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DRV1 [X]Y" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "CAB1 [X]Y" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "REV1 X/Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "CHO1 X/Y" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "AMP2 X" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP2 Y" });
    await t.expectSwitch(S("UP"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Channels" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.hold(S("DOWN"));
    // Hold Down: tuner off (CC 15 = 0)
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(7);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:onX AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(67);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 8");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DRV1 [X]Y" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "CAB1 [X]Y" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "REV1 X/Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "CHO1 X/Y" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "AMP2 X" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP2 Y" });
    await t.expectSwitch(S("UP"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Channels" });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });

    t.expectOnlyWhitelisted();
})
