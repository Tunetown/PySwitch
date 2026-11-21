describe('General', function() {
    
    it('Serial match', async function() {
       await (new TestGeneral()).process()
    });
});


class TestGeneral extends TestBase {
    async process() {
        await this.init();

        const pySwitchVersion = this.runner.pyswitch.pyodide.runPython(`
            from pyswitch.misc import PYSWITCH_VERSION
            PYSWITCH_VERSION
        `);
        
        expect(pySwitchVersion.length).toBeGreaterThan(0);
        expect(Controller.VERSION.startsWith(pySwitchVersion)).toBe(true);
    }
}