describe('Client Imports', function() {

    const tests = new ClientImportsTests();

    beforeEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000;
    });

    it('Single client', async function() {
        await tests.singleClient();
    });

    it('Two clients with the same action name (aliases)', async function() {
        await tests.twoClients();
    });

    it('Existing import without alias keeps its name', async function() {
        await tests.existingPlainImport();
    });

    it('Change the client of an action', async function() {
        await tests.changeClient();
    });

    it('Remove alias when not needed anymore', async function() {
        await tests.removeAlias();
    });

    it('Unchanged configuration keeps the clients', async function() {
        await tests.unchanged();
    });

    it('Client functions in code strings', async function() {
        await tests.codeStrings();
    });

    it('Qualified names of same-named client functions in code strings', async function() {
        await tests.qualifiedCodeStrings();
    });

    it('Unchanged code strings keep the clients', async function() {
        await tests.unchangedCodeStrings();
    });

    it('Mapping options distinguish same-named mappings', async function() {
        await tests.mappingOptions();
    });

    it('Run PySwitch with two clients', async function() {
        await tests.runTwoClients();
    });
});
