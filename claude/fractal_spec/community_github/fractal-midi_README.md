# fractal-midi

Pure-TypeScript codec and parameter dictionaries for Fractal Audio
guitar processors. Build and parse the SysEx wire bytes a Fractal
device speaks, without pulling in a MIDI transport library.

> Covers AM4 and Axe-Fx II at hardware-verified parity, the modern Fractal
> family (Axe-Fx III / FM3 / FM9 / VP4) at codec and calibration via
> public-capture verification and editor-binary mining, and the Axe-Fx
> Standard/Ultra (gen-1) as a set + parameter-read descriptor. The gen-3
> family stays community-driven for hardware verification; see the
> per-device notes in the coverage table.

> **Unaffiliated community library.** "Fractal Audio", "AM4",
> "Axe-Fx", "Axe-Fx II", "Axe-Fx III", "FM3", "FM9", and "VP4" are
> trademarks of Fractal Audio Systems, Inc. This project neither
> claims endorsement from, nor affiliation with, Fractal Audio
> Systems. The package name uses the "Fractal" trademark
> descriptively (nominative fair use) to identify the hardware
> family this library targets. See [`NOTICE`](./NOTICE) for the
> full trademark statement.

## What this is

- **JSON-shaped parameter dictionaries.** Every block-and-param the
  device understands, with display unit, value range, and the
  paramId that goes on the wire. Reverse-engineered against real
  hardware and Fractal's own published 3rd-party MIDI specs.
- **Pure-TypeScript codec.** Display value in (`gain: 7.5`,
  `'Plexi 100W High'`), SysEx bytes out (`Uint8Array`). No MIDI
  library required.
- **Parsers and validators.** Given captured bytes, parse back to
  display values for round-trip equality testing.
- **Reference data.** Fractal's amp / cab / drive lineage tables
  (the "the JC-120 model is based on this real-world amp" data),
  factory bank metadata, applicability tables.

## What this is not

- **Not a MIDI library.** Routing bytes to and from your hardware
  is your responsibility. Use `node-midi`, `webmidi`,
  `easymidi`, JUCE, RtMidi, CoreMIDI, ALSA, whatever fits.
- **Not a preset editor.** This package gives you the wire-level
  primitives a preset editor would be built on top of.
- **Not affiliated with Fractal Audio Systems.** See the trademark
  notice above and [`NOTICE`](./NOTICE).

## Install

```bash
npm install fractal-midi
```

Node >= 18. ESM-only.

## Usage

```ts
import { buildSetParam, KNOWN_PARAMS } from 'fractal-midi/am4';

// Build the SysEx bytes for "set amp gain to 7.5" (display value in)
const bytes = buildSetParam('amp.gain', 7.5);
// → number[] starting with 0xF0 ... ending 0xF7 — send via your MIDI library

// Inspect the dictionary directly
console.log(KNOWN_PARAMS['amp.gain']);
// → { block: 'amp', name: 'gain', unit: ..., displayMin: 0, displayMax: 10,
//     pidLow: ..., pidHigh: ..., ... }
```

The Axe-Fx II and Axe-Fx III sub-paths follow the same shape (each
device's builders and dictionaries carry that device's own names):

```ts
import { buildSetBlockParameterValue, KNOWN_PARAMS } from 'fractal-midi/gen2/axe-fx-ii';
import { buildSetParameter, PARAMS_BY_FAMILY } from 'fractal-midi/gen3/axe-fx-iii';
```

> **Breaking change in 0.4.0 — generation-prefixed subpaths.** Device
> subpaths are now organized by Fractal codec generation:
> `fractal-midi/gen1` (Axe-Fx Standard/Ultra, formerly `/axe-fx-gen1`),
> `fractal-midi/gen2/axe-fx-ii` (formerly `/axe-fx-ii`), and
> `fractal-midi/gen3/{axe-fx-iii,fm3,fm9,vp4}` (formerly `/axe-fx-iii`,
> `/fm3`, `/fm9`, `/vp4`). `fractal-midi/am4` and `fractal-midi/shared`
> are unchanged (the AM4 is its own codec, not one of the three
> generations), and **`catalog/*.json` paths are unchanged** — JSON
> consumers are unaffected.

### Not using TypeScript? Use the JSON catalog

`catalog/` ships a generated, language-agnostic export of every device's
parameter dictionary, block tables, enum rosters, and ranges — one JSON file
per device. Read it straight from the installed package
(`node_modules/fractal-midi/catalog/<device>.json`) or from a pinned git tag.
Pin a version rather than copying the files: calibration fixes and enum-roster
fills land here first. Shape contract:
[docs/CATALOG-SCHEMA.md](docs/CATALOG-SCHEMA.md). The JSON is regenerated from
the TypeScript source on every change and CI-gated against drift.

## Per-device coverage

| Device | Catalog | Codec | Calibration | Hardware-verified |
|---|---|---|---|---|
| AM4 | ✅ | ✅ | ✅ | ✅ |
| Axe-Fx II | ✅ | ✅ | ✅ | ✅ |
| Axe-Fx III | ✅ (full catalog) | ✅ ([see note](#axe-fx-iii-codec-note)) | ✅ ([see note](#axe-fx-iii-calibration-note)) | 🟡 community beta ([see note](#axe-fx-iii-hardware-note)) |
| FM3 | ✅ (device-true, mined from FM3-Edit) | ✅ (shared gen-3) | 🟡 (linear; some non-linear pending) | 🟡 community beta ([see note](#fm3--fm9) — core surface field-confirmed 2026-06) |
| FM9 | ✅ (device-true, mined from FM9-Edit) | ✅ (shared gen-3) | 🟡 (linear; some non-linear pending) | ❌ community beta |
| VP4 | ✅ (device-true, mined from VP4-Edit) | ✅ (gen-3 envelope; own fn=0x01 write frame, decoded byte-exact from community captures, fw 4.03) | 🟡 (continuous writes take raw wire values; calibration pending) | 🟡 community beta (reads confirmed via community captures; decoded writes untested on hardware) |
| Axe-Fx Standard/Ultra (gen-1) | ✅ (922 params) | ✅ (nibble-split, set + param read) | 🟡 (linear; 171 non-linear pending) | ❌ community beta (no gen-1 hardware) |

### Coverage notes

#### Axe-Fx III codec note

The III's SET_PARAMETER wire envelope (fn=0x01, sub-action `09 00`,
23-byte frame) is byte-verified against 10 public community captures
spanning two effect blocks and two sub-action codes. See the
`axe-fx-iii/setparam` test goldens (302 cases: 36 envelope vectors,
264 round-trip `build` to `parse` to equality cases, and 2
`parseStateBroadcast` assertions). The GET-response shape is
hypothesis-only (no public capture exists); the parser handles both
the `09 00` / `52 00` set-echo shape and the async `04 01`
STATE_BROADCAST shape via `parseSetGetParameterResponse` /
`parseStateBroadcast`.

#### Axe-Fx III calibration note

III calibration = 100% of catalog entries carry a non-`'unverified'`
unit tag (16 string-typed `_NAME` / `_LABEL` / `_MSG` entries are
exempted by the calibration gate, since they have no `'string'` unit in
the `Param` type). Enum vocabularies are resolved at runtime via
`resolveEnumValues(name)` from `enumOverlay.ts`, which carries a
`provenance` field on every entry: `'am4-shared'` (AM4-verified,
shared with III), `'fractal-convention'` (universal Fractal-family
convention like OFF/ON / channel pickers), or `'iii-spec'` (hand-
curated for III-only params). Coverage of enum vocabularies and
numeric display ranges is partial: `resolveEnumValues` returns
`undefined` for params not yet mapped, and many XML-derived numeric
entries carry a unit tag but no `displayMin` / `displayMax`. Treat
the catalog as the wire-level truth; treat the calibration overlay
as display guidance the user can correct via GitHub issue.

#### Axe-Fx III hardware note

The 🟡 hardware-verified status means the maintainer does not own an
Axe-Fx III for round-trip confirmation. Community users running the
device are invited to file GitHub issues against any wire or label
that disagrees with their hardware.

#### FM3 / FM9

FM3 and FM9 share the III protocol family (model bytes `0x11` /
`0x12` vs III's `0x10`, identical envelope per Fractal's v1.4 MIDI
spec). Both ship device-true param catalogs mined from their own
FM3-Edit / FM9-Edit JUCE binaries (paramIds are device-specific and are
never reused from the III) on the shared gen-3 codec. Calibration
covers the linear params; some non-linear display formulas are still
pending. Neither has been hardware-verified by the maintainer, so they
remain community beta. The FM9 has real community captures confirming
the shared read and preset-dump paths. The FM3's core surface was
hardware-confirmed end-to-end by a 2026-06-12 community field test over
its USB-serial transport (discovery, framing, the whole read path,
continuous SET, bypass, scene and preset switching, all through this
codec's own frames), and discrete set-by-name SET was confirmed on FM3
hardware by a 2026-06-10 community session via frames byte-identical to
this codec's builder; block placement (`set_block`), store-to-location,
and the Windows serial-driver path remain unconfirmed.

## License

[Apache License 2.0](./LICENSE). See [`NOTICE`](./NOTICE) for the
trademark statement.
