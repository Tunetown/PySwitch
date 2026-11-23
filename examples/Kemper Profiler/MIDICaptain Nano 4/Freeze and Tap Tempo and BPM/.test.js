/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Effect states A and B (switches 1, 2), reverb freeze (A, momentary), tap tempo with BPM display (B).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const tap = async (name) => { for (let i = 0; i < 4; ++i) await t.press(name, 100, 5); await t.ticks(); };
    t.startRecording();

    const c = () => ({
        "t.param(new NRPNKey([50, 3]))": t.param(new NRPNKey([50, 3])),
        "t.param(new NRPNKey([51, 3]))": t.param(new NRPNKey([51, 3])),
        "t.takeCCs()": t.takeCCs()
    });

    t.client.tempo.set(120);
    await t.ticks();
    // Start, 120 bpm
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[1, 2, 0], [1, 2, 0], [1, 2, 0]], label: "RvFreeze" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.press(S(1));
    // Press 1: A off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[17, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[1, 2, 0], [1, 2, 0], [1, 2, 0]], label: "RvFreeze" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.press(S(2));
    // Press 2: B off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[18, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[1, 2, 0], [1, 2, 0], [1, 2, 0]], label: "RvFreeze" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await t.press(S("A"));
    // Press A: freeze (momentary)
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[1, 2, 0], [1, 2, 0], [1, 2, 0]], label: "RvFreeze" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
    await tap(S("B"));
    // Tap 4 times (900 ms): CC 30 sent (the virtual Kemper measures the taps in real time, so its BPM is not checked)
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[30, 1], [30, 0], [30, 1], [30, 0], [30, 1], [30, 0], [30, 1], [30, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[1, 2, 0], [1, 2, 0], [1, 2, 0]], label: "RvFreeze" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: null });
})
