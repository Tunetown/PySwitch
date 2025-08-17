# PySwitch v2.4.7
- Features
    - Added an action to switch the new fixed effect slots of the Kemper MkII products on/off with bidirectional feedback from the Kemper. There is a simple demo example in the examples/Kemper/MIDICaptain 10 folder, and the states are also included in the Virtual Kemper.
    - Added support for the Boomerang III Phrase Sampler (Added generic Program Change Mapping and an example, thanks to @manderscripts)
    - Added some parameters to the "Other Parameter" action which is now called "Other Paremeter with Feedback" (which it is: If you just want to send messages, there is the new "Rotating MIDI Messages" action you can use with just one message)
    - Added a Rotating MIDI Messages action. This can be used to set up certain scenarios with rotating messages, texts, colors (LED and/or display) etc. Has been added as a side-product of the boomerang support.
    - Added new effect slot IDs which control the DLY and REV slots without spillover

- Bugfix: use_internal_state parameter of BINARY_SWITCH action was not working

### Emulator 2.4.7.14
- Features:
    - Added a Settings tab, which can control the following:
        - MIDI channels the emulator uses
        - config.py settings for the emulator. These can also be downloaded to be used on a real device.
- Some optimizations
- Some minor bug fixes

# PySwitch v2.4.6
- Features:
    - Added **Mapping for Space Intensity** to clients/kemper/mappings/system.py (@quemper)

- Bug Fixes / Optimizations:
    - **Bank Up/Down, Bank Select, Rig Select** Actions: These were updating their displays also when not enabled. This led to wrong displays when a Pager is used. (@quemper)
    - **Other Parameter** (BINARY_SWITCH) Action: Auto-quantize the input values of the parameters "value_enable", "value_disable" and "reference_value" to integer. Float values never make sense here.

### Emulator 2.4.6.13
- Features:
    - Added a new **Graphical Display Editor** making it possible to edit the display layout (display.py) in a user friendly way. Open it by clicking on the display or the new button on the top right. You can select display labels, drag them around, create/delete labels, set colors annd callbacks etc.
    - Added **Save to last used Controller** option (CTRL-T)
    - The Emulator can now be installed as **PWA** (<a href="https://developer.mozilla.org/en/docs/Web/Progressive_web_apps">Progressive Web App</a>). In Chrome, select "Install PySwitch Emulator" at the right of your address bar, and you will get a standalone App separated from Chrome.
    
- Cosmetical improvements

# PySwitch v2.4.5
- Features:
    - Added **Bank Select Action for the Wheel Encoder**. Turning the wheel preselects the bank. To use the wheel pushbutton to acknowledge the bank keeping the current rig, the possibility to set rig = None for the Rig Select action(s) has been added. This enables to use it as push action for the wheel when used as bank preselector, to acknowledge the preselected bank with the current rig.

- Bug Fixes: 
    - **Rig Select, Rig Select & Morph Display, Bank Select, Bank Up/Down, Rig Up/Down**: Now the rig select trigger sequence is correct, sending 1 at push and 0 at release, instead of sending them both on push. This enables the Kemper rig button morph function to work also in momentary mode. (@NickMrChaos)
        - Added an option "momentary_morph" to the Rig Select action(s) which adjusts the "simulated" morph state in accordance to that. Set this to True if you use momentary morph in your rigs.
    - **Bank up/down** Action: LEDs are now reset correctly after exiting tuner mode (@MetalMauce and others)
    - Updated examples: 
        - Nano 4 / tunetown KBDN
        - Nano 4 / tunetown Session with Looper and Pages

### Emulator 2.4.5.11
- Features: 
    - Added support for opening folders on the local file system:
        - "Open Directory..." lets you choose a folder to open, containing your configuration (inputs.py and display.py)
        - After changing, you can save anytime with CTRL-S, overwriting the loaded files
        - Changes made from external editors will immediately reload the emulator automatically if no unsaved changes exist, making it possible to work with external IDEs seamlessly
        - "Save to Directory..." lets you save the current config to any folder on your file system (you have to create the folder yourself first, which is possible in the selection dialog directly)
        
        The feature is implemented using the <a href="https://developer.mozilla.org/en-US/docs/Web/API/File_System_API">File System API</a>, which must be supported to use the functionality. Also, you have to grant access to any folders you want to access.

- Some minor cosmetical changes
- Rework of the publishing helper scripts (internal)

### Emulator 2.4.5.12
- Features:
    - Added a link to the MC10 wheel which opens/closes the additional inputs panel at the bottom.

- Bug Fixes:
    - Input Settings could not be changed due to an error.

# PySwitch v2.4.3
- Features:
    - Added mappings for some system parameters (can be used with the wheel encoder, pedals or the "Other Parameter" Actions):
        - Main volume
        - Monitor volume
        - Looper volume

- Minor improvements:
    - Explore Mode: After a pin has been triggered, do never return it to dark blue but keep it light blue. This way no triggers will be missed if they are very short after each other.
    - Added some undocumented, fine grained effect type names for the "Effect State (extended)" action
    - Updated the "Expression Pedals and Wheel" example to use the newer wheel accept/cancel functions on the button

- Bug Fixes:
    - The LED lightup on boot caused crashes due to insufficient power from a toaster of one user on the forum (@seve), so it has been removed.
    - Removed the Expression pedal assignment in the default preset (this causes problems out of the box when no pedal is connected)
    - Parameter Up/Down action: This was interfering with the tuner mode LED control, causing the LEDs not to go dark when tuner mode is activated.

### Emulator 2.4.3.10
- Fixes:
    - Sorting of mappings in the select dropdowns

- Cosmetic improvements:
    - Added a note to check versions when a python error is displayed (incl. link to older versions of the emulator)

# PySwitch v2.4.2
- Features:
    - Values in the Big Display Label:
        - Added the preview display parameters (like for the encoder) also to the pedal action (if change_display is set, this will display the exact value for 1.5s, then revert to the original display text)
        - Added the preview display parameters (like for the encoder) also to the Show Tempo action (which now can also show BPM in a header/footer display as well as in the Rig Name display when change_display is set). All examples using Show Tempo have been updated to use this feature.
    
    - Added Parameter Up/Down action: This can for example be used to lower/raise the value of a parameter by a given offset. (Also for this there are several value display possibilities). This can replace missing expression pedals :) I personally use it for changing the Reverb Mix on the fly without sacrificing my Volume Pedal. See the "Parameter Up Down" example for the Nano 4 for demonstration.

    - Added a custom MIDI message action. This (for now) just sends a single arbitrary byte sequence, set by the message parameter. Especially useful when exploring the MIDI specification of devices like the Kemper, in conjunction with the new MIDI monitor (see Emulator changes).

    - Added mapping for global rig transpose, as well as a dedicated whell encoder action showing the correct values
    - Added all fonts from the original firmware (they dont take up RAM if not loaded, but now they are all available)

- Fixes:
    - Bank Preselect: When you pre-select a bank, and then change the rig on the Kemper, the preselect stays valid in the Kemper. This behaviour (which is kind of unlogical) is now also reflected in PySwitch: You have to send a Rig Select message to end the preselection. This resembles the Kemper behaviour better.

- Optimizations:
    - Modularized colors out of misc.py (some RAM gain). This import path for color stuff has changed to "pyswitch.colors", if you use that in your config somewhere, it has to be adjusted. All examples are already adapted.
    - Changed mapping names to fit better into the preview displays
    - Added some mapping dependencies (no functional changes)
    - Changed the internal interface of the action callbacks a bit. If you defined your own callbacks: The action parameter is removed from most methods, replace this with "self.action" if you need it. This saves some (minor but still) RAM again. No other changes to the config files.
    - Optimized Pager (in terms of RAM, no functional changes)
    - Renamed mapping MAPPING_DELAY_MIX to MAPPING_DLY_REV_MIX (config needs to be changed only if you have this mapping adressed in the "Other" action or by code)
    - Cosmetical: Reset all LEDs before processing (this way, unused LEDs are not randomly lit anymore)

### Emulator 2.4.2.9
    - Added a MIDI Traffic Monitor, showing all MIDI messages sent and received by the PySwitch emulator.
    - Other cosmetic optimizations

# PySwitch v2.4.1
- Optimizations for performance/RAM:
    - Modularized the misc.py code out, only loaded when debugging is active. This gave us another ~5-10kB from the start!
    - Singletons for all Mappings: This led to huge RAM savings with larger constellations (up to 10kB, because of fewer MIDI message objects in memory). This especially helped when mappings are used multiple times (for example the morph state in RIG_SELECT_AND_MORPH_STATE). No changes to config files necessary.
- Refactorings: 
    - Changes import structure. For most users using the standard MIDI routing delivered with PySwitch, there is nothing to change. If you implemented custom routings: There is one change to the communication.py file: The line "from lib.pyswitch.controller.MidiController import MidiRouting" must be changed to "from lib.pyswitch.controller.midi import MidiRouting".

### Emulator 2.4.1.8
- Added MIDI traffic stats display to Virtual Kemper
- Optimized a bug that caused double the MIDI traffic needed when using the Virtual Kemper (no effect when connected to a real client)


# PySwitch v2.4.0
- Changed default preset to a MC10 example close to the original PaintAudio KPP firmware
- Option "hold_repeat" for Inputs: When enabled, the hold action is repeated again and again as long as the switch is held down.
- Added Pushbutton Option "NO_STATE_CHANGE", to be able to have a completely passive action assigned to a switch, for example to just show the effect state of a lot without having a switch for that functionality
- Rework of Paging:
    - Removed display parameter from Select Action (the display should be assigned only to the pager), see next point
    - Changed display handling: Formerly, for direct page select, displays were needed for each page, being a waste of space so no one did that. Now, only one display can be assigned to the pager itself, which always shows the current page.
    - Added an Error if a PagerAction is used by a Select Page (proxy) Action while not being part of any switch itself.
- Effect State action:
    - Added text/color override parameters
    - Added "show_slot_names" option, adding the slot name as prefix to the effect category
    - Added an extended variant which shows dedicated type names for each Kemper type ID. This gives more information, but also needs a bit more RAM, so use with care.
- Added "max_bank" parameter to Bank Up/Down actions. Set this to 10 for the Player Level I. Only relevant if the preselect option is enabled.
- Added HID (Human Interface Device) support, see the new Action "USB Keyboard". This basically emulates an USB Keyboard: with the new action you can send key commands to the USB host. This way, PySwitch can additionally become a page turner for example. Also sequences of keys can be sent with one switch.
- Wheel Encoder: 
    - Added preview display parameter: Can be set to a diplay label which will then show the values while adjusting
    - Added parameter "accept_action" and a corresponding action "Accept Encoder Value" action. If these are used in conjunction, the wheel does not send any value until the accept switch is pushed. See the default PySwitch preset and the action info texts.
- Minor refactorings:
    - Merged KemperParameterMapping and KemperTwoPartParameterMapping classes into the Client implementation
- Added instructions (README) and examples for creating multi-boot scenarios, to load the original firmware when some switch is pushed during bootup.

### Emulator 2.4.0.7
- Load time optimization (load python files in parallel)

### Emulator 2.4.0.6
- Added switch settings (new button beneath the "+" button): Here you can adjust the hold time as well as the new "Hold Repeat" option (see above)
- More "realistic" rig names in the virtual Kemper client (the old ones suggested there is a rig ID by default)
- Review of tooltips, descriptions etc.
- Levels of advanced parameters: When clicking "show more...", the parameters will be unveiled by level of "advancedness". All nerdy parameters only show up in the last level. This keeps the technical parameters hidden except you really want to see them.
- Fixed a visual bug with color inputs
- Fixed a bug that did not show error messages in the PySwitch tick routine correctly


# PySwitch v2.3.5
- Changed parameters for PagerAction (all config options now accessible as parameters directly). Examples have been adjusted, some documentation can be found in the Emulator [README](https://github.com/Tunetown/PySwitch/blob/main/web/README.md).
- Added option to directly select pages (see proxy method of PagerAction, demonstrated in some new examples for the MIDI Captain 10)

### Emulator 2.3.5.5
- Added color input help
- Added explanation to the client select dialog
- Auto-add quotes to text parameters and page texts
- Prevent assigning pagers to their own pages

### Emulator 2.3.5.4
- Added full support for all Paging functionality (see Pager and Select Page actions)
- Usability changes: 
    - Parameter comments now shown as tooltips to reduce information overflow
    - Better display names for some actions


# PySwitch v2.3.4
- Reset state of the Effect Button actions on rig changes
- RIG_SELECT_AND_MORPH_STATE now can be used inside [] brackets like any other action (action lists are flattened initially)
- Bug Fix in the Kemper Bidirectional Protocol Implementation: Send init beacon even if we already received keep-alive messages from a former connection. This makes re-connecting easier in development and the new Emulator currently being developed.
- Changed the order of the bottom LEDs, to be a mirror of the upper LEDs order. This makes way more sense for switches with two actions sharing the LEDs, where the second action used the wrong LED before. The fix was just swapping the pixel addressing in lib/pyswitch/hardware/devices, if you like the old order better, just copy the definitions into inputs.py (just the bottom switches) and swap them back to linear order.
- Finally there is a **Web-based Configuration Tool**, currently released in alpha phase: The **"PySwitch Emulator"!** See README. This can change patches with a graphical user interface, and directly load/save them to the device. Also, it can directly control your Kemper! PySwitch is running in an emulated Python environment called "Pyodide" to achieve that (the original PySwitch code, no fake!), which is very handy for configuring the controller, trying things out, even for development of new features!

### Emulator 2.3.4.3
- Updated Pyodide to 0.27.3, fixing issues on Safari on iOS


# PySwitch v2.3.3
- Fixed behaviour of bank preselect:
    - **BANK_SELECT**: Now also can override a previously made selection
    - **BANK_UP, BANK_DOWN**: Preselect mode added. Can be used to step through banks before selection.

# PySwitch v2.3.2
- Bug Fixes:
    - **RIG_SELECT_AND_MORPH_STATE, RIG_UP, RIG_DOWN, BANK_SELECT, BANK_UP, BANK_DOWN**:
        - Reset the internal morph state globally (like RIG_SELECT did before already)
    - **RIG_UP, RIG_DOWN**:
        - Fixed overflow behaviour (RIG_UP at rig "125-5" now switches to "1-1" and vice versa)
    - **BANK_SELECT** with Preselect Option enabled:
        - Do not enter preselect mode again when the bank is already selected        
    - **Tuner**:
        - All buttons disable the tuner now, also if no TUNER_MODE action is contained in the preset
        - Strobe: Only show one spot on all devices, and disable by default
    - The maximum number of banks was incorrectly set to 126 (now: 125)
    
- Added/extended Features:
    - Added an option "process_overridden_actions" to TunerDisplayCallback (disabled by default). If this is enabled, the buttons keep their functionality when in tuner mode. But still, all buttons trigger switching off the tuner.
    - **BANK_SELECT** with preselect option enabled: 
        - Will now also show the preselected bank in the rig name label
        - All RIG_SELECT switches will blink as well until the rig is selected


# PySwitch v2.3.1
- Bug fix crashing the controller in certain constellations


# PySwitch v2.3.0
- Added Expression Pedal support (for MIDI Captain 10-Switch versions). This includes renaming the switches.py file to inputs.py. See examples for the 10 switch MIDI Captain.
- Added support for the rotary wheel on the MIDI Captain 10-Switch versions. Both the rotary encoder as well as the push button can be mapped. See examples.
- Added BANK_SELECT action for changing/toggling banks but stay at the same rig
- Added RIG_UP and RIG_DOWN actions (see examples for the Nano 4)
- Added option to RIG_SELECT and RIG_AND_BANK_SELECT which remembers the current rig in "off" state and switches back to it when disabling again. 
- Added option to RIG_SELECT and etc. to regard the "Rig Btn Morph" setting in the Kemper when selecting the current rig again. See the CurryFlurry Example for the Mini 6.
See example Nano 4 -> tunetown Session.
- Tuner mode:
    - Disable tuner mode with any switch
    - Added strobe tuner using all available LEDs when in tuner mode (active by default, can be disabled with parameter "strobe" in TunerDisplayCallback / display.py if you do not like to use it)
- Morph Button: When pushing this, the displayed state will be toggled whatever the Kemper says. Only if the Kemper sends an updated value, it will be updated on the controller, too. Note: This does only work when morph is triggered from the Controller! When using the Kemper "Rig Btn Morph" option, this will not be reflected.
- Added Looper mappings (see example Nano 4 -> tunetown Session with Looper and Pages). 
- Added Paging: Use class PagerAction to step through multiple pages with individual actions. Also partial pages are possible. The actions are switched via callback, see example Nano 4 -> tunetown Session.with Looper and Pages.
- Tempo Display is now darker by default, and brightness for on and off states can be adjusted by using the "led_brightness_\*" parameters of the SHOW_TEMPO action
- Effect Button mappings now just toggle their states regardless of the state on the Kemper (much of you wanted this). Can be disabled to the old behaviour by setting use_internal_state to False.
- Default global brightness factors for LEDs and DisplayLabels can now be set optionally in config.py, see comments there.
- Now supporting file editing from the browser via MIDI using the <a href="https://github.com/Tunetown/MidiBridge">MidiBridge</a> library. <a href="https://demo.midibridge.tunetown.de">Click here</a> with your device connected to the computer via USB (no switches pressed!) and it will automatically connect. This needs no USB mounting/unmounting and is useful for quick experimenting and changing settings. Should also serve as proof-of-concept for building a visual editor in the future (!)
- The code from code.py now is moved to a function inside the init script of the module, so multi-boot scenarios (different firmwares on button presses on boot, like @gstrotmanns version does) are also possible. Unit tests added for the init script.
- Further performance optimizations, the following ones need config file adjustments:
    - Merged HoldAction into Footswitch controller (put "actionsHold" into the switch definition directly instead)
    - All Kemper action pre-definitions are now separated in files. In switches.py, you now have to omit the KemperActionDefinitions. prefixes, and import the action definitions you need separately (see examples) which is a huge memory benefit.
    Implementation Notes: kemper.py code is now way smaller and moved to pyswitch/clients/kemper/\__init__.py
    - Hardware implementations are now separated into files for the different MIDI Captains. At the top of inputs.py (formerly switches.py), adjust to the device you use, see examples.
    - Removed performance dot (remove this from display.py if exists)
    - Merged HierarchicalDisplayElement into DisplayElement (replace HierarchicalDisplayElement with DisplayElement in display.py)
    - Removed DisplaySplitContainer and subtractive layouting (manually set display areas instead in display.py, see examples)
    - Removed some redundant actions for the sake of memory savings:
        - RIG_AND_BANK_SELECT: Use RIG_SELECT instead (which now supports bank and bank_off parameters)
        - RIG_AND_BANK_SELECT_AND_MORPH_STATE: Use RIG_SELECT_AND_MORPH_STATE instead (which now supports bank and bank_off parameters)
        - MORPH_BUTTON_WITH_DISPLAY: Use MORPH_BUTTON instead, setting the color parameter to "kemper".
- Removed the davjunk example (the Arek77 example does the same but better), added several new examples

# PySwitch v2.2.2
- Morph pedal position can now be requested from the Kemper. The position can be visualized with colors (faded between red and blue). See tehguitarist's example. Thanks to @sumsar for the NRPN mapping info.
- Prepared support for transfering files from and to to device via MIDI SysEx. Currently no client for this is implemented yet, so this is deactivated by default. 

# PySwitch v2.2.1
- Added first experimental hardware assignments and example for MIDICaptain 10

# PySwitch v2.2.0
- Tempo-synced blinking switch LEDs (all examples using TAP_TEMPO now include this feature) or labels
- Show current bank colors for RIG_SELECT (...) and bank up/down action definitions
- RIG_SELECT (and the new RIG_AND_BANK_SELECT): 
    - Correct call sequence to also support the Kemper "Rig Btn Morph" option correctly. If you activate the option on the Kemper (System Menu), the actions will toggle morph state just like the internal Kemper switches.
    - Two display modes are supported:
        - Show the current rig and bank
        - Show the rig and bank which will be switched to when the switch is pushed.
    - Text of the display label can be set via a custom callback function.
    - Color of the display label can be set via a custom callback function.
- RIG_VOLUME_BOOST now remembers the current rig volume before turning the boost on, and restores this volume when disabled again.
- Added morph button support (sadly there is no feedback from kemper about the current state, so the action does not show any states)
- Fixed calibration of TunerDisplay (this now can also be customized in display.py as well as tuner colors and note names)
- Changes to configuration and general concept:
    - Conceptual changes:
        - Displays are not addressed via ID/index anymore, instead a reference to the DisplayLabel instances has to be passed to "display". See examples.
        - Conditions are replaced completely by callbacks, which provide more flexible programming of custom displays. See README.
        - ParameterAction and EffectEnableAction have been replaced completely with callbacks, too. See BinaryParameterCallback and EffectEnableCallback.
    - Minor changes to config:
        - communication.py: "valueProvider" no longer needed (now implemented in the mappings directly)
        - All members of KemperMappings now are functions (some still have been class attributes)

# PySwitch v2.1.2
- Memory usage optimized: 
    - Avoid keeping of config dictionaries for longer than __init__
    - Removed corner radius from display elements
    - "fake stroke" (DisplayLabel)
    - On-flash consts (micropython optimization)
    - Reduced class footprint
    -> Tested with big configuration (4 FX slot display labels, rig name, Tuner, 10 Switches with 3 LEDs each, Effect Enable Actions with expensive mappings on all switches) with no problems and still about 20% of RAM left
- Added examples
- Tuner sensitivity adjusted, colors changed for lighter ones

# PySwitch v2.1.1
- Added mappings for Effect Buttons I-IIII (set only, sadly there is no state feedback possibility from Kemper)

# PySwitch v2.1.0
- Bidirectional communication with the Kemper devices
- Tuner Splash showing tuner note and deviation from the note visually
- HoldAction to assign different actions on long press
- ParameterAction: Supports different comparison modes now
- Bug fixes / Unit Tests updated
 
# PySwitch v2.0.0
- Complete Rewrite (standalone firmware without dependency on PaintAudio Code, object oriented design etc.)
- Customization by config script
- Out-of-the-box Compatibility with PaintAudio MIDICaptain Nano (4 Switches) and Mini (6 Switches),
  configurable easily for other devices using the new Explore mode (Detect IO addressing for new devices)
- Activate auto-reload when switch 2 (GP25) is pressed during boot
- Conditions in switch assignents an display layouts, to make the configuration depending on device 
  parameters like the rig name
- ...

