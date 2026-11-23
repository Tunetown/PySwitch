/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Rig select with custom texts (switches 1, 2: rig 1, bank 3 rig 2; A: rig 1 with rig_off 2), bank up (B).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const c = () => ({ "t.client.getRigId()": t.client.getRigId() });

    await t.setRigId(7);
    // Rig 2-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(7);
    await t.expectSwitch(S("1"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: "Marge 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: "Marge 3" });
    await t.expectSwitch(S("B"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: "Marge 3" });

    await t.press(S(1));
    // Press 1: rig 2-1
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(5);
    await t.expectSwitch(S("1"), { leds: [[76, 76, 0], [76, 76, 0], [76, 76, 0]], label: "Marge 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: "Marge 1" });
    await t.expectSwitch(S("B"), { leds: [[5, 5, 0], [5, 5, 0], [5, 5, 0]], label: "Marge 1" });

    await t.press(S(2));
    // Press 2: rig 3-2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Bart 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 2" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 2" });

    await t.press(S("A"));
    // Press A: rig 3-1
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(10);
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Bart 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 1" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 1" });

    await t.press(S("A"));
    // Press A again: rig_off 3-2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Bart 2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 2" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 2" });

    await t.press(S("B"));
    // Press B: bank up
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(16);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Lisa 1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bart 2" });
    await t.expectSwitch(S("A"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Lisa 2" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Lisa 2" });
})
