describe('Parser for available mappings', function() {
    
    const tests = new MappingParserTests();

    it('Get available mappings', async function() {
        await tests.getAvailableMappings();
    });
});

