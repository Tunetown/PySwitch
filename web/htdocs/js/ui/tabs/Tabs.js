/**
 * Implements tabs handling
 */
class Tabs {

    #controller = null;
    #container = null;
    #showTabsButton = null;
    
    #content = null;
    #header = null;
    #headerButtons = null;
    
    #tabs = [];
    #state = null;
    active = null;               // Active Tab instance

    constructor(controller, container, showTabsButton) {
        this.#controller = controller;
        this.#container = container;
        this.#showTabsButton = showTabsButton;

        this.#state = new LocalState("tabs");

        this.init();
    }

    /**
     * Set up DOM, handlers etc.
     */
    init() {
        // DOM
        this.#container.append(
            $('<div class="header" />').append(
                // Header (tab headers)
                $('<div class="header-tabs-container" />').append(
                    // Header (tab headers)
                    this.#header = $('<div class="header-tabs" />'),
                ),
            
                // Header buttons
                $('<div class="header-buttons" />').append(
                    // Tab specific buttons
                    this.#headerButtons = $('<span />'),

                    $('<span />').append(
                        // Show/hide tabs button
                        $('<div class="close-tabs fas fa-times"/>')
                        .on('click', async function() {
                            try {
                                that.hide();
                            
                            } catch (e) {
                                that.#controller.handle(e);
                            }
                        })
                    )
                )
            ),
            this.#content = $('<div class="content" />'),
        )

        // Make tabs resizable (using jquery UI)
        const that = this;
        this.#container.resizable({ 
            handles: "s",
            stop: function() {
                that.#state.set('width', that.#container.width());
            }
        });

        // Set state according to local storage (defaults to hidden)
        if (this.#state.get('show')) {
            this.show();
        } else {
            this.hide();
        }
    }

    /**
     * Add a new Tab instance
     */
    add(tab, index = null) {          // TODO Index not respected currently
        if (!tab) return;
        
        tab.init(this);
        
        this.#content.append(tab.container);

        this.#header.append(
            tab.getHeader()
        )

        this.#tabs.push(tab);
        this.#update();
    }

    /**
     * Remove a Tab instance
     */
    remove(tab) {
        if (!tab) return;
        if (!tab.confirmIfDirty()) return;

        tab.destroy();

        if (tab == this.active) this.active = null;
        
        const index = this.#tabs.indexOf(tab);
        if (index > -1) { 
            this.#tabs.splice(index, 1); 
        }

        this.#update();
    }

    /**
     * Get a tab by name, or null if not found
     */
    getTabByName(name) {
        for (const tab of this.#tabs) {
            if (tab.name == name) return tab;
        }
        return null;
    }

    confirmIfDirty() {
        for (const tab of this.#tabs) {
            if (!tab.confirmIfDirty()) return false;
        }
        return true;
    }

    /**
     * Show tabs
     */
    show() {
        const width = this.#state.get('width');
        if (width) {
            this.#container.width(width);
        }

        this.#container.show();
        this.#showTabsButton.hide();

        this.#state.set('show', true);  
        
        // When a tab is shown, the editors need refreshing
        if (this.active) {
            this.active.refresh();
        }
    }

    /**
     * Hide tabs
     */
    hide() {
        this.#container.hide();
        this.#showTabsButton.show();

        this.#state.set('show', false);
    }

    /**
     * Is the tabs panel visible?
     */
    visible() {
        return !!this.#container.is(":visible");
    }

    /**
     * Toggle tabs panel visibility
     */
    toggle() {
        if (this.visible()) {
            this.hide();
        } else {
            this.show();
        }
    }

    /**
     * Sets a specific tab active
     */
    setActive(tab) {
        if (!tab) throw new Error('No tab passed');

        this.active = tab;
        this.#updateActive();

        this.#state.set('current', tab.name);

        // When a tab is shown, the editors need refreshing
        this.active.refresh();

        // Replace buttons
        this.#headerButtons.empty();
        this.#headerButtons.append(
            this.active.getButtons()
        )
    }

    /**
     * Activate a tab by name, if found
     */
    setActiveByName(name) {
        const tab = this.getTabByName(name);
        if (!tab) return;

        this.setActive(tab);
    }

    /**
     * Updates the tabs to the current active tab
     */
    #updateActive() {
        for (const tab of this.#tabs) {
            if (tab == this.active) {
                tab.activate();
            } else {
                tab.deactivate();
            }
        }
    }

    /**
     * Update after tab changes
     */
    #update() {
        if (this.#tabs.length > 0 && !this.active) {
            const current = this.#state.get('current');
            if (current) {
                const tab = this.getTabByName(current);

                if (tab) {
                    this.setActive(tab);
                    return;
                }

            } else {
                this.setActive(this.#tabs[0]);
                return;
            }            
        }

        this.#updateActive();        
    }
}