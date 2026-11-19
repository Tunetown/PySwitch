# Feature: Looper

Protocol: [FRACTAL.md 3.2 (`0F`)](../../../FRACTAL.md). Architecture: [architecture.md](../architecture.md).


## Mappings (`mappings/looper.py`)

| Mapping                 | Request | Response | Set     | Value                     |
|-------------------------|---------|----------|---------|---------------------------|
| `LOOPER_STATE()`        | `0F 7F` | `0F dd`  | –       | bit field (FRACTAL.md 3.2) |
| `LOOPER_BUTTON(button)` | –       | –        | `0F dd` | button 0–5                |


## Actions (`actions/looper.py`)

| Action              | Button | LED on when      |
|---------------------|--------|------------------|
| `LOOPER_RECORD`     | 0      | Record or Overdub (different colors) |
| `LOOPER_PLAY`       | 1      | Play             |
| `LOOPER_UNDO`       | 2      | – (momentary)    |
| `LOOPER_ONCE`       | 3      | Once             |
| `LOOPER_REVERSE`    | 4      | Reverse          |
| `LOOPER_HALF_SPEED` | 5      | Half             |

`LOOPER_STATE` is only polled while at least one looper action is configured.
