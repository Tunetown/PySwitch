# Feature: Tempo

Protocol: [FRACTAL.md 3.2 (`10`, `14`), 3.3 (beat push)](../../../FRACTAL.md). Architecture: [architecture.md](../architecture.md).
The beat display requires DIN MIDI and *Send Realtime Sysex* = ON.


## Mappings (`mappings/tempo.py`)

| Mapping        | Request    | Response        | Set        | Value             |
|----------------|------------|-----------------|------------|-------------------|
| `TAP_TEMPO()`  | –          | –               | `10`       | –                 |
| `TEMPO_BEAT()` | –          | `10` (push)     | –          | beat counter      |
| `TEMPO_BPM()`  | `14 7F 7F` | `14 tL tH`      | `14 tL tH` | BPM               |

The tap message and the beat push both use function `10`; the push has no checksum (shorter) and is recognised by its length.


## Actions and callbacks

| Action        | File               | Function                                          |
|---------------|--------------------|---------------------------------------------------|
| `TAP_TEMPO`   | `tempo.py`         | tap the tempo                                     |
| `SHOW_TEMPO`  | `tempo.py`         | LED blinks on every beat push                     |
| `ENCODER_BPM` | `tempo_bpm.py`     | change the BPM with a rotary encoder              |

- `FractalTempoDisplayCallback` (`callbacks/tempo_bpm.py`): shows the BPM.
