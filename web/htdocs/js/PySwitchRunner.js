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
     *      updateIntervalMillis: 10,        Tick interval in milliseconds. On CircuitPython, the program does as much ticks as it can (in a while True loop),
     *                                       which in a browser woult block all user interaction, so the ticks are triggered in intervals. Mandatory.
     *      coverage: False                  Measure coverage
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

        // Source paths
        const localPythonPath = basePath + "python/";
        const circuitpyPath = basePath + "circuitpy/lib/";

        // Set up pyodide
        console.log("Initialize Pyodide");
        this.pyodide = await loadPyodide();
        
        // Load all files by GETing them and storing them to the virtual FS.
        // TODO this could be optimized
        console.log("Load files to Pyodide");

        await this.#loadModule("PySwitchRunner.py", localPythonPath);
        await this.#loadModule("mocks.py", localPythonPath);

        this.pyodide.FS.mkdir("definitions");
        await this.#loadModule("definitions/actions.json", basePath);
        await this.#loadModule("definitions/mappings.json", basePath);

        this.pyodide.FS.mkdir("parser");
        await this.#loadModule("parser/PySwitchParser.py", localPythonPath);
        await this.#loadModule("parser/PySwitchHardware.py", localPythonPath);

        this.pyodide.FS.mkdir("parser/misc");
        await this.#loadModule("parser/misc/VisitorsWithStack.py", localPythonPath);
        await this.#loadModule("parser/misc/AddElementTransformer.py", localPythonPath);
        await this.#loadModule("parser/misc/RemoveDictElementTransformer.py", localPythonPath);
        await this.#loadModule("parser/misc/RemoveUnusedImportTransformer.py", localPythonPath);
        // await this.#loadModule("parser/misc/StripImportsTransformer.py", localPythonPath);
        await this.#loadModule("parser/misc/CollectCommentsTransformer.py", localPythonPath);
        await this.#loadModule("parser/misc/AddImportsTransformer.py", localPythonPath);
        await this.#loadModule("parser/misc/FunctionExtractor.py", localPythonPath);
        await this.#loadModule("parser/misc/ClassItemExtractor.py", localPythonPath);
        await this.#loadModule("parser/misc/AssignmentExtractor.py", localPythonPath);
        await this.#loadModule("parser/misc/AssignmentNameExtractor.py", localPythonPath);
        await this.#loadModule("parser/misc/ImportExtractor.py", localPythonPath);
        await this.#loadModule("parser/misc/RemoveAssignmentTransformer.py", localPythonPath);
        await this.#loadModule("parser/misc/AddAssignmentTransformer.py", localPythonPath);

        this.pyodide.FS.mkdir("parser/inputs");
        await this.#loadModule("parser/inputs/Action.py", localPythonPath);
        await this.#loadModule("parser/inputs/Actions.py", localPythonPath);
        await this.#loadModule("parser/inputs/Arguments.py", localPythonPath);
        await this.#loadModule("parser/inputs/Input.py", localPythonPath);
        await this.#loadModule("parser/inputs/InputReplacer.py", localPythonPath);
        await this.#loadModule("parser/inputs/InputAssignment.py", localPythonPath);
        await this.#loadModule("parser/inputs/CreateInputTransformer.py", localPythonPath);
        
        // this.pyodide.FS.mkdir("parser/pager");
        // await this.#loadModule("parser/pager/Pager.py", localPythonPath);

        this.pyodide.FS.mkdir("wrappers");
        await this.#loadModule("wrappers/__init__.py", localPythonPath);
        await this.#loadModule("wrappers/wrap_io.py", localPythonPath);
        await this.#loadModule("wrappers/wrap_adafruit_midi.py", localPythonPath);
        await this.#loadModule("wrappers/wrap_adafruit_led.py", localPythonPath);
        await this.#loadModule("wrappers/wrap_adafruit_display.py", localPythonPath);
        await this.#loadModule("wrappers/wrap_time.py", localPythonPath);
        await this.#loadModule("wrappers/WrapDisplayDriver.py", localPythonPath);
        
        //////////////////////////////////////////////////////////////////////////////////////////////

        this.pyodide.FS.mkdir("adafruit_midi");
        await this.#loadModule("adafruit_midi/__init__.py", localPythonPath);
        await this.#loadModule("adafruit_midi/active_sensing.py", localPythonPath);
        await this.#loadModule("adafruit_midi/channel_pressure.py", localPythonPath);
        await this.#loadModule("adafruit_midi/control_change.py", localPythonPath);
        await this.#loadModule("adafruit_midi/midi_continue.py", localPythonPath);
        await this.#loadModule("adafruit_midi/midi_message.py", localPythonPath);
        await this.#loadModule("adafruit_midi/mtc_quarter_frame.py", localPythonPath);
        await this.#loadModule("adafruit_midi/note_off.py", localPythonPath);
        await this.#loadModule("adafruit_midi/note_on.py", localPythonPath);
        await this.#loadModule("adafruit_midi/pitch_bend.py", localPythonPath);
        await this.#loadModule("adafruit_midi/polyphonic_key_pressure.py", localPythonPath);
        await this.#loadModule("adafruit_midi/program_change.py", localPythonPath);
        await this.#loadModule("adafruit_midi/start.py", localPythonPath);
        await this.#loadModule("adafruit_midi/stop.py", localPythonPath);
        await this.#loadModule("adafruit_midi/system_exclusive.py", localPythonPath);
        await this.#loadModule("adafruit_midi/timing_clock.py", localPythonPath);

        //////////////////////////////////////////////////////////////////////////////////////////////

        this.pyodide.FS.mkdir("pyswitch");
        await this.#loadModule("pyswitch/__init__.py", circuitpyPath);
        await this.#loadModule("pyswitch/misc.py", circuitpyPath);
        await this.#loadModule("pyswitch/stats.py", circuitpyPath);

        this.pyodide.FS.mkdir("pyswitch/clients");
        await this.#loadModule("pyswitch/clients/__init__.py", circuitpyPath);

        this.pyodide.FS.mkdir("pyswitch/clients/kemper");
        await this.#loadModule("pyswitch/clients/kemper/__init__.py", circuitpyPath);
        
        this.pyodide.FS.mkdir("pyswitch/clients/kemper/actions");         
        await this.#loadModule("pyswitch/clients/kemper/actions/__init__.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/bank_select.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/bank_up_down.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/binary_switch.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/effect_button.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/effect_state.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/looper.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/morph.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/rig_select_and_morph_state.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/rig_select.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/rig_up_down.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/rig_volume_boost.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/tempo.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/actions/tuner.py", circuitpyPath);

        this.pyodide.FS.mkdir("pyswitch/clients/kemper/mappings");
        await this.#loadModule("pyswitch/clients/kemper/mappings/__init__.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/amp.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/bank.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/cabinet.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/effects.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/freeze.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/looper.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/morph.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/pedals.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/rig.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/rotary.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/select.py", circuitpyPath);
        await this.#loadModule("pyswitch/clients/kemper/mappings/tempo.py", circuitpyPath);
        
        this.pyodide.FS.mkdir("pyswitch/controller");
        await this.#loadModule("pyswitch/controller/__init__.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/actions.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/AnalogAction.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/callbacks.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/Client.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/Controller.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/EncoderAction.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/ExploreModeController.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/InputControllers.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/MidiController.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/pager.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/RuntimeMeasurement.py", circuitpyPath);
        await this.#loadModule("pyswitch/controller/strobe.py", circuitpyPath);

        this.pyodide.FS.mkdir("pyswitch/hardware");  
        await this.#loadModule("pyswitch/hardware/__init__.py", circuitpyPath);

        this.pyodide.FS.mkdir("pyswitch/hardware/adafruit");  
        await this.#loadModule("pyswitch/hardware/adafruit/__init__.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/adafruit/AdafruitDinMidiDevice.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/adafruit/AdafruitEncoder.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/adafruit/AdafruitPotentiometer.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/adafruit/AdafruitSwitch.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/adafruit/AdafruitUsbMidiDevice.py", circuitpyPath);

        this.pyodide.FS.mkdir("pyswitch/hardware/devices");  
        await this.#loadModule("pyswitch/hardware/devices/__init__.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/devices/pa_midicaptain_10.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/devices/pa_midicaptain_mini_6.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/devices/pa_midicaptain_nano_4.py", circuitpyPath);
        await this.#loadModule("pyswitch/hardware/devices/pa_midicaptain.py", circuitpyPath);
        
        this.pyodide.FS.mkdir("pyswitch/ui");  
        await this.#loadModule("pyswitch/ui/__init__.py", circuitpyPath);
        await this.#loadModule("pyswitch/ui/elements.py", circuitpyPath);
        await this.#loadModule("pyswitch/ui/DisplaySplitContainer.py", circuitpyPath);
        await this.#loadModule("pyswitch/ui/layout.py", circuitpyPath);
        await this.#loadModule("pyswitch/ui/ui.py", circuitpyPath);
        await this.#loadModule("pyswitch/ui/UiController.py", circuitpyPath);

        await this.pyodide.loadPackage("libcst");
        
        if (this.#options.coverage) {
            await this.pyodide.loadPackage("coverage");
        }

        // Create external refs object (used to communicate with the python scripts)
        if (!window.externalRefs) {
            window.externalRefs = {};
        }  
        
        this.#initialized = true;
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
        console.log(this.#runner.running)
        return this.#runner.running;
    }

    /**
     * Run PySwitch, terminating an existing runner before. Expects a Configuration instance.
     */
    async run(config, dontTick = false) {
        console.log("Run PySwitch");
        
        await this.stop();

        // Copy the configuration to the virtual FS
        this.pyodide.FS.writeFile("/home/pyodide/inputs.py", config.inputs_py);
        this.pyodide.FS.writeFile("/home/pyodide/display.py", config.display_py);

        // Run PySwitch!
        this.#runner = await this.pyodide.runPython(`
            from PySwitchRunner import PySwitchRunner
            runner = PySwitchRunner(
                container_id = "` + this.#containerId + `", 
                dom_namespace = "` + this.#options.domNamespace + `", 
                update_interval_ms = "` + this.#options.updateIntervalMillis + `",
                coverage = ` + (this.#options.coverage ? "True" : "False") + `
            )
            runner.` + (dontTick ? 'init()' : 'run()') + `
            runner      # Returns the runner as a JS proxy
        `);
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
            from pyswitch.misc import PYSWITCH_VERSION
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