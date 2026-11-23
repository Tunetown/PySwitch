/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Kemper effect buttons I-IV (switches 1, 2, A, B): CC messages.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const tap = async (name) => { for (let i = 0; i < 4; ++i) await t.press(name, 100, 5); await t.ticks(); };
    t.startRecording();

    const c = () => ({ "t.takeCCs()": t.takeCCs() });

    await t.ticks();
    // Start
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX I" });
    await t.expectSwitch(S("2"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX II" });
    await t.expectSwitch(S("A"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX III" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX IIII" });
    await t.press(S(1));
    // Press 1
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[75, 1]]);
    await t.expectSwitch(S("1"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "FX I" });
    await t.expectSwitch(S("2"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX II" });
    await t.expectSwitch(S("A"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX III" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX IIII" });
    await t.press(S(1));
    // Press 1 again
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[75, 0]]);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX I" });
    await t.expectSwitch(S("2"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX II" });
    await t.expectSwitch(S("A"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX III" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX IIII" });
    await t.press(S(2));
    // Press 2
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[76, 1]]);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX I" });
    await t.expectSwitch(S("2"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "FX II" });
    await t.expectSwitch(S("A"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX III" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX IIII" });
    await t.press(S("A"));
    // Press A
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[77, 1]]);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX I" });
    await t.expectSwitch(S("2"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "FX II" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "FX III" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX IIII" });
    await t.press(S("B"));
    // Press B
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[78, 1]]);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "FX I" });
    await t.expectSwitch(S("2"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "FX II" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "FX III" });
    await t.expectSwitch(S("B"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "FX IIII" });
})
