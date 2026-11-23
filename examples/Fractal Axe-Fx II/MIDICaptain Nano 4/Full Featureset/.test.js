/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Axe-Fx II: all pages.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new FractalIITestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
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

    await t.loadPreset(5, 0);
    await t.selectPage(S("B"), "Presets");
    // Presets page, preset 006
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("006 5153 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.press(S(2));
    // Press 2: 007
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "5153 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "JCM800 1" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.hold(S(2));
    // Hold 2: next bank (no preset loaded)
    expect(axe.preset).withContext("axe.preset").toEqual(6);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("007 JCM800 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Recto 2" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Deluxe 2" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "AC30 2" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.press(S(1));
    // Press 1: preset 011
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Recto 2" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Deluxe 2" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "AC30 2" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.selectPage(S("B"), "Scenes");
    await t.press(S("A"));
    // Scenes page, press A: next scene
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:offX DRV1:onX AMP1:onX AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[38, 0, 0], [38, 0, 0], [38, 0, 0]], label: "Scenes" });
    await t.selectPage(S("B"), "Effects");
    await t.press(S(1));
    // Effects page, press 1: drive 1
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:offX DRV1:offX AMP1:onX AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Delay 1" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Reverb 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Effects" });
    await t.selectPage(S("B"), "Channels");
    await t.press(S(1));
    // Channels page, press 1: amp 1 X/Y
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:offX DRV1:offX AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DRV1 [X]Y" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Channels" });
    axe.setX(133, false);
    await t.ticks();
    // Drive 1 set to Y on the device
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:offX DRV1:offY AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "DRV1 X[Y]" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Channels" });
    await t.hold(S("B"));
    // Hold B: tuner on (CC 15 = 127)
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:offX DRV1:offY AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(true);
    expect(await tunerNote()).withContext("await tunerNote()").toEqual("A");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "DRV1 X[Y]" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Channels" });
    await t.hold(S("B"));
    // Hold B: tuner off (CC 15 = 0)
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:offX DRV1:offY AMP1:onY AMP2:onX CAB1:onX DLY1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "AMP1 X[Y]" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "DRV1 X[Y]" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "DLY1 [X]Y" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Channels" });

    t.expectOnlyWhitelisted();
})
