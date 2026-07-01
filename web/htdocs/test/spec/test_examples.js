describe('Examples with Parser Identity', function() {
    
    beforeEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 500000;
    });

    it('Examples (high level test)', async function() {
        // console.error("Examples tests are deactivated!");
        // return;  // TODO!

        await (new ExampleTestRunner("../examples").process());   
    });
});

