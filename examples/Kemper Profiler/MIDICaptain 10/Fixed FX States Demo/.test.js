/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Fixed effect states Transpose, Gate, Comp, Boost, Wah, Chorus, Air, Double Tracker (switches 1-4, Up, A-C).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_10_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const fx = (slot) => t.param(new NRPNKey([slot, 3]));
    t.startRecording();

    const all = [S(1), S(2), S(3), S(4), S("UP"), S("A"), S("B"), S("C")];
    const fixed = (n) => t.param(new NRPNKey([5, n]));
    const c = () => ({
        "fixed(1)": fixed(1), "fixed(6)": fixed(6), "fixed(11)": fixed(11), "fixed(16)": fixed(16),
        "fixed(21)": fixed(21), "fixed(26)": fixed(26), "fixed(36)": fixed(36), "fixed(41)": fixed(41)
    });

    await t.ticks();
    // Start: all off
    expect(fixed(1)).withContext("fixed(1)").toEqual(0);
    expect(fixed(6)).withContext("fixed(6)").toEqual(0);
    expect(fixed(11)).withContext("fixed(11)").toEqual(0);
    expect(fixed(16)).withContext("fixed(16)").toEqual(0);
    expect(fixed(21)).withContext("fixed(21)").toEqual(0);
    expect(fixed(26)).withContext("fixed(26)").toEqual(0);
    expect(fixed(36)).withContext("fixed(36)").toEqual(0);
    expect(fixed(41)).withContext("fixed(41)").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Transpose" });
    await t.expectSwitch(S("2"), { leds: [[2, 2, 5], [2, 2, 5], [2, 2, 5]], label: "Gate" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: "Comp" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("UP"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    for (const name of all) {
        await t.press(name);
    }
    // All pressed: all on
    expect(fixed(1)).withContext("fixed(1)").toEqual(1);
    expect(fixed(6)).withContext("fixed(6)").toEqual(1);
    expect(fixed(11)).withContext("fixed(11)").toEqual(1);
    expect(fixed(16)).withContext("fixed(16)").toEqual(1);
    expect(fixed(21)).withContext("fixed(21)").toEqual(1);
    expect(fixed(26)).withContext("fixed(26)").toEqual(1);
    expect(fixed(36)).withContext("fixed(36)").toEqual(1);
    expect(fixed(41)).withContext("fixed(41)").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[76, 76, 76], [76, 76, 76], [76, 76, 76]], label: "Transpose" });
    await t.expectSwitch(S("2"), { leds: [[30, 30, 76], [30, 30, 76], [30, 30, 76]], label: "Gate" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: "Comp" });
    await t.expectSwitch(S("4"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("UP"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.press(S(1));
    await t.press(S("C"));
    // Press 1 and C: Transpose and Double Tracker off
    expect(fixed(1)).withContext("fixed(1)").toEqual(0);
    expect(fixed(6)).withContext("fixed(6)").toEqual(1);
    expect(fixed(11)).withContext("fixed(11)").toEqual(1);
    expect(fixed(16)).withContext("fixed(16)").toEqual(1);
    expect(fixed(21)).withContext("fixed(21)").toEqual(1);
    expect(fixed(26)).withContext("fixed(26)").toEqual(1);
    expect(fixed(36)).withContext("fixed(36)").toEqual(1);
    expect(fixed(41)).withContext("fixed(41)").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Transpose" });
    await t.expectSwitch(S("2"), { leds: [[30, 30, 76], [30, 30, 76], [30, 30, 76]], label: "Gate" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: "Comp" });
    await t.expectSwitch(S("4"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("UP"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    set(new NRPNKey([5, 16]), 0);
    await t.ticks();
    // Boost switched off on the device
    expect(fixed(1)).withContext("fixed(1)").toEqual(0);
    expect(fixed(6)).withContext("fixed(6)").toEqual(1);
    expect(fixed(11)).withContext("fixed(11)").toEqual(1);
    expect(fixed(16)).withContext("fixed(16)").toEqual(0);
    expect(fixed(21)).withContext("fixed(21)").toEqual(1);
    expect(fixed(26)).withContext("fixed(26)").toEqual(1);
    expect(fixed(36)).withContext("fixed(36)").toEqual(1);
    expect(fixed(41)).withContext("fixed(41)").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Transpose" });
    await t.expectSwitch(S("2"), { leds: [[30, 30, 76], [30, 30, 76], [30, 30, 76]], label: "Gate" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: "Comp" });
    await t.expectSwitch(S("4"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("UP"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 76], [0, 0, 76], [0, 0, 76]], label: null });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
})
