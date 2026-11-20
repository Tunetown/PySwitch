# Feature: Tuner

Protocol: [FRACTAL.md 3.2 (`11`), 3.3 (push), 5 (behaviour)](../../../FRACTAL.md). FC function: Utility: Tuner ([FRACTAL.md 7](../../../FRACTAL.md)). Common action behaviour: [architecture.md 7](../architecture.md).
Requires DIN MIDI and *Send Realtime Sysex* = ON on the device.


## Mappings (`FractalMappings` in `fractal/__init__.py`)

| Mapping            | Request | Response (push)  | Set     | Value                                         |
|--------------------|---------|------------------|---------|-----------------------------------------------|
| `TUNER_ON_OFF()`   | –       | –                | `11 dd` | 1 = on                                        |
| `TUNER_STATE()`    | –       | `11 nn ss cc`    | –       | 1 while push data arrives                     |
| `TUNER_NOTE()`     | –       | `11 nn ss cc`    | –       | note 0–11                                     |
| `TUNER_DEVIANCE()` | –       | `11 nn ss cc`    | –       | 8192 + cents × 8192 / 50, clamped to 0–16383 (8192 = in tune) |

All three response mappings parse the same push message (length 10, no checksum). The deviance is converted so that the core `TunerDisplay` and `StrobeController` work unchanged; the default in-tune range ±350 is about ±2 cents.


## Tuner state

There is no tuner state query. The state mechanism (push data, 1.5 s timeout, 0.5 s ignore window after switching off, local feedback when switching on) is described in [architecture.md 3](../architecture.md). Every callback using `TUNER_STATE` calls its `check()` in `update()`.


## Actions and callbacks

- `TUNER` (`actions/tuner.py`): switches the tuner on/off; LED bright while the tuner is on, else dim; Utility color; label "Tuner".
- `TunerDisplayCallback` (`fractal/__init__.py`): same parameters as the Kemper one (splash switching, strobe, note names, calibration) except `midi_channel` (SysEx only), using the Fractal mappings. Releasing any switch while the tuner is shown switches it off.
