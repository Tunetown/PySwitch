# Feature: Scenes

Protocol: [FRACTAL.md 3.2 (`0C`, `0E`)](../../../FRACTAL.md). Architecture: [architecture.md](../architecture.md).


## Mappings (`mappings/scene.py`)

| Mapping         | Request  | Response  | Set     | Value                    |
|-----------------|----------|-----------|---------|--------------------------|
| `SCENE()`       | `0C 7F`  | `0C dd`   | `0C dd` | current scene (0–7)      |
| `SCENE_NAME()`  | `0E 7F`  | `0E nn …` | –       | name of the current scene |


## Actions

| Action                   | File              | Function                                                     |
|--------------------------|-------------------|--------------------------------------------------------------|
| `SCENE_SELECT`           | `scene_select.py` | select scene 1–8; optional `scene_off` toggle (`"auto"` possible) |
| `SCENE_UP` / `SCENE_DOWN`| `scene_up_down.py`| next / previous scene (via `0C`), wrap optional              |

LED/display: on when the action's scene is the current one; text = scene name or number (parameter).


## Callbacks

- `FractalSceneNameCallback` (`callbacks/scene_name.py`): shows the current scene name, optionally with the scene number.
