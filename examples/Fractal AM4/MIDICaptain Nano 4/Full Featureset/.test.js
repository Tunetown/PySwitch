/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * AM4: all pages.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new FractalAM4TestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
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

    await t.loadPreset(4, 0);
    await t.selectPage(S("B"), "Presets");
    // Presets page, preset B01
    expect(am4.location).withContext("am4.location").toEqual(4);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("B01 AC30 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "AC30 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "5153 1" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.press(S(2));
    // Press 2: B02
    expect(am4.location).withContext("am4.location").toEqual(5);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("B02 5153 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "AC30 1" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "5153 1" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "JCM800 1" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.hold(S(2));
    // Hold 2: next bank (C01)
    expect(am4.location).withContext("am4.location").toEqual(8);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C01 Clean 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Clean 2" });
    await t.expectSwitch(S("2"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Plexi 2" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Recto 2" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 0], [0, 38, 0], [0, 38, 0]], label: "Presets" });
    await t.selectPage(S("B"), "Scenes");
    // Scenes page
    expect(am4.location).withContext("am4.location").toEqual(8);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C01 Clean 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("B"), { leds: [[38, 0, 0], [38, 0, 0], [38, 0, 0]], label: "Scenes" });
    await t.press(S("A"));
    // Press A: next scene
    expect(am4.location).withContext("am4.location").toEqual(8);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C01 Clean 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Lead" });
    await t.expectSwitch(S("B"), { leds: [[38, 0, 0], [38, 0, 0], [38, 0, 0]], label: "Scenes" });
    await t.selectPage(S("B"), "Effects");
    await t.press(S(1));
    // Effects page, press 1: slot 1
    expect(am4.location).withContext("am4.location").toEqual(8);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C01 Clean 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive" });
    await t.expectSwitch(S("2"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 38, 38], [0, 38, 38], [0, 38, 38]], label: "Effects" });
    await t.selectPage(S("B"), "Modes");
    await t.press(S(2));
    // Modes page, press 2: AM4 scene mode
    expect(am4.location).withContext("am4.location").toEqual(8);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(73);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("C01 Clean 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Presets" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Scenes" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Effects" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 38], [0, 0, 38], [0, 0, 38]], label: "Modes" });
    await t.hold(S("B"));
    // Hold B: tuner on (CC 15 = 127)
    expect(am4.location).withContext("am4.location").toEqual(8);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(73);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(127);
    expect(await presetText()).withContext("await presetText()").toEqual("C01 Clean 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Presets" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Scenes" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Effects" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 38], [0, 0, 38], [0, 0, 38]], label: "Modes" });
    await t.hold(S("B"));
    // Hold B: tuner off (CC 15 = 0)
    expect(am4.location).withContext("am4.location").toEqual(8);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(73);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(0);
    expect(await presetText()).withContext("await presetText()").toEqual("C01 Clean 2");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Presets" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Scenes" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Effects" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 38], [0, 0, 38], [0, 0, 38]], label: "Modes" });

    t.expectOnlyWhitelisted();
})
