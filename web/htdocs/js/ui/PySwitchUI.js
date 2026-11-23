/**
 * User interface controller
 */
class PySwitchUI {

    #controller = null;
    #options = null;
    
    #block = null;
    #progressBar = null;            // Progress bar inner element (the one to resize)
    #progressMessage = null;        // Messages for progress
    #progressBarContainer = null;
    #contentHeadline = null;
    #deviceElement = null;
    #changeMarker = null;
    #popupContainer = null;
    #virtualClientTabs = [];       // Tabs of the virtual clients (one per client)
    #virtualClientUIs = [];
    #additionalInputsContainer = null;
    #additionalInputsButton = null;
    midiMonitor = null;
    
    container = null;

    notifications = null;
    loadBrowser = null;
    saveBrowser = null;
    clientBrowser = null;
    clientButton = null;
    frontend = null;
    tabs = null;

    editors = {
        inputs: null,
        display: null
    }

    /**
     * Options:
     * {
     *      containerElementSelector: "body",       DOM Selector for the container DOM element the ui should be built in 
     *                                             (optional, default: "body")
     * }
     */
    constructor(controller, options) {
        this.#controller = controller;
        this.#options = options;
    }

    /**
     * Reset the UI
     */
    async reset() {
        this.notifications.reset();

        // Clean up file inputs which have been canceled
        (new Upload(this.#controller)).cleanup();
    }

    /**
     * Build the DOM tree
     */
    async build() {
        const containerElement = $(this.#options.containerElementSelector);
        if (!containerElement) {
            throw new Error("Container " + this.#options.containerElementSelector + " not found");
        }

        let messageElement = null;
        let clientButtonElement = null;
        let tabsElement = null;
        let showTabsButton = null;
        let additionalInputsElement = null;
        
        // Settings panel
        const that = this;
        containerElement.append(
            this.container = $('<div class="container"/>').append(
                // Tabs area
                tabsElement = $('<div class="tabs" />'),

                // Application area
                $('<div class="application"/>').append(
                    
                    $('<div class="about" />').append(
                        // Version
                        $('<div class="version"/>')
                        .html("PySwitch Emulator<br>v" + Controller.VERSION)
                        .on('click', async function() {
                            try {
                                await that.showAbout();

                            } catch (e) {
                                that.#controller.handle(e);
                            }
                        }),

                        // Donate
                        $('<a class="donate" href="https://www.paypal.com/webapps/mpp/page-not-found?cmd=_s-xclick&hosted_button_id=6WHW7WRXSGQXY" target="_blank" />')
                        .text('Donate')
                    ),
                    
                    // Client connection button (class is set in the ClientConnectionButton)
                    clientButtonElement = $('<div data-toggle="tooltip"/>'),

                    // This will be filled by python and show the device. Can not have any class names in 
                    // here, or they will be overwritten by python code.
                    this.#deviceElement = $('<div id="pyswitch-device"></div>'),

                    // Buttons
                    $('<div class="buttons" />').append(
                        // Load
                        $('<div class="appl-button fas fa-folder-open" data-toggle="tooltip" title="Open configuration..." />')
                        .on("click", async function() {
                            try {
                                that.loadBrowser.options.selectedValue = that.#controller.currentConfig ? (await that.#controller.currentConfig.name()) : null;
                                await that.loadBrowser.browse();

                            } catch (e) {
                                that.#controller.handle(e);
                            }
                        }),

                        // Save
                        $('<div class="appl-button fas fa-save" data-toggle="tooltip" title="Save configuration..." />')
                        .on("click", async function() {
                            try {
                                that.saveBrowser.options.selectedValue = that.#controller.currentConfig ? (await that.#controller.currentConfig.name()) : null;
                                await that.saveBrowser.browse();

                            } catch (e) {
                                that.#controller.handle(e);
                            }
                        }),

                        // Display Editor
                        showTabsButton = $('<div class="appl-button fas fa-tv" data-toggle="tooltip" title="Open display editor..."/>')
                        .on('click', async function() {
                            try {
                                await that.frontend.parserFrontend.showDisplayEditor();

                            } catch (e) {
                                that.#controller.handle(e);
                            }
                        }),

                        // Show/hide tabs
                        showTabsButton = $('<div class="appl-button fas fa-code" data-toggle="tooltip" title="Show code"/>')
                        .on('click', async function() {
                            try {
                                that.tabs.toggle();

                            } catch (e) {
                                that.#controller.handle(e);
                            }
                        })
                    ),

                    // Header, showing the current Configuration name
                    $('<div class="headline"/>').append(
                        this.#contentHeadline = $('<span />'),
                        
                        // Change marker
                        this.#changeMarker = $('<span class="change-marker" />')
                        .text("*")
                        .hide()
                    ),

                    // Additional parameters: Container
                    this.#additionalInputsContainer = $('<div class="additional-parameters-container" />')
                    .addClass('hidden')
                    .append(
                        // Additional parameters: Button
                        this.#additionalInputsButton = $('<div class="additional-button appl-button fas" data-toggle="tooltip" title="Show additional inputs" />')
                        .addClass('fa-ellipsis-v')
                        .on("click", async function() {
                            try {
                                that.showAdditionalInputs(!that.additionalInputsShown());
                                
                            } catch (e) {
                                that.#controller.handle(e);
                            }
                        }),

                        // Additional parameters
                        additionalInputsElement = $('<div class="additional-parameters" />')
                    )
                    .hide()
                ),

                /////////////////////////////////////////////////////////////////////////////////////

                // Progress bar and blocker
                this.#block = $('<div class="block"/>').append(
                    this.#progressBarContainer = $('<span class="progressBar" />').append(   // progressBarOuterContainer
                        $('<span />').append(  //progressBarContainer
                            $('<span />').append(   // progressBarBack
                                this.#progressBar = $('<span />')  // progressBar
                            )
                        ),                        
                    ),
                    this.#progressMessage = $('<span class="progressMessage" />').text("Initializing")
                ),

                /////////////////////////////////////////////////////////////////////////////////////

                // Popups (will apply their content to this)
                this.#popupContainer = $('<div class="popup-container" />').hide(),

                // Messages
                messageElement = $('<div class="messages"/>')
            )
        );

        // Browsers
        await this.#initLoadBrowser();
        await this.#initSaveBrowser();
        await this.#initClientBrowser();

        // Client state button
        this.clientButton = new ClientConnectionButton(this.#controller, clientButtonElement);      

        // Message alerts etc.
        this.notifications = new Notifications(messageElement);

        // Parser UI handler
        this.frontend = new PySwitchFrontend(this.#controller, this.#deviceElement, {
            domNamespace: this.#options.domNamespace,
            globalContainer: additionalInputsElement
        });

        // Show or hide tabs
        this.tabs = new Tabs(this.#controller, tabsElement, showTabsButton);

        // CTRL-S key to save to current location
        $(window).on('keydown', async function(event) {
            try {
                if (event.ctrlKey || event.metaKey) {
                    switch (String.fromCharCode(event.which).toLowerCase()) {
                        case 's':
                            event.preventDefault();
                            
                            try {
                                await that.#controller.currentConfig.save();
                                that.notifications.message("Successfully saved configuration to " + (await that.#controller.currentConfig.name()), "S");    
                                
                            } catch(e) {
                                console.error(e);

                                that.saveBrowser.options.selectedValue = that.#controller.currentConfig ? (await that.#controller.currentConfig.name()) : null;
                                await that.saveBrowser.browse();
                            }
                            
                            break;	
                            
                        case 't':
                            event.preventDefault();
                            
                            try {
                                const portName = (new LocalState("controllers")).get("last");
                                if (!portName) {
                                    throw new Error("No last used controller found to save to")
                                }
                                await that.#saveToController(portName, true);

                            } catch(e) {
                                console.error(e);

                                that.saveBrowser.options.selectedValue = that.#controller.currentConfig ? (await that.#controller.currentConfig.name()) : null;
                                await that.saveBrowser.browse();
                            }
                            
                            break;	
                    }
                }
            } catch (e) {
                that.#controller.handle(e);
            }
        });

        // if (!this.#controller.getState('suppressInfoPopup')) {
        //     await this.showAbout();
        // }
    }

    /**
     * Shows/hides the additional inputs panel
     */
    showAdditionalInputs(show) {
        this.#additionalInputsContainer.toggleClass('hidden', !show);
                                
        this.#additionalInputsButton.toggleClass('fa-ellipsis-v', !show);
        this.#additionalInputsButton.toggleClass('fa-times', show);
    }

    /**
     * Returns if the additional inputs are visible.
     */
    additionalInputsShown() {
        return !this.#additionalInputsContainer.hasClass('hidden');
    }

    /**
     * Completely show/hide the additional inputs panel (incl. the button)
     */
    #enableAdditionalInputs(enable) {
        this.#additionalInputsContainer.toggle(enable);
    }

    /**
     * Show the about popup
     */
    async showAbout() {
        // const that = this;

        this.getPopup({ 
            fullscreen: true,
            onClose: function() {
                // that.#controller.setState('suppressInfoPopup', true);
            }
        })
        .show(
            $('<div class="about-content" />').append(
                await Tools.fetch('about.html')
            )
        );
    }

    /**
     * Returns a new simple Popup instance
     */
    getPopup(options = {}) {
        if (!options.container) options.container = this.#popupContainer;
        if (!options.errorHandler) options.errorHandler = this.#controller;
        return new Popup(options);        
    }

    /**
     * Returns a new BrowserPopup instance
     */
    getBrowserPopup(options = {}) {
        if (!options.container) options.container = this.#popupContainer;
        if (!options.errorHandler) options.errorHandler = this.#controller;
        return new BrowserPopup(options);        
    }

    /**
     * Init browser for loading configurations
     */
    async #initLoadBrowser() {
        const that = this;

        // A browser for loading configurations, triggered by the load button
        this.loadBrowser = this.getBrowserPopup({
            wide: true,
            headline: "Please select a configuration to load",
            providers: [
                // Templates
                new TemplatesProvider(this.#controller, "templates/toc.php"),

                // Examples
                new ExamplesProvider(this.#controller, "examples/toc.php"),
                
                // Connected controllers
                new PortsProvider(this.#controller, {
                    rootText: "Connected Controllers",
                    onSelect: async function(entry) {
                        that.#controller.routing.call(that.#controller.getControllerUrl(entry.value));
                    }
                }),

                // Presets
                new LocalPresetsProvider(this.#controller, {
                    onSelect: async function(entry) {
                        // Open existing preset
                        that.#controller.routing.call(encodeURI("preset/" + entry.value));
                    }
                }),

                // Local Filesystem
                new SingleEntryProvider({
                    text: "Open Directory...",
                    onSelect: async function(entry) {
                        const sel = new LocalFolderSelection();

                        // Select a directory (which is stored in indexedDB)
                        if (!await sel.select()) return;
                        
                        // Call the local folder config (which loads the dir handle from indexedDB)
                        await sel.call(that.#controller);                        
                    },
                    sortString: "XXXXXXXXXXXXXXXX1"
                }),

                // Upload
                new SingleEntryProvider({
                    text: "Upload...",
                    onSelect: async function(entry) {
                        await (new Upload(that.#controller)).upload(that.#controller.currentConfig);
                    },
                    sortString: "XXXXXXXXXXXXXXXX2"
                })
            ]
        }); 
    }

    /**
     * Init browser for loading configurations
     */
    async #initSaveBrowser() {
        const that = this;

        // A browser for loading configurations, triggered by the load button
        this.saveBrowser = this.getBrowserPopup({
            wide: true,
            headline: "Please select a destination to store the current configuration",
            iconOpen: "fa-save",
            providers: [
                // Save to current location
                new SingleEntryProvider({
                    showCallback: async function() {
                        return that.#controller.currentConfig ? that.#controller.currentConfig.canBeSaved() : false;
                    },
                    text: async function(entry) {
                        return "Save current configuration (" + (await that.#controller.currentConfig.name()) + ") [Ctrl+S]";
                    },
                    onSelect: async function(entry) {
                        that.saveBrowser.hide();
                        await that.#controller.currentConfig.save();
                        that.notifications.message("Successfully saved configuration to " + (await that.#controller.currentConfig.name()), "S");
                    },
                    sortString: "________________"
                }),

                // Save to last used controller
                new SingleEntryProvider({
                    showCallback: async function() {
                        return !!(new LocalState("controllers")).get("last");
                    },
                    text: async function(entry) {
                        return "Save to last used controller (" + (new LocalState("controllers")).get("last") + ") [Ctrl+T]";
                    },
                    onSelect: async function(entry) {
                        const portName = (new LocalState("controllers")).get("last");
                        await that.#saveToController(portName, true);
                    },
                    sortString: "________________"
                }),

                // Connected controllers
                new PortsProvider(this.#controller, {
                    rootText: "Connected Controllers",
                    onSelect: async function(entry) {
                        await that.#saveToController(entry.value);
                    }
                }),

                // Presets
                new LocalPresetsProvider(this.#controller, {
                    newPresetsEntry: true,
                    onSelect: async function(entry) {
                        let data = null;
                        try {
                            data = await that.#controller.currentConfig.get();

                        } catch(e) {
                            console.log(e);
                            throw new Error("No data to save");
                        }

                        let presetId = null;
                        if (entry.data.newPreset) {
                            // Create new preset                            
                            while (!presetId || that.#controller.presets.has(presetId)) {
                                presetId = prompt("Name for the new preset:");
                                if (!presetId) return; // Canceled by user
                            }
                        } else {
                            presetId = entry.text;
                            if (!confirm("Do you want to overwrite preset " + presetId + "?")) return;
                        }

                        const dummyConfig = new PresetConfiguration(that.#controller, presetId);
                        dummyConfig.set(data);
                        await dummyConfig.save();

                        that.#controller.currentConfig.resetDirtyState();

                        that.notifications.message("Successfully saved preset " + presetId, "S");
                        that.#controller.routing.call(encodeURI("preset/" + presetId));
                    }
                }),

                // Local Folder
                new SingleEntryProvider({
                    text: "Save to Directory...",
                    onSelect: async function(entry) {
                        let data = null;
                        try {
                            data = await that.#controller.currentConfig.get();

                        } catch(e) {
                            console.log(e);
                            throw new Error("No data to save");
                        }

                        // Select a directory (which is stored in indexedDB)
                        const sel = new LocalFolderSelection();                        
                        if (!await sel.select()) return;

                        // Save the configuration
                        const dummyConfig = new LocalFolderConfiguration(that.#controller);
                        dummyConfig.set(data);
                        await dummyConfig.save();

                        that.#controller.currentConfig.resetDirtyState();

                        that.notifications.message("Successfully saved the configuration to the local folder", "S");
                        
                        await sel.call(that.#controller);
                    },
                    sortString: "XXXXXXXXXXXXXXXX1"
                }),

                // Download
                new SingleEntryProvider({
                    text: "Download ZIP",
                    onSelect: async function(entry) {
                        await (new Download()).download(that.#controller.currentConfig);
                    },
                    sortString: "XXXXXXXXXXXXXXXX2"
                })
            ]
        }); 
    }

    /**
     * Init browser for client connection select
     */
    async #initClientBrowser() {
        const that = this;

        const additionalEntries = [                        
            {
                value: "auto",
                text: function(/*entry*/) {
                    const client = that.#controller.client.state.get("selectedClient");
                    const currentDeviceText = (client == "auto") ? (" (" + (that.#controller.client.current ? that.#controller.client.current : "None found") + ")") : "";

                    return "Auto-detect client device" + currentDeviceText;
                },
                sortString: "___01"
            },
            {
                value: "Not connected",
                text: "Not connected",
                sortString: "___02"
            }
        ];

        const clients = await Client.getAvailable();
        for (const client of clients) {
            const vc = await client.getVirtualClient();
            if (!vc) continue;
                    
            additionalEntries.push({
                value: "virtual-" + client.id,
                text: async function(/*entry*/) {
                    return vc.name;
                },
                sortString: "ZZZZZZZ" + vc.name
            });
        }

        // A browser to select client connections (to Kemper etc.), triggered by the client select button
        this.clientBrowser = this.getBrowserPopup({
            headline: "Please select a client device to connect to",
            providers: [
                new PortsProvider(this.#controller, {
                    onSelect: async function(entry) {
                        that.#controller.client.state.set("selectedClient", entry.value);
                        
                        await that.#controller.client.init(that.#controller.currentConfig);
                    },
                    additionalEntries: additionalEntries
                })
            ]
        });
    }

    /**
     * Save current config to a controller
     */
    async #saveToController(portName, noConfirm = false) {
        let data = null;
        try {
            data = await this.#controller.currentConfig.get();

        } catch(e) {
            console.log(e);
            throw new Error("No data to save");
        }

        if (!noConfirm) {
            if (!confirm("Save current configuration to " + portName + "?")) return;
        }

        this.saveBrowser.hide();

        const dummyConfig = new ControllerConfiguration(this.#controller, portName);
        dummyConfig.set(data);
        await dummyConfig.save();    

        this.#controller.currentConfig.resetDirtyState();
        
        this.notifications.message("Successfully saved configuration to " + portName, "S");
    }

    /**
     * Sets the UI properties for the configuration
     */
    async applyConfig(config) {
        if (!config) {
            this.#contentHeadline.text("");
            
            await this.frontend.reset();

            await this.editors.inputs.setConfig(null);
            await this.editors.display.setConfig(null);
            return;
        }
        // Headline (config name)
        this.#contentHeadline.text(await config.name());
        
        // Show/hide additional parameters container
        const device = await config.parser.device();
        this.#enableAdditionalInputs(device.hasAdditionalInputs());
        
        // Apply the parser to the frontend (generates all switches etc.)
        await this.frontend.apply(config.parser);

        // Create editor tabs if not yet done
        if (!this.editors.inputs) {
            this.editors.inputs = new CodeEditor(this.#controller, "inputs.py", "inputs_py");
            this.tabs.add(this.editors.inputs, 0);
        }
        if (!this.editors.display) {
            this.editors.display = new CodeEditor(this.#controller, "display.py", "display_py");
            this.tabs.add(this.editors.display, 1);
        }
        
        // Set new content on editors
        await this.editors.inputs.setConfig(config);
        await this.editors.display.setConfig(config);

        await this.#initMidiMonitor(config);
        await this.#initSettings(config);
    }

    /**
     * Setup the MIDI monitor if not already there
     */
    async #initMidiMonitor() {
        if (this.midiMonitor) {
            this.midiMonitor.addComment("init")
            return;
        }
        
        this.tabs.add(
            this.midiMonitor = new MidiMonitor(this.#controller, "MIDI Monitor")
        );

        await this.midiMonitor.initMonitor();
    }

    /**
     * Setup the MIDI settings if not already there
     */
    async #initSettings() {
        if (this.emulatorSettings) {
            return;
        }
        
        this.tabs.add(
            this.emulatorSettings = new EmulatorSettings(this.#controller, "Settings")
        );

        // await this.emulatorSettings.initSettings();
    }

    /**
     * Let all tabs confirm if they have unapplied content
     */
    confirmIfDirty() {
        // First ask the tabs
        if (!this.tabs.confirmIfDirty()) return false;

        // Tabs said everything is ok, so check if the config is dirty
        if (this.#controller.currentConfig && this.#controller.currentConfig.isDirty()) {
            if (!confirm("You have unsaved changes. Do you want to continue?")) return false;
        }

        return true;
    }

    /**
     * Shows the passed virtual clients (array, can be empty) as tabs, one tab per virtual client.
     */
    showVirtualClients(clients) {
        for (const tab of this.#virtualClientTabs) {
            this.tabs.remove(tab);
        }
        this.#virtualClientTabs = [];

        for (const ui of this.#virtualClientUIs) {
            ui.destroy();
        }
        this.#virtualClientUIs = [];
        
        for (const client of clients) {
            // Try to create an UI
            const virtualClientElement = $('<div class="virtual-client"/>');
            const tab = new Tab(
                virtualClientElement,
                client.name ? client.name : "Virtual Client"
            )

            const ui = client.getUserInterface(virtualClientElement);    
            if (!ui) continue;   // No UI

            this.#virtualClientUIs.push(ui);
            this.#virtualClientTabs.push(tab);

            // Add tab
            this.tabs.add(tab);
        }
    }

    /**
     * Show a block screen
     */
    block() {
        this.#progressBarContainer.hide();
        this.#progressMessage.hide();

        this.#block.show();
    }

    /**
     * Show progress. Values above (and including) 1 hide the progress bar.
     * 
     * @param {*} percentage range [0..1]
     * @param {*} message 
     */
    progress(percentage, message) {
        if (!this.#block) return;

        if (percentage >= 1) {
            this.#block.hide();
            return;
        }

        const perc = (percentage * 100).toFixed(2);  
		
        this.#progressBarContainer.show();
		this.#progressBar.css('width', perc + '%');		

        this.#progressMessage.show();
        this.#progressMessage.text(message);

        this.#block.show();
    }

    /**
     * Show the dirty mark
     */
    setDirty() {
        this.#changeMarker.show();
    }

    /**
     * Hide the dirty mark
     */
    resetDirtyState() {
        this.#changeMarker.hide();
    }

    /**
     * Wrapper to show messages.
     */
    message(msg, type, options) {
        this.progress(1);

        if (this.notifications) {
            this.notifications.message(msg, type, options);
        } else {
            switch (type) {
                case 'I':
                    console.log(msg);
                    break;
                case 'S':
                    console.log(msg);
                    break;
                case 'W':
                    console.warn(msg);
                    break;
                default:
                    console.error(msg)
                    break;
            }            
        }
    }   
}