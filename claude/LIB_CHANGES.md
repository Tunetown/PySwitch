# Changes to existing files (compared to `dev_midi` @ `955fdd0`)

Every change to a file that already exists on `dev_midi` is logged here. New files are not listed.

Format, one block per file:

```
### <path>
- <Class.method or function> – <description>
```

---

### web/htdocs/clients/ClientFactory.js
- `ClientFactory.getInstance()` – `case "fractal"` returns a `FractalClient`.
- `ClientFactory.estimateClient()` – returns `"fractal"` when `inputs.py` uses `pyswitch.clients.fractal`.

### web/htdocs/js/PySwitchRunner.js
- `PySwitchRunner` (module loading) – creates the folders `pyswitch/clients/fractal{,/actions,/mappings,/callbacks}` and loads all modules of the Fractal Python client; loads the new parser module `parser/misc/ClientImports.py`.

### CHANGELOG.md
- New entry for PySwitch 2.4.11 / Emulator 2.4.11.18.

### content/lib/pyswitch/misc.py
- `PYSWITCH_VERSION` – "2.4.11".

### content/config.py
- Commented documentation of the Fractal options `fractalModel`, `fractalBankSize`, `fractalPresetDisplayOffset` (after the LED brightness options).

### web/htdocs/js/Controller.js
- `Controller.PYSWITCH_VERSION` – "2.4.11"; `Controller.VERSION` suffix ".18" (as with every version change, the emulator's local storage starts empty).

### web/htdocs/templates/config-template.py
- Tokens and comments for `fractalModel`, `fractalBankSize`, `fractalPresetDisplayOffset` (section "Fractal Audio Client").

### web/htdocs/js/model/ConfigFile.js
- `ConfigFile` constructor – defaults `fractalModel: 17`, `fractalBankSize: 5`, `fractalPresetDisplayOffset: 0`.

### web/htdocs/js/ui/misc/EmulatorSettings.js
- `#getConfigSettings()` – fields "Fractal: Device model" (select), "Fractal: Bank size" (number), "Fractal: Preset numbers" (select).
- `#setConfigFromInput()` – new case for select elements (stored as integer).
- `#createSelect()` – new helper.

### web/htdocs/definitions/meta.json
- New client block `"fractal"` (inserted after `"kemper"`, the other clients are unchanged): parameter metadata for all Fractal actions and callbacks.

### web/htdocs/index.html
- Script tags for `clients/fractal/*.js` and `clients/fractal/virtual/*.js`.

### web/htdocs/test/index.html
- Script tags for `clients/fractal/*.js` and `clients/fractal/virtual/*.js` (without the UI), and for the test classes in `spec/examples/fractal/`.
- Script tags for the client import tests (`spec/parser/ClientImportsTests.js`, `spec/test_client_imports.js`).

### web/htdocs/python/parser/PySwitchParser.py
- `PySwitchParser._generate_action_imports()` – additional imports for the Fractal parameter value classes used in `meta.json` (`FractalLabel`, `FractalBlock`, `FractalChannel`, `FractalPresetLoad`, `FractalSecondPress`), like `KemperEffectSlot` for Kemper. Without them, configurations using these values failed after editing in the emulator (`NameError: name 'FractalLabel' is not defined`).
- Client aware imports ([spec/emulator/parser.md](spec/emulator/parser.md)): `__init__()` (plans, `ClientImports` instance), `set_inputs()`/`set_splashes()` (import plan from the tree data, passed to the `CodeGenerator`), `to_source()` (`_apply_client_imports()` before the name based imports), new `_client_imports()`, `_plan_client_imports()`, `_collect_calls()`, `_apply_client_imports()`, `resolve_name()`; `determine_client()` uses `resolve_name()` (client from the module path `pyswitch.clients.<client>`); `_add_all_possible_imports_inputs()` no longer adds the client functions (actions and mappings without a dot in the name).

### web/htdocs/python/parser/misc/CodeGenerator.py
- `CodeGenerator.__init__()` – optional `names(name, client)` callback; new `_call_name()`, used by `_generate_call_node()` (import aliases of client functions).

### web/htdocs/python/parser/misc/ImportExtractor.py
- `ImportExtractor` – additionally sets `result_name` (real name of an aliased import) and `result_module`.

### web/htdocs/python/parser/InputsExtractor.py
- `InputsExtractor.postprocess_call()` – resolves import aliases to the real name and client (`PySwitchParser.resolve_name()`).

### web/htdocs/python/parser/SplashesExtractor.py
- `SplashesExtractor.postprocess_call()` – same as `InputsExtractor`.

### web/htdocs/js/model/parser/ParserInput.js
- `ParserInput.setActions()` – passes the `client` of the actions to the parser (was dropped).

### web/htdocs/python/PySwitchRunner.py
- Module imports – removed `from pyswitch.misc import get_option`; `PySwitchRunner.init()` reads the `exploreMode` option directly. The module level import loaded `pyswitch.misc` outside the patched `sys.modules` context, so it used the real `time` module and the time override of the tests (`PySwitchRunner.setTimeCallback()`) never had an effect (bug since `06efec6`). Only affects the tests (the override is not used otherwise).

### examples/Line 6/HX Stomp/display.py
- Imports – `pyswitch.clients.local.mappings.general` → `pyswitch.clients.local.mappings.generic` (the module does not exist under the old name; the example could not be loaded, which broke the Jasmine example test).

### content/lib/pyswitch/hardware/devices/pa_midicaptain.py
- `PA_MIDICAPTAIN_DIN_MIDI()` – signature changed to `(receive_chunk_size = 50)`, passed through to `AdafruitDinMidiDevice`. The old parameters `in_channel`, `out_channel`, `in_buf_size` are no longer accepted by `AdafruitDinMidiDevice.__init__()` (since `993406c`) and caused a `TypeError` on construction. All existing callers use no arguments.
