# FM9 Editor Protocol: Findings Ledger

Wire-level findings from hardware verification on a Fractal FM9 (firmware
11.00 unless noted), offered as a reference for tool builders. Everything
here was proven by write-plus-readback on a real unit, by front-panel
cross-verification with a human reading the screen, or is explicitly
marked UNDECODED. Prior art: the mcp-midi-control project decoded the
foundations (see THIRD_PARTY_NOTICES); this ledger extends and corrects
it. Corrections to our own earlier claims are kept, marked SUPERSEDED.

## Frame basics

- Envelope: F0 00 01 74 <model> <fn> <payload...> <checksum> F7; model
  0x12 = FM9; checksum = XOR of all preceding bytes & 0x7F.
- 14-bit values: little-endian septet pairs (lo7, hi7).
- Float32: 5 septets, little-endian, 7 bits per septet.
- Strings (names): 8-to-7 packing, length-prefixed, chunked.
- SIGNED values (e.g. pitch shift semitones): 16-bit two's complement on
  the wire; -12 = 65524. Positive values are plain. Verified by
  front-panel cross-check (owner turned the knob to -12, wire read
  65524).

## Function surface used

| fn | purpose | notes |
|---|---|---|
| 0x01 | editor sub-actions | see below |
| 0x0A | bypass get/set | set = payload with state byte; get = shorter |
| 0x0B | channel get/set | |
| 0x0C | scene get/set | 0x7F = get |
| 0x0D/0x0E | preset / scene name | 0x0D answers for ANY slot by number, out of flash, without selecting it |
| 0x13 | status dump | blocks + bypass + channel; the most honest state read |
| 0x14 | tempo | 14-bit BPM |
| 0x1F | bulk param read | replies 0x74/0x75/0x76 burst; channel-blocked (index = channel * stride + paramId) |

fn 0x01 sub-actions: 0x09 discrete set (float32 ordinal), 0x52 continuous
set (normalized float32), 0x1F display-name query, 0x26 store, 0x28/0x2B
preset/scene rename, 0x2E grid read, 0x30 cell select (RAW uint32, not
float32), 0x32 grid insert, 0x35 cable draw.

## Verified behaviors

1. **Grid insert requires a preceding cell select** (sub 0x30, raw
   uint32). Without it the insert lands on the device's internal cursor.
   Status-dump verification cannot catch this; grid-read verification can.
2. **Grid-read effect IDs alias mod 128** (id stored as (id << 1) in 8
   bits). FX Return (186) reads as 58 and will masquerade as an amp in
   naive scans. Disambiguate with the fn 0x13 status dump.
3. **Writes are asynchronous.** A read immediately after a write returns
   the PRE-write state with no error. Settle ~150ms and verify by
   read-back. Every "verified" claim in this ledger means exactly that.
4. **A zero-valued discrete set is a GET, not a set.** Sub 0x09 with
   value 0 is the device's zeroed-GET no-op, so ORDINAL 0 CANNOT BE SET
   through the discrete path: the write silently does nothing. Route
   ordinal 0 through a continuous 0.0 write instead. (Found by replay
   testing; an earlier session's "Small Room" (ordinal 0) reverb change
   is believed to have silently no-opped this way.)
5. **The display-name query (sub 0x1F) is a trap.** For the amp block it
   returns the roster's FIRST entry regardless of the actual amp type,
   before and after writes, through seconds of settle (fw 11.00 and
   12.00, verified independently by two contributors). For modifier
   source enums it returns "NONE"; for other type enums a stale
   constant. Never verify any type through it: read the wire value and
   map through a roster. SUPERSEDED: our earlier "fresh only for the amp
   block" claim was a misread.
6. **Cable drawing (sub 0x35).** The community 6-row encoding formula
   draws correct cables for: adjacent-row diagonals (verified
   repeatedly), and row-3, row-4 and row-5 same-row runs. Row 3 was added
   by finding 20 and is what the simulator's row-3 handling relies on.
   Row-2 same-row runs use their OWN encoding (odd source column:
   dest_sign 0 / b23 3; even: dest_sign 1 / b23 1), decoded by probe.
   UNDECODED: draws from row 1 of even columns; 2-row-plus diagonals
   (they do not register at all).
   Cable draw is IDEMPOTENT: re-sending does not remove a cable.
   Removal is a separate op on the same message, see finding 24.
   SUPERSEDED: "the removal message is UNKNOWN" - it was never unknown,
   only untested.
7. **Shunt-replacement inheritance is IN-side only.** Placing a block on
   a shunt keeps the shunt's incoming cable but can DROP the outgoing
   one, silently severing everything downstream. After any insert, read
   the next cell's input mask and redraw if zero.
8. **Shunts cannot be inserted** (no effect id lands one via sub 0x32).
   A unity Volume block is the practical pass-through hop.
9. **Inserts are silently refused over the DSP budget.** Nothing lands,
   no error. Diagnose by retrying the same insert on a light preset.
10. **Param existence is type-dependent.** Writes to params the current
    type does not expose clamp or misbehave (pitch shift under Dual
    Detune clamps at 24). Set the type FIRST, then its params.
11. **Front-panel enum lists are not enum order.** A dictated type list
    placed Dual Chromatic 4th; the wire says ordinal 2. Verify each
    ordinal by wire. Wire-verified pitch types so far: Dual Detune = 0,
    Dual Chromatic = 2 (the FM9's POG equivalent via +12/-12 voices).
12. **Modifier bindings from scratch are UNDECODED** (reversed or dead
    sweeps). Working practice: clone a proven slot within the same
    preset context and retarget only its target effect/param ids,
    leaving the curve bytes untouched. Live modulation (a moving pedal)
    is invisible to every known read: verify sweeps by ear.
13. **Read honesty ranking** for anything audible: human ear > fn 0x13
    status dump > bulk read (0x1F) > get-style reads > display-name
    query (never). Channel-indexed reads require the channel count cache
    to be populated (a status dump) or every channel silently reads as
    channel A.
14. **Empty slots identify themselves, and leave a ghost.** The FM9
    names an unused preset slot `<EMPTY>`: the device's own marker, not an
    inference. Clearing a slot writes `"<EMPTY>\0"` over the FIRST 8 BYTES
    of the 32-byte name field and leaves the remainder of the previous name
    in flash, so a name field must be cut at the FIRST NUL. Right-stripping
    it instead (what this project did until now) yields
    `'<EMPTY>\x00 Phat Time'` - the marker glued to the tail of a preset
    that no longer exists. The surviving tail starts at byte 8, which is why
    ghosts read as fragments (`'ror'`, `'2C'`, `'tep Closer'`). An empty
    slot's scene-name fields read as all-NUL, with no ghost. Verified over
    all 512 slots on fw 12.00: 440 occupied, 72 empty, 68 of those carrying
    a ghost.
15. **fn 0x0D reads any slot without loading it.** Passing a preset number
    (rather than 0x7F 0x7F for "current") answers from flash and leaves the
    loaded preset and the edit buffer alone, and the reply echoes the
    requested number so it cannot be confused with the current preset. A
    512-slot query sweep was byte-identical to a select-and-read sweep of
    the same unit, took 4.7s instead of ~4.5 minutes (9ms/slot vs a 400ms
    select settle), and the front panel never moved. This is the only known
    whole-library read that costs the player nothing - every other preset
    inspection here discards the edit buffer.

16. **Modifier slots are validated at preset load; incomplete revives
    self-clear.** A modifier slot whose source field is written back on
    without a full slot rebuild reads healthy immediately, survives a
    store, and is then found with target AND source zeroed after the
    preset reloads. Any modifier-write verification must include a
    reload cycle (store, select away, select back, re-read); immediate
    read-back races the validation pass and can report state the device
    is about to discard. (fw 11.00, observed across 13 presets.)

17. **A modifier revive sequence that survives reload.** Rewrite the
    slot's fields (pids 1-14, excluding the target fields) as continuous
    writes, then the target effect id, target param id, and source as
    discrete writes, in that order. Verified across 16 presets, two
    ear-confirmed. Rewriting fields beyond pid 14 corrupted a slot and
    triggered the load-time clear. Note: a dead binding can read
    byte-identical to a live one, so field reads alone can never certify
    a binding; physical verification (or the finding-16 reload test for
    structure) is required.
18. **An empty slot is emptier than it looks.** A slot the device names
    `<EMPTY>` has NO grid cells at all - not even Input or Output - and its
    status dump carries only effect ids 200 and 201, which are present in
    every preset and are not in the registry's roster. A hand-built preset
    has INPUT (37) and OUTPUT (42) as real blocks and shunts filling the
    row; an empty one has none of it. The grid read still answers normally
    (746 payload bytes, 47 non-zero against 341 for an occupied preset), so
    zero cells is a true reading, not a decode failure.
19. **Placing blocks into a blank grid works, Input and Output included.**
    Cell-select plus insert lands each block exactly where targeted with no
    cable inheritance to rely on, because there is nothing to inherit from.
    Every cell arrives with `cable_in_mask` 0: placed and silent until
    cabled. This is the easy case of #10 rather than an instance of it -
    that issue is about splicing into an existing cable, and here there is
    no cable to splice.
20. **Row-3 same-row cable draws work with the general formula.** Verified
    on fw 12.00 by building INPUT -> amp -> cab -> OUTPUT across columns
    1-4 of display row 3 in an empty preset: each draw set the downstream
    cell's `cable_in_mask` to 0b1000, matching a hand-built preset on the
    same row, and the result was **confirmed audible by the owner**.
    Previously only rows 4 and 5 were verified for same-row runs (row 2 has
    its own encoding, finding 6). Cables only ever run to the NEXT column,
    and shunts cannot be inserted (finding 8), so a from-scratch chain must
    occupy consecutive columns or hop through a unity Volume block.
21. **Preset numbering is 0-based on the wire, 1-based everywhere a human
    looks.** The wire numbers the 512 slots 0-511; FM9-Edit and the front
    panel number the same slots 1-512. Wire 0 is `59 Bassguy`, which the
    editor lists as 001; a chain built at wire 386 appears in FM9-Edit as
    387. Anything an owner reads has to say which it means, or the wrong
    preset gets cleared. Note `TONECOMMAND_STORE_SLOTS` is WIRE-numbered:
    `133-148` is what the editor shows as 134-149.
22. **Out-of-range preset queries are ANSWERED, not refused.** fn 0x0D for
    preset 512 or beyond echoes the requested number back with a blank
    (all-NUL) name field rather than staying silent. A blank is not the
    `<EMPTY>` marker, so a naive reader concludes the slot is OCCUPIED -
    the wrong direction for any code deciding where it is safe to write.
    Validate the range before trusting the reply.
23. **FM9-Edit coexists with a third-party client; connecting does not
    clear the edit buffer.** Tested with FM9-Edit 1.03.21 against fw 12.00:
    an unsaved chain built over MIDI survived the editor connecting to the
    same unit, and 12 consecutive rounds of `current_preset`, by-number
    slot name, grid read and bulk read all returned identical correct
    values while the editor polled fn 0x01 at ~61 messages/second on the
    shared CoreMIDI port. Buffer edits are lost to a PRESET LOAD from
    either side, which is the documented mechanism and not editor-specific.
    UNTESTED: simultaneous writes from both clients, older editor versions,
    and fw 11.00. This corrects a longstanding note in the README that
    connecting resets the buffer.
24. **Cable REMOVAL works: same message, op byte 0x02.** sub 0x35 carries
    an op byte that the codec has always had as `ROUTING_DISCONNECT = 0x02`
    beside `ROUTING_CONNECT = 0x01`, and nothing had ever sent it - so the
    ledger recorded removal as unknown and the plan was to sniff FM9-Edit's
    traffic for it. It needs no sniffing. Verified on fw 12.00 with the
    identical geometry encoding as the draw:
    - it clears the cable: destination mask 0b1000 -> 0b0
    - repeatable: three remove/redraw cycles, clean each time
    - IDEMPOTENT in its own right: a second removal leaves it off rather
      than toggling it back on
    - SELECTIVE, which is the property a splice needs: on a cell fed by two
      sources (mask 0b11000), removing one feed left 0b1000 - only the
      named source bit cleared
    - works for same-row and 1-row-diagonal geometry alike
    The simulator has modelled exactly this behaviour all along
    (`cable_in_mask &= ~(1 << sr)`); hardware now agrees with it. This
    unblocks the splice half of issue #10.
25. **Displacing a block costs it nothing.** Clearing a cell removes the
    block from the grid AND from the status dump, but its settings stay in
    the preset: re-inserting the same effect id at another cell restores
    them. Verified on fw 12.00 by comparing the whole parameter array around
    a move - all 588 values across all four channels byte-identical - with
    the selected channel and the bypass state preserved too. Only the
    cables die with the cell (finding 7), and those can now be redrawn and
    removed at will. This is what makes a splice into a packed row possible:
    neighbours shift right without losing anyone's tone.
26. **Splicing into a packed row works, and needs slack to the right.**
    Cables only ever run to the NEXT column, so nothing can be inserted
    between two adjacent blocks by cable alone - one of them has to move.
    Verified end to end on fw 12.00: a GEQ spliced ahead of the amp in a
    packed lane (INPUT, drive, comp, amp, cab), the amp and cab each shifted
    one column right with the amp's parameters identical afterwards, the
    span re-cabled, and a live Input-to-Output path confirmed by walking the
    cable masks rather than by checking the blocks are still present. The shift needs a free cell or
    a shunt to its right to absorb it; shunts cannot be re-inserted
    (finding 8), so spending one is one-way, and a row with neither must be
    refused rather than pushing a block off the end of the grid.
27. **Spending a shunt is one-way within the edit buffer, and only there.**
    Verified on fw 12.00, preset wire 1 (`65 Bassguy`), whose row 3 was
    packed from column 1 to 10 with its only shunt at column 11. A GEQ
    spliced in ahead of the amp shifted five blocks right, consumed the
    shunt, and left row 3 with no pass-through cell at all; an independent
    read-back in a separate process showed every cell carrying an incoming
    cable and a live Input-to-Output path. Re-selecting the same preset
    brought the shunt back along with everything else, because that reloads
    from flash. So the accurate claim is NOT that a spent cell never
    returns: it is that nothing can return it on its own, the only route is
    discarding the whole edit, and a store makes the loss permanent. A
    confirmation that overstates this teaches the reader to stop believing
    confirmations.

## Undecoded territory (help welcome)

Multi-row diagonal draw encoding; row-1 even-column
source draws; modifier curve semantics for from-scratch bindings; most
type-enum ordinal tables (delay, chorus, reverb beyond name lists);
DSP budget introspection; the precise conditions under which the
per-scene bypass GET (fn 0x0A) disagrees with the status dump (observed
once contradicting audible reality; status dump has matched the ears
every time since - use it).
