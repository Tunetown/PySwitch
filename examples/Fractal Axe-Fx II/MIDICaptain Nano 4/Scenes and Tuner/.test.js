/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Axe-Fx II: scenes and tuner.
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

    await t.loadPreset(0, 0);
    // Preset 001, scene 1
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.press(S(2));
    // Press 2: scene 2
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:offX AMP1:onX CAB1:onX DLY1:onX REV1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.press(S("B"));
    // Press B: scene 4
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(3);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:offX AMP1:onX CAB1:onX DLY1:onX REV1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 4");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 4" });
    axe.setScene(2);
    await t.ticks();
    // Scene 3 selected on the device
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(2);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 3");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.loadPreset(5);
    // Preset 006 loaded on the device
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("006 5153 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    axe.setName("My Preset");
    await t.loadPreset(6);
    await t.loadPreset(5);
    // Preset 006 renamed on the device
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("006 My Preset");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.hold(S("B"));
    // Hold B: tuner on (CC 15 = 127)
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(true);
    expect(await tunerNote()).withContext("await tunerNote()").toEqual("A");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    axe.setTunerData(4, 10);
    await t.ticks();
    // Tuner: E +10 cents
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(true);
    expect(await tunerNote()).withContext("await tunerNote()").toEqual("E");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.press(S(1));
    // Press 1 while the tuner is shown: tuner off (CC 15 = 0)
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("006 My Preset");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    axe.setTuner(true);
    await t.ticks();
    // Tuner switched on at the device
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(true);
    expect(await tunerNote()).withContext("await tunerNote()").toEqual("E");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    axe.setTuner(false);
    await t.ticks();
    // Tuner switched off at the device
    expect(axe.preset).withContext("axe.preset").toEqual(5);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("006 My Preset");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });

    t.expectOnlyWhitelisted();
})
