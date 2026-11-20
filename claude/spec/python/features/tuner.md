# Feature: Tuner

Protocol: [FRACTAL.md 3.2 (`11`), 3.3 (push), 5 (behaviour)](../../../FRACTAL.md). Architecture: [architecture.md](../architecture.md).
FC function: Utility: Tuner ([FRACTAL.md 7](../../../FRACTAL.md)). Common action behaviour: [architecture.md 7](../architecture.md).
Requires DIN MIDI and *Send Realtime Sysex* = ON on the device.


## Mappings (`mappings/tuner.py`)

| Mapping            | Request | Response (push)  | Set     | Value                                         |
|--------------------|---------|------------------|---------|-----------------------------------------------|
| `TUNER_ON_OFF()`   | –       | –                | `11 dd` | 1 = on                                        |
| `TUNER_STATE()`    | –       | `11 nn ss cc`    | –       | 1 while push data arrives                     |
| `TUNER_NOTE()`     | –       | `11 nn ss cc`    | –       | note 0–11                                     |
| `TUNER_DEVIANCE()` | –       | `11 nn ss cc`    | –       | cents converted to the core scale (8192 = in tune) |

All three response mappings parse the same push message. The deviance is converted so that the core `TunerDisplay` and `StrobeController` work unchanged.


## Tuner state

There is no tuner state query. The tuner counts as on while push data arrives, and as off when it stops for a timeout (≈1 s) or after switching it off (then late push data is ignored for a short time). The timeout is checked in the callback's `update()`.


## Actions and callbacks

- `TUNER` (`actions/tuner.py`): switch the tuner on/off; LED bright while the tuner is on (from `TUNER_STATE`), else dim; Utility color; label "Tuner".
- `TunerDisplayCallback` (`fractal/__init__.py`): same parameters as the Kemper one (splash switching, strobe, note names, calibration), using the Fractal mappings.
