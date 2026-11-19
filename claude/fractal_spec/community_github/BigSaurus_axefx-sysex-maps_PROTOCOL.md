# PROTOCOL — Axe-Fx III SysEx basics

Everything you need to read the JSON maps and turn an entry into a real MIDI message.
Verified on **firmware 32.02**.

## Frame envelope

Every message to/from the unit looks like:

```
F0 00 01 74 10 <cc> <data…> <cks> F7
```

- `F0 … F7` — standard MIDI SysEx start/end.
- `00 01 74` — Fractal Audio manufacturer ID.
- `10` — model byte for the **Axe-Fx III**.
- `<cc>` — the function/command byte.
- `<cks>` — **checksum** = XOR of every byte from `F0` through the last data byte, then `& 0x7F`,
  placed right before `F7`.
- A negative acknowledgement (NAK) comes back as `0x64 <rejected_func> <errcode>`.

## 14-bit IDs

Block IDs and parameter IDs are **14-bit**, sent as two 7-bit bytes, low byte first:

```
lo =  id        & 0x7F
hi = (id >> 7)  & 0x7F
```

Block IDs are in the master map (`block_id` / `block_id_hex`). A few anchors: AMP1 = `0x3A`
(the amp block is internally "DISTORT"), CAB1 = `0x3E`, DELAY1 = `0x46`, REVERB1 = `0x42`,
INPUT1 = `0x25`, COMP1 = `0x2E`, DRIVE1 = `0x76`, GATE1 = `0x92`.

## Value encoding (the important part)

A continuous parameter value is sent as an **IEEE-754 float32, little-endian, packed into five
7-bit MIDI bytes** (septets), least-significant first:

```
f = displayed_value / scale          # scale comes from the map entry
bytes = little-endian float32(f)     # 4 bytes -> 32 bits
septets = [ (bits >> 0)  & 0x7F,
            (bits >> 7)  & 0x7F,
            (bits >> 14) & 0x7F,
            (bits >> 21) & 0x7F,
            (bits >> 28) & 0x7F ]     # 5 x 7-bit, LSB first
```

The **`scale`** for each parameter is in the map. The convention:

| scale | meaning |
|---|---|
| `10` | 0–10 knob (send `displayed / 10`) |
| `100` | percent |
| `1` | dB, Hz, seconds, or a raw index/enum |
| `0.001` | a millisecond value stored as seconds |
| `null` | non-linear display — store/send the raw float directly |

**Enums / model selectors** are sent as `float(index)` — e.g. the amp model is parameter 0 of the
amp block, value = `float(model_id)` from `amp_model_ids.json`. The model IDs are an internal enum,
**not** the combo-box order.

## SET a parameter — `01 09`

```
F0 00 01 74 10 01 09 00 <blkLo blkHi> <prmLo prmHi> <v0 v1 v2 v3 v4> 00 00 00 00 <cks> F7
```

Function `0x01`, sub `0x09`. Block and param IDs are 14-bit; the five value bytes are the float
septets above. Example — set AMP1 Gain to 7.5: param 1, scale 10 → f = 0.75 → pack and send.

This works with Axe-Edit open (the contention is read-only), but for **topology** edits and for
reading back, close Axe-Edit (see [TOPOLOGY.md](TOPOLOGY.md)).

### The alternate SET — `01 52`

A class of firmware-added parameters (e.g. Delay Drive, Cab Drive, IR Player Low/High Cut, Flanger
Bass Focus, and other "Drive" params) **silently no-op on `01 09`**. They take the identical frame
with the sub byte swapped to `0x52`:

```
F0 00 01 74 10 01 52 00 <blkLo blkHi> <prmLo prmHi> <v0..v4> 00 00 00 00 <cks> F7
```

Where a parameter needs it, the map flags it (`set_command`). If a SET seems to do nothing, try
`01 52`. Probe these with a **mid-range** value (e.g. 1.0), not a maxed one — high-end clamping can
mask a failure.

## Read a value — `01 19`

Use `01 19` for a passive value GET. **Do not** use `0x0A`/`0x0B`/`0x0E` to read — they change
state (see [SAFETY.md](SAFETY.md)). If your firmware exposes the passive display-text read, that's
the one that also returns the on-screen text without setting the EDITED flag.

## Status / topology readback — `0x13`

`0x13` returns a status dump: triples of `<blkLo> <blkHi> <state>`, where the state byte packs
bit 0 = bypass, bits 1–3 = channel, bits 4–6 = channel count. It's the readback oracle for which
blocks are present and their bypass/channel state.

## Other useful function bytes

`0x0A` bypass · `0x0B` channel · `0x0C` scene · `0x0D` patch name · `0x0E` scene name ·
`0x0F` looper · `0x10` tap · `0x11` tuner. Preset select is standard MIDI Bank Select + Program
Change. **Note the safety caveats** on `0x0A`/`0x0B`/`0x0C`/`0x0D` before you send any of them —
see SAFETY.md.
