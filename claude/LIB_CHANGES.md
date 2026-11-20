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
- `PySwitchRunner` (module loading) – creates the folders `pyswitch/clients/fractal{,/actions,/mappings,/callbacks}` and loads all modules of the Fractal Python client.

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

### content/lib/pyswitch/hardware/devices/pa_midicaptain.py
- `PA_MIDICAPTAIN_DIN_MIDI()` – signature changed to `(receive_chunk_size = 50)`, passed through to `AdafruitDinMidiDevice`. The old parameters `in_channel`, `out_channel`, `in_buf_size` are no longer accepted by `AdafruitDinMidiDevice.__init__()` (since `993406c`) and caused a `TypeError` on construction. All existing callers use no arguments.
