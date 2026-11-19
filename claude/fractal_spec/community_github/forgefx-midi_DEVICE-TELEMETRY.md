# Device Telemetry Roundtrip

**What each Fractal device streams to an editor, vs. what this codec already implements.**

> Companion doc: [`CATALOG-COVERAGE.md`](./CATALOG-COVERAGE.md) covers the static **editing
> catalog** (params / ranges / type rosters / enum vocab / layouts) per device. This doc is the
> **streaming telemetry** side. Together they are the device implementation checklist.

Scope: every device→editor telemetry / metering / broadcast stream — home in/out meters,
per‑block level/VU/gain‑reduction meters, looper waveform+level, RTA spectrum, CPU, tuner,
tempo, scene/preset change, status dump, modifier values. Cross‑referenced against the
reverse‑engineering scratchpad (`~/Dokumente/fm3-scratchpad`, LOCAL‑ONLY) and the current
forgefx‑midi + ForgeFX code (2026‑07‑04).

Envelope (all gen‑3): `F0 00 01 74 <model> <fn> … <cs> F7`. Models: III `0x10`, FM3 `0x11`,
FM9 `0x12`, VP4 `0x14`, AM4 `0x15`.

Status legend: **DONE** = polled/streamed and surfaced today · **DORMANT** = decoded in the
codec but ForgeFX never surfaces it · **PARTIAL** = partly surfaced · **ABSENT** = needs new
RE/codec · **GAP** = wire shape unknown, needs a capture.

---

## Master matrix

| Telemetry | III `0x10` | FM3 `0x11` | FM9 `0x12` | AM4 `0x15` | Codec status | Cheapest next step |
|---|---|---|---|---|---|---|
| Output levels (out1/2 L/R) | ✅ | ✅ | ✅ | ⛔ | **DONE** | — |
| CPU load | ✅ push* | ✅ poll | ✅ | ⛔ | **DONE** (gen3 poll) | — |
| Tuner (Hz/note/cents) | ✅ | ✅ | ✅ | 🟡polls | **DONE** for gen-3; AM4 parser absent | decode AM4 `action=0x0010` |
| Tempo / BPM | ✅ | ✅ | ✅ | 🟡polls | **DONE** for gen-3; AM4 parser absent | decode AM4 `action=0x0010` |
| Scene change | ✅ | ✅ | ✅ | ✅(4) | **DONE** | — |
| Preset change (name/num) | ✅ | ✅ | ✅ | ✅ | **DONE** | — |
| Input level | ✅ | ✅ | ✅ | ⛔ | **DONE** via `liveMonitors` | — |
| **Per‑block VU / level / gain‑reduction** | ✅ | ✅ | ✅ | ⛔ | **DONE** (2026‑07‑04, all gen‑3) | — |
| Looper transport state (rec/play/…) | ✅ | 🟢 | ✅ | ⛔ | **DORMANT** | wire the existing parser |
| Status dump (bypass/channel) | ✅ | 🟢 | 🟢 | 🟡 | PARTIAL | — |
| Looper waveform + playhead + level | ✅ | ✅ | 🟢 | ⛔ | **DONE** (2026-07-04, all gen-3) | — |
| RTA spectrum bands | 🟡 | 🟡fw | 🟡 | ⛔ | **ABSENT/GAP** | capture RTA page |
| Graph curves (PEQ/EQ/comp/LFO/ADSR) | ✅w | ✅w | ✅w | — | **ABSENT/GAP** | capture `AskGraphN` |
| All AM4 live telemetry | — | — | — | 🟡 | **CAPTURED, UNMAPPED** | correlate `action=0x0010` |

`*` III pushes CPU/meters as its own messages (`AxeCpu`, `Axe3In/OutMeters`) but over USB the
editors poll; the genuine unsolicited pushes (tempo down‑beat `0x10`, tuner `0x11`) are
**5‑pin DIN only, never USB** (`axe3spec.txt:120‑124`). `w` = editor renders a graph widget.
`ed` = FM3 firmware has the block but FM3‑Edit renders no widget. `fw` = registers exist in
firmware, no editor graph.

---

## DONE — polled and surfaced today

All gen‑3; AM4 has none of these on the wire (see below).

- **Output levels** — `buildOutputMeterPoll` / `parseOutputMeterRms` / `meterRmsToDb`
  (`gen3/axe-fx-iii/telemetry.ts:109‑122`, 5‑septet float32 RMS → `10·log10`, clamp −40…+6 dB).
  ForgeFX `registryCore.#pollMeters()` round‑robins the 4 outputs → SSE `{type:'meters'}`.
- **CPU** — `buildCpuPoll`/`parseCpuRawLoad`/`cpuPercentFromRaw` (`telemetry.ts:139‑151`,
  `32 + raw·0.5`). `#pollMeters()` every ~8th tick → SSE `{type:'cpu'}`.
- **Tuner** — `buildTunerPageOpen/Close/Poll`, `parseTunerFreqHz` (`telemetry.ts:65‑81`). FM3
  byte‑confirmed: fn `0x01` sub `0x19`, field `0x02` = fundamental Hz as float32 @ frame off 12.
- **Tempo** — `buildSetTempoViaParam` + `parseTempoResponse`; III cmd `0x14`.
- **Scene / preset** — fn `0x0C` scene, `0x0D` query‑patch‑name (III spec `axe3spec.txt:39‑55`).
  AM4 has its own scene (4) + preset‑name codec.
- **Input level** — `liveMonitors()` reads the INPUT block's primary monitor pid (`INPUT_GAINMONITOR`
  pid 8, −60…0 dB) → `GET /preset/monitors/live`.

---

## DORMANT — code exists, just not surfaced (cheap wins)

### 1. Per‑block VU / level / gain‑reduction meters — **IMPLEMENTED 2026‑07‑04 (all gen‑3)**

> **Shipped:** `buildBlockMonitorPoll(eid, pid, model)` + `isBlockMonitorResponse` + `parseBlockMonitorNorm`
> (`gen3/axe-fx-iii/telemetry.ts`); ForgeFX `gen3.liveMonitors()` now polls **every** monitor pid of the
> open block via that builder (was: primary only, via an eid‑only sub‑0x01 GET) and maps each 0..1 norm
> → dB with the device table; Axis `liveMeters` stores all monitors per block and `ControlSurface`
> renders a bar per monitor (L/R / band tags). Model‑generic → FM3/FM9/III (VP4 lacks a monitor table).
> The encoding notes below are the confirming evidence.


> **Capture verdict (FM3, `fm3-midi-bridge` FM3_CAPALL tap):** a per‑block monitor value is a
> **normalized `0..1` float32** (5‑septet LE at frame offset 12) that maps **linearly onto the
> block's `[min_dB, max_dB]` range** — exactly what `fm3MonitorDb()`/`fm9MonitorDb()`/`axe3MonitorDb()`
> already assume. Correlations: comp `COMP_GAINMONITOR` (eid 46, pid 25) idle **1.0** → playing
> **0.02–0.25** over range −40…0 dB (norm 1.0 = 0 dB, 0.0 = −40 dB); gate `GATE_GAINMONITOR`
> (eid 146, pid 13) 0.0…1.0 over −60…0; `MULTICOMP_GAINMON1/2/3` (eid 154, pids 28/29/30) three
> 0..1 streams. **NOT dB, NOT raw 0..65534.**

> ⚠️ **Encoding exception — the OUTPUT block VU is RMS, not norm.** The OUTPUT block's effectId is
> `0x2a` and its `OUTPUT_VUL/VUR` pids `16/17` = `0x10/0x11`, so `buildBlockMonitorPoll(outEid, 16)` is
> byte-identical to the leveling-meter poll and its value is **RMS energy (0..8 → `10·log10`)**, not a
> 0..1 norm. `gen3.liveMonitors()` special-cases `family === 'OUTPUT'` → `parseOutputMeterRms` +
> `meterRmsToDb` (then renormalizes into [min,max] for the bar). Decoding it as a norm clamps to 1.0 →
> the VU pins at +6 dB. All *other* block monitors (input/comp/gate/m-comp/cab) are the 0..1 norm.

**How FM3‑Edit actually reads them (also confirmed):** a **rapid fn‑0x01 sub‑0x19 single‑param poll**
of `(effectId, monitorPid)` — the *same frame shape as the output‑meter poll*, just with
`addr = effectId` and `sub = monitorPid`. It does **not** use the `0x1F` bulk read for live meters
(that's only the page‑load snapshot, and returns raw `0..65534`). In the ~230k‑line capture the
output meters (addr `0x2a`/`0x2b`, sub `0x10`/`0x11`) were polled 115k× and the comp/gate/m‑comp
monitors were polled the identical way.

The poll frame generalizes `buildOutputMeterPoll` (`telemetry.ts:109`):
`envelope(0x01, [0x19, 0x00, eidLo, eidHi, pidLo, pidHi, 0×…])`; the reply value is
`decode5SeptetFloat32(frame[12..16])` (already exists). Output meters carry **RMS energy** (→ `10·log10`);
block monitors carry the **0..1 norm** (→ `*MonitorDb()` linear map). Same frame, two value meanings.

Monitor pids are already tabulated per device (never reuse FM3 ids) with dB ranges + a `*MonitorDb()`
mapper (`fm3/meters.ts`, `fm9/meters.ts`, `axe-fx-iii/meters.ts`): FM3 ids `INPUT_GAINMONITOR` 8
(−60…0), `OUTPUT_VUL/VUR` 16/17, `COMP_GAINMONITOR` 25 (−40…0 / makeup 0…40, type‑gated by
`COMP_TYPE`), `MULTICOMP_GAINMON1/2/3` 28/29/30 (−30…0), `GATE_GAINMONITOR` 13 (−60…0),
`FILTER_DETMON` 33, `DISTORT_GAINMON/VPLATEMON` 121/132, `CABINET_VUMETER` 61 (−40…20),
`CONTROLLERS_ENV_GAINMONITOR` 109, `VOLUME_METER` 14.

**Action (codec):** add `buildBlockMonitorPoll(eid, pid, modelByte)` (the generalized state‑read
above) + reuse `decode5SeptetFloat32`; map the 0..1 result through the family's `*MonitorDb()`.
**Action (ForgeFX):** a per‑open‑block monitor poller (model on `#pollMeters`, but for the open
block's `monitorParams` pids) → new `blockMeters`/`monitor` `DeviceEvent` → Axis renders per‑block
bars. `liveMonitors()` (`gen3.ts:859`) already does a one‑pid‑per‑block hand‑built read but collapses
each family to its **primary** def (`primaryByFamily` `:864`) — generalize it to poll all monitor
pids for the open block, at UI rate, via the new builder.

> Remaining verify‑before‑ship: FM9/III dB ranges are "shared/confirmed" not independently
> hardware‑pinned (`fm9/meters.ts:13`, `axe-fx-iii/meters.ts:14`); the FM3 norm→dB direction is now
> capture‑confirmed and can seed them.

### 2. Looper transport state — **no new codec**

`buildGetLooperState`/`buildSetLooper`/`parseLooperStateResponse` (`setParam.ts:1714‑1949`)
are implemented + exported but **never called by ForgeFX**. III spec cmd `0x0F`, reply bitfield:
bit0 Record · bit1 Play · bit2 Overdub · bit3 Once · bit4 Reverse · bit5 Half (`axe3spec.txt:66‑88`).

**Action:** add a driver `looperState()` + a `looper` `DeviceEvent`; poll while a Looper block
is open (or on a `changed`). `LOOPER_LEVEL` pid (III/FM9 tables; **missing from `fm3/meters.ts`**
though pid 22 exists in FM3 firmware — one‑line add after a pid check).

---

### 3. Looper — waveform + playhead + level — **WIRE DECODED (FM3 capture 2026-07-04)**

Contrary to older notes, **FM3-Edit *does* render a live looper waveform** (with a moving playhead and a
level indicator; pressing record again while playing drops straight into overdub and overwrites the
waveform live). All of it rides fn `0x01` on the Looper effectId (FM3 = **eid 166**), decoded from the
capture:

- **Waveform** — `sub 0x23` poll (`buildLooperWaveformPoll(eid, model)`); reply is a ~609-byte frame whose
  payload (bytes 12..len-2) is **~595 raw 7-bit envelope magnitudes (0..127)**, one per display column.
  `parseLooperWaveform()` → normalized 0..1 array. (NOT a float; NOT the gen-3 graph channel.)
- **Playhead position** — `sub 0x19` monitor poll at **pid 14**, a 0..1 position (`buildBlockMonitorPoll`
  + `parseBlockMonitorNorm`). 0 before playback, ramps 0→1 across the loop.
- **Level** — `sub 0x19` monitor poll at **pid 22** (`LOOPER_LEVEL`); a live 0..1-ish level. (Its FM3
  catalog range is 0..0, so a monitor-table entry needs an explicit dB range — III/FM9 use −80…20.)
- **Transport state** (record/play/overdub/reverse/half) — read as Looper block params (the `sub 0x1a`
  60-byte param frames + `sub 0x39` momentary reads on eid 166); exact field→button map not yet pinned
  (needs correlating the capture against the button presses). The III/FM9 spec also exposes a top-level
  `cmd 0x0F` looper-state bitfield (`buildGetLooperState`/`parseLooperStateResponse`, unwired).

**Shipped (2026-07-04):** codec `buildLooperWaveformPoll`/`isLooperWaveformResponse`/`parseLooperWaveform`
(`telemetry.ts`); ForgeFX `gen3.looperTelemetry(eid)` → `{wave, position, level}` via `GET /preset/looper`
(returns empty with no device I/O for non-looper blocks); Axis polls it in `startLiveMeters` when the open
block's slug is `looper` and `ControlSurface` renders a `wave` widget (SVG envelope bars + live playhead
line + level bar + transport buttons).

**Transport control (2026-07-04):** decoded from the capture — FM3-Edit toggles a control via **fn 0x01
SUB 0x10** → (Looper eid, control pid) with a 5-septet-LE float **1.0 (on) / 0.0 (off)**
(`buildLooperControl`; Record on = `…01 10 00 <eid> 08 00 00 00 00 7c 03`). ForgeFX `gen3.looperControl(eid,
action, on)` maps `action` (record/play/stop/overdub/undo/once/reverse/half) → the block's control pid via
the catalog (model-agnostic) behind `POST /preset/looper/control`; Axis renders REC/▶/■/DUB/↺/REV/½ buttons.
Record (pid 8) + Play (pid 9) are capture-confirmed; the rest are inferred from the same param family (same
sub-0x10 float mechanism). **Reading** the device-side transport state (rec/play/overdub indicators) is
still un-decoded — Axis latches button state locally for now.

## ABSENT / GAP — need a capture or new codec

1. **RTA spectrum bands** (III/FM9; FM3 firmware has `RTA_BAND` pid 4 / `RTA_FREQ` pid 5 but
   FM3‑Edit renders no graph). Only **config** params exist in the codec (`RTA_SOURCE/NUMBANDS/
   DECAY/WINDOW`). Live band magnitudes are unmapped — either indexed polls of `RTA_BAND`/`RTA_FREQ`
   on eid 174, or editor‑side FFT of USB audio. **Capture:** open the RTA page with signal, watch
   for `0x76`/`0x01` polls of eid 174 — present ⇒ wire path (recover encoding); silent ⇒ editor‑side FFT.
2. **Looper waveform** — ~~unknown~~ **DECODED** (FM3 capture 2026-07-04): a dedicated fn 0x01 `sub 0x23`
   read on the Looper eid, ~595 raw 7-bit magnitudes — NOT the generic graph channel. See §3 above.
   (The `AxeAskGraphN`/`Axe3Graph` graph channel is still unknown, but the looper doesn't use it.)
3. **Graph curves** (PEQ/EQ/amp/comp‑transfer/LFO‑scope/ADSR/modifier) — same `AskGraphN` channel;
   mostly computable editor‑side from params, but the device can return computed graph data. Opcode/
   payload **unknown**.
4. **III CPU / in‑out meter push opcodes** — `AxeCpu`, `Axe3InMeters`, `Axe3OutMeters` are confirmed
   message *names*; the frame bytes are not in the scratchpad and not in the 3rd‑party spec (which
   documents only tempo+tuner push). We already poll CPU/output meters the FM3/`0x19`/`0x2e` way, so
   this only matters if we want the III's native push.
5. **All AM4 live telemetry** — fresh AM4 capture analyzed 2026-07-06 from
   `/home/pascal/Downloads/BigCapture/MISTER MEAL.pcapng`; see
   [`AM4-CAPTURE-2026-07-05.md`](./AM4-CAPTURE-2026-07-05.md). No standalone gen-3-style AM4
   telemetry or push channel appeared. AM4-Edit uses ordinary `fn 0x01 PARAM_RW` polls instead:
   `action=0x0010` for live/value-like reads and `action=0x0026` for status/zero polls. The codec now
   labels these shapes diagnostically, but it does **not** parse them into tuner/meter/CPU events yet.
   `GET_METER` remains wire-confirmed dead (100-sample probe, zero variance).
6. **VP4 (`0x14`)** — **no artifacts in the scratchpad at all**. Gen‑3 mechanisms *probably*
   transfer, but nothing is confirmed; no meter table, no telemetry flags.

---

## Cross‑cutting facts

- **Universal gen‑3 value encoding** — fn `0x01` param frames carry a **5‑septet little‑endian
  float32 at frame offset 12** (`u |= (byte[12+i]&0x7f)<<7*i`, i=0..4, reinterpret float32) — used
  by tuner Hz, tempo BPM, single‑param reads. The **bulk read** (`0x1F`/`0x76`) instead returns raw
  `0..65534` ints, positional by paramId.
- **Push is DIN‑only.** The III's genuine unsolicited streams (tempo down‑beat `0x10`, tuner
  `0x11 nn ss cc`) require Global → *Send Realtime Sysex = On* and go out the **5‑pin MIDI‑Out jack
  only, never MIDI‑over‑USB** (`axe3spec.txt:120‑124`). Over USB, **editors poll everything**. This is
  why our poll‑based telemetry is the right model, and why FM3/AM4 (USB) never push param edits.
- **`AxeTurnBroadcast*` / `AxeBroadCastKnob`** (touched‑knob push) is a **gen‑2 Axe‑Fx II** FracPad
  feature — **absent from every FM3/FM9/III/AM4 editor** — so it is *not* a route to front‑panel
  edit reflection on these devices. (Front‑panel edit reflection: FM9/III push a `0x74` burst
  natively → we listen; FM3/AM4 don't → we poll the open block. See the driver edit‑watch/edit‑push code.)

---

## Recommended order of work (all in forgefx‑midi + a thin ForgeFX surface)

1. **Per‑block meters from the bulk read we already do** (DORMANT #1) — biggest visible win, no new
   device traffic. Verify the pid value scaling live first.
2. **Looper transport state** (DORMANT #2) — parser already exists; add event + poll.
3. **`LOOPER_LEVEL` for FM3** — one‑line table add after a pid check.
4. **RTA bands** — needs the one capture to decide wire vs. editor‑FFT; then codec.
5. **Looper waveform / graph channel** — capture `AskGraphN`/`Axe3Graph`, then codec.
6. **AM4 telemetry / VP4** — fresh RE passes; low priority (AM4 metering wire‑confirmed absent).

---

### Sources
- Code: `gen3/axe-fx-iii/telemetry.ts`, `.../meters.ts`, `fm3/meters.ts`, `fm9/meters.ts`,
  `gen3/axe-fx-iii/setParam.ts` (bulk read `608‑790`, looper `1687‑1965`), `devices/gen3/reader.ts`;
  ForgeFX `drivers/registryCore.ts` (`#pollMeters` `~521‑645`), `drivers/gen3.ts`
  (`meters()` `809`, `liveMonitors()` `859`), `drivers/am4.ts`, `drivers/types.ts`.
- RE (`~/Dokumente/fm3-scratchpad`): `reference/axefx3-3rdparty.pdf`→`axe3spec.txt`,
  `reference/fp_strings.txt` (FracPad message classes), `devices/{fm3,fm9,axefx3,am4}/findings/*.md`,
  `devices/*/decompile/juce_xml/__block_layout.xml`, `devices/fm3/decompile/param_table.txt`,
  `ROADMAP-full-api.md`.
