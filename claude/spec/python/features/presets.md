# Feature: Presets and Banks

Protocol: [FRACTAL.md 3.2 (`0D`) and 3.4](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).


## Bank concept

Mirrors Fractal's FC banks ([FRACTAL.md 7.1](../../../FRACTAL.md)):
- One global **bank size N** (any N ≥ 1, default 5): `fractalBankSize` ([architecture.md 6](../architecture.md)). All bank functions use it, so they cannot get out of sync.
- Current bank = current preset // N. Number of banks = number of presets of the model / N, rounded up.
- Positions after the last preset of a partial last bank are shown dimmed and do nothing.
- Numbers: presets 0-based with 3 digits ("000") by default; `fractalPresetDisplayOffset` = 1 shows them 1-based (like the device's Display Offset). Action parameters use the device numbers (0-based). Banks and positions in a bank are 1-based.
- **Selected bank** (`FRACTAL.selected_bank`): normally the bank of the current preset. A bank function with `preset_load = NONE` changes only the selected bank (no preset is loaded); the Select in Bank switches then show the selected bank until a preset is loaded (any preset change resets it).


## Mappings

| Mapping                                         | Request     | Response     | Set        | Value                                   |
|-------------------------------------------------|-------------|--------------|------------|-----------------------------------------|
| `FractalMappings.PRESET()`                      | `0D 7F 7F`  | `0D …`       | –          | current preset number                   |
| `FractalMappings.PRESET_NAME()`                 | –           | `0D …`       | –          | current preset name                     |
| `FractalMappings.PRESET_SELECT(channel)`        | –           | –            | CC0 + PC   | preset number (0-based)                 |
| `FractalPresetTargetNameMapping()` (`mappings/preset.py`) | `0D nL nH`  | `0D nL nH …` | –  | name of the target preset (one instance per action, not a singleton) |

- `PRESET_NAME` has no request: it receives the answers to the `PRESET` request ([architecture.md 3](../architecture.md)).
- **Names of other presets**: `FractalPresetTargetNameMapping.set_target()` rewrites the request bytes and checksum in place; the mapping only accepts answers for its target (and completes a request sent for the previous target). Its answers look like answers to `PRESET`: every mapping receiving `0D` answers calls `FRACTAL.is_target_answer()`. The first one consumes the pending entry (`FRACTAL.pending_names`) and remembers the message, so the others recognize it regardless of the order in which the client's requests parse it. Entries of terminated requests are discarded.
- Target names are requested with `send_request()` while their value is `None` (after a target change or a timeout), not every interval.


## Actions

Files: `actions/bank.py`, `actions/preset.py`. LED rules per function: FRACTAL.md 7.2 (all LEDs are off while no preset is known).

| Action                  | FC function              | Specific parameters                                          | Default label |
|-------------------------|--------------------------|--------------------------------------------------------------|---------------|
| `BANK_SELECT`           | Bank: Select             | `bank`, `preset_load`, `second_press_previous`               | `NUMBER`      |
| `BANK_TOGGLE`           | Bank: Toggle             | `primary`, `secondary`, `preset_load`                        | `BOTH_NUM`    |
| `BANK_INC_DEC`          | Bank: Inc / Dec          | `step`, `wrap`, `lower_limit`, `upper_limit`, `preset_load`  | `ACTION`      |
| `PRESET_SELECT`         | Preset: Select by Number | `preset`, `second_press_previous`                            | `NAME`        |
| `PRESET_SELECT_IN_BANK` | Preset: Select in Bank   | `position` (1..N), `second_press_previous`                   | `NAME`        |
| `PRESET_TOGGLE`         | Preset: Toggle by Number | `primary`, `secondary`                                       | `BOTH_NUM`    |
| `PRESET_TOGGLE_IN_BANK` | Preset: Toggle in Bank   | `primary`, `secondary` (positions)                           | `BOTH_P_NUM`  |
| `PRESET_INC_DEC`        | Preset: Inc / Dec        | `step`, `wrap`, `lower_limit`, `upper_limit`                 | `ACTION`      |
| `ENCODER_PRESET_SELECT` | – (PySwitch only)        | rotary encoder, `actions/preset_select_encoder.py`           | –             |

- `preset_load`: `FractalPresetLoad.NONE` (default), `FIRST`, `CURRENT` (same position in the new bank).
- Presets are selected with CC0 + PC (`PRESET_SELECT` mapping) on `midi_channel`, followed by local feedback on `PRESET`.
- Labels (`FractalLabel`): Bank: `NUMBER` (destination, "Bank 3"), `CURRENT_NUM`, `BOTH_NUM` ("[B1] B2"), `ACTION` ("Bank +1"). Preset: `NAME`, `NUMBER` ("007"), `P_NUM` ("P2"), `BOTH_NUM` ("[P000] P001"), `BOTH_P_NUM` ("[P1] P2"), `DESTINATION_NAME`, `DESTINATION_NUM`, `CURRENT_NAME`, `CURRENT_NUM`, `ACTION` ("Preset +1").


## Callbacks

- `FractalPresetNameCallback` (`callbacks/preset_name.py`): shows the current preset name and/or number (like the FC main display); parameters `show_name`, `show_number`, `default_text`.
