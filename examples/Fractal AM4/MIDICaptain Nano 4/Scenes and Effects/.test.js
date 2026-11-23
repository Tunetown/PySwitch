/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * AM4: scenes and effects of slots 1 and 2.
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

    await t.loadPreset(0, 0);
    // Preset A01, scene 1
    expect(am4.location).withContext("am4.location").toEqual(0);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A01 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.press(S(2));
    // Press 2: scene 2
    expect(am4.location).withContext("am4.location").toEqual(0);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A01 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.press(S("A"));
    // Press A: slot 1 (drive) bypassed
    expect(am4.location).withContext("am4.location").toEqual(0);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A01 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.press(S("B"));
    // Press B: slot 2 (amp) bypassed
    expect(am4.location).withContext("am4.location").toEqual(0);
    expect(am4.scene).withContext("am4.scene").toEqual(1);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, true, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A01 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("2 Crunch");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Amp" });
    await t.press(S(1));
    // Press 1: scene 1
    expect(am4.location).withContext("am4.location").toEqual(0);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A01 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Drive" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    am4.setBypass(0, false);
    await t.ticks();
    // Slot 1 engaged on the device
    expect(am4.location).withContext("am4.location").toEqual(0);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A01 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    am4.setName("My Scene", 0);
    await t.ticks();
    // Scene 1 renamed on the device
    expect(am4.location).withContext("am4.location").toEqual(0);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A01 Clean 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 My Scene");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "My Scene" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Drive" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.loadPreset(3, 2);
    // Preset A04 (amp, reverb), scene 3 (no name)
    expect(am4.location).withContext("am4.location").toEqual(3);
    expect(am4.scene).withContext("am4.scene").toEqual(2);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([false, false, false, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A04 Deluxe 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("3 Lead");
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Reverb" });
    await t.loadPreset(1);
    // Preset A02 (compressor, amp)
    expect(am4.location).withContext("am4.location").toEqual(1);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(null);
    expect(await presetText()).withContext("await presetText()").toEqual("A02 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Compressor" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.hold(S("B"));
    // Hold B: tuner on (CC 15 = 127)
    expect(am4.location).withContext("am4.location").toEqual(1);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(127);
    expect(await presetText()).withContext("await presetText()").toEqual("A02 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Compressor" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });
    await t.hold(S("B"));
    // Hold B: tuner off (CC 15 = 0)
    expect(am4.location).withContext("am4.location").toEqual(1);
    expect(am4.scene).withContext("am4.scene").toEqual(0);
    expect(am4.mode).withContext("am4.mode").toEqual(null);
    expect(am4.preset.bypass[am4.scene]).withContext("am4.preset.bypass[am4.scene]").toEqual([true, false, true, false]);
    expect(am4.cc[15] ?? null).withContext("am4.cc[15] ?? null").toEqual(0);
    expect(await presetText()).withContext("await presetText()").toEqual("A02 Plexi 1");
    expect(await sceneText()).withContext("await sceneText()").toEqual("1 Clean");
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Clean" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Crunch" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Compressor" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Amp" });

    t.expectOnlyWhitelisted();
})
