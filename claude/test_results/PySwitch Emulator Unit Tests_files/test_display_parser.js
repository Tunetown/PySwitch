describe('Display Parser', function() {
    
    const tests = new DisplayParserTests();

    it('Get: Minimal', async function() {
        await tests.getDisplaysMinimal();
    });

    it('Generic: Get list', async function() {
        await tests.getDisplaysArray();
    });

    it('Get: No items', async function() {
        await tests.getDisplaysEmpty();
    });

    it('Get displays (default)', async function() {
        await tests.getDisplaysDefault();
    });


    it('Code for single tree nodes', async function() {
        await tests.codeForNode();
    });


    it('Generic: Replace list', async function() {
        await tests.replaceDisplaysArray();
    });

    it('Generic: Replace dict', async function() {
        await tests.replaceDisplaysDict();
    });

    it('Generic: Replace call', async function() {
        await tests.replaceDisplaysCall();
    });

    it('Generic: Replace with code attribute', async function() {
        await tests.replaceDisplaysCode();
    });

    it('Replace displays (fantasy values)', async function() {
        await tests.replaceDisplaysFantasy();
    });

    it('Get displays (real values)', async function() {
        await tests.replaceDisplaysReal();
    });
});

