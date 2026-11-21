/**
 * Provider for browser popups, loading the examples.
 */
class ExamplesProvider extends BrowserProvider {
    
    #toc = null;
    #path = null;
    #controller = null;

    constructor(controller, path) {
        super();
        this.#controller = controller;
        this.#path = path;
    }

    /**
     * Return TOC for all examples if not yet loaded
     */
    async getToc(browser) {
        if (this.#toc) return this.#toc;

        // Load TOC data
        const toc = JSON.parse(await Tools.fetch(this.#path));
        
        const that = this;

        /**
         * Select the entry
         */
        function onSelect(entry) {
            that.#controller.routing.call(encodeURI("example" + entry.data.callPath));
        }
        
        // Build hierarchy        
        function crawl(entry, prefix) {
            // Make it a callable entry if it is a folder and does not have any subfolders
            if (entry.type == "dir" && !entry.children.filter((e) => e.type == "dir").length) {
                // Example
                return new BrowserEntry(
                    browser,
                    {
                        value: entry.name,                        
                        callPath: prefix + entry.name,
                        onSelect: onSelect,
                        toc: entry
                    }                    
                );
            }

            // Folder
            const ret = new BrowserEntry(
                browser,
                {
                    value: entry.name,
                    callPath: prefix + entry.name,
                    childLayout: [
                        // Type icon
                        {
                            type: "typeIcon"
                        },
        
                        // README icon
                        {
                            get: function(entry) {
                                return !entry.isCallable() ? null : 
                                    $('<span class="clickable fa fa-info"/>')
                                    .on('click', async function() {
                                        try {
                                            let content = null;
                                            
                                            if (entry.data.callPath) {
                                                const url = 'examples' + entry.data.callPath + '/README.md';

                                                try {                                       
                                                    marked.use({
                                                        async: true,
                                                        silent: true
                                                    });
        
                                                    content = $('<span class="clickable markdown" />')
                                                        .html(await marked.parse(await Tools.fetch(url)))
                                                        .on('click', async function() {
                                                            window.open(url, '_blank');
                                                        })
    
                                                } catch (e2) {
                                                    content = "Error loading README";
                                                }
                                                
                                            } else {
                                                content = "No information available";
                                            }
        
                                            browser.showInfoPanel(content);

                                        } catch (e) {
                                            that.#controller.handle(e);
                                        }
                                    })
                            }
                        },
        
                        // Link
                        {
                            type: "link"
                        }
                    ]
                }
            );

            for(const child_def of entry.children || []) {
                // Exclude MIDI Routing examples
                if (child_def.name.includes("MIDI Routings") || child_def.name.includes("Multiboot")) continue;

                const child = crawl(child_def, prefix + entry.name + "/");
                child.parent = ret;
                ret.children.push(child);
            }

            return ret;
        }

        const examples = crawl(toc, "");
        examples.text = "Examples";

        // Add "Default PySwitch" option at root level
        examples.children.unshift(
            new BrowserEntry(
                browser,
                {
                    value: "PySwitch Default",
                    onSelect: async function(/*entry*/) {
                        try {
                            that.#controller.routing.call(that.#controller.getControllerUrl("pyswitch-default"));

                        } catch (e) {
                            that.#controller.handle(e);
                        }
                    },
                    parent: examples
                }
            )
        )

        this.#toc = examples;
        return examples;
    }
}