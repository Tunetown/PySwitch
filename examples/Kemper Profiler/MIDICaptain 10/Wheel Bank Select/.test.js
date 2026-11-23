/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Effect states A-D (switches 1-4), rig select 1-5 (A-D, Down), bank down/up on hold A/Down, tap tempo (Up), tuner on hold Up. The wheel is not tested.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_10_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const fx = (slot) => t.param(new NRPNKey([slot, 3]));
    t.startRecording();

    const all = [S(1), S(2), S(3), S(4), S("UP"), S("A"), S("B"), S("C"), S("D"), S("DOWN")];
    const c = async () => ({
        "t.client.getRigId()": t.client.getRigId(),
        "fx(50)": fx(50), "fx(51)": fx(51), "fx(52)": fx(52), "fx(53)": fx(53),
        "t.param(new NRPNKey([127, 126]))": t.param(new NRPNKey([127, 126])),
        "await t.tunerShown()": await t.tunerShown(),
        "t.takeCCs()": t.takeCCs()
    });

    await t.setRigId(12);
    // Rig 3-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 0, 0], [5, 0, 0], [2, 5, 2]], label: null });
    await t.press(S("B"));
    // Press B: rig 3-2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[51, 1], [51, 0]]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[5, 0, 0], [5, 0, 0], [2, 5, 2]], label: null });
    await t.press(S("DOWN"));
    // Press Down: rig 3-5
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(14);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[54, 1], [54, 0]]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: null });
    await t.hold(S("DOWN"));
    // Hold Down: bank up
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(19);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[48, 0]]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[1, 5, 1], [1, 5, 1], [5, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("C"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("D"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[30, 76, 30], [30, 76, 30], [3, 0, 2]], label: null });
    await t.hold(S("A"));
    // Hold A: bank down
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(14);
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[49, 0]]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: null });
    await t.press(S(1));
    // Press 1: A off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(14);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(0);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[17, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: null });
    await t.press(S(3));
    // Press 3: C on
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(14);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(1);
    expect(fx(53)).withContext("fx(53)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[19, 1]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 76, 76], [0, 76, 76], [0, 76, 76]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: null });
    await t.press(S(4));
    // Press 4: D off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(14);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(1);
    expect(fx(53)).withContext("fx(53)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[20, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: null });
    for (let i = 0; i < 4; ++i) await t.press(S("UP"), 100, 5);
    await t.ticks();
    // Tap Up 4 times: CC 30 sent
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(14);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(1);
    expect(fx(53)).withContext("fx(53)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[30, 1], [30, 0], [30, 1], [30, 0], [30, 1], [30, 0], [30, 1], [30, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: null });
    await t.hold(S("UP"));
    // Hold Up: tuner on
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(14);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(1);
    expect(fx(53)).withContext("fx(53)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(1);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(true);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[31, 1]]);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: null });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: null });
    await t.press(S(1));
    // Press 1: tuner off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(14);
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(52)).withContext("fx(52)").toEqual(1);
    expect(fx(53)).withContext("fx(53)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[31, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Dist" });
    await t.expectSwitch(S("4"), { leds: [[0, 5, 5], [0, 5, 5], [0, 5, 5]], label: "Comp" });
    await t.expectSwitch(S("UP"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: null });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("C"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("D"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: null });
    await t.expectSwitch(S("DOWN"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: null });
})
