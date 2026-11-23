/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Rig select in the current bank (switches 1, 2, A, B), bank down/up on hold A/B.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const c = () => ({ "t.client.getRigId()": t.client.getRigId() });

    await t.setRigId(12);
    // Rig 3-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-2" });
    await t.expectSwitch(S("A"), { leds: [[76, 0, 0], [76, 0, 0], [5, 5, 0]], label: "Rig 3-3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [2, 5, 2]], label: "Rig 3-4" });

    await t.press(S(2));
    // Press 2: rig 3-2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Rig 3-2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: "Rig 3-3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [2, 5, 2]], label: "Rig 3-4" });

    await t.press(S(2));
    // Press 2 again: no change
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(11);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-1" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Rig 3-2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: "Rig 3-3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [2, 5, 2]], label: "Rig 3-4" });

    await t.press(S("B"));
    // Press B: rig 3-4
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(13);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: "Rig 3-3" });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: "Rig 3-4" });

    await t.hold(S("B"));
    // Hold B: bank up
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(18);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Rig 4-1" });
    await t.expectSwitch(S("2"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Rig 4-2" });
    await t.expectSwitch(S("A"), { leds: [[1, 5, 1], [1, 5, 1], [5, 0, 0]], label: "Rig 4-3" });
    await t.expectSwitch(S("B"), { leds: [[30, 76, 30], [30, 76, 30], [3, 0, 2]], label: "Rig 4-4" });

    await t.hold(S("A"));
    // Hold A: bank down
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(13);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: "Rig 3-3" });
    await t.expectSwitch(S("B"), { leds: [[76, 0, 0], [76, 0, 0], [2, 5, 2]], label: "Rig 3-4" });

    await t.press(S(1));
    // Press 1: rig 3-1
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(10);
    await t.expectSwitch(S("1"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Rig 3-1" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-2" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 5, 0]], label: "Rig 3-3" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [2, 5, 2]], label: "Rig 3-4" });
})
