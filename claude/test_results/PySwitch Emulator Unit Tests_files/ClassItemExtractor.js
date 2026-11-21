/**
 * Adapter to the python based ClassItemExtractor (which can extract all attributes of a class)
 */
class ClassItemExtractor {

    #runner = null  // PySwitchRunner instance

    constructor(runner) {
        this.#runner = runner;
    }

    /**
     * options: {
     *      file: The file to parse,
     *      className
     *      importPath
     *      includeUnderscore: bool,
     *      functions: bool,
     *      attributes: bool
     * }
     */
    async get(options) {
        // Tell the python code which files to examine, process it and return the decoded result.
        const resultJson = await this.#runner.pyodide.runPython(`
            import json
            from parser.misc.ClassItemExtractor import ClassItemExtractor

            classItemExtractor = ClassItemExtractor(
                file               = '` + options.file + `',
                className          = '` + options.className + `',
                importPath         = '` + options.importPath + `',
                include_underscore = ` + (options.includeUnderscore ? "True" : "False") + `
            )
            
            json.dumps(classItemExtractor.get(
                functions  = ` + (options.functions ? "True" : "False") + `,
                attributes = ` + (options.attributes ? "True" : "False") + `
            ))
        `);
        
        return JSON.parse(resultJson);
    }
}