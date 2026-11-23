/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Bank down/up with preselect (switches 1, 2), rig select (switches A, B).
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;
    const t = new KemperTestBase(runner);
    const all = [S(1), S(2), S("A"), S("B")];
    const c = () => ({ "t.client.getRigId()": t.client.getRigId(), "t.param(new CCKey(47))": t.param(new CCKey(47)) });

    await t.setRigId(12);
    // Rig 3-3
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(null);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-1" });
    await t.expectSwitch(S("B"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Rig 3-2" });

    await t.press(S(2));
    // Press 2: bank 4 preselected
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(3);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rig 4-1" });
    await t.expectSwitch(S("B"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rig 4-2" });

    await t.press(S(2));
    // Press 2 again: bank 5 preselected
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(12);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(4);
    await t.expectSwitch(S("1"), { leds: [[5, 0, 0], [5, 0, 0], [5, 0, 0]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[76, 0, 0], [76, 0, 0], [76, 0, 0]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: "Rig 5-1" });
    await t.expectSwitch(S("B"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: "Rig 5-2" });

    await t.press(S("B"));
    // Press B: rig 5-2
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(21);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(null);
    await t.expectSwitch(S("1"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: "Rig 5-1" });
    await t.expectSwitch(S("B"), { leds: [[54, 0, 36], [54, 0, 36], [54, 0, 36]], label: "Rig 5-2" });

    await t.press(S(1));
    // Press 1: bank 4 preselected
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(21);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(3);
    await t.expectSwitch(S("1"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[3, 0, 2], [3, 0, 2], [3, 0, 2]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rig 4-1" });
    await t.expectSwitch(S("B"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rig 4-2" });

    await t.press(S("A"));
    // Press A: rig 4-1
    expect(t.client.getRigId()).withContext("t.client.getRigId()").toEqual(15);
    expect(t.param(new CCKey(47))).withContext("t.param(new CCKey(47))").toEqual(null);
    await t.expectSwitch(S("1"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Bank dn" });
    await t.expectSwitch(S("2"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Bank up" });
    await t.expectSwitch(S("A"), { leds: [[30, 76, 30], [30, 76, 30], [30, 76, 30]], label: "Rig 4-1" });
    await t.expectSwitch(S("B"), { leds: [[2, 5, 2], [2, 5, 2], [2, 5, 2]], label: "Rig 4-2" });
})
