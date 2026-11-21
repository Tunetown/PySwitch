describe('Parser for available HID keycodes', function() {
    
    const tests = new KeycodeParserTests();

    it('Available keycodes', async function() {
        await tests.getAvailableKeycodes();
    });
});

