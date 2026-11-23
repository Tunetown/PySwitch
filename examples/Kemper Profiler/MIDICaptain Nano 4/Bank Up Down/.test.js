/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Bank down/up (switches 1, 2), effect states DLY and REV (switches A, B).
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
        "t.param(new NRPNKey([60, 3]))": t.param(new NRPNKey([60, 3])),
        "t.param(new NRPNKey([61, 3]))": t.param(new NRPNKey([61, 3]))
    });

    await t.setRigId(12);
    // Rig 3-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.press(S(2));
    // Press 2: bank up
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(17);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.press(S(1));
    // Press 1: bank down
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.press(S("A"));
    // Press A: DLY off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(0);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    await t.press(S("A"));
    // Press A: DLY on
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
    set(new NRPNKey([61, 3]), 0);
    await t.ticks();
    // REV switched off on the device
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(0);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 5, 0], [0, 5, 0], [0, 5, 0]], label: "Reverb" });
    await t.press(S("B"));
    // Press B: REV on
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new NRPNKey([60, 3]))).withContext("t.param(new NRPNKey([60, 3]))").toEqual(1);
    expect(t.param(new NRPNKey([61, 3]))).withContext("t.param(new NRPNKey([61, 3]))").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Delay" });
    await t.expectSwitch(S("B"), { leds: [[0, 76, 0], [0, 76, 0], [0, 76, 0]], label: "Reverb" });
})
