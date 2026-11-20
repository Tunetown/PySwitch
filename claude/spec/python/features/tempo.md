# Feature: Tempo

Protocol: [FRACTAL.md 3.2 (`10`, `14`), 3.3 (beat push)](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).
The beat display requires DIN MIDI and *Send Realtime Sysex* = ON.


## Mappings (`mappings/tempo.py`)

| Mapping                | Request    | Response        | Set        | Value             |
|------------------------|------------|-----------------|------------|-------------------|
| `MAPPING_TAP_TEMPO()`  | –          | –               | `10`       | – (fixed message) |
| `MAPPING_TEMPO_BEAT()` | –          | `10` (push)     | –          | beat counter (0–127) |
| `MAPPING_TEMPO_BPM()`  | `14 7F 7F` | `14 tL tH`      | `14 tL tH` | BPM               |

The tap message and the beat push both use function `10`; the push has no checksum and is recognised by its length (7).


## Actions and callbacks

| Action        | File               | FC function         | Function                                                    |
|---------------|--------------------|---------------------|-------------------------------------------------------------|
| `TAP_TEMPO`   | `tap_tempo.py`     | Utility: Tap Tempo  | taps the tempo; the LED flashes bright on every beat push (`flash_millis`, default 100 ms), else dim |
| `ENCODER_BPM` | `tempo_bpm.py`     | – (PySwitch only)   | changes the BPM with a rotary encoder (24–250)              |

- `TAP_TEMPO` labels (`FractalLabel`): `FUNCTION` ("Tap Tempo", default), `BPM` ("120 bpm"; polls `TEMPO_BPM` only with this label).
- `FractalTempoDisplayCallback` (`callbacks/tempo_bpm.py`): shows the BPM.
