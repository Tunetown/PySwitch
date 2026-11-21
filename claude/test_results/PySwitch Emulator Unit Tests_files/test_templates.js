describe('Templates with Parser Identity', function() {
    
    beforeEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000;
    });

    it('Templates (high level test)', async function() {
        // console.error("Templates tests are deactivated!");
        // return;  // TODO!

        await (new ExampleTestRunner("../templates").process());   
    });
});

