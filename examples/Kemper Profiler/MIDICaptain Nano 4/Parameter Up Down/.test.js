/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Reverb mix up/down (switches 1, A), amp gain up/down (switches 2, B): parameter set messages.
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
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Rev Up" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Gain Up" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rev Down" });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Gain Down" });
    await t.press(S(1));
    // Press 1: reverb mix up
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[0, 2, 0], [0, 2, 0], [0, 2, 0]], label: "Rev Up" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Gain Up" });
    await t.expectSwitch(S("A"), { leds: [[29, 74, 29], [29, 74, 29], [29, 74, 29]], label: "Rev Down" });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Gain Down" });
    await t.press(S("A"));
    // Press A: reverb mix down
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Rev Up" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Gain Up" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rev Down" });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Gain Down" });
    await t.press(S(2));
    // Press 2: gain up
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Rev Up" });
    await t.expectSwitch(S("2"), { leds: [[2, 0, 0], [2, 0, 0], [2, 0, 0]], label: "Gain Up" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rev Down" });
    await t.expectSwitch(S("B"), { leds: [[74, 0, 0], [74, 0, 0], [74, 0, 0]], label: "Gain Down" });
    await t.press(S("B"));
    // Press B: gain down
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Rev Up" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Gain Up" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rev Down" });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Gain Down" });
})
