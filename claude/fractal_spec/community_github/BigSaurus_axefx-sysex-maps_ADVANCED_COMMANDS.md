# ADVANCED COMMANDS — passive reads, block dumps, modifiers, grid read

Four higher-level SysEx commands beyond the basic SET/GET, all verified on **firmware 32.02**.
These cover reading a parameter's display text without side effects, dumping a whole block in one
round-trip (including inactive channels), the modifier (controller-assignment) protocol, and a
positional grid read that includes shunts.

Frame envelope and checksum are as in [PROTOCOL.md](PROTOCOL.md):
`F0 00 01 74 10 <cc> <data…> <cks> F7`, checksum = XOR(F0..last data) & 0x7F.
Two packings are used below:
- **float5** — an IEEE-754 float32 packed LSB-first into five 7-bit septets
  `(v&0x7F, v>>7&0x7F, v>>14&0x7F, v>>21&0x7F, v>>28&0x7F)`.
- **pack16** — a 14-bit value as two 7-bit bytes, LSB first.

> See [SAFETY.md](SAFETY.md) first. In particular, `0x0A`/`0x0B` mutate on read and `0x0E` sets the
> EDITED flag — the passive read below (`0x10`) exists precisely so you don't have to use those.

---

## 1. Passive parameter read + display text — `01 10`

The passive read-with-text channel. Returns the same value payload as `0x0E`, but **does not set the
EDITED flag** (a single `0x0E` read flips a clean preset to edited). Use `0x10` for any read that
needs the on-screen text.

### Request (14-byte short form)
```
idx: 0  1  2  3  4  5    6  7    8      9      10     11     12  13
     F0 00 01 74 10 01 | 10 00 | blkLo  blkHi | prmLo  prmHi | ck  F7
```
`10 00` = the type-0x10 subcommand; block id and param id are 14-bit pack16 (LSB first).

### Reply (~60 bytes: header + value + length + text)
- **Value** = float5 at reply bytes 12–16 — byte-exact equal to the `01 19` GET value.
- **Display text**: a 14-bit length field precedes the text; text bytes start at reply byte 21.
  Decode by **7-bit MSB-first repack to 8-bit ASCII** (concatenate the 7-bit bytes MSB-first and read
  out as bytes), then trim at the first non-printable/zero byte. A naive direct-ASCII read is wrong;
  the 7→8 MSB repack is right.
  - Verified strings: AMP1 Level → `-4.0 dB`, DELAY Time → `500 ms`, CONTROL Tempo → `250 BPM`,
    AMP1 model → `Friedman HBE V3`, GLOBAL Tempo → `120`.

### Notes
- **Passive** — a clean preset stays EDITED=false across a whole `0x10` batch.
- **Answers on system blocks** (e.g. SCENEMIDI) where the plain `01 19` GET is silent.
- **End-of-block sentinel**: reading past a block's last valid param returns a short reply with
  length 0, empty text, value 0.0.
- **Tempo is exact via `0x10`**: CONTROL tempo 1.0 → `250 BPM`, GLOBAL tempo 0.424779 → `120`,
  confirming `BPM = 24 + 226 * normalized`.

---

## 2. Block object (bulk) dump — `0x1F`

A whole-block census in one round-trip, **including inactive-channel values**. Read-only. Needs a
quiet bus (close Axe-Edit) — it races under contention.

### Request (10-byte frame)
```
idx: 0  1  2  3  4  5    6      7      8   9
     F0 00 01 74 10 1F | blkLo  blkHi | ck  F7
```
Payload is just the 2-byte block id (pack16). Read **one block at a time** — the reply carries no
block id, so key off the block you requested.

### Reply sequence
`0x74` (ready ack) + N × `0x75` (object-dump frames) + `0x76` (end-of-dump marker).
- Each `0x75` frame's bytes[6:8] = a 14-bit LSB-first **word count** for that frame (equal to
  `payload_bytes / 3`). Strip the 6-byte header + these 2 count bytes (and trailing ck+F7) from each
  `0x75`, then concatenate the payloads.
- **Unpack**: 3 packed 7-bit bytes → one uint16 (`v = b0 | b1<<7 | b2<<14`).
  - **Continuous** param: normalized value = `word / 65534` (byte-exact vs the GET).
  - **Discrete** param: `word` = the raw option index.

### Word count is per-block-type — don't hardcode it
- Example: the DELAY block = 89 words/channel × 4 channels (A–D) = 356 words. Every block type has a
  different size — read the per-frame word-count fields; never assume a fixed length.

### Caveat — alias/duplicate-name pids
Where a block has two params with the same display name (an alias pid), the bulk `word[n]` holds the
value for the pid at that index, which may differ from what a by-name resolver picks. The dump is
faithful; the ambiguity is in name→pid resolution.

---

## 3. Modifiers — attach / detach / slot read

Modifiers (controller assignments) live in **slots = blocks 3–26**. Full protocol confirmed with no
packet capture needed. Do this with Axe-Edit closed and back up first.

### Attach — `01 3A` (the unit assigns the slot)
```
idx: 0  1  2  3  4  5    6  7    8         9         10        11        12  13
     F0 00 01 74 10 01 | 3A 00 | tgtBlkLo  tgtBlkHi | tgtPrmLo  tgtPrmHi | ck  F7
```
The unit echoes a 23-byte `01 3A` frame and assigns the next free slot (3–26). Find which slot got
the assignment by scanning slot blocks 3–26 with `0x1F` and matching your (block, param) target.

### Slot read — via `0x1F` (NOT `01 07`)
A slot's `0x1F` dump = **25 words**, the modifier field table:

| word | field | word | field |
|---|---|---|---|
| w0 | Source 1 | w13 | Scale |
| w1 | Min | w14 | Offset |
| w2 | Max | w15 | Release |
| w3 | Start | w16 | Update Rate |
| w4 | Mid | w17 | Channel |
| w5 | End | w18 | (unnamed, 0) |
| w6 | Slope | w19 | (unnamed, 0) |
| w7 | Attack | w20 | Source 2 |
| w8 | TARGET blockId | w21 | Scale 1 |
| w9 | TARGET paramId | w22 | Scale 2 |
| w10 | Auto Engage | w23 | Operation |
| w11 | PC Reset | w24 | Damping type |
| w12 | Off Value | | |

`w8 = 0` means a free slot. Continuous fields normalize `word/65534`; selectors/flags are the raw
index. Source 1 is the 75-source enum.

> Note: `01 07` is **not** the modifier-slot read channel — it reads all-zero even with a modifier
> attached, both before and after a source is assigned. The real slot read is `0x1F` on blocks 3–26.
> Slots also do **not** appear in the `0x13` status dump.

### Source SET — index-as-float via `01 09`
Write Source 1 with `01 09` to the **slot block, param 0**, value = **index-as-float** (e.g. `70.0`
for Manual 1). The GET normalizes by /74, so writing the normalized value floors straight back to
NONE — send the raw index.

### Detach — zero the source, then release the slot
1. `01 09` write **0.0** to the slot block param 0 (source → NONE).
2. Release the slot:
```
idx: 0  1  2  3  4  5    6  7    8       9       10  11
     F0 00 01 74 10 01 | 3B 00 | slotLo  slotHi | ck  F7
```

> The factory empty preset (0000) carries two factory modifiers in slots 3/4 — treat pre-occupied
> slots as read-only and leave them alone.

---

## 4. Grid read — `01 2E`

A positional grid/topology read on demand (no editor needed). Closes the gap that the `0x13` status
dump leaves — it includes shunts and wires.

### Request
```
idx: 0  1  2  3  4  5    6  7    8   9
     F0 00 01 74 10 01 | 2E 00 | 3A  F7      (ck 0x3A)
```

### Reply — a 755-byte blob
Reply byte 12 echoes the editor-selected block id (a UI cursor — ignore it for topology).

### Placement law (14 columns × 6 rows), frame-absolute `m[]` (`m[0]` = F0)
```
B     = -2580 - 192*col - 32*row           # bit position
shift = (3*(1 + row - col)) mod 7           # per-cell phase 0..6
O     = (shift + 2580 + 192*col + 32*row) / 7   # exact integer byte index
value = m[O] | (m[O-1] << 7)                # 14-bit, LSB-first at byte O
id    = value >> shift                       # divide out the phase
```
- `id >= 37` → a real block (37–41 = In1–5, 186–189 = Return1–4, otherwise a placed block id).
- `id == 256` or `1–36` → a shunt / id-bearing wire (low ids 1–36 are real shunt instances).
- value nonzero but unaligned (`value % (1<<shift) != 0`) → a bare merge wire.

### Input (wiring) field
A 6-bit field (one bit per source row), 16 stream-bits below the marker: bit *r* set ⇔ the cell is
fed from absolute source row *r* (multiple bits = fan-in), at stream bit `(-7*O + shift - 16 + r)`
for `r = 0..5`. Source blocks (In/Return) carry no field; a non-source block with an empty field is
genuinely unwired. The input link is explicit even for a plain same-row series connection.

---

Every frame in this document was verified on real hardware running firmware 32.02.
