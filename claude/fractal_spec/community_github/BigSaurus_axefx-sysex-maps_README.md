# Axe-Fx III SysEx & Parameter Maps

An open reference for the **Fractal Audio Axe-Fx III** MIDI SysEx protocol, reverse-engineered
and device-verified on **firmware 32.02**. These maps let you address **any block and any
parameter on the device by name** — every effect block, every parameter within it, plus device
and global settings — reading and writing each one with its real display value, and identifying
amp/cab/drive models along the way. Nothing here is limited to a handful of block types: the
master map spans the whole device, so you can build and edit a complete signal chain over SysEx
without starting from zero.

This is **reference data only**: JSON maps plus protocol notes. There is no editor, controller,
or automation here. Use it to build your own tools.

> Not affiliated with or endorsed by Fractal Audio Systems. "Axe-Fx" and "Fractal Audio" are
> trademarks of Fractal Audio Systems. Firmware differs between versions — treat **32.02** as the
> baseline and re-verify anything critical on your own unit before relying on it.

## Updates / what's new → [CHANGELOG.md](CHANGELOG.md)

This is an **actively developed** reverse-engineering effort — new parameters get decoded,
renamed, and corrected between releases (including at least one **breaking** param-ID fix so far).
**[CHANGELOG.md](CHANGELOG.md) is the source of truth for what is actually released.** Read it
before building against the maps, and read it again when you pull an update.

These maps are **maintained and kept current with Fractal's firmware releases.** As Fractal ships
new firmware, new and changed parameters get folded into the maps and noted in the changelog. The
current baseline is **FW 32.02**; when you pull an update, check [CHANGELOG.md](CHANGELOG.md) for
what moved and which firmware it was verified against.

## Current coverage (this release)

Numbers are counted from the shipped JSON, not estimated:

- **46 blocks**, **1,987 named parameters** in the master map.
- **331 amp models** and **87 drive models**, each linked to the real-world gear it's based on.
- DynaCab speakers/mics and per-block type/model selectors, as enums.

Honest caveat on completeness: every parameter here carries its **param ID, display label, type,
and page**, and selectors carry their **enum**. The **value encoding (display↔wire scale) is
derived for many but not all** parameters — where it isn't, the entry is addressable but you must
re-derive the scaling before writing continuous values (see [How the maps were made](#how-the-maps-were-made)
and the `note` fields in the JSON). Coverage is also **firmware-specific**: this is FW 32.02.

> Development runs ahead of what's published — the working map is larger than this release at any
> given moment. Only what is in these files (and in [CHANGELOG.md](CHANGELOG.md)) is released.
> Don't infer coverage from progress notes elsewhere; trust the shipped data and the changelog.

## Start here

1. **[SAFETY.md](SAFETY.md)** — read this first. Which commands write flash, which requests can
   corrupt a live block, which reads mutate state, and how to pace MIDI so you don't wedge the unit.
2. **[PROTOCOL.md](PROTOCOL.md)** — the SysEx frame format, checksum, the parameter SET/GET commands,
   and how values are encoded. This is what makes the JSON maps usable.
3. **[TOPOLOGY.md](TOPOLOGY.md)** — the grid: cell addressing and the frames to place, connect,
   and delete blocks.
4. **[ADVANCED_COMMANDS.md](ADVANCED_COMMANDS.md)** — passive display-text reads, whole-block dumps,
   the modifier protocol, and a positional grid read.

## What's in here

### `maps/`
| File | What it is |
|---|---|
| `axefx_sysex_map.json` | **The master map.** All 46 blocks, 1,987 named parameters, each with its param ID, display label, type, and page (and, where derived, its value scale). Includes a `protocol` header and embedded enums. This one file lets you address any parameter. See [CHANGELOG.md](CHANGELOG.md) for what changed between releases. |
| `device_relationships.json` | Real gear → Axe-Fx model. 331 amps + 87 drives, each with the real amp/pedal it's based on and search terms (e.g. "plexi", "bassman", "tube screamer"). |
| `cab_device_relationships.json` | The same, for cabs: DynaCab speakers/mics + legacy IR cabs → real-world gear. |
| `display_label_index.json` | The knob names shown in the editor mapped to the underlying generic parameter (e.g. a Pro Co RAT's printed "Volume" → the generic "Level" param), per model. |
| `param_word_laws.json` | Display-value → wire-word encoding laws for parameters whose value isn't a simple scale (dB levels, log tapers, linear time ranges). Pair with the master map's param IDs. This file grows as more encodings are derived. |

### `enums/`
| File | What it is |
|---|---|
| `amp_model_ids.json` | Flat amp-model name → model-ID (331 models). The simplest amp lookup. |
| `dynacab_enum.json`, `dynacab_speakers.json`, `dynacab_mics.json` | DynaCab speaker and mic selector values. |
| `block_types/*_types.json` | Per-block model/type selectors: every drive pedal, delay type, reverb type, pitch mode, etc. → its ID. |

## How the maps were made

Everything here was worked out on real hardware (FW 32.02) and cross-checked between independent
methods. No single source is trusted alone; entries carry `note` fields recording how they were
confirmed, and which are still inferred rather than write-verified.

- **SET write-verification.** Set a distinctive value (or toggle a switch) via the parameter SET
  command and read the block back over MIDI to confirm which param ID actually moved and how the
  value was encoded. This is the strongest evidence and is what promotes an entry from "named" to
  "verified."
- **Full-device census cross-checks.** Whole-block dumps and status readbacks enumerated over the
  device, cross-referenced so param IDs and block membership agree across passes.
- **Axe-Edit UI label capture.** The knob/label names the editor displays, captured via the
  accessibility layer and correlated to the underlying generic parameters — this is where the
  human-readable names and the display-label index come from.
- **Additional custom tooling (newest).** Purpose-built tooling that identifies parameter IDs
  without writing to the device, then cross-checks each one against the methods above. This is how
  the most recent additions were identified, and what has sped the work up considerably.

**On value encodings:** deriving the display↔wire scaling is a separate step from identifying a
parameter. Many entries are addressable (ID, label, type, page, enum) before their scale is worked
out; those are flagged, and derived encodings live in `param_word_laws.json`. Don't write a
continuous value against an entry whose scale you haven't confirmed.

## Contributing

Corrections, additions, and newly derived value encodings for the Axe-Fx III are always
welcome — open an issue or PR.

### Help map the other Fractal devices

If you can capture SysEx from another Fractal unit, please pitch in. This reference covers the
Axe-Fx III, but the wider Fractal line — the **FM9**, **FM3**, **Axe-Fx II**, and **AX8** —
deserves the same open treatment, and contributions to map them are warmly invited.

There's a head start built in. From the reverse-engineering done here, the Fractal devices
appear to **share a common base SysEx mapping**: the smaller units look less like a different
protocol and more like a **subset** of the same block-and-parameter space, implementing a
portion of what the Axe-Fx III exposes rather than re-inventing the scheme. This is an observed
finding from our exploration, not a guarantee — but if it holds, mapping an FM3 or FM9 is
largely a matter of **validating this Axe-Fx III map against that unit and trimming it to the
subset the device implements**, rather than starting from zero. That lowers the effort
dramatically. If you take one on, the master map is your baseline; note what matches, what's
absent, and anything that genuinely differs, and send it back as a PR.

## License

Data and docs are released under **CC BY 4.0** — free to use, adapt, and build on, with attribution
to **Big Saurus**. See [LICENSE](LICENSE).
