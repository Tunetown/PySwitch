/**
 * Parser frontend for one input (shows actions for one input)
 */
class ParserFrontendInput {

    #grid = null;
    #controller = null;
    #parserFrontend = null;
    #inputElement = null;
    #gridElement = null;

    input = null;                     // Input handler (may be null)
    definition = null;

    constructor(controller, parserFrontend, inputDefinition, input, inputElement) {
        this.#controller = controller;
        this.#parserFrontend = parserFrontend;
        this.#inputElement = inputElement;
        this.input = input;
        this.definition = inputDefinition;
    }

    /**
     * Destroy the input
     */
    async destroy() {
        if (this.#grid) await this.#grid.destroy();

        this.input = null;
        this.definition = null;
    }

    /**
     * Adds the parser frontend for one input
     */
    async init() {
        await this.#initDom();
        await this.#initGrid();
    }

    /**
     * Searches for a action definition by name and client ID. Returns null if not found.
     */
    async #getActionDefinition(name, clientId) {
        // Load all available clients
        const clients = await this.#parserFrontend.parser.getAvailableActions();

        for (const client of clients) {
            if (client.client != clientId && client.client != "local") continue;

            for (const action of client.actions) {
                if (!action.meta) console.log(action)
                if (action.meta.data.target != this.definition.data.model.type) continue;
                if (action.name == name) return action;
            }
        }
        return null;
    }

    /**
     * Generate item text
     */
    async #getActionText(actionCallProxy, short = false) {
        const action = await this.#getActionDefinition(
            actionCallProxy.definitionName ? actionCallProxy.definitionName : actionCallProxy.name, 
            actionCallProxy.client
        );
        
        if (!action) return actionCallProxy.name;
        
        return short ? action.meta.getShortDisplayName(actionCallProxy) : action.meta.getDisplayName(actionCallProxy);
    }

    /**
     * Init the UI
     */
    async #initDom() {
        const that = this;

        // Get actions to show
        const actions = this.input ? (await this.input.actions()) : [];
        const actionsHold = this.input ? (await this.input.actions(true)) : [];

        // The promises in the upcoming map() call will run pseudo-parallel, so we better
        // scan messages beforehand (even if the messagesForAction() method would do that automatically).
        // Same goes for the available actions, which we also call here to fill the buffers.
        await that.#parserFrontend.parser.checks.process();
        await this.#parserFrontend.parser.getAvailableActions();

        /**
         * Determines the additional classes for the actions (warnings etc)
         */
        async function getAdditionalClasses(item) {
            const errorMsgs = await that.#parserFrontend.parser.checks.messagesForAction(item, "E");
            if (errorMsgs.length > 0) return "error";
            const warnMsgs = await that.#parserFrontend.parser.checks.messagesForAction(item, "W");
            if (warnMsgs.length > 0) return "warn";
        }
        
        async function getActionElements(a, buttonClass, hold, tooltip) {
            return await Promise.all(
                a.map(
                    async (item) => {       
                        const addClasses = await getAdditionalClasses(item);

                        return $('<div class="action-item" />').append(
                            $('<div class="action-item-content action-button" />')
                            .append(
                                // Action
                                $('<span class="button ' + buttonClass + ' name" data-toggle="tooltip" title="' + tooltip + '" />')
                                .addClass(addClasses)
                                .append(
                                    await that.#parserFrontend.icons.get(item, await that.#getActionDefinition(item.name, item.client)),

                                    $('<span />').text(await that.#getActionText(item, true))
                                )
                                .on('click', async function() {
                                    try {                                        
                                        await that.promptEditAction(
                                            item, 
                                            hold, 
                                            await that.#parserFrontend.parser.checks.messagesForAction(item)
                                        );

                                    } catch (e) {
                                        that.#controller.handle(e);
                                    }
                                }),

                                // Remove button
                                $('<span class="button ' + buttonClass + ' remove-action fas fa-times" data-toggle="tooltip" title="Remove action" />')
                                .addClass(addClasses)
                                .on('click', async function() {
                                    try {
                                        const action = $(this).parent().parent().data('handler');

                                        if (!confirm("Do you want to delete " + action.name + " from " + that.definition.displayName + "?")) {
                                            return;
                                        }
                                                                                    
                                        await that.removeAction(action);

                                    } catch (e) {
                                        that.#controller.handle(e);
                                    }
                                })
                            )                    
                        )
                        .data('handler', item)
                        .data('hold', hold)                        
                    }
                )
            )
        }

        this.#inputElement.append(
            $('<div class="pyswitch-parser-frontend" />').append(                
                this.#gridElement = $('<div class="action-grid" />').append(
                    // Actions
                    await getActionElements(
                        actions,
                        "actions",
                        false,
                        "Action on normal press"
                    ),

                    // Hold actions
                    await getActionElements(
                        actionsHold,
                        "actions-hold",
                        true,
                        "Action on long press"
                    ),

                    // Buttons item
                    $('<div class="action-item" />').append(
                        $('<div class="action-item-content input-button fixed" />').append(
                            // Add action button
                            $('<div class="button actions add-action fas fa-plus" data-toggle="tooltip" title="Add an action" />')
                            .on('click', async function() {
                                try {
                                    await that.promptAddAction();

                                } catch (e) {
                                    that.#controller.handle(e);
                                }
                            }),

                            // Input settings button
                            !(await (new InputSettings(this.#controller, this.definition, this.input, this.#parserFrontend.parser).get())) ? null :
                            $('<div class="button actions input-settings fas fa-wrench" data-toggle="tooltip" title="Settings for ' + this.definition.displayName + '" />')
                            .on('click', async function() {
                                try {
                                    await that.promptInputSettings();

                                } catch (e) {
                                    that.#controller.handle(e);
                                }
                            })
                        )
                    )
                )
            )
        )
    }

    /**
     * Init the grid (Muuri)
     */
    async #initGrid() {
        if (!this.#gridElement) return;
        
        // Init grid
        const that = this;
        this.#grid = new Muuri(this.#gridElement[0], {
            /**
             * Drag options
             */
            dragEnabled: true,

            // dragContainer: document.body,

            dragSort: function () {
                return that.#parserFrontend.inputs
                    .filter((item) => !!item.#grid && item.definition.data.model.type == that.definition.data.model.type)
                    .map((item) => item.#grid);
            },
            
            dragStartPredicate: function (item, e) {
                // Fix some items
                if ($(item.getElement()).find('.fixed').length > 0) return false;

                if (e.deltaTime > 50 && e.distance > 20) {
                    return Muuri.ItemDrag.defaultStartPredicate(item, e);
                }
            },

            dragSortPredicate: function (item) {
                const result = Muuri.ItemDrag.defaultSortPredicate(item, {
                    action: 'swap',
                    threshold: 50
                });

                if (result) {
                    // Get target item
                    const target = $(item.getElement()).parent().children().eq(result.index);
                    if (target.find('.fixed').length > 0) {
                        return false;
                    }
                }

                return result;
            },

            /**
             * Custom layout
             */
            layout: function (grid, layoutId, items, width, height, callback) {
                const layout = {
                    id: layoutId,
                    items: items,
                    slots: [],
                    styles: {},
                };

                let y = 0;
                let w = 0;
                let h = 0;

                for (let i = 0; i < items.length; ++i) {
                    const item = items[i];

                    y += h;
                    const m = item.getMargin();

                    const itemWidth = item.getWidth() + m.left + m.right;
                    if (itemWidth > w) w = itemWidth;
                    
                    h = item.getHeight() + m.top + m.bottom;
                 
                    layout.slots.push(0, y);
                }

                h += y;

                // Set the CSS styles that should be applied
                // to the grid element.
                layout.styles.width = w + 'px';
                layout.styles.height = h + 'px';

                callback(layout);
            }
        });

        // Grid events: On drag end we just schedule this grid for updating the config
        this.#grid.on('dragEnd', async function(item, event) {            
            that.#parserFrontend.scheduleForUpdate(that);
        });

        // On release end (which is after dragEnd), we also schedule the input and trigger the update.
        this.#grid.on('dragReleaseEnd', async function(item, event) {
            that.#parserFrontend.scheduleForUpdate(that);
            
            // No await!
            that.#parserFrontend.updateConfig();
        });          
    }

    /**
     * Updates the parser from the current DOM state
     */
    async updateInput() {
        // Build actions definitions
        const newActions = this.#getItemHandlers(false)
            .map((item) => { return {
                name: item.name,
                assign: item.assign,
                arguments: item.arguments()
            }});

        const newActionsHold = this.#getItemHandlers(true)
            .map((item) => { return {
                name: item.name,
                assign: item.assign,
                arguments: item.arguments()
            }});

        // Set the inputs accordingly (no update)
        await this.#setActions(newActions, false, true);
        await this.#setActions(newActionsHold, true, true);
    }

    /**
     * Shows the add action dialog
     */
    async promptAddAction() {
        const inputName = this.definition.displayName;
        const that = this;

        await this.#promptAction(
            async function(action, hold) {
                await that.addAction(action, hold);
            },
            "Add an action to " + inputName,
            "Add"
        );        
    }

    /**
     * Shows the edit action dialog
     */
    async promptEditAction(action, hold, messages = []) {
        const inputName = this.definition.displayName;
        const that = this;

        await this.#promptAction(
            // onCommit
            async function(actionNew, holdNew) {
                if (hold == holdNew) {
                    await that.replaceAction(action, actionNew);
                } else {
                    await that.removeAction(action);
                    await that.addAction(actionNew, holdNew);
                }                
            },

            // Headline
            "Edit/replace action \"" + (await this.#getActionText(action)) + "\" of " + inputName,

            // Button text
            "Apply",

            // Preselected action
            {
                name: action.name,
                definitionName: action.definitionName,
                assign: action.assign,
                arguments: action.arguments(),
                hold: hold
            },

            // Messages
            messages
        );
    }

    /**
     * Shows the action edit/create dialog
     */
    async #promptAction(onCommit, headline, buttonText, preselectAction = null, messages = []) {
        const that = this;

        let props = null;
        let actionsProvider = null;

        /**
         * Select an action (show its Properties)
         */
        async function onSelect(entry) {
            props = new ActionProperties(
                that.#controller,
                that.#parserFrontend,
                entry.data.actionDefinition,
                props,
                messages
            );

            browser.showInfoPanel(await props.get());
            browser.setSelected(entry)

            await props.init();
        }

        /**
         * Commit popup
         */
        async function commit() {
            if (!props) {
                alert("Please select an action first");
                return;
            }

            const action = props.createActionDefinition();
            const hold = props.hold();

            await onCommit(action, hold);

            browser.hide();
        }

        // A browser to select client connections (to Kemper etc.), triggered by the client select button
        const browser = this.#controller.ui.getBrowserPopup({
            additionalClasses: "select-actions",
            headline: headline,
            wide: true,
            dontCloseOnSelect: true,
            onReturnKey: commit,
            providers: [
                actionsProvider = new ActionsProvider(
                    this.#parserFrontend.parser,
                    {
                        onSelect: onSelect,
                        preselectActionName: preselectAction ? (preselectAction.definitionName ? preselectAction.definitionName : preselectAction.name) : null,
                        target: this.definition.data.model.type
                    }                    
                )
            ]
        });

        await browser.browse();

        // Preselected entry, if any
        if (actionsProvider.preselectEntry) {
            await onSelect(actionsProvider.preselectEntry);

            if (preselectAction) {
                await props.setHold(preselectAction.hold);
                await props.setAssign(preselectAction.assign);

                if (preselectAction.definitionName) {
                    const splt = preselectAction.name.split(".");
                    if (splt.length == 2) {
                        await props.setPagerProxy(splt[0])
                    }                    
                }                

                await props.setArguments(preselectAction.arguments);                
            }
        } else {
            browser.showInfoPanel("Please select an action to add");
        }

        // Preselected entry not found: Show a note that this can only be edited via Code Editor
        if (preselectAction && !actionsProvider.preselectEntry) {
            browser.showInfoPanel(
                [
                    $('<span />')
                    .text(preselectAction.name + " can only be edited directly in "),

                    $('<span class="underline-link" />')
                    .text("Source Code...")
                    .on('click', async function() {
                        browser.hide();

                        that.#controller.ui.tabs.show();
                        that.#controller.ui.tabs.setActiveByName("inputs.py");
                    })
                ]
            );
        }

        // Commit button
        browser.setButtons(
            $('<div class="button" />')
            .text(buttonText)
            .on('click', async function() {
                try {
                    await commit();

                } catch(e) {
                    that.#controller.handle(e);
                }
            })
        );

        return browser;
    }

    /**
     * Shows the action edit/create dialog
     */
    async promptInputSettings() {
        const that = this;

        async function commit() {
            browser.hide();
        }
        
        const browser = this.#controller.ui.getPopup({
            onReturnKey: commit,
            additionalClasses: "medium",
            buttons: [
                {
                    text: "Done",
                    onClick: commit
                }
            ]
        });

        const props = new InputSettings(
            this.#controller,
            this.definition,
            this.input,
            this.#parserFrontend.parser
        );

        const propsContent = await props.get();
        if (!propsContent) return null;

        await browser.show(
            propsContent,
            "General Settings for " + this.definition.displayName
        );

        return browser;
    }

    /**
     * Adds an action to the passed input (proxy)
     */
    async addAction(actionDefinition, hold = false) {
        // Build actions definitions
        const newActions = this.#getItemHandlers(hold)
            .map((item) => { 
                return {
                    name: item.name,
                    client: item.client,
                    assign: item.assign,
                    arguments: item.arguments()
                }
            });
        
        // Add new action
        newActions.push(actionDefinition);
        
        // Update config
        const that = this;
        setTimeout(
            async function() {
                await that.#setActions(newActions, hold, true);

                await that.#parserFrontend.updateConfig();    
            }, 
            100
        );
    }

    /**
     * Replaces an action. 
     */
    async replaceAction(actionToReplace, actionDefinition) {
        const hold = this.#getHold(actionToReplace);

        const newActions = this.#getItemHandlers(hold)
            .map((item) => { 
                if (item == actionToReplace) return actionDefinition;

                return {
                    name: item.name,
                    client: item.client,
                    assign: item.assign,
                    arguments: item.arguments()
                }
            });
                
        // Update config
        const that = this;
        setTimeout(
            async function() {
                await that.#setActions(newActions, hold, true);

                await that.#parserFrontend.updateConfig();    
            }, 
            100
        );
    }
    
    /**
     * Removes an action from the passed input (proxy)
     */
    async removeAction(action) {
        const hold = this.#getHold(action);

        const newActions = this.#getItemHandlers(hold)
            .filter((item) => item != action)
            .map((item) => { 
                return {
                    name: item.name,
                    client: item.client,
                    assign: item.assign,
                    arguments: item.arguments()
                }
            });
                
        // Update config
        const that = this;
        setTimeout(
            async function() {
                await that.#setActions(newActions, hold, true);

                await that.#parserFrontend.updateConfig();    
            }, 
            100
        );
    }

    /**
     * Returns if the action is a hold action
     */
    #getHold(action) {
        const actions = this.#getItemHandlers(false);
        for (const a of actions) {
            if (a == action) return false;
        }

        const actionsHold = this.#getItemHandlers(true);
        for (const a of actionsHold) {
            if (a == action) return true;
        }

        throw new Error("Action not contained: " + action.name);
    }

    /**
     * Returns the item handlers in the correct order
     */
    #getItemHandlers(hold) {
        const items = this.#grid.getItems();

        return items
            .filter((item) => $(item.getElement()).data('hold') == hold)
            .map((item) => $(item.getElement()).data('handler'));
    }

    /**
     * Sets actions on the input, which will be created if not existent.
     */
    async #setActions(actions, hold, noUpdate) {
        if (!this.input) {
            // Create input
            this.input = await this.#parserFrontend.parser.input(this.definition.data.model.port, true);
        }

        this.input.setActions(actions, hold, noUpdate);
    }
}