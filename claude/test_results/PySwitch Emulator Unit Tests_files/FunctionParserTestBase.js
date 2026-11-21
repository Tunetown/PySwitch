class FunctionParserTestBase extends TestBase {

    /**
     * Checks if a definition file is still up to date.
     * 
     * loadCallback() => definitions must return the definitions loaded from the buffered file
     * generateCallback() => definitions must return the definitions generated from scratch
     */
    async checkDefinitions(downloadFilename, loadCallback, generateCallback) {
        const generated = await generateCallback();

        try {
            // Try to load. If not possible, generate the list and fail the test.
            const loaded = await loadCallback();

            if (JSON.stringify(generated) != JSON.stringify(loaded)) {
                this.download(generated, downloadFilename);

                throw new Error("Definition file " + downloadFilename + " is outdated, see next error(s)");
            } 
            
            // Everything fine (this line prevents the Jasmine warning that no expectations are contained in the test)
            expect(1).toBe(1);            

        } catch (e) {
            console.error(e);

            this.download(generated, downloadFilename);
            
            throw new Error("The definitions file " + downloadFilename + " is outdated or does not exist. Please store the downloaded file at web/htdocs/definitions.");
        }
    }

    /**
     * Download data as JSON file
     */
    download(data, fileName) {
        const dataString = JSON.stringify(data);
        const dataBlob = new Blob([dataString], {type: 'text/plain'});
        const url = URL.createObjectURL(dataBlob);
        
        window.saveAs(url, fileName);
    }
}