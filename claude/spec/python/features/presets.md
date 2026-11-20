# Feature: Presets and Banks

Protocol: [FRACTAL.md 3.2 (`0D`) and 3.4](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).


## Bank concept

Mirrors Fractal's FC banks ([FRACTAL.md 7.1](../../../FRACTAL.md)):
- One global **bank size N** (any N ≥ 1, default 5): `fractalBankSize` ([architecture.md 6](../architecture.md)). All bank functions use it, so they cannot get out of sync.
- Current bank = current preset // N. Number of banks = number of presets of the model / N, rounded up.
- Positions after the last preset of a partial last bank are shown dimmed and do nothing.
- Numbers: presets 0-based with 3 digits ("000") by default; `fractalPresetDisplayOffset` = 1 shows them 1-based (like the device's Display Offset). Banks and positions in a bank are 1-based.
- **Selected bank**: normally the current bank. A bank function with `preset_load = NONE` changes only the selected bank (no preset is loaded); the Select in Bank switches then show the selected bank until a preset is selected. The selected bank is shared by all bank and preset actions (one value in the fractal package).


## Mappings (`mappings/preset.py`)

| Mapping                  | Request     | Response    | Set        | Value                                   |
|--------------------------|-------------|-------------|------------|-----------------------------------------|
| `PRESET()`               | `0D 7F 7F`  | `0D …`      | –          | current preset number                   |
| `PRESET_NAME()`          | –           | `0D …`      | –          | current preset name                     |
| `PRESET_TARGET_NAME()`   | `0D nL nH`  | `0D nL nH …`| –          | name of preset n (one instance per action, not a singleton) |
| `PRESET_SELECT(channel)` | –           | –           | CC0 + PC   | preset number (0-based)                 |

- `PRESET_NAME` has no request: it receives the answers to the `PRESET` request ([architecture.md 3](../architecture.md)).
- **Names of other presets**: `PRESET_TARGET_NAME` has a changeable target n; changing it rewrites the request bytes and checksum in place. It only accepts answers for its target. Its answers look like answers to `PRESET`, so `PRESET` and `PRESET_NAME` ignore `0D` answers for a preset number whose target name query is pending (a small shared set in the fractal package; an entry is cleared by the answer or after `maxRequestLifetimeMillis`).
- Target names are only requested when the target changes (preset or bank change) and again while no name has been received; they are not polled every interval.


## Actions

Files: `actions/bank.py`, `actions/preset.py`. LED rules per function: FRACTAL.md 7.2.

| Action                  | FC function              | Specific parameters                                                     |
|-------------------------|--------------------------|-------------------------------------------------------------------------|
| `BANK_SELECT`           | Bank: Select             | `bank`, `preset_load`, `second_press_previous`                          |
| `BANK_TOGGLE`           | Bank: Toggle             | `primary`, `secondary`, `preset_load`                                   |
| `BANK_INC_DEC`          | Bank: Inc / Dec          | `step`, `wrap`, `lower_limit`, `upper_limit`, `preset_load`             |
| `PRESET_SELECT`         | Preset: Select by Number | `preset`, `second_press_previous`                                       |
| `PRESET_SELECT_IN_BANK` | Preset: Select in Bank   | `position` (1..N), `second_press_previous`                              |
| `PRESET_TOGGLE`         | Preset: Toggle by Number | `primary`, `secondary`                                                  |
| `PRESET_TOGGLE_IN_BANK` | Preset: Toggle in Bank   | `primary`, `secondary` (positions)                                      |
| `PRESET_INC_DEC`        | Preset: Inc / Dec        | `step`, `wrap`, `lower_limit`, `upper_limit`                            |
| `ENCODER_PRESET_SELECT` | – (PySwitch only)        | select presets with a rotary encoder                                    |

- `preset_load`: `FractalPresetLoad.NONE` (default), `FIRST`, `CURRENT` (same position in the new bank).
- Presets are selected with CC0 + PC (`PRESET_SELECT` mapping), on `midi_channel`.
- Labels (`FractalLabel`): Bank: `BOTH`, `NUMBER` (= Destination, default), `CURRENT`, `ACTION`. Preset: `NAME` (default), `NUMBER`, `P_NUM`, `BOTH_NUM`, `BOTH_P_NUM`, `DESTINATION_NAME`, `DESTINATION_NUM`, `CURRENT_NAME`, `CURRENT_NUM`, `ACTION`. Formats as in FRACTAL.md 7.3.


## Callbacks

- `FractalPresetNameCallback` (`callbacks/preset_name.py`): shows the current preset name, optionally with the preset number (like the FC main display); display modes analog to `KemperRigNameCallback`.
