/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Effect states A, B, DLY, REV (switches 1, 2, A, B), tuner (3), rig volume boost (C).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_MINI_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const fx = (slot) => t.param(new NRPNKey([slot, 3]));
    t.startRecording();

    const all = [S(1), S(2), S(3), S("A"), S("B"), S("C")];
    const c = async () => ({
        "fx(50)": fx(50), "fx(51)": fx(51), "fx(60)": fx(60), "fx(61)": fx(61),
        "t.param(new NRPNKey([127, 126]))": t.param(new NRPNKey([127, 126])),
        "await t.tunerShown()": await t.tunerShown(),
        "t.takeCCs()": t.takeCCs()
    });

    await t.ticks();
    // Start
    expect(fx(50)).withContext("fx(50)").toEqual(1);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(60)).withContext("fx(60)").toEqual(1);
    expect(fx(61)).withContext("fx(61)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "Boost" });
    await t.press(S(1));
    // Press 1: A off
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(1);
    expect(fx(60)).withContext("fx(60)").toEqual(1);
    expect(fx(61)).withContext("fx(61)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[17, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "Boost" });
    await t.press(S(2));
    // Press 2: B off
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(0);
    expect(fx(60)).withContext("fx(60)").toEqual(1);
    expect(fx(61)).withContext("fx(61)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[18, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "Boost" });
    await t.press(S("A"));
    // Press A: DLY off
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(0);
    expect(fx(60)).withContext("fx(60)").toEqual(0);
    expect(fx(61)).withContext("fx(61)").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[27, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "Boost" });
    await t.press(S("B"));
    // Press B: REV off
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(0);
    expect(fx(60)).withContext("fx(60)").toEqual(0);
    expect(fx(61)).withContext("fx(61)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[29, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "Boost" });
    await t.press(S("C"));
    // Press C: boost on
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(0);
    expect(fx(60)).withContext("fx(60)").toEqual(0);
    expect(fx(61)).withContext("fx(61)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[76, 37, 21], [76, 37, 21], [76, 37, 21]], label: "Boost" });
    await t.press(S("C"));
    // Press C: boost off
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(0);
    expect(fx(60)).withContext("fx(60)").toEqual(0);
    expect(fx(61)).withContext("fx(61)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "Boost" });
    await t.press(S(3));
    // Press 3: tuner on
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(0);
    expect(fx(60)).withContext("fx(60)").toEqual(0);
    expect(fx(61)).withContext("fx(61)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(1);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(true);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[31, 1]]);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Boost" });
    await t.press(S(3));
    // Press 3: tuner off
    expect(fx(50)).withContext("fx(50)").toEqual(0);
    expect(fx(51)).withContext("fx(51)").toEqual(0);
    expect(fx(60)).withContext("fx(60)").toEqual(0);
    expect(fx(61)).withContext("fx(61)").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[31, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("3"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
    await t.expectSwitch(S("C"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "Boost" });
})
