describe('Multiple Clients', function() {

    const tests = new MultiClientTests();

    beforeEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000;
    });

    it('Detect the clients of a configuration', async function() {
        await tests.estimateClients();
    });

    it('Protocol client', async function() {
        await tests.protocolClient();
    });

    it('Combined MIDI wrapper', async function() {
        await tests.combinedMidiWrapper();
    });

    it('Run PySwitch with two virtual clients', async function() {
        await tests.runTwoClients();
    });
});
