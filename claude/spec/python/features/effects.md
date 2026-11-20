# Feature: Effect Blocks

Protocol: [FRACTAL.md 3.2 (`0A`, `0B`, `13`) and 4 (IDs)](../../../FRACTAL.md). FC functions: [FRACTAL.md 7](../../../FRACTAL.md). Common action behaviour: [architecture.md 7](../architecture.md).
Switches are bound to a fixed block + instance, like Fractal's Effect functions; no Kemper-like slots (SPEC 5.4).


## Block addressing

- `FractalBlock.<TYPE>` constants = type index in the enum order (FRACTAL.md 4), followed by the special blocks `INPUT`, `OUTPUT`, `MULTIPLEXER`, `IR_PLAYER` (first IDs in `FractalBlock.SPECIAL_IDS`).
- Actions take `block` + `instance` (1-based); `FractalBlock.effect_id()` computes the ID.
- Long names (max. 10 characters, e.g. "MultiDly", "TremPan") and 3-letter abbreviations (Blocks Guide) are tuples indexed by the type.
- Blocks not in the published enum (Dynamic Distortion, NAM Player, ID 201) are not supported in the alpha (TODO.md).


## Mappings

| Mapping                                         | Request | Response       | Set              | Value                     |
|-------------------------------------------------|---------|----------------|------------------|---------------------------|
| `FractalMappings.STATUS_DUMP()`                 | `13`    | `13 …`         | –                | raw packets (`bytes`)     |
| `MAPPING_BLOCK_BYPASS(effect_id)` (`mappings/effects.py`)  | – | –        | `0A idL idH dd`  | 1 = engaged, 0 = bypassed (inverted for the device) |
| `MAPPING_BLOCK_CHANNEL(effect_id)` (`mappings/effects.py`) | – | –        | `0B idL idH dd`  | channel 0–5               |


## Actions

| Action                   | File                | FC function               | Specific parameters                                                    | Default label        |
|--------------------------|---------------------|---------------------------|------------------------------------------------------------------------|----------------------|
| `EFFECT_BYPASS`          | `effect_bypass.py`  | Effect: Bypass            | `block`, `instance`, `mode` (PushButtonAction, default `LATCH`)        | `LONG_NAME`          |
| `EFFECT_CHANNEL_SELECT`  | `effect_channel.py` | Effect: Channel Select    | `block`, `channel`, `instance`, `second_press`                         | `SHORT_NAME_CHANNEL` |
| `EFFECT_CHANNEL_TOGGLE`  | `effect_channel.py` | Effect: Channel Toggle    | `block`, `primary`, `secondary`, `instance`                            | `BOTH_CHANNELS`      |
| `EFFECT_CHANNEL_INC_DEC` | `effect_channel.py` | Effect: Channel Inc / Dec | `block`, `instance`, `step`, `wrap`, `lower_limit`, `upper_limit`      | `ACTION`             |

- `second_press`: `None` (default, no function), `FractalSecondPress.SMART_BYPASS` (pressing the active channel engages/bypasses the block), `FractalSecondPress.PREVIOUS_CHANNEL`.
- Channels are given as `FractalChannel.A`..`F` (0..5). Inc / Dec without upper limit uses the number of channels from the status dump.
- LED rules per function: FRACTAL.md 7.2. Additionally, Channel Inc / Dec is off when the block is not in the preset. Pressing a switch of a block that is not in the preset does nothing.
- The "+ channel" labels show the switch's own channel for Channel Select (e.g. "AMP1 C" on the channel C switch), else the current channel of the block.
- Labels (`FractalLabel`): `LONG_NAME` ("Drive 1"), `SHORT_NAME` ("DRV1"), `SHORT_NAME_CHANNEL` ("DRV1 B"), `LONG_NAME_CHANNEL` ("Drive 1 B"), `BOTH_CHANNELS` ("DRV1 [A]B", "DRV1 A/B"), `DESTINATION_CHANNEL`, `CURRENT_CHANNEL`, `ACTION` ("DRV1 +1") (FRACTAL.md 7.3).


## Callback

`FractalEffectCallback` (`actions/effect_bypass.py`, shared by all effect actions): registers `STATUS_DUMP`, scans the packets for its effect ID → present / engaged / channel / number of channels (only when a new dump object arrived). After a set it shows the new state locally until the next accepted dump ([architecture.md 2](../architecture.md), `feedback()`).
