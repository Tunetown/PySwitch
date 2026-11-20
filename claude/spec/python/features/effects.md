# Feature: Effect Blocks

Protocol: [FRACTAL.md 3.2 (`0A`, `0B`, `13`) and 4 (IDs)](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).
Switches are bound to a fixed block + instance, like Fractal's Effect functions; no Kemper-like slots (SPEC 5.4).


## Block addressing

- `FractalBlock.<TYPE>` constants = type index in the enum order (FRACTAL.md 4), plus the special blocks (Multiplexer, IR Player, …) handled by an ID offset.
- Actions take `block` + `instance` (1-based); the effect ID is computed.
- Blocks not in the published enum (Dynamic Distortion, NAM Player, ID 201) are not supported in the alpha (TODO.md).


## Mappings (`mappings/effects.py`)

| Mapping                    | Request | Response       | Set              | Value                     |
|----------------------------|---------|----------------|------------------|---------------------------|
| `STATUS_DUMP()`            | `13`    | `13 …`         | –                | raw packets (`bytes`)     |
| `BLOCK_BYPASS(effect_id)`  | –       | –              | `0A idL idH dd`  | 1 = engaged, 0 = bypassed |
| `BLOCK_CHANNEL(effect_id)` | –       | –              | `0B idL idH dd`  | channel 0–3 (0–5 Multiplexer) |

The bypass set value is inverted internally (`dd` = 1 − value) so that 1 = on everywhere in PySwitch.


## Actions

| Action                   | File                | FC function               | Specific parameters                                                    |
|--------------------------|---------------------|---------------------------|------------------------------------------------------------------------|
| `EFFECT_BYPASS`          | `effect_bypass.py`  | Effect: Bypass            | `block`, `instance`                                                    |
| `EFFECT_CHANNEL_SELECT`  | `effect_channel.py` | Effect: Channel Select    | `block`, `instance`, `channel` (A–D, E/F Multiplexer), `second_press`  |
| `EFFECT_CHANNEL_TOGGLE`  | `effect_channel.py` | Effect: Channel Toggle    | `block`, `instance`, `primary`, `secondary`                            |
| `EFFECT_CHANNEL_INC_DEC` | `effect_channel.py` | Effect: Channel Inc / Dec | `block`, `instance`, `step`, `wrap`, `lower_limit`, `upper_limit`      |

- `second_press`: `None` (default), `FractalSecondPress.SMART_BYPASS` (pressing the active channel engages/bypasses the block), `FractalSecondPress.PREVIOUS_CHANNEL`.
- Channels are given as `FractalChannel.A`..`F` (0..5). Inc / Dec without limits uses the number of channels from the status dump.
- LED rules per function (incl. "off if the block is not in the preset"): FRACTAL.md 7.2.
- Labels (`FractalLabel`): `LONG_NAME` (default, e.g. "Drive 1"), `SHORT_NAME` ("DRV1"), `SHORT_NAME_CHANNEL` ("DRV1 B"), `LONG_NAME_CHANNEL`, `BOTH_CHANNELS` ("DRV1 [A]B"), `DESTINATION_CHANNEL`, `CURRENT_CHANNEL`, `ACTION` ("DRV1 +1") (FRACTAL.md 7.3).


## Callback

`FractalEffectCallback` (shared by all effect actions): registers `STATUS_DUMP`, scans the packets for its effect ID → present / engaged / channel / number of channels. After a set it shows the new state locally until the next dump.
