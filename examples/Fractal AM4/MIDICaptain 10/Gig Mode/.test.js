/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * AM4: scenes, effect slots, presets.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_10_SWITCH_" + name;
    const t = new FractalAM4TestBase(runner);
    const all = [S(1), S(2), S(3), S(4), S("A"), S("B"), S("C"), S("D"), S("UP"), S("DOWN")];
    const am4 = t.client;
    const presetText = () => t.displayText("FractalAM4PresetNameCallback");
    const sceneText = () => t.displayText("FractalAM4SceneNameCallback");
    const c = async () => ({
        "am4.location": am4.location,
        "am4.scene": am4.scene,
        "am4.mode": am4.mode,
        "am4.preset.bypass[am4.scene]": am4.preset.bypass[am4.scene],
        "am4.cc[15] ?? null": am4.cc[15] ?? null,
        "await presetText()": await presetText(),
        "await sceneText()": await sceneText()
    });

    await t.loadPreset(2, 0);
    // Preset A03, scene 1
    expect(am4.location).withContext("am4.location").toEqual(2);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A03 Recto 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp" });
    await t.expectSwitch(S("D"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Delay" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S(4));
    // Press 4: scene 4
    expect(am4.location).withContext("am4.location").toEqual(2);
    expect(am4.scene).withContext("am4.scene").toEqual(3);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, false, false, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A03 Recto 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 4");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.expectSwitch(S("D"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Delay" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("A"));
    await t.press(S("D"));
    // Press A and D: slots 1 and 4
    expect(am4.location).withContext("am4.location").toEqual(2);
    expect(am4.scene).withContext("am4.scene").toEqual(3);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, false, true]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A03 Recto 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 4");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("UP"));
    // Press Up: next preset A04
    expect(am4.location).withContext("am4.location").toEqual(3);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A04 Deluxe 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.hold(S("UP"));
    // Hold Up: next bank (B01)
    expect(am4.location).withContext("am4.location").toEqual(4);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("B01 AC30 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay" });
    await t.expectSwitch(S("D"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.press(S("DOWN"));
    // Press Down: previous preset (A04)
    expect(am4.location).withContext("am4.location").toEqual(3);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A04 Deluxe 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.hold(S("DOWN"));
    // Hold DOWN: tuner on (CC 15 = 127)
    expect(am4.location).withContext("am4.location").toEqual(3);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(127);
    expect(await presetText()).withContext("await presetText()").toEqual("A04 Deluxe 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.hold(S("DOWN"));
    // Hold DOWN: tuner off (CC 15 = 0)
    expect(am4.location).withContext("am4.location").toEqual(3);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(0);
    expect(await presetText()).withContext("await presetText()").toEqual("A04 Deluxe 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "" });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "" });
    await t.expectSwitch(S("UP"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: null });

    t.expectOnlyWhitelisted();
})
