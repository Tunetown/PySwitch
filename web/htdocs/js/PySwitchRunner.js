/**
 * Manages running PySwitch on Pyodide
 */
class PySwitchRunner {

    pyodide = null;         // Pyodide instance, can be used to run code.

    #runner = null;         // Internal runner instance (python Proxy)
    #containerId = null;    // ID of the container to be used by python scripts
    #initialized = false;
    #options = null;

    /**
     * Options:
     * {
     *      domNamespace: "pyswitch",        ID prefix for access to DOM elements from Python code. All generated elements will be prefixed with this. Mandatory.
     *      updateIntervalMillis,
     *      coverage: False                  Measure coverage
     *      errorHandler: null               Optional error handler, providing a handle(exc) method
     *      configProvider: null,            Optional config.py provider, provifing an async get() method
     *      commSettingsProvider: null,      Optional comm settings provider, provifing an async get() method
     *      messageHandler: null             Optional message handler, providing a message(msg, type) method
     * }
     */
    constructor(options, containerId) {
        this.#options = options;     
        this.#containerId = containerId;   
    }

    /**
     * Set up Pyodide and copy all sources to the Emscripten virtual file system.
     */
    async init(basePath = "") {
        if (this.#initialized) return;

        // Set up pyodide
        console.log("Initialize Pyodide");
        this.pyodide = await loadPyodide();
        
        // Load all files by GETing them and storing them to the virtual FS.
        // TODO this could be optimized
        console.log("Load files to Pyodide");
        await this.#loadModules(basePath);

        await this.pyodide.loadPackage("libcst");
        
        if (this.#options.coverage) {
            await this.pyodide.loadPackage("coverage");
        }

        // Create external refs object (used to communicate with the python scripts)
        if (!window.externalRefs) {
            window.externalRefs = {};
            
            if (this.#options.errorHandler) {
                window.externalRefs.errorHandler = this.#options.errorHandler;
            }
            if (this.#options.messageHandler) {
                window.externalRefs.messageHandler = this.#options.messageHandler;
            }
        }
        
        this.#initialized = true;
    }

    /**
     * Load all files needed
     */
    async #loadModules(basePath) {
        // Source paths
        const localPythonPath = basePath + "python/";
        const circuitpyPath = basePath + "circuitpy/lib/";

        await this.pyodide.FS.mkdir("definitions");
        await this.pyodide.FS.mkdir("parser");
        await this.pyodide.FS.mkdir("parser/misc");
        await this.pyodide.FS.mkdir("wrappers");
        await this.pyodide.FS.mkdir("adafruit_midi");
        await this.pyodide.FS.mkdir("adafruit_hid");
        await this.pyodide.FS.mkdir("pyswitch");
        await this.pyodide.FS.mkdir("pyswitch/clients");
        await this.pyodide.FS.mkdir("pyswitch/controller");
        await this.pyodide.FS.mkdir("pyswitch/controller/actions");
        await this.pyodide.FS.mkdir("pyswitch/controller/callbacks");
        await this.pyodide.FS.mkdir("pyswitch/hardware");  
        await this.pyodide.FS.mkdir("pyswitch/hardware/adafruit");  
        await this.pyodide.FS.mkdir("pyswitch/hardware/devices");  
        await this.pyodide.FS.mkdir("pyswitch/ui");  

        await this.pyodide.FS.mkdir("pyswitch/clients/kemper");
        await this.pyodide.FS.mkdir("pyswitch/clients/kemper/actions");
        await this.pyodide.FS.mkdir("pyswitch/clients/kemper/mappings");
        await this.pyodide.FS.mkdir("pyswitch/clients/kemper/callbacks");
        
        await this.pyodide.FS.mkdir("pyswitch/clients/boomerang");
        await this.pyodide.FS.mkdir("pyswitch/clients/boomerang/actions");
        
        await this.pyodide.FS.mkdir("pyswitch/clients/local");
        await this.pyodide.FS.mkdir("pyswitch/clients/local/actions");
        await this.pyodide.FS.mkdir("pyswitch/clients/local/mappings");
        await this.pyodide.FS.mkdir("pyswitch/clients/local/callbacks");        
                    
        return Promise.all([
            this.#loadModule("PySwitchRunner.py", localPythonPath),
            this.#loadModule("mocks.py", localPythonPath),
            
            this.#loadModule("definitions/actions.json", basePath),
            this.#loadModule("definitions/mappings.json", basePath),
            this.#loadModule("definitions/callbacks.json", basePath),
            
            this.#loadModule("parser/PySwitchParser.py", localPythonPath),
            this.#loadModule("parser/PySwitchHardware.py", localPythonPath),
            this.#loadModule("parser/InputsExtractor.py", localPythonPath),
            this.#loadModule("parser/SplashesExtractor.py", localPythonPath),
            
            this.#loadModule("parser/misc/VisitorsWithStack.py", localPythonPath),
            this.#loadModule("parser/misc/RemoveUnusedImportTransformer.py", localPythonPath),
            this.#loadModule("parser/misc/CollectCommentsTransformer.py", localPythonPath),
            this.#loadModule("parser/misc/AddImportsTransformer.py", localPythonPath),
            this.#loadModule("parser/misc/FunctionExtractor.py", localPythonPath),
            this.#loadModule("parser/misc/ClassItemExtractor.py", localPythonPath),
            this.#loadModule("parser/misc/ClassNameExtractor.py", localPythonPath),
            this.#loadModule("parser/misc/ClassNamesExtractor.py", localPythonPath),
            this.#loadModule("parser/misc/AssignmentExtractor.py", localPythonPath),
            this.#loadModule("parser/misc/AssignmentNameExtractor.py", localPythonPath),
            this.#loadModule("parser/misc/ImportExtractor.py", localPythonPath),
            this.#loadModule("parser/misc/ReplaceAssignmentTransformer.py", localPythonPath),
            this.#loadModule("parser/misc/AddAssignmentTransformer.py", localPythonPath),
            this.#loadModule("parser/misc/CodeExtractor.py", localPythonPath),
            this.#loadModule("parser/misc/CodeGenerator.py", localPythonPath),        

            this.#loadModule("wrappers/__init__.py", localPythonPath),
            this.#loadModule("wrappers/wrap_io.py", localPythonPath),
            this.#loadModule("wrappers/wrap_adafruit_midi.py", localPythonPath),
            this.#loadModule("wrappers/wrap_adafruit_led.py", localPythonPath),
            this.#loadModule("wrappers/wrap_adafruit_display.py", localPythonPath),
            this.#loadModule("wrappers/wrap_time.py", localPythonPath),
            this.#loadModule("wrappers/wrap_hid.py", localPythonPath),
            this.#loadModule("wrappers/WrapDisplayDriver.py", localPythonPath),
            
            //////////////////////////////////////////////////////////////////////////////////////////////

            this.#loadModule("adafruit_midi/__init__.py", localPythonPath),
            this.#loadModule("adafruit_midi/active_sensing.py", localPythonPath),
            this.#loadModule("adafruit_midi/channel_pressure.py", localPythonPath),
            this.#loadModule("adafruit_midi/control_change.py", localPythonPath),
            this.#loadModule("adafruit_midi/midi_continue.py", localPythonPath),
            this.#loadModule("adafruit_midi/midi_message.py", localPythonPath),
            this.#loadModule("adafruit_midi/mtc_quarter_frame.py", localPythonPath),
            this.#loadModule("adafruit_midi/note_off.py", localPythonPath),
            this.#loadModule("adafruit_midi/note_on.py", localPythonPath),
            this.#loadModule("adafruit_midi/pitch_bend.py", localPythonPath),
            this.#loadModule("adafruit_midi/polyphonic_key_pressure.py", localPythonPath),
            this.#loadModule("adafruit_midi/program_change.py", localPythonPath),
            this.#loadModule("adafruit_midi/start.py", localPythonPath),
            this.#loadModule("adafruit_midi/stop.py", localPythonPath),
            this.#loadModule("adafruit_midi/system_exclusive.py", localPythonPath),
            this.#loadModule("adafruit_midi/timing_clock.py", localPythonPath),

            this.#loadModule("adafruit_hid/__init__.py", localPythonPath),
            this.#loadModule("adafruit_hid/keycode.py", localPythonPath),

            //////////////////////////////////////////////////////////////////////////////////////////////

            this.#loadModule("pyswitch/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/misc.py", circuitpyPath),
            this.#loadModule("pyswitch/colors.py", circuitpyPath),
            this.#loadModule("pyswitch/debug_tools.py", circuitpyPath),
            this.#loadModule("pyswitch/stats.py", circuitpyPath),
            
            this.#loadModule("pyswitch/clients/__init__.py", circuitpyPath),

            this.#loadModule("pyswitch/clients/kemper/__init__.py", circuitpyPath),
            
            this.#loadModule("pyswitch/clients/kemper/actions/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/bank_select.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/bank_up_down.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/effect_button.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/effect_state.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/effect_state_extended_names.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/looper.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/morph.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/rig_select_and_morph_state.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/rig_select.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/rig_up_down.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/rig_volume_boost.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/rig_transpose.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/tempo.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/tempo_bpm.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/tuner.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/amp.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/bank_select_encoder.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/actions/fixed_fx.py", circuitpyPath),

            this.#loadModule("pyswitch/clients/kemper/mappings/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/amp.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/bank.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/cabinet.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/effects.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/freeze.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/looper.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/morph.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/pedals.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/rig.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/rotary.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/select.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/tempo.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/tempo_bpm.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/system.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/mappings/fixed_fx.py", circuitpyPath),
            
            this.#loadModule("pyswitch/clients/kemper/callbacks/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/callbacks/tempo_bpm.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/kemper/callbacks/convert_volume.py", circuitpyPath),

            this.#loadModule("pyswitch/clients/local/__init__.py", circuitpyPath),
            
            this.#loadModule("pyswitch/clients/local/actions/binary_switch.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/local/actions/pager.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/local/actions/pager_direct.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/local/actions/hid.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/local/actions/encoder_button.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/local/actions/param_change.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/local/actions/custom.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/local/actions/rotate.py", circuitpyPath),

            this.#loadModule("pyswitch/clients/local/callbacks/splashes.py", circuitpyPath),

            this.#loadModule("pyswitch/clients/local/mappings/generic.py", circuitpyPath),

            this.#loadModule("pyswitch/clients/boomerang/__init__.py", circuitpyPath),

            this.#loadModule("pyswitch/clients/boomerang/actions/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/clients/boomerang/actions/boomerang.py", circuitpyPath),

            this.#loadModule("pyswitch/controller/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/controller.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/client.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/explore.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/inputs.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/midi.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/measure.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/strobe.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/preview.py", circuitpyPath),

            this.#loadModule("pyswitch/controller/actions/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/actions/AnalogAction.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/actions/EncoderAction.py", circuitpyPath),

            this.#loadModule("pyswitch/controller/callbacks/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/callbacks/effect_enable.py", circuitpyPath),
            this.#loadModule("pyswitch/controller/callbacks/parameter_display.py", circuitpyPath),

            this.#loadModule("pyswitch/hardware/__init__.py", circuitpyPath),

            this.#loadModule("pyswitch/hardware/adafruit/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/adafruit/AdafruitDinMidiDevice.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/adafruit/AdafruitEncoder.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/adafruit/AdafruitPotentiometer.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/adafruit/AdafruitSwitch.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/adafruit/AdafruitUsbMidiDevice.py", circuitpyPath),

            this.#loadModule("pyswitch/hardware/devices/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/devices/pa_midicaptain_10.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/devices/pa_midicaptain_mini_6.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/devices/pa_midicaptain_nano_4.py", circuitpyPath),
            this.#loadModule("pyswitch/hardware/devices/pa_midicaptain.py", circuitpyPath),
            
            this.#loadModule("pyswitch/ui/__init__.py", circuitpyPath),
            this.#loadModule("pyswitch/ui/elements.py", circuitpyPath),
            this.#loadModule("pyswitch/ui/DisplaySplitContainer.py", circuitpyPath),
            this.#loadModule("pyswitch/ui/layout.py", circuitpyPath),
            this.#loadModule("pyswitch/ui/ui.py", circuitpyPath),
            this.#loadModule("pyswitch/ui/UiController.py", circuitpyPath),
        ]);
    }

    /**
     * Set a callback on change of protocol state
     * cb(state) => void
     */
    setProtocolStateCallback(cb) {
        window.externalRefs.stateCallback = cb;
    }

    /**
     * Returns the current protocol state
     */
    getProtocolState() {
        if (!window.externalRefs) return null;
        return window.externalRefs.protocolState;
    }

    /**
     * Overrides current time for testing
     * 
     * callback() => seconds (replaces time.monotonic())
     */
    setTimeCallback(callback) {
        if (!window.externalRefs) {
            window.externalRefs = {};
        }
        window.externalRefs.overrideMonotonic = callback;
    }

    /**
     * Has to be called before running to provide a MIDI wrapper. This has to feature a send(bytes) method and
     * a messageQueue attribute holding incoming messages as raw bye arrays (one per queue entry).
     */
    setMidiWrapper(midiWrapper) {
        if (!window.externalRefs) return;

        // If there is an old MIDI wrapper, detach it so it does not listen anymore
        if (window.externalRefs.midiWrapper) {
            window.externalRefs.midiWrapper.detach();
        }

        // Set the new MIDI wrapper. This will be accessed in the python MIDI wrappers.
        window.externalRefs.midiWrapper = midiWrapper;
    }

    /**
     * Returns if a MIDI wrapper is set
     */
    hasMidiWrapper() {
        if (!window.externalRefs) return false;
        return (!!window.externalRefs.midiWrapper);
    }

    /**
     * Adds a MIDI monitor. Must provide monitorInput and monitorOutput methods.
     */
    setMidiMonitor(monitor) {
        if (!window.externalRefs) return;
        window.externalRefs.midiMonitor = monitor;
    }

    /**
     * Stop if already running
     */
    async stop() {
        if (this.#runner) {
            this.#runner.stop()

            while(true) {
                if (!this.#runner || !this.#runner.running) break;
                await new Promise(r => setTimeout(r, this.#options.updateIntervalMillis / 4));
            }   
             
            this.#runner = null;
        }        
    }

    /**
     * Is the PySwitch engine running?
     */
    isRunning() {
        if (!this.#runner) return false;
        
        return this.#runner.running;
    }

    /**
     * Run PySwitch, terminating an existing runner before. Expects a Configuration instance.
     */
    async run(config, dontTick = false) {
        console.log("Run PySwitch");
        
        await this.stop();

        const data = await config.get();

        // Copy the configuration to the virtual FS
        this.pyodide.FS.writeFile("/home/pyodide/inputs.py", data.inputs_py);
        this.pyodide.FS.writeFile("/home/pyodide/display.py", data.display_py);

        // Determine display dimensions
        const displayDimensions = (await Device.getInstance(config)).getDisplayDimensions();
        const displayWidth = displayDimensions[0];
        const displayHeight = displayDimensions[1];

        // Create runner proxy
        this.#runner = await this.pyodide.runPython(`
            import json
            from lib.pyswitchRunner import PySwitchRunner
            runner = PySwitchRunner(
                container_id = "` + this.#containerId + `", 
                dom_namespace = "` + this.#options.domNamespace + `", 
                coverage = ` + (this.#options.coverage ? "True" : "False") + `,
                tickInterval = ` + this.#options.updateIntervalMillis + `,
            )
            runner      # Returns the runner as a JS proxy
        `);

        const client = ClientFactory.getInstance(await ClientFactory.estimateClient(config));
        
        const config_py = this.#options.configProvider ? (await this.#options.configProvider.get()) : {};
        const comm_settings = this.#options.commSettingsProvider ? (await this.#options.commSettingsProvider.get()) : {};

        if (dontTick) {
            // Initialize, but dont run PySwitch
            this.#runner.init(displayWidth, displayHeight, client, config_py, comm_settings);
        } else {
            // Run PySwitch!
            this.#runner.run(displayWidth, displayHeight, client, config_py, comm_settings);
        }
    }

    /**
     * For testing, this executes a tick manually.
     */
    async tick() {
        if (!this.#runner) throw new Error("No runner found");

        this.#runner.tick();
    }

    /**
     * Get PySwitch version
     */
    async getVersion() {
        console.log("Get PySwitch version");
        
        return this.pyodide.runPython(`
            from lib.pyswitch.misc import PYSWITCH_VERSION
            PYSWITCH_VERSION
        `);
    }

    /**
     * Load a file into the virtual Emscripten file system. fileName is the path and name of the file inside the virtual FS,
     * rscPath will be added as prefix if set for getting the files on the web server.
     */
    async #loadModule(fileName, srcPath) {
        const code = await Tools.fetch((srcPath ? srcPath : "") + fileName);
        this.pyodide.FS.writeFile("/home/pyodide/" + fileName, code);
    }
}