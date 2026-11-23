/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Axe-Fx II: all pages.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_MINI_SWITCH_" + name;
    const t = new FractalIITestBase(runner);
    const all = [S(1), S(2), S(3), S("A"), S("B"), S("C")];
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
        "await presetText()": await presetText(),
        "await sceneText()": await sceneText()
    });

    await t.loadPreset(7, 0);
    await t.selectPage(S("C"), "Presets");
    // Presets page, preset 008
    expect(axe.preset).withContext("axe.preset").toEqual(7);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("AMP1:onX CAB1:onX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("008 Twin 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 1" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 3" });
    await t.expectSwitch(S("C"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.press(S(1));
    // Press 1: 006
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("006 5153 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "5153 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 1" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 1" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 1" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 3" });
    await t.expectSwitch(S("C"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.press(S("B"));
    // Press B: next bank (011)
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Recto 2" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Deluxe 2" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "AC30 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 2" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 4" });
    await t.expectSwitch(S("C"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.press(S("A"));
    await t.press(S("A"));
    await t.press(S("A"));
    // Press A three times: wrap to the last bank (766)
    expect(axe.preset).withContext("axe.preset").toEqual(765);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("766 5153 96");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "5153 96" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 96" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 96" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 153" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.selectPage(S("C"), "Scenes");
    await t.press(S(3));
    // Scenes page, press 3: scene 3
    expect(axe.preset).withContext("axe.preset").toEqual(765);
    expect(axe.scene).withContext("axe.scene").toEqual(2);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("766 5153 96");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 3");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene -1" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene +1" });
    await t.expectSwitch(S("C"), { leds: [[38, 0, 0], [38, 0, 0], [38, 0, 0]], label: "Scenes" });
    await t.press(S("A"));
    // Press A: previous scene
    expect(axe.preset).withContext("axe.preset").toEqual(765);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:offX AMP1:onX CAB1:onX CHO1:onX REV1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("766 5153 96");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene -1" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene +1" });
    await t.expectSwitch(S("C"), { leds: [[38, 0, 0], [38, 0, 0], [38, 0, 0]], label: "Scenes" });
    await t.loadPreset(1, 0);
    await t.selectPage(S("C"), "Effects");
    // Preset 002 (compressor, amp, cab, chorus, reverb), effects page
    expect(axe.preset).withContext("axe.preset").toEqual(1);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("002 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Drive 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Delay 1" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb 1" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Chorus 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Compressor 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Effects" });
    await t.press(S("B"));
    await t.press(S("A"));
    // Press B and A: compressor 1, chorus 1
    expect(axe.preset).withContext("axe.preset").toEqual(1);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:offX AMP1:onX CAB1:onX CHO1:onX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("002 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Drive 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Delay 1" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb 1" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Chorus 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Compressor 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Effects" });
    await t.selectPage(S("C"), "Channels");
    await t.press(S(1));
    await t.press(S("B"));
    // Channels page, press 1 and B: amp 1, cab 1 X/Y
    expect(axe.preset).withContext("axe.preset").toEqual(1);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:offX AMP1:onY CAB1:onY CHO1:onX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("002 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "DRV1 X/Y" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "DLY1 X/Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "REV1 [X]Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "CAB1 X[Y]" });
    await t.expectSwitch(S("C"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Channels" });
    await t.hold(S("C"));
    // Hold C: tuner on (CC 15 = 127)
    expect(axe.preset).withContext("axe.preset").toEqual(1);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:offX AMP1:onY CAB1:onY CHO1:onX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(true);
    expect(await tunerNote()).withContext("await tunerNote()").toEqual("A");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "DRV1 X/Y" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "DLY1 X/Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "REV1 [X]Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "CAB1 X[Y]" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Channels" });
    await t.hold(S("C"));
    // Hold C: tuner off (CC 15 = 0)
    expect(axe.preset).withContext("axe.preset").toEqual(1);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:offX AMP1:onY CAB1:onY CHO1:onX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("002 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "DRV1 X/Y" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "DLY1 X/Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "REV1 [X]Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "CAB1 X[Y]" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Channels" });

    t.expectOnlyWhitelisted();
})
