describe('Parser for available actions', function() {
    
    const tests = new ActionParserTests();

    it('Available actions', async function() {
        await tests.getAvailableActions();
    });

    it('Metadata', async function() {
        await tests.getAvailableActionsMeta();
    });
});

