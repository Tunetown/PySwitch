describe('Parser for available callbacks', function() {
    
    const tests = new CallbackParserTests();

    beforeEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 500000;
    });
    
    it('Available callbacks', async function() {
        await tests.getAvailableDisplayLabelCallbacks();
    });
});

