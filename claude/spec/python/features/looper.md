# Feature: Looper

Protocol: [FRACTAL.md 3.2 (`0F`)](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).


## Mappings (`mappings/looper.py`)

| Mapping                         | Request | Response | Set     | Value                      |
|---------------------------------|---------|----------|---------|----------------------------|
| `MAPPING_LOOPER_STATE()`        | `0F 7F` | `0F dd`  | –       | bit field (`LOOPER_STATE_*`, FRACTAL.md 3.2) |
| `MAPPING_LOOPER_BUTTON(button)` | –       | –        | `0F dd` | button 0–5 (`LOOPER_BUTTON_*`), fixed message |


## Actions (`actions/looper.py`)

No specific parameters; labels and colors are automatic, like the FC (`text` and `color` override them).

| Action              | FC function | Button | Color                | Label                | LED bright when       |
|---------------------|-------------|--------|----------------------|----------------------|-----------------------|
| `LOOPER_RECORD`     | Record      | 0      | Red, Yellow in Overdub | "Record" / "Overdub" | Record or Overdub   |
| `LOOPER_PLAY_STOP`  | Play/Stop   | 1      | Green                | "Play" / "Stop" (while playing) | Play       |
| `LOOPER_UNDO`       | Undo/Erase  | 2      | Purple               | "Undo"               | while pressed         |
| `LOOPER_ONCE`       | Once        | 3      | Blue                 | "Once"               | Once                  |
| `LOOPER_REVERSE`    | Reverse     | 4      | Orange               | "Reverse"            | Reverse               |
| `LOOPER_HALF_SPEED` | Half Speed  | 5      | Pink                 | "Half"               | Half                  |

- Otherwise the LED is dim; it is **off** when the preset has no Looper block (ID 166 in `STATUS_DUMP()`) or no state is known.
- The looper actions register `LOOPER_STATE` and `STATUS_DUMP`, so both are only polled while a looper or effect action is configured.
