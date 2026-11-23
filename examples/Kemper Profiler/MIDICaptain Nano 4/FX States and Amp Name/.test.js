/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Effect states A, B, DLY, REV (switches 1, 2, A, B), labels and colors follow the effect types.
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
        "t.param(new NRPNKey([60, 3]))": t.param(new NRPNKey([60, 3])),
        "t.param(new NRPNKey([61, 3]))": t.param(new NRPNKey([61, 3]))
    });

    await t.ticks();
    // Start
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.press(S(1));
    // Press 1: A off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.press(S(2));
    // Press 2: B off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.press(S("A"));
    // Press A: DLY off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.press(S("B"));
    // Press B: REV off
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
    await t.press(S(1));
    // Press 1: A on
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [76, 37, 0]], label: "Wah" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
    set(new NRPNKey([50, 0]), 104);
    await t.ticks();
    // Effect type of A changed on the device (type 104)
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "EQ" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
    set(new NRPNKey([50, 0]), 0);
    await t.ticks();
    // Slot A empty
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[1, 1, 1], [1, 1, 1], [1, 1, 1]], label: "-" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 2, 0]], label: "Wah" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
})
