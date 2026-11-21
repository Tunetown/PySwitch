/**
 * Adapter to the python based ClassNameExtractor (which can extract all public classes of a file)
 */
class ClassNameExtractor {

    #runner = null  // PySwitchRunner instance

    constructor(runner) {
        this.#runner = runner;
    }

    /**
     * options: {
     *      file: The file to parse,
     *      importPath
     *      includeUnderscore: bool,
     * }
     */
    async get(options) {
        // Tell the python code which files to examine, process it and return the decoded result.
        const resultJson = await this.#runner.pyodide.runPython(`
            import json
            from parser.misc.ClassNameExtractor import ClassNameExtractor

            classNameExtractor = ClassNameExtractor(
                file               = '` + options.file + `',
                import_path        = '` + options.importPath + `',
                include_underscore = ` + (options.includeUnderscore ? "True" : "False") + `
            )
            
            json.dumps(classNameExtractor.get())
        `);
        
        return JSON.parse(resultJson);
    }
}