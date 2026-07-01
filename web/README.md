# PySwitch Emulator

This is a web based configuration/emulation tool for PySwitch. If you just want to use it, you can access the demo of this code here:

https://pyswitch.tunetown.de

![image](https://github.com/user-attachments/assets/e773644b-3e74-48e6-8a7e-b6406f0ba8f0)

NOTE: This uses some quite new web features, so take care to use it with a reasonably new browser version. The emulator still is in Alpha state, so currently it is only tested in the latest Chrome browser, but Safari/Firefox should work as well. Please open an issue on Github or inform me directly if you encounter problems.

## Compatibility

The emulator needs the [Web MIDI API](https://developer.mozilla.org/en-US/docs/Web/API/Web_MIDI_API) to connect to devices. If no Web MIDI access is provided, you can still use it, but without MIDI for sure.

In general, the emulator uses pretty modern CSS features, so be sure to run a recent version of your browser, and in case anything is not working, first update the browser before opening an issue.

Tested browsers:

- Chrome: This is the recommended browser for the emulator. 
- Firefox: Fully supported.
- Safari: Works basically, but there are a few issues:
    - No MIDI
    - The rendering is blurry sometimes, but this seems like a Safari bug

## Versioning

The emulator version always consists of the PySwitch version it is based on, plus one digit for the emulator itself. Always ensure that the controllers you connect run the same version, or you might get syntax errors when running the generated configurations on your real device.

If you cannot do this for whatever reason, any older release of the emulator is also still accessible at:

https://pyswitch.tunetown.de/versions

## Usage

When launched, the emulator does the following:

1. Scan all available MIDI ports for connected controllers (like a MIDI Captain) running a suitable version of PySwitch. 
    a. If there is one found, it loads the configuration from it and runs it in the browser, on an emulated device.
    b. If no controller is connected, the default PySwitch configuration is loaded and run.
2. Now the emulator scans again on all MIDI ports, if a client device (like the Kemper Player) is connected. 
    a. If one has been found, it will be connected to the running PySwitch emulation, so the emulated device controls your Kemper in realtime.
    b. If no client has been found, a virtual Kemper implementation is created and connected, so you can play around and develop presets also when no Kemper is at hand.

### Clients

When we are taking about "clients", this always means devices to control like the Kemper Player. As PySwitch can in theory control multiple clients (even at once), there can be multiple clients.

The emulator (as stated above) will scan automatically for connected clients if nothing is manually done, but you can set the client manually also if you like. Click on the client state button in the lower right corner to set the connected client.

![image](https://github.com/user-attachments/assets/e61ed695-2c3c-429e-8668-8a7472c6a60e)

### Devices

If the word "device" is used, we always mean the device running PySwitch. The emulator (as well as PySwitch itself) supports multiple devices. Currently only the MIDI Captain series of PaintAudio is provided, but others (including DIY controllers) can be added easily. The only prerequisite for the device is to run CircuitPython.

The emulator simulates all hardware switches etc. with HTML, so you can click on the foot switches for example to trigger the actions.

### Configurations

A configuration for PySwitch consists of the following files:

- **display.py:** Defines the display layout
- **inputs.py:** Defines the input assignments

In the emulator, configurations each have their own URLs. You can load/save configurations from/to various sources:

- **Examples:** You can run any example provided with PySwitch directly.
- **Controllers:** You can load from/save to any connected Controller device directly. This is realized via a proprietary MIDI SysEx protocol.
- **Local Presets:** You can store/load configurations locally in your browser. These presets will persist untile someone clears your browser's cache manually.
- **Open Directory / Save to Directory:** You can open a local folder on your file system, containing inputs.py and display.py files. After opening, the emulator can save back to those files with CTRL-S quickly. Also, if the files are changed by an external program, the emulator automatically reloads the configuration from the changed files (if no unsaved changes exist in the emulator itself, of course). This makes working with external IDEs pretty easy.
- **Upload/Download:** You can upload configuration files, and download the current configuration as ZIP.

There are two buttons at the top right for loading and saving stuff. See there, its pretty self explanatory ;)

![image](https://github.com/user-attachments/assets/fc540480-0d15-4724-af48-c87a44634177)

### Edit configurations

To edit the currently loaded configuration, there are two possibilities (besides file Upload):

- **Edit via Drag'n'Drop:** The emulator shows you the actions currently assigned to every input. You can:
    - **Add new actions:** Just click on "+", select an action and its parameters, and add the action. For most parameters there is input help also.
    - **Remove Actions** 
    - **Edit existing actions:**: Just click on the actions to edit them. You can also replace them here.
    - **Drag'n'Drop:** You can drag the actions between the inputs with the mouse, to easily swap things etc.

    Every change done here will be instantly run in the emulator!

    ![image](https://github.com/user-attachments/assets/2a38e44c-4430-4f6e-82ee-c5364c049ee0)

- **Edit Code:** When you click on the "Code" button at the top left, a side area opens, providing tabs for the source files. You can edit them directly here. To apply the changes, hit the "Okay" button above the editor or hit F8. Note that this does NOT save the preset somewhere, it just applies the changed code to the emulator.

    ![image](https://github.com/user-attachments/assets/229558f3-05ea-44ef-a3ac-28d34b93be8f)

Both of these methods work hand in hand also: PySwitch allows for custom Python implementations, so if you for example add custom code (Callbacks etc.) in your code, the emulator will not touch this, so you can still use the graphical editor and vice versa! If you change the actions with the graphical interface, the code will follow, keeping your custom implementations 100%. This is possible through the use of CSTs (Concrete Syntax Trees) for manipulating the source tree, which preserve all formatting and comments.

After editing the configuration, click the save button on the top left to choose from a destination to save to, or just use CTRL-S / CMD-S to save to the current location (if possible). If your MIDI Captain is selected for example, CTRL-S will "flash" the configuration to the device, which runs the new configuration after a reboot.

#### Paging

Paging means to have different actions active for the switches, depending on pre-defined pages which are either rotated through with one switch or selected directly with many switches. To realize paging, there are two dedicated actions defined:

- PagerAction: This defines pages and itself also acts as an action either rotating thjrough pages or directly selecting one (see below).
- PagerAction.proxy: This creates a proxy action to extend the pager for direct selection of other pages. If you rotate through pages, you dont need this.

**NOTE:** It is also possible to have multiple pagers at once, for example to toggle the upper and lower buttons separately. See example MC 10 / "Twin Pagers".

##### PagerAction

This action (shown as Pager in the Emulator) defines the pages. Each page must have an id unique within the pager, and can have a color and a text optionally.

###### Rotate through Pages

By default, the Pager action, when its switch is triggering, rotates through the pages. 

###### Directly access pages

The optional parameter "select_page" can be set to change this behaviour to directly select a page by its ID. When directly selecting the pages, one of the switches must always be a PagerAction which defines the pages. The other must be created with PagerAction.proxy() (shown as "Select Page" in the emulator). This creates a proxy action which is connected to the Pager action. This way we can create proxies for each page but the one selected by the pager itself.

*Note that the Pager Action must always be assigned to a switch! You cannot just use proxies, or the main pager will not be initialized and updated correctly!*

#### Expression Pedals and other Off-Screen Inputs

For additional inputs like expression pedals, there is a separate panel if the selected device supports any of those. You can access it by the three dots at the bottom left.

![image](https://github.com/user-attachments/assets/a189bd6c-c737-4a8c-b879-0f757cc8ad82)

NOTE: The Encoder wheel of the MIDI Captain 10 currently also is located in this panel, as the screen already is overcrouded. You can also adjust the wheel encoder and switch in the panel, as well as the expression pedals.

Also note that analog inputs can only use one kind of action: AnalogAction, the same for EncoderAction for rotary encoders. The graphical editor will always only show allowed actions.

### Restrictions

- **display.py:** At the current (alpha) state of the emaulator, no graphical editor for the display areas is implemented yet. Currently the emulator focuses on the inputs. However there are several examples for display.py among the examples, you can copy the code of any of them and reuse it.

- **Paging:** Currently, the emulator recognizes if you use PagerAction in inputs.py, but there is no graphical editor for this, you have to implement the pager in code manually.

- **MIDI:** The emulator uses the Web MIDI API which is widely available. However, the only tested browser is Chrome, so if you have problems, try a current version of Chrome first. Also, you have to allow the domain to use MIDI (including System Exclusive) once at first usage.

- **Screen Size:** The emulator is designed to be run on rather large screens. It is reponsive to the screen size, but the CSS could be optimized far better for mobile devices. However, on Pads for example it is usable. For editing source code for example, a big PC screen is best.

- **Performance:** The emulator runs on WASM (Web Assembly) internally which is pretty fast. However, the engine takes some seconds to launch, on current laptops this is okay but on older CPUs the emulator might be laggy. Especially the manipulation algorithms and parser will take some CPU power. This could perhaps be optimized, but the launch overhead is eminent to the Pyodide implementation.

- **Program Size**: The emulator is a web site, and uses pretty much resources which need to be loaded (around 30MB). The browser can cache a lot, so nowadays this is no real problem. Also see the next point.

- **Installation / Run offline:** Currently this is NOT usable offline, however it will eventually be converted to a PWA (Progressive Web App) in the future, then you can use it even when there is no internet connection. This could be handy for example when the Pad is hooked to the Player's WiFi for Rig Manager, where no Internet connection exists.

- **Emulated Display:** The display emulates the original hardware on a high level, so one restriction is that the fonts will be replaced by a web font of approximately the same size. Be aware that the texts in the display will not match the formatting of the hardware, but it is close enough to be really usable.

- **LED Colors:** The hardware LEDs are not gama corrected, and in general RGB LEDs have very different color response than a computer display. The emulator applies inverse gamma correction, but the LED colors will sometimes be not as bright as they are when the patch is run on the actual device. So do not fine adjust colors based on the emulator....

- **Code Linting:** Currently there is no auto-complete or syntax check feature implemented yet in the code editors. However this will be added in the future, as Pyodide makes this feasable. Stay tuned.

- **Code Readability:** The code generated by the graphical UI is not yet pretty. In the future i plan to use a suitable code formatter to really generate clean code, but this is not of the highest priority now as long as the syntax is correct and at least the basic newlines etc. are generated. You can however format the code in the source editors afterwards (which will stay untoughed when using the graphical editor again).


## Development

The emulator is built in pure JavaScript plus JQuery. The complete DOM is created by JS.  

The folder structure is as follows:

- **circuitpy:** This folder has to contain the PySwitch code. If you run the emulator on Docker, the PySwitch content folder is mapped there. If you deploy it to a website, you have to copy or link the code.
- **clients:** This contains all client specific implementations (currently only Kemper).
- **devices:** This contains all device specific implementations and CSS
- **definitions:** Some JSON definitions. See the README file there.
- **examples:** This folder has to contain the PySwitch examples. If you run the emulator on Docker, the PySwitch examples folder is mapped there. If you deploy it to a website, you have to copy or link the files yourself.
- **templates:** Contains code for creating new configurations. 
- **js:**: Contains all application source code (JavaScript).
- **python:** Contains all emulator Python code.
- **lib:** Used libraries
- **styles:** All emulator CSS
- **test:** Unit Test suite built with Jasmine. Can be diretly run in the browser.

### Used Frameworks

The <a href="https://pyodide.org">Pyodide</a> project is used to run python code locally on your browser. The project is a port of CPython for the WASM/Emscripten environment.

The original PySwitch code is loaded into Pyodide, as well as a lot of additional wrappers and parser code specific to the emulator. Dependencies like CircuitPython or the Adafruit hardware libraries are mocked in a similar way as it is common for unit tests. The entry point is PySwitchRunner.js, see there how the python code is run.

For the source code manipulation and parsing algorithms, <a href="https://libcst.readthedocs.io">LibCST</a> is used. This enables manipulating single statements and leaving other code as is.

### Server side Scripts

Basically the application is a pure client application, so no server side rendering is used etc., everything runs locally at the client. However, to provide the TOC (Table of Contents) for the examples and clients, only some small PHP scripts are used (toc.php) delivering a JSON TOC for the directory they are located in, but that's all.

### Sources Overview

The most basic classes of the emulator are the following:

- **Controller.js:** This is the basic controlling class, which keeps references to implementations which are more specific. It manages the application flow on a high abstraction layer.

- **ClientController.js:** This controls the handling of clients (like Kemper). It implements the scanning algorithm etc.
- **DeviceController.js:** This controls the handling of devices (like a MIDI Captain). It implements the scanning algorithm etc.
- **PySwitchRunner.js:** This wraps the Pyodide environment, copies all files to the Emscripten File System etc.

- **routing/\*:** The routing of URIs is done with a library called Sammy.js, which is a bit outdated but works well and is very lightweight. In the Routing.js class, all routed are defined: Each configuration has its own location (a bit like REST). There are separate routes for examples, templates, presets, controllers etc., see Routing.js for details.

- **model/\*:** All classes in the model folder implement data model bases like CLient, Device etc. 
- **model/configurations/\*:**  The COnfiguration class is the base for all more special configuartions. It holds the two relevant files as strings. There are derivatives of this class which can load/save from/to different locations.
- **model/parser/\*:** Contains all basic parser implementations, for meta data etc. Every configuration has its own instance of Parser, used to access all functionality.

- **ui/PySwitchUI.js:** This is the main controller for all User Interface stuff. It builds the DOM etc.
- **ui/editor/\*:** Source code editor. This is based on <a href="https://codemirror.net" >CodeMirror</a>.
- **ui/parser/\*:** Implements the graphical frontend for editing the configuration. The action display is implemented using <a href="https://muuri.dev">Muuri</a>.
- **ui/popups/\*:** All popups are using the same code base implemented here.Popup.js is a basic popup (as used for the about link in the top right corner), BrowserPopup implements a popup which lets you browse through a hierarchical tree of options (built from BrowserEntry instances). The BrowserPopup class expects so-called Data Providers to generate the tree, all inheriting from BrowserProvider.js. There are several examples for Providers, for example for local presets, examples, MIDI ports, etc. See PySwitchUI for examples on how the load/save popups are created.
- **ui/tabs/\*:** Contains the tabs implementation for the left side panel, holding the code editors and virtual client UIs.

- **ui/PySwitchFrontend.js:** This implements the mocked inputs for the emulator. The python mocks access the created DOM elements by ID later. Also the parser frontend is built here using the parser frontend classes mentioned above.

### Metadata Model

The parser provides a lot of metadata to each action available. Basically, the available actions are determined the following way:

1. Using LibCST, all files in the pyswitch/clients folder are searched for available actions and mappings. This gets us info about the action name, its parameters including default values and comments. This information is buffered in the files definition/actions.json and definitions/mappings.json for faster access.
2. The emulator reads this data, as well as the data provided in meta.json. meta.json is a common metadata definition file for actions and mappings, providing additional info needed like parametery types or select values, action categories and hardware targets etc.
3. The program accesses this information by the methods getAvailableActions and getAvailableMappings of the class Parser.js. However the result is not just the action/mapping data mixed with the meta.json data, but each entry (action, mapping or parameter) also has a meta object which contains the meta.json data plus provides custom functions delivering display names etc., which can be overridden with client specific implementations, too (see KemperFunctionMeta for example).

#### Update Metadata Buffers

If PySwitch code is updated (new/changed actions or mappings, or just changed comments), the actions.json and mappings.json buffer files have to be updated for the changes to be reflected in the emulator. This is done using the Jasmine unit tests (can be run by appending /test to the emulator base URL). Just run the test, it will detect the outdated buffers and automatically download the new definitions. Replace the old json with the new data, and the tests should succeed again.

### Parsing / Manipulation of Configurations

LibCST visitors are used to gain info about the actions and their parameters. This is implemented in the python/PySwitchParser class, which is proxied by the Parser.js class for usage in the JS frontend.

The basic method for accessing the parser tree is parser.input(modelName). This method returns a proxy object representing the input with the passed name (names are defined in the hardware mapping, for example "A" for switch A on a MidiCaptain Nano 4). 

The proxies are instances of Python class Input.py, which in turn provides methods to get/set all actions of the input.

After you changed the actions, you have to update the configuration source code using parser.updateConfig. See the usages of input() for examples of usage.

#### Import Handling

Each action and mapping has to be imported in Python. The parser handles things this way:

- Before the trees are converted to source code again, all import statements for all available actions, mappings and some more for parameter defaults are added to the inputs.py file.
- Then, a LibCST algorithm removes all unused imports again from the script.

### Virtual Clients

To provide usage experience also when no Kemper of other client is connected, a virtual Kemper implementation is included in folder clients/kemper/virtual. This client implements the basic behaviour of the Kemper, without being complete in any way. It provides a basic user interface (accessible in the tabs panel - click the Source Code button on the top left, beneath the save button) where you can for example change the (virtual) morph state, set effects parameters etc. to see them reflect in the emulator.

It does not implement all parameters available right away, but features an automatic algorithm for that: Whenever a parameter change or request comes in which is not yet defined, it will define one on the fly. Parameters (like for example volume pedal, wah etc.) added on the fly will be shown by their NRPN/CC keys in the uiser interface and can also be set there.

# How to install

If you just want to use it, you can access the demo of this code here:

https://pyswitch.tunetown.de

## Run locally

If you want to run it locally or do any development to it, you need to install Docker if not already done. Then you can just open a terminal in this folder and run this command:

docker compose up -d

It will link all necessary sources and examples into the container, you can run it at http://localhost

To shut down:

docker compose down

## Deploy to a Server

To deploy the application to a server, you have two choices:
- Use docker (preferred) with the same volume mounts
- Use a normal webspace (must have PHP enabled):
    - Check out the project on your webspace
    - Point your domain to the web/htdocs folder
    - Copy the following folders into the web/htdocs folder:
        - content -> web/htdocs/circuitpy
        - examples -> web/htdocs/examples

For the last step, symlinks also work well.

## Donate

If you use and like the application, please consider donating to support open source development: <a href="https://www.paypal.com/webapps/mpp/page-not-found?cmd=_s-xclick&hosted_button_id=6WHW7WRXSGQXY" target="_blank">Donate</a> Thanks a lot for appreciating the big efforts to create a full application free of charge, and also free of advertisement ;)
