# Python Client – Architecture

General rules: [SPEC.md section 5](../../SPEC.md). Protocol: [FRACTAL.md](../../FRACTAL.md). Why there is no protocol class: [FRACTAL_ANALYSIS.md](../../FRACTAL_ANALYSIS.md).
Features (mappings, actions, callbacks per topic): [features/](features/).


## 1. Package layout

`content/lib/pyswitch/clients/fractal/`, analog to `clients/kemper/`:

```
fractal/
  __init__.py      constants (manufacturer ID, function codes, block types, names, colors),
                   checksum helper, FractalParameterMapping, FractalMappings (shared mappings),
                   FractalColors (only if Colors lacks needed colors), TunerDisplayCallback
  actions/         one file per feature group (preset_select.py, bank_up_down.py, scene_select.py,
                   effect_state.py, effect_channel.py, tuner.py, tempo.py, tempo_bpm.py, looper.py, ...)
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
- Device model byte: see TBC (selection mechanism open).


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
- Example `communication.py` files route `PA_MIDICAPTAIN_DIN_MIDI` to and from the application. This currently fails on `dev_midi` (TBC).


## 5. Memory

- Block types are addressed as type + instance; the effect ID is computed (`46 + 4 × type_index + instance − 1`), no table of ~160 IDs.
- Block names and colors are tuples indexed by the type index (convention 7).
- The status dump payload is kept once (in the shared mapping); callbacks scan it without copying.
