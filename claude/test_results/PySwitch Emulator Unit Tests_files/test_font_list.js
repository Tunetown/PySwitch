describe('Font list', function() {
    
    const tests = new FontListTests();

    it('Get available fonts', async function() {
        await tests.getAvailableFonts();
    });
});

