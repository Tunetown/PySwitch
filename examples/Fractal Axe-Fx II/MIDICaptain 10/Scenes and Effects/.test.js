/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Axe-Fx II: scenes and effects.
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
        "await presetText()": await presetText(),
        "await sceneText()": await sceneText()
    });

    await t.loadPreset(0, 0);
    // Preset 001 (drive, amp, cab, delay, reverb), scene 1
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
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
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("A"));
    // Press A: drive 1
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:onX REV1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("B"));
    // Press B: delay 1
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("D"));
    // Press D: amp 2 (not in the preset)
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    axe.setEngaged(110, false);
    await t.ticks();
    // Reverb 1 bypassed on the device
    expect(axe.preset).withContext("axe.preset").toEqual(0);
    expect(axe.scene).withContext("axe.scene").toEqual(1);
    expect(blocks()).withContext("blocks()").toEqual("DRV1:onX AMP1:onX CAB1:onX DLY1:offX REV1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("001 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 2");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("UP"));
    await t.press(S("UP"));
    // Press Up twice: preset 003 (wah, drive, amp 1 + 2, cab, delay)
    expect(axe.preset).withContext("axe.preset").toEqual(2);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:offX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("003 Recto 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("D"));
    // Press D: amp 2
    expect(axe.preset).withContext("axe.preset").toEqual(2);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("WAH1:onX DRV1:offX AMP1:onX AMP2:onX CAB1:onX DLY1:offX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("003 Recto 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("DOWN"));
    // Press Down: preset 002
    expect(axe.preset).withContext("axe.preset").toEqual(1);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("002 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.hold(S("DOWN"));
    // Hold Down: tuner on (CC 15 = 127)
    expect(axe.preset).withContext("axe.preset").toEqual(1);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(true);
    expect(await tunerNote()).withContext("await tunerNote()").toEqual("A");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.hold(S("DOWN"));
    // Hold Down: tuner off (CC 15 = 0)
    expect(axe.preset).withContext("axe.preset").toEqual(1);
    expect(axe.scene).withContext("axe.scene").toEqual(0);
    expect(blocks()).withContext("blocks()").toEqual("CPR1:onX AMP1:onX CAB1:onX CHO1:offX REV1:onX");
    expect(axe.tuner).withContext("axe.tuner").toEqual(false);
    expect(await presetText()).withContext("await presetText()").toEqual("002 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 1");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 2" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 3" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Drive 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Delay 1" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb 1" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });

    t.expectOnlyWhitelisted();
})
