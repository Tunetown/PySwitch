/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Tuner (switch 1), rig volume boost (switch 2), effect states A and B (switches A, B).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const tap = async (name) => { for (let i = 0; i < 4; ++i) await t.press(name, 100, 5); await t.ticks(); };
    t.startRecording();

    const c = async () => ({
        "t.param(new NRPNKey([127, 126]))": t.param(new NRPNKey([127, 126])),
        "await t.tunerShown()": await t.tunerShown(),
        "t.param(new NRPNKey([50, 3]))": t.param(new NRPNKey([50, 3])),
        "t.param(new NRPNKey([51, 3]))": t.param(new NRPNKey([51, 3])),
        "t.takeCCs()": t.takeCCs()
    });

    await t.ticks();
    // Start
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "RigBoost" });
    await t.expectSwitch(S("A"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.press(S(2));
    // Press 2: boost on
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 21], [76, 37, 21], [76, 37, 21]], label: "RigBoost" });
    await t.expectSwitch(S("A"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.press(S(2));
    // Press 2: boost off
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "RigBoost" });
    await t.expectSwitch(S("A"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.press(S("A"));
    // Press A: A off
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[17, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "RigBoost" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.press(S("B"));
    // Press B: B off
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[18, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "RigBoost" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.press(S(1));
    // Press 1: tuner on
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(1);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(true);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[31, 1]]);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Tuner" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "RigBoost" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Wah" });
    await t.press(S(1));
    // Press 1: tuner off
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[31, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], label: "Tuner" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 1], [5, 2, 1], [5, 2, 1]], label: "RigBoost" });
    await t.expectSwitch(S("A"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("B"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
})
