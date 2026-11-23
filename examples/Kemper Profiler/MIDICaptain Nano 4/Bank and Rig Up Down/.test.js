/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator 
 * docker container running, you can run the tests calling http://localhost/test
 */
(async function(runner) {
    // Tuner display
    await (new KemperTunerTests(runner)).testTriggeredFromClient();

    // Bank up/down
    const bankTests = new KemperBankTests(runner);
    await bankTests.testBankUp("PA_MIDICAPTAIN_NANO_SWITCH_2", { labelTestCoordinates: [238, 1] });
    await bankTests.testBankDown("PA_MIDICAPTAIN_NANO_SWITCH_B", { labelTestCoordinates: [238, 238] });

    // Rig up/down
    const rigTests = new KemperRigTests(runner);
    await rigTests.testRigUp("PA_MIDICAPTAIN_NANO_SWITCH_1", { keepBank: true, labelTestCoordinates: [1, 1] });
    await rigTests.testRigDown("PA_MIDICAPTAIN_NANO_SWITCH_A", { keepBank: true, labelTestCoordinates: [1, 238] });
})