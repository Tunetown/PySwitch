/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Bank preselect 1-5 (switches 1-4, Up), rig select 1-5 (A-D, Down), effect states A-D on hold A-D.
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
        "t.param(new CCKey(47))": t.param(new CCKey(47)),
        "fx(50)": fx(50), "fx(51)": fx(51), "fx(52)": fx(52), "fx(53)": fx(53)
    });

    await t.setRigId(12);
    // Rig 3-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(null);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("4"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("UP"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [0, 76, 76]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.press(S(2));
    // Press 2: bank 2 preselected
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(1);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("4"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("UP"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[76, 76, 0], [76, 76, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[76, 76, 0], [76, 76, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 76, 0], [76, 76, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[76, 76, 0], [76, 76, 0], [0, 76, 76]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: null });
    await t.press(S("C"));
    // Press C: rig 2-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(7);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(null);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: null });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("4"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("UP"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 5, 0], [5, 5, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 5, 0], [5, 5, 0], [76, 37, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 76, 0], [76, 76, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 5, 0], [5, 5, 0], [0, 76, 76]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: null });
    await t.press(S("UP"));
    // Press Up: bank 5 preselected
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(7);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(4);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: null });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("4"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("UP"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[54, 0, 36], [54, 0, 36], [76, 37, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[54, 0, 36], [54, 0, 36], [76, 37, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[54, 0, 36], [54, 0, 36], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[54, 0, 36], [54, 0, 36], [0, 76, 76]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[54, 0, 36], [54, 0, 36], [54, 0, 36]], label: null });
    await t.press(S("DOWN"));
    // Press Down: rig 5-5
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(24);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(null);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("4"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("UP"), { leds: [[54, 0, 36], [54, 0, 36], [54, 0, 36]], label: null });
    await t.expectSwitch(S("A"), { leds: [[3, 0, 2], [3, 0, 2], [76, 37, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[3, 0, 2], [3, 0, 2], [76, 37, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[3, 0, 2], [3, 0, 2], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[3, 0, 2], [3, 0, 2], [0, 76, 76]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[54, 0, 36], [54, 0, 36], [54, 0, 36]], label: null });
    await t.hold(S("A"));
    // Hold A: effect A off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(24);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(null);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("4"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("UP"), { leds: [[54, 0, 36], [54, 0, 36], [54, 0, 36]], label: null });
    await t.expectSwitch(S("A"), { leds: [[3, 0, 2], [3, 0, 2], [5, 2, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[3, 0, 2], [3, 0, 2], [76, 37, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[3, 0, 2], [3, 0, 2], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[3, 0, 2], [3, 0, 2], [0, 76, 76]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[54, 0, 36], [54, 0, 36], [54, 0, 36]], label: null });
    await t.hold(S("D"));
    // Hold D: effect D off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(24);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(null);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 5]], label: null });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("4"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("UP"), { leds: [[54, 0, 36], [54, 0, 36], [54, 0, 36]], label: null });
    await t.expectSwitch(S("A"), { leds: [[3, 0, 2], [3, 0, 2], [5, 2, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[3, 0, 2], [3, 0, 2], [76, 37, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[3, 0, 2], [3, 0, 2], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[3, 0, 2], [3, 0, 2], [0, 5, 5]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[54, 0, 36], [54, 0, 36], [54, 0, 36]], label: null });
})
