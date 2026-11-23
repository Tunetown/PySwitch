/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Bank select (switches 1, 2), rig select (switches A, B), morph state on the second LED segment of all switches.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const c = () => ({ "t.client.getRigId()": t.client.getRigId() });
    const morph = (value) => t.client.parameters.get(new NRPNKey([0, 11])).setValue(value);

    await t.setRigId(12);
    // Rig 3-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [76, 0, 0]], label: "Bank 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [76, 0, 0]], label: "Bank 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [76, 0, 0]], label: "Rig 3-1" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [76, 0, 0]], label: "Rig 3-2" });

    await t.press(S(2));
    // Press 2: bank 2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(7);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [76, 0, 0]], label: "Bank 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 0, 0]], label: "Bank 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 5, 0], [5, 5, 0], [76, 0, 0]], label: "Rig 2-1" });
    await t.expectSwitch(S("B"), { leds: [[5, 5, 0], [5, 5, 0], [76, 0, 0]], label: "Rig 2-2" });

    await t.press(S("B"));
    // Press B: rig 2-2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(6);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [76, 0, 0]], label: "Bank 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 0, 0]], label: "Bank 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 5, 0], [5, 5, 0], [76, 0, 0]], label: "Rig 2-1" });
    await t.expectSwitch(S("B"), { leds: [[76, 76, 0], [76, 76, 0], [76, 0, 0]], label: "Rig 2-2" });

    morph(16383);
    await t.ticks();
    // Morph state on
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(6);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [0, 0, 76]], label: "Bank 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [0, 0, 76]], label: "Bank 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 5, 0], [5, 5, 0], [0, 0, 76]], label: "Rig 2-1" });
    await t.expectSwitch(S("B"), { leds: [[76, 76, 0], [76, 76, 0], [0, 0, 76]], label: "Rig 2-2" });

    morph(0);
    await t.ticks();
    // Morph state off
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(6);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 5], [0, 0, 5], [76, 0, 0]], label: "Bank 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 76, 0], [76, 76, 0], [76, 0, 0]], label: "Bank 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 5, 0], [5, 5, 0], [76, 0, 0]], label: "Rig 2-1" });
    await t.expectSwitch(S("B"), { leds: [[76, 76, 0], [76, 76, 0], [76, 0, 0]], label: "Rig 2-2" });

    await t.press(S(1));
    // Press 1: bank 1
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(1);
    await t.expectSwitch(S("1"), { leds: [[0, 0, 76], [0, 0, 76], [76, 0, 0]], label: "Bank 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 5, 0], [5, 5, 0], [76, 0, 0]], label: "Bank 2" });
    await t.expectSwitch(S("A"), { leds: [[0, 0, 5], [0, 0, 5], [76, 0, 0]], label: "Rig 1-1" });
    await t.expectSwitch(S("B"), { leds: [[0, 0, 76], [0, 0, 76], [76, 0, 0]], label: "Rig 1-2" });
})
