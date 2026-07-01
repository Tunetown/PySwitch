class ParserChecks {

    #messages = null;
    #usages = null;

    #parser = null;

    constructor(parser) {
        this.#parser = parser;
        this.reset();
    }

    /**
     * Reset messages buffer
     */
    reset() {
        this.#messages = null;
        this.#usages = new Map();
    }

    /**
     * Process checks
     */
    async process() {
        if (this.#messages != null) return;

        const msgs = []
        await this.#checkDisplayLabels(msgs);
        this.#messages = msgs;
    }

    /**
     * Process all checks (buffered)
     */
    async messages() {
        await this.process();
        return this.#messages;
    }

    /**
     * Returns if the action has any relevant messages of the given type
     */
    async messagesForAction(actionCallProxy, type = null) {
        await this.process();
        
        const ret = [];
        
        for (const msg of this.#messages) {
            if (type && (msg.type != type)) continue;

            for (const action of msg.actions || []) {
                if (action.id() == actionCallProxy.id()) ret.push(msg);
            }
        }
        return ret;
    }

    /**
     * Check for multiple assignments of DisplayLabels
     */
    async #checkDisplayLabels(messages) {
        const displays = await this.#parser.getAvailableDisplays();

        // Crawl all actions for parameters with the displays
        for (const display of displays) {
            const usages = await this.getDisplayUsages(display);
            const pagers = [];

            function getPager(pagerName) {
                for (const pager of pagers) {
                    if (pager.name == pagerName) return pager;
                }

                const ret = {
                    name: pagerName,
                    pages: []
                }

                pagers.push(ret)
                return ret;
            }

            function addToPager(pager, pageName) {
                for (const page of pager.pages) {
                    if (page == pageName) return;
                }
                pager.pages.push(pageName);
            }

            function addPage(usage) {
                const pagerName = usage.pager();
                const page = usage.page();

                const pager = getPager(pagerName);
                addToPager(pager, page);
            }

            // Build tree of all pages using this display
            for (const usage of usages) {
                addPage(usage);
            }

            function addMessage(message) {
                for (const msg of messages) {
                    if (msg.parameter == message.parameter && 
                        msg.value == message.value && 
                        msg.message == message.message && 
                        msg.type == message.type
                    ) {
                        msg.actions = [...new Set(msg.actions.concat(message.actions))]
                        return;
                    }
                }
                messages.push(message);
            }
            
            for (const pager of pagers) {
                for (const page of pager.pages) {
                    const usagesFiltered = usages.filter((item) => (item.pager() != pager.name) || (item.page() == page && item.pager() == pager.name));
                    
                    if (usagesFiltered.length > 1) {
                        addMessage({
                            type: "W",
                            message: "DisplayLabel " + display + " is possibly used more than once at a time (paging regarded). You might get inconsistent displays, use at your own risk.",
                            parameter: "display",
                            value: display,
                            actions: usagesFiltered
                        })    
                    }
                }
            }
        }
    }

    /**
     * Returns an array of usages containing the display as an argument (buffered)
     * 
     * If all is false, preview and change displays will be ignored.
     */
    async getDisplayUsages(displayId, all = false) {
        const bufferId = displayId + (all ? '-all' : '');
        if (this.#usages.has(bufferId)) return this.#usages.get(bufferId);

        /**
         * Returns an array of actions containing the display as an argument
         */
        async function getActionsWithDisplay(input, hold) {
            if (!input) return [];
            
            const actions = await input.actions(hold);

            const ret = [];
            for (const action of actions || []) {
                const args = action.arguments();

                for (const arg of args) { 
                    if (arg.value == displayId) {
                        if (all) {
                            ret.push(action);
                        } else {
                            if (!arg.name.includes("preview") && !arg.name.includes("change")) {  // TODO put to Meta
                                ret.push(action);
                            }
                        }
                    }                                        
                }
            }
            return ret;
        }

        // Crawl all actions for parameters with the display
        const hw = await this.#parser.getHardwareInfo();
        
        let usages = [];
        for (const inputDescr of hw) {
            const input = await this.#parser.input(inputDescr.data.name);

            const contained = await getActionsWithDisplay(input, false);
            const containedHold = await getActionsWithDisplay(input, true);

            usages = usages.concat(contained, containedHold);
        }

        this.#usages.set(bufferId, usages);

        return usages;        
    }
}