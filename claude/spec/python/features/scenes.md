# Feature: Scenes

Protocol: [FRACTAL.md 3.2 (`0C`, `0E`)](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).


## Mappings (`mappings/scene.py`)

| Mapping             | Request  | Response    | Set     | Value                     |
|---------------------|----------|-------------|---------|---------------------------|
| `SCENE()`           | `0C 7F`  | `0C dd`     | `0C dd` | current scene (0–7)       |
| `SCENE_NAME(scene)` | `0E n`   | `0E n …`    | –       | name of scene n (0–7)     |

- One name mapping per scene number (singletons). The answer carries the scene number, so there is no conflict between queries.
- The current scene name is `SCENE_NAME(current scene)`.
- Scene names are requested after a preset change, a change of the current scene (for the name display) and while no name has been received; they are not polled every interval.


## Actions (`actions/scene.py`)

| Action          | FC function       | Specific parameters                                   |
|-----------------|-------------------|-------------------------------------------------------|
| `SCENE_SELECT`  | Scene: Select     | `scene` (1–8), `second_press_previous`                |
| `SCENE_TOGGLE`  | Scene: Toggle     | `primary`, `secondary`                                |
| `SCENE_INC_DEC` | Scene: Inc / Dec  | `step`, `wrap`, `lower_limit`, `upper_limit`          |

Labels (`FractalLabel`): `NAME` (default), `NUMBER`, `BOTH_NUM`, `DESTINATION_NAME`, `DESTINATION_NUM`, `CURRENT_NAME`, `CURRENT_NUM`, `ACTION` (FRACTAL.md 7.3).


## Callbacks

- `FractalSceneNameCallback` (`callbacks/scene_name.py`): shows the current scene name, optionally with the scene number (like the FC main display).
