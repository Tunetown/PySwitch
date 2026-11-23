/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Effect states (extended names) A, B, DLY, REV (switches 1, 2, A, B), bank down/up on hold 1/2.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const set = (key, value) => t.client.parameters.get(key).setValue(value);
    const tap = async (name) => { for (let i = 0; i < 4; ++i) await t.press(name, 100, 5); await t.ticks(); };
    t.startRecording();

    const c = () => ({
        "t.client.getRigId()": t.client.getRigId(),
        "t.param(new NRPNKey([50, 3]))": t.param(new NRPNKey([50, 3])),
        "t.param(new NRPNKey([51, 3]))": t.param(new NRPNKey([51, 3])),
        "t.param(new NRPNKey([60, 3]))": t.param(new NRPNKey([60, 3])),
        "t.param(new NRPNKey([61, 3]))": t.param(new NRPNKey([61, 3]))
    });

    await t.setRigId(12);
    // Rig 3-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[76, 37, 0], [76, 37, 0], [5, 0, 0]], label: "Wah RR" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [5, 0, 0]], label: "VinylStp" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "LoopPitch" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Echo" });
    await t.press(S(1));
    // Press 1: A off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "Wah RR" });
    await t.expectSwitch(S("2"), { leds: [[76, 37, 0], [76, 37, 0], [5, 0, 0]], label: "VinylStp" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "LoopPitch" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Echo" });
    await t.press(S(2));
    // Press 2: B off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "Wah RR" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "VinylStp" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "LoopPitch" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Echo" });
    await t.press(S("A"));
    // Press A: DLY off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "Wah RR" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "VinylStp" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "LoopPitch" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Echo" });
    await t.press(S("B"));
    // Press B: REV off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "Wah RR" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "VinylStp" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "LoopPitch" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Echo" });
    await t.hold(S(2));
    // Hold 2: bank up
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(17);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [2, 5, 2]], label: "Wah RR" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [2, 5, 2]], label: "VinylStp" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "LoopPitch" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Echo" });
    await t.hold(S(1));
    // Hold 1: bank down
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "Wah RR" });
    await t.expectSwitch(S("2"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "VinylStp" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "LoopPitch" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Echo" });
    set(new NRPNKey([51, 0]), 104);
    await t.ticks();
    // Effect type of B changed on the device (type 104)
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([50, 3]))).withContext("t.param(new NRPNKey([50, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([51, 3]))).withContext("t.param(new NRPNKey([51, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 2, 0], [5, 2, 0], [5, 0, 0]], label: "Wah RR" });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [5, 0, 0]], label: "Double" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "LoopPitch" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Echo" });
})
