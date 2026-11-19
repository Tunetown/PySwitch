# Feature: Presets and Banks

Protocol: [FRACTAL.md 3.2 (`0D`) and 3.4](../../../FRACTAL.md). Architecture: [architecture.md](../architecture.md).
Bank concept and number display: **open, see TBC**. The items below that depend on it are marked (TBC).


## Mappings (`mappings/preset.py`)

| Mapping                       | Request     | Response   | Set        | Value                       |
|-------------------------------|-------------|------------|------------|-----------------------------|
| `PRESET()`                    | `0D 7F 7F`  | `0D …`     | –          | current preset number       |
| `PRESET_NAME()`               | –           | `0D …`     | –          | current preset name         |
| `PRESET_SELECT(channel)`      | –           | –          | CC0 + PC   | preset number (0-based)     |

- `PRESET_NAME` has no request: it receives the answers to the `PRESET` request (architecture.md 3).
- Names of other presets (`0D nL nH`) are not queried in the alpha: their answers would be taken as the current preset by `PRESET`.


## Actions

| Action                  | File               | Function                                                         |
|-------------------------|--------------------|------------------------------------------------------------------|
| `PRESET_SELECT`         | `preset_select.py` | select a preset; optional `preset_off` toggle (`"auto"` possible) |
| `PRESET_UP` / `_DOWN`   | `preset_up_down.py`| next / previous preset, wrap optional                            |
| `BANK_UP` / `BANK_DOWN` | `bank_up_down.py`  | bank change with preselect (TBC)                                 |
| `ENCODER_PRESET_SELECT` | `preset_select_encoder.py` | select presets with a rotary encoder                     |

LED/display: on when the action's preset is the current one; color and text per bank like Kemper (TBC).


## Callbacks

- `FractalPresetNameCallback` (`callbacks/preset_name.py`): shows the preset name, optionally with the preset number; display modes analog to `KemperRigNameCallback`.
