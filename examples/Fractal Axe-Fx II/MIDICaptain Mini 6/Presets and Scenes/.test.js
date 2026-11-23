/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Axe-Fx II (Mark I/II, .test.config.json): scenes, presets and tap tempo.
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
        "axe.bpm": axe.bpm,
        "axe.modelByte": axe.modelByte,
        "await presetText()": await presetText(),
        "await sceneText()": await sceneText()
    });

    await t.loadPreset(10, 0);
    // Preset 011, scene 1
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "120 bpm" });
    await t.press(S(3));
    // Press 3: scene 3
    expect(axe.preset).withContext("axe.preset").toEqual(10);
    expect(axe.scene).withContext("axe.scene").toEqual(2);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    expect(await presetText()).withContext("await presetText()").toEqual("011 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 3");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 2" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Deluxe 2" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: "120 bpm" });
    await t.press(S("B"));
    // Press B: next preset 012
    expect(axe.preset).withContext("axe.preset").toEqual(11);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("AMP1:onX CAB1:onX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    expect(await presetText()).withContext("await presetText()").toEqual("012 Deluxe 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Recto 2" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "AC30 2" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "120 bpm" });
    await t.press(S("A"));
    await t.press(S("A"));
    // Press A twice: preset 010
    expect(axe.preset).withContext("axe.preset").toEqual(9);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    expect(await presetText()).withContext("await presetText()").toEqual("010 Plexi 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Clean 2" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Recto 2" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "120 bpm" });
    await t.loadPreset(0);
    await t.press(S("A"));
    // Preset 001, press A: wrap to 384
    expect(axe.preset).withContext("axe.preset").toEqual(383);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("AMP1:onX CAB1:onX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    expect(await presetText()).withContext("await presetText()").toEqual("384 Twin 48");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 48" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Clean 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: "120 bpm" });
    await t.press(S("B"));
    // Press B: wrap to 001
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(120);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 48" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: "120 bpm" });
    await t.press(S("C"), 100, 5);
    await t.press(S("C"), 100, 5);
    await t.press(S("C"), 100, 5);
    // Tap C three times (500 ms)
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(67);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 48" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "67 bpm" });
    await t.hold(S("C"));
    // Hold C: tuner on (CC 15 = 127)
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(true);
    expect(await tunerNote()).withContext("await tunerNote()").toEqual("A");
    expect(axe.bpm).withContext("axe.bpm").toEqual(67);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 48" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: "67 bpm" });
    await t.hold(S("C"));
    // Hold C: tuner off (CC 15 = 0)
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(axe.bpm).withContext("axe.bpm").toEqual(67);
    expect(axe.modelByte).withContext("axe.modelByte").toEqual(3);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 48" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: "67 bpm" });

    t.expectOnlyWhitelisted();
})
