/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * AM4: all pages.
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

    await t.loadPreset(13, 1);
    await t.selectPage(S("UP"), "Presets");
    // Presets page, preset D02
    expect(am4.location).withContext("am4.location").toEqual(13);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("D02 5153 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "D01" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "5153 2" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 2" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Twin 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank C" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank E" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "D01" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.press(S(4));
    // Press 4: D04
    expect(am4.location).withContext("am4.location").toEqual(15);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("D04 Twin 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "AC30 2" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "D02" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 2" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Twin 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank C" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank E" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 2" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Clean 3" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.press(S("A"));
    // Press A: previous bank (C01)
    expect(am4.location).withContext("am4.location").toEqual(8);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C01 Clean 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Clean 2" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 2" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Recto 2" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "C04" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank B" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank D" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "B04" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.press(S("D"));
    // Press D: next preset (C02)
    expect(am4.location).withContext("am4.location").toEqual(9);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C02 Plexi 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Clean 2" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Plexi 2" });
    await t.expectSwitch(S("3"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Recto 2" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Deluxe 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank B" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Bank D" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Clean 2" });
    await t.expectSwitch(S("D"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Recto 2" });
    await t.expectSwitch(S("UP"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.selectPage(S("UP"), "Scenes + Effects");
    await t.press(S(3));
    await t.press(S("B"));
    // Scenes + Effects page: scene 3, slot 2
    expect(am4.location).withContext("am4.location").toEqual(9);
    expect(am4.scene).withContext("am4.scene").toEqual(2);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, true, false, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C02 Plexi 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("3 Lead");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene 4" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Compressor" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp" });
    await t.expectSwitch(S("C"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Chorus" });
    await t.expectSwitch(S("D"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[38, 0, 0], [38, 0, 0], [38, 0, 0]], label: "Scenes + Effects" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.selectPage(S("UP"), "Modes");
    await t.press(S("A"));
    // Modes page, press A: AM4 tuner mode
    expect(am4.location).withContext("am4.location").toEqual(9);
    expect(am4.scene).withContext("am4.scene").toEqual(2);
    expect(am4.mode).withContext("am4.mode").toEqual(24);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, true, false, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C02 Plexi 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("3 Lead");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Presets" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Scenes" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Effects" });
    await t.expectSwitch(S("4"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Amp" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Tuner" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset -1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset +1" });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene +1" });
    await t.expectSwitch(S("UP"), { leds: [[0, 0, 38], [0, 0, 38], [0, 0, 38]], label: "Modes" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.press(S("D"));
    // Modes page, press D: next scene (4)
    expect(am4.location).withContext("am4.location").toEqual(9);
    expect(am4.scene).withContext("am4.scene").toEqual(3);
    expect(am4.mode).withContext("am4.mode").toEqual(24);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, false, false, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C02 Plexi 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("Scene 4");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Presets" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Scenes" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Effects" });
    await t.expectSwitch(S("4"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Amp" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Tuner" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset -1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset +1" });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene +1" });
    await t.expectSwitch(S("UP"), { leds: [[0, 0, 38], [0, 0, 38], [0, 0, 38]], label: "Modes" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.press(S("C"));
    // Modes page, press C: next preset (C03)
    expect(am4.location).withContext("am4.location").toEqual(10);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(24);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C03 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Presets" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Scenes" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Effects" });
    await t.expectSwitch(S("4"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Amp" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Tuner" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset -1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset +1" });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene +1" });
    await t.expectSwitch(S("UP"), { leds: [[0, 0, 38], [0, 0, 38], [0, 0, 38]], label: "Modes" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.press(S("DOWN"));
    // Press DOWN: tuner on (CC 15 = 127)
    expect(am4.location).withContext("am4.location").toEqual(10);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(24);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(127);
    expect(await presetText()).withContext("await presetText()").toEqual("C03 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Presets" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Scenes" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Effects" });
    await t.expectSwitch(S("4"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Amp" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Tuner" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset -1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset +1" });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene +1" });
    await t.expectSwitch(S("UP"), { leds: [[0, 0, 38], [0, 0, 38], [0, 0, 38]], label: "Modes" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });
    await t.press(S("DOWN"));
    // Press DOWN: tuner off (CC 15 = 0)
    expect(am4.location).withContext("am4.location").toEqual(10);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(24);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(0);
    expect(await presetText()).withContext("await presetText()").toEqual("C03 Recto 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Presets" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Scenes" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Effects" });
    await t.expectSwitch(S("4"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Amp" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Tuner" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset -1" });
    await t.expectSwitch(S("C"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Preset +1" });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Scene +1" });
    await t.expectSwitch(S("UP"), { leds: [[0, 0, 38], [0, 0, 38], [0, 0, 38]], label: "Modes" });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: null });

    t.expectOnlyWhitelisted();
})
