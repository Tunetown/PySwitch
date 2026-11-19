# Feature: Effect Blocks

Protocol: [FRACTAL.md 3.2 (`0A`, `0B`, `13`) and 4 (IDs)](../../../FRACTAL.md). Architecture: [architecture.md](../architecture.md).
Dynamic "slot" switching like Kemper: **open, see TBC**.


## Block addressing

- `FractalBlock.<TYPE>` constants = type index in the enum order (FRACTAL.md 4), plus the special blocks (Multiplexer, IR Player, …) handled by an ID offset.
- Actions take `block` + `instance` (1-based); the effect ID is computed.
- Blocks not in the published enum (Dynamic Distortion, NAM Player, ID 201) are not supported in the alpha (TODO.md).


## Mappings (`mappings/effects.py`)

| Mapping                    | Request | Response       | Set              | Value                     |
|----------------------------|---------|----------------|------------------|---------------------------|
| `STATUS_DUMP()`            | `13`    | `13 …`         | –                | raw packets (`bytes`)     |
| `BLOCK_BYPASS(effect_id)`  | –       | –              | `0A idL idH dd`  | 1 = engaged, 0 = bypassed |
| `BLOCK_CHANNEL(effect_id)` | –       | –              | `0B idL idH dd`  | channel 0–3               |

The set values are inverted internally (`dd` = 1 − value) so that 1 = on everywhere in PySwitch.


## Actions

| Action           | File                | Function                                                                     |
|------------------|---------------------|------------------------------------------------------------------------------|
| `EFFECT_STATE`   | `effect_state.py`   | toggle a block on/off; optional channel letter in the label                  |
| `EFFECT_CHANNEL` | `effect_channel.py` | select channel A–D of a block, or cycle through its channels (count from `13`) |


## Display

- Label: short block name + instance, e.g. "Drive 1", "Amp 1", "Dly 2"; optionally the channel letter ("Drive 1 B").
- Block not in the current preset: label "-", dimmed.
- Colors: approximated from the Fractal block colors, per block type. Colors missing in `Colors` go into a `FractalColors` class in `fractal/__init__.py`. Testers verify them later (TODO.md).


## Callback

`FractalEffectCallback` (in `actions/effect_state.py` or `__init__.py` if shared): registers `STATUS_DUMP`, scans the packets for its effect ID → present / engaged / channel / number of channels. Push → sends `BLOCK_BYPASS` and shows the new state locally until the next dump.
