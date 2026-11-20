# Feature: Scenes

Protocol: [FRACTAL.md 3.2 (`0C`, `0E`)](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).


## Mappings

| Mapping                              | Request  | Response    | Set     | Value                     |
|--------------------------------------|----------|-------------|---------|---------------------------|
| `FractalMappings.SCENE()`            | `0C 7F`  | `0C dd`     | `0C dd` | current scene (0–7)       |
| `FractalMappings.SCENE_NAME(scene)`  | `0E n`   | `0E n …`    | –       | name of scene n (0–7)     |

- One name mapping per scene number (singletons, also listed in `FRACTAL.scene_names`). The answer carries the scene number, so there is no conflict between queries.
- The current scene name is `SCENE_NAME(current scene)`.
- Scene names are requested while their value is `None`; a preset change resets them (`FRACTAL.track_preset()`), so callbacks showing names also register `PRESET()`.


## Actions (`actions/scene.py`)

| Action          | FC function       | Specific parameters                                   | Default label |
|-----------------|-------------------|-------------------------------------------------------|---------------|
| `SCENE_SELECT`  | Scene: Select     | `scene` (1–8), `second_press_previous`                | `NAME`        |
| `SCENE_TOGGLE`  | Scene: Toggle     | `primary`, `secondary`                                | `BOTH_NUM`    |
| `SCENE_INC_DEC` | Scene: Inc / Dec  | `step`, `wrap`, `lower_limit`, `upper_limit`          | `ACTION`      |

Labels (`FractalLabel`): `NAME`, `NUMBER` ("Scene 1"), `BOTH_NUM` ("Scene [1] 2"), `DESTINATION_NAME`, `DESTINATION_NUM`, `CURRENT_NAME`, `CURRENT_NUM`, `ACTION` ("Scene +1").


## Callbacks

- `FractalSceneNameCallback` (`callbacks/scene_name.py`): shows the current scene name and/or number (like the FC main display); parameters `show_name`, `show_number`, `default_text`.
