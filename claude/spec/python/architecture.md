# Python Client – Architecture

General rules: [SPEC.md section 5](../../SPEC.md). Protocol: [FRACTAL.md](../../FRACTAL.md). Why there is no protocol class: [FRACTAL_ANALYSIS.md](../../FRACTAL_ANALYSIS.md).
Features (mappings, actions, callbacks per topic): [features/](features/).


## 1. Package layout

`content/lib/pyswitch/clients/fractal/`, analog to `clients/kemper/`:

```
fractal/
  __init__.py      constants (manufacturer ID, function codes, block types, block names and
                   abbreviations, FractalLabel, category colors), checksum helper,
                   FractalParameterMapping, FractalMappings (shared mappings), client settings (6),
                   shared action base (7), TunerDisplayCallback
  actions/         one file per FC category or function group (bank.py, preset.py, scene.py,
                   effect_bypass.py, effect_channel.py, tuner.py, tap_tempo.py, looper.py,
                   preset_select_encoder.py, tempo_bpm.py)
  mappings/        mapping factories grouped by topic (preset.py, scene.py, effects.py, tuner.py,
                   tempo.py, looper.py)
  callbacks/       display callbacks (preset name, scene name, tempo BPM)
```

No protocol class. `communication.py` of Fractal configurations sets no `"protocol"`, so the core uses the plain `Client`.


## 2. FractalParameterMapping

The core `ClientParameterMapping.parse_against()` only understands Kemper SysEx (compares bytes 6..10, value = last two bytes MSB first). Fractal uses a subclass inside the fractal package (no core change):

- Own static `get()` singleton factory (same pattern as `ClientTwoPartParameterMapping.get()`), names include all parameters.
- **Response template** = the fixed message start up to the value, e.g. `F0 00 01 74 <model> 0D`. `parse()` compares from the function byte (index 5) to the end of the template; the manufacturer ID and the model byte are not compared (performance, like the Kemper parser ignores the manufacturer ID).
- **Value decoding** by mapping type: 7-bit number, 14-bit number (LS first), string (32 chars, cut at the first NUL, trimmed), raw payload (`bytes`, for the status dump). Callbacks decode bit fields themselves.
- **Messages without checksum** (push data) are recognised by their length.
- `set_value()` writes the value bytes and recomputes the checksum. CC/PC set messages behave like in the core.
- Request and set messages are built once at construction (helper `_sysex(function, data)` adds header, checksum and `F7`).
- Device model byte: from the client settings (section 6).


## 3. Polling and state

- Every mapping with a request is polled once per `updateInterval` through `Callback.update()` → `Client.request()`; the `Client` never sends a second request while one is pending, so shared mappings are sent once per interval.
- **Status dump** (`13`): one shared mapping, value = raw payload. All effect callbacks use it, so the traffic does not depend on the number of effect switches.
- **Response-only mappings** (no request) are registered permanently by the `Client` and receive passively:
  - push data (tempo beat, tuner),
  - secondary values of a polled answer (e.g. the preset name from the `0D` answer that the preset number mapping requests). A callback that needs such a value also registers the polling mapping.
- **Local feedback**: after sending a set message, callbacks show the new state immediately; the next poll confirms or corrects it.
- **Offline**: requests expire after `maxRequestLifetimeMillis`; the value becomes `None` and the callbacks show their "no value" state.


## 4. Transport

- The MIDI Captain USB port and all Fractal USB ports are USB **devices**, so the controller connects via **DIN MIDI** (In + Out). The FM3 has no USB MIDI at all.
- Example `communication.py` files route `PA_MIDICAPTAIN_DIN_MIDI` to and from the application (factory fixed, see [LIB_CHANGES.md](../../LIB_CHANGES.md)).


## 5. Memory

- Block types are addressed as type + instance; the effect ID is computed (`46 + 4 × type_index + instance − 1`), no table of ~160 IDs.
- Block long names and 3-letter abbreviations are tuples indexed by the type index (convention 7). Colors are per FC category (section 7), not per block, and all exist in the core `Colors`.
- The status dump payload is kept once (in the shared mapping); callbacks scan it without copying.


## 6. Client settings (`config.py`)

| Key                          | Values                         | Default      | Used for                                         |
|------------------------------|--------------------------------|--------------|--------------------------------------------------|
| `fractalModel`               | model byte (FRACTAL.md 1)      | `0x11` (FM3) | model byte of all SysEx messages                 |
| `fractalBankSize`            | ≥ 1                            | 5            | all bank functions ([presets.md](features/presets.md)) |
| `fractalPresetDisplayOffset` | 0 or 1                         | 0            | displayed preset numbers ("000" or "001")         |

- Mapping messages are built while `inputs.py` is imported, before the config is available. They are built with the default model byte. The first Fractal callback `init()` reads the settings from `appl.config` (once), and if the model differs, patches model byte + checksum of all registered Fractal mappings (singleton registry, one-time, no RAM cost). Mappings created later use the stored model directly.
- Emulator: the keys are part of the emulator's global settings and `config.py` template ([emulator/integration.md](../emulator/integration.md)).


## 7. Common action behaviour

All actions mirror an FC footswitch function ([SPEC 5.4](../../SPEC.md), [FRACTAL.md 7](../../FRACTAL.md)). Feature specs only list what differs per function.

- **LED states**: off / dim / bright as defined per FC function in FRACTAL.md 7.2. Bright = `ledBrightnessOn`, dim = `ledBrightnessOff`, off = LED dark. The display label uses `displayDimFactorOn` for bright and `displayDimFactorOff` for dim and off; its text is never replaced by "off" states (e.g. a block missing in the preset keeps its label).
- **Colors**: FC category colors from the core `Colors`: Bank `ORANGE`, Preset `GREEN`, Scene `RED`, Effect `CYAN`, Utility `BLUE`; Looper per function (looper.md). Parameter `color` overrides it (FC "Switch Ring Color").
- **Labels**: parameter `label` = one of the `FractalLabel` constants offered for the category (FRACTAL.md 7.3); parameter `text` = custom text (FC "Custom"), which overrides `label`. Names are shown in full; the display label shortens them as usual.
- **Parameter names**: FC parameters in snake case: `second_press_previous`, `primary` / `secondary`, `step` (± step size, default +1), `wrap` (default True), `lower_limit` / `upper_limit` (default None = no limit), `preset_load`. They come before the standard parameters (SPEC convention 8).
- **2nd Press = Previous**: the action stores the value that was active before its own switch was pressed and restores it on the next press while its target is active.
- **Toggle functions**: a press while the primary is active selects the secondary, any other press selects the primary.
- **Inc / Dec**: LED is bright while the switch is pressed, else dim (FC "while active").
- **Hold functions** are configured with PySwitch's existing hold actions; FC Layouts/Views correspond to PySwitch pages.
- **Local feedback** after a set (section 3).
