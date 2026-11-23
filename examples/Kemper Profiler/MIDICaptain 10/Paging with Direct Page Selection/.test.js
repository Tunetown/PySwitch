/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Page 1: effect states A-D (switches 1-4), rig select and morph 1-4 (A-D); page 2: effect states X, MOD, DLY, REV, looper (A-D). Up: next page, Down: page 2, bank up/down on hold Up/Down.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_10_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const fx = (slot) => t.param(new NRPNKey([slot, 3]));
    t.startRecording();

    const all = [S(1), S(2), S(3), S(4), S("UP"), S("A"), S("B"), S("C"), S("D"), S("DOWN")];
    const c = () => ({
        "t.client.getRigId()": t.client.getRigId(),
        "fx(50)": fx(50), "fx(56)": fx(56), "fx(58)": fx(58),
        "t.takeCCs()": t.takeCCs()
    });

    await t.setRigId(12);
    // Rig 3-3, page 1
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(56)).withContext("fx(56)").toEqual(1);
    expect(fx(58)).withContext("fx(58)").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.press(S(1));
    // Press 1: A off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(1);
    expect(fx(58)).withContext("fx(58)").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[17, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.press(S("B"));
    // Press B: rig 3-2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(1);
    expect(fx(58)).withContext("fx(58)").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[51, 1], [51, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.press(S("DOWN"));
    // Press Down: page 2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(1);
    expect(fx(58)).withContext("fx(58)").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 2], [5, 2, 2], [5, 2, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.press(S(1));
    // Press 1: X off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(fx(58)).withContext("fx(58)").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[22, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 2], [5, 2, 2], [5, 2, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.press(S(2));
    // Press 2: MOD off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(fx(58)).withContext("fx(58)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[24, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 2], [5, 2, 2], [5, 2, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.press(S("A"));
    // Press A: looper record
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(fx(58)).withContext("fx(58)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 2], [5, 2, 2], [5, 2, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.press(S("B"));
    // Press B: looper erase
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(fx(58)).withContext("fx(58)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 2], [5, 2, 2], [5, 2, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.press(S("UP"));
    // Press Up: page 1
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(fx(58)).withContext("fx(58)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
    await t.hold(S("UP"));
    // Hold Up: bank up
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(16);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(fx(58)).withContext("fx(58)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[48, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[76, 76, 76], [76, 76, 76], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("B"), { leds: [[30, 76, 30], [30, 76, 30], [76, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [2, 5, 2]], label: null });
    await t.hold(S("DOWN"));
    // Hold Down: bank down
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(fx(58)).withContext("fx(58)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[49, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[76, 76, 76], [76, 76, 76], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 5], [5, 5, 5], [5, 0, 0]], label: null });
})
