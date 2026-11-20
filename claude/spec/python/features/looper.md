# Feature: Looper

Protocol: [FRACTAL.md 3.2 (`0F`)](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).


## Mappings (`mappings/looper.py`)

| Mapping                 | Request | Response | Set     | Value                     |
|-------------------------|---------|----------|---------|---------------------------|
| `LOOPER_STATE()`        | `0F 7F` | `0F dd`  | –       | bit field (FRACTAL.md 3.2) |
| `LOOPER_BUTTON(button)` | –       | –        | `0F dd` | button 0–5                |


## Actions (`actions/looper.py`)

No specific parameters; labels and colors are automatic, like the FC (custom `text` and `color` possible).

| Action              | FC function | Button | Color             | Label             | LED bright when       |
|---------------------|-------------|--------|-------------------|-------------------|-----------------------|
| `LOOPER_RECORD`     | Record      | 0      | Red, Overdub Yellow | "Record" / "Overdub" | Record or Overdub |
| `LOOPER_PLAY_STOP`  | Play/Stop   | 1      | Green             | "Play" / "Stop"   | Play                  |
| `LOOPER_UNDO`       | Undo/Erase  | 2      | Purple            | "Undo"            | while pressed         |
| `LOOPER_ONCE`       | Once        | 3      | Blue              | "Once"            | Once                  |
| `LOOPER_REVERSE`    | Reverse     | 4      | Orange            | "Reverse"         | Reverse               |
| `LOOPER_HALF_SPEED` | Half Speed  | 5      | Pink              | "Half"            | Half                  |

- Otherwise the LED is dim; it is **off** when the preset has no Looper block (status dump, `STATUS_DUMP()` from effects.md).
- `LOOPER_STATE` is only polled while at least one looper action is configured.
