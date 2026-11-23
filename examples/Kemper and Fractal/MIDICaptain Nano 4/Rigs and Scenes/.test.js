/**
 * Example test script, will be executed by a Jasmine test spec. When you have the PySwitch emulator
 * docker container running, you can run the tests calling http://localhost/test
 *
 * Kemper and Fractal in one configuration: both virtual clients are connected.
 */
(async function(runner) {
    const S = (name) => "PA_MIDICAPTAIN_NANO_SWITCH_" + name;

    const kemper = runner.runner.clients.kemper;
    const fractal = runner.runner.clients.fractal;

    expect(kemper).toBeInstanceOf(VirtualKemperClient);
    expect(fractal).toBeInstanceOf(VirtualFractalClient);

    // Fractal scenes (switches A and B)
    const sceneTests = new FractalSceneTests(runner);
    await sceneTests.testSceneSelect([S("A"), S("B")]);

    // Fractal scene name display
    fractal.presets.setScene(1);
    await sceneTests.ticks();
    expect(await sceneTests.displayText("FractalSceneNameCallback")).toBe("2 " + fractal.presets.getSceneName(1));

    // Kemper rigs (switches 1 and 2)
    await sceneTests.press(S(2));
    expect(kemper.getRigId()).toBe(1);

    await sceneTests.press(S(1));
    expect(kemper.getRigId()).toBe(0);

    // Selecting a Kemper rig does not change the Fractal scene
    expect(fractal.presets.currentScene).toBe(1);
})
