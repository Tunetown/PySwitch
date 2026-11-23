/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Effect states A and B (switches 1, 2), tuner on hold 1, rotary speed of A (switch A), amp on/off (switch B).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const tap = async (name) => { for (let i = 0; i < 4; ++i) await t.press(name, 100, 5); await t.ticks(); };
    t.startRecording();

    const c = async () => ({
        "t.param(new NRPNKey([50, 3]))": t.param(new NRPNKey([50, 3])),
        "t.param(new NRPNKey([51, 3]))": t.param(new NRPNKey([51, 3])),
        "t.param(new NRPNKey([127, 126]))": t.param(new NRPNKey([127, 126])),
        "await t.tunerShown()": await t.tunerShown(),
        "t.takeCCs()": t.takeCCs()
    });

    await t.ticks();
    // Start
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [5, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 2], [0, 0, 2], [0, 0, 2]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[3, 3, 3], [3, 3, 3], [3, 3, 3]], label: "Amp" });
    await t.press(S(1));
    // Press 1: A off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[17, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 2], [0, 0, 2], [0, 0, 2]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[3, 3, 3], [3, 3, 3], [3, 3, 3]], label: "Amp" });
    await t.press(S(2));
    // Press 2: B off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[18, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 2], [0, 0, 2], [0, 0, 2]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[3, 3, 3], [3, 3, 3], [3, 3, 3]], label: "Amp" });
    await t.press(S("A"));
    // Press A: rotary fast
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 36], [0, 0, 36], [0, 0, 36]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[3, 3, 3], [3, 3, 3], [3, 3, 3]], label: "Amp" });
    await t.press(S("A"));
    // Press A: rotary slow
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 2], [0, 0, 2], [0, 0, 2]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[3, 3, 3], [3, 3, 3], [3, 3, 3]], label: "Amp" });
    await t.press(S("B"));
    // Press B: amp
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 2], [0, 0, 2], [0, 0, 2]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[57, 57, 57], [57, 57, 57], [57, 57, 57]], label: "Amp" });
    await t.press(S("B"));
    // Press B: amp again
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 2], [0, 0, 2], [0, 0, 2]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[3, 3, 3], [3, 3, 3], [3, 3, 3]], label: "Amp" });
    await t.hold(S(1));
    // Hold 1: tuner on
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(1);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(true);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[31, 1]]);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], label: "Amp" });
    await t.press(S(2));
    // Press 2: tuner off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([127, 126]))).withContext("t.param(new NRPNKey([127, 126]))").toEqual(0);
    expect(await t.tunerShown()).withContext("await t.tunerShown()").toEqual(false);
    expect(t.takeCCs()).withContext("t.takeCCs()").toEqual([[31, 0]]);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 5, 5]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 2], [0, 0, 2], [0, 0, 2]], label: "A: Fast" });
    await t.expectSwitch(S("B"), { leds: [[3, 3, 3], [3, 3, 3], [3, 3, 3]], label: "Amp" });
})
