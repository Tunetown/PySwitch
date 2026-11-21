/**
 * Adapter to the python based ClassNamesExtractor (which can extract all public classes in a folder)
 */
class ClassNamesExtractor {

    #runner = null  // PySwitchRunner instance

    constructor(runner) {
        this.#runner = runner;
    }

    /**
     * Generates the list of available public classes in all files of a given path using libCST and returns it
     * as a descriptor object.
     * 
     * options: {
     *      tocPath is the URL of the toc.php script.
     *      subPath is a path inside the toc to start at
     *      targetPath is the target path inside the pyodide FS to the files containing the function definitions
     * }
     */
    async get(options) {
        // Get TOC of clients
        const toc = JSON.parse(await Tools.fetch(options.tocPath));

        /**
         * Returns a direct child by name 
         */
        function getChild(node, name) {
            for(const child of node.children || []) {
                if (child.name == name) return child;
            }
            return null;
        }

        // Get actions dir node
        const splt = options.subPath.split("/");
        let actions = toc;
        for (const token of splt) {
            actions = getChild(actions, token);

            if (actions == null) {
                return [];
            }
        }        

        // Get python paths for all files (the files are already located in the Pyodide FS, so python 
        // can just open them to get their contents)
        const importPaths = [];

        function crawl(node, prefix = options.targetPath) {
            if (node.type == "file") {
                if (node.name.endsWith(".py") && !node.name.startsWith("__")) {
                    importPaths.push(prefix);
                }                
                return;
            }

            for (const child of node.children) {
                crawl(child, prefix + (prefix ? "/" : "") + child.name);
            }
        }
        crawl(actions);

        return this.getFromPaths(importPaths);
    }

    async getFromPaths(importPaths) {
        // Tell the python code which files to examine, process it and return the decoded result.
        const resultJson = await this.#runner.pyodide.runPython(`
            import json
            from parser.misc.ClassNamesExtractor import ClassNamesExtractor

            classNamesExtractor = ClassNamesExtractor(
                import_paths       = json.loads('` + JSON.stringify(importPaths) + `')
            )
            
            json.dumps(classNamesExtractor.get())
        `);
        
        return JSON.parse(resultJson);
    }
}