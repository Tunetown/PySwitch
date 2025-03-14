/**
 * Parser frontend (shows all actions etc.)
 */
class ParserFrontend {

    inputs = [];   // Array of parser frontends
    parser = null;
    icons = null;

    #controller = null;
    #toUpdate = [];    // Queue for parser frontends which had changes recently.

    constructor(controller, parser) {
        this.#controller = controller;
        this.parser = parser;

        this.icons = new ParserFrontendIcons(parser);
    }

    async destroy() {
        for(const f of this.inputs) {
            await f.destroy();
        }
    }

    /**
     * Adds a new frontend for an input
     */
    async addInput(inputDefinition, inputElement) {
        if (!inputElement) return;

        const input = await this.parser.input(inputDefinition.data.model.port);
        
        this.inputs.push(
            new ParserFrontendInput(this.#controller, this, inputDefinition, input, inputElement)
        );
    }

    /**
     * Must be called after all inputs have been added
     */
    async init() {
        for(const f of this.inputs) {
            await f.init();
        }
    }

    /**
     * Schedules an input frontend for updating the Configuration
     */
    scheduleForUpdate(input) {
        if (this.#toUpdate.includes(input)) return;

        this.#toUpdate.push(input);
    }

    /**
     * Update the Configuration data from the input frontends. Includes exception handling
     * as this is eventually called without await.
     */
    async updateConfig() {
        try {
            await this.#doUpdateConfig();

        } catch (e) {
            this.#controller.handle(e);
        }
    }

    /**
     * Implementation for updateConfig
     */
    async #doUpdateConfig() {
        const that = this;
        await this.#controller.restart({
            message: "none",
            changeCallback: async function() {
                // Update the input queue
                while (that.#toUpdate.length > 0) {
                    const inputToUpdate = that.#toUpdate.shift();
                    await inputToUpdate.updateInput();
                }

                that.parser.updateConfig();
            }
        });
    }
}