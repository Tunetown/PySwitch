/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Upper pager (Up): effect states A-D or X, MOD, DLY, REV (switches 1-4). Lower pager (Down): rig select and morph 1-4 or looper (A-D). Bank up/down on hold Up/Down.
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
        "fx(50)": fx(50), "fx(56)": fx(56),
        "t.takeCCs()": t.takeCCs()
    });

    await t.setRigId(12);
    // Rig 3-3, both pagers on page 1
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(56)).withContext("fx(56)").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[7, 7, 7], [7, 7, 7], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[7, 7, 7], [7, 7, 7], [5, 0, 0]], label: null });
    await t.press(S(1));
    // Press 1: A off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[17, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[7, 7, 7], [7, 7, 7], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[7, 7, 7], [7, 7, 7], [5, 0, 0]], label: null });
    await t.press(S("UP"));
    // Press Up: upper page 2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[38, 38, 38], [38, 38, 38], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[7, 7, 7], [7, 7, 7], [5, 0, 0]], label: null });
    await t.press(S(1));
    // Press 1: X off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[22, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[38, 38, 38], [38, 38, 38], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[7, 7, 7], [7, 7, 7], [5, 0, 0]], label: null });
    await t.press(S("C"));
    // Press C: rig 3-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[52, 1], [52, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[38, 38, 38], [38, 38, 38], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[7, 7, 7], [7, 7, 7], [5, 0, 0]], label: null });
    await t.press(S("DOWN"));
    // Press Down: lower page 2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[38, 38, 38], [38, 38, 38], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 2], [5, 2, 2], [5, 2, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[38, 38, 38], [38, 38, 38], [5, 0, 0]], label: null });
    await t.press(S("A"));
    // Press A: looper record
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[38, 38, 38], [38, 38, 38], [5, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 2], [5, 2, 2], [5, 2, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[38, 38, 38], [38, 38, 38], [5, 0, 0]], label: null });
    await t.hold(S("UP"));
    // Hold Up: bank up
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(17);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(56)).withContext("fx(56)").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[48, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Boost" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("3"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("UP"), { leds: [[38, 38, 38], [38, 38, 38], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 2], [5, 2, 2], [5, 2, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[38, 38, 38], [38, 38, 38], [2, 5, 2]], label: null });
})
