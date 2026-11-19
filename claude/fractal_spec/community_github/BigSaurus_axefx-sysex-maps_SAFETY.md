# SAFETY — read before you send anything

Reverse-engineering a live rig means you can corrupt a preset, flip persistent settings, or wedge
the unit's MIDI if you're careless. None of the maps here are dangerous to *read*; the danger is in
what you *send*. This page is the short list of things that bite.

All findings below were observed on **firmware 32.02**. Other firmware may differ.

## Pace your MIDI

- **Throttle every message to ~80–100 ms apart and use a ping/watchdog.** Un-throttled bursts can
  **wedge the device's MIDI** — it stops responding.
- A real wedge is **not recoverable in software** — it needs a physical power-cycle. If the link
  goes silent and won't come back after a backoff, stop and power-cycle; don't keep hammering it.
- A "dead link" is often just **port contention**, not a wedge: **Axe-Edit holds the Axe-Fx MIDI
  port exclusively while connected**, so your own code gets nothing. Close Axe-Edit for direct MIDI
  work — but don't force-kill it mid-connection.

## Reads that change state (use the passive read)

Some read commands are **not** side-effect-free:

- **`fn 01` types `0x0A` / `0x0B` MUTATE on read** — each call nudges the value one display step
  (0x0B silently decrements). Never use them to "read" a value.
- **`fn 01` type `0x0E` sets the EDITED flag** — a single 0x0E read flips a clean preset to edited.
- Use the passive value GET (`01 19`) for values. If your firmware exposes it, the passive
  display-text read is the one that reads a parameter's shown text **without** editing the preset.
- **Never read the amp block's parameter 0 (the amp model) on a live preset you care about** —
  reading the model re-applies it and flattens the tone stack (Bass/Mid/Treble reset). Read the amp
  model from an offline preset dump instead.

## Requests that can corrupt a live block

- **Never send `fn 01` types `0x02` / `0x03` / `0x0C` / `0x0D` as REQUESTS.** A blind probe of these
  corrupted a live amp block on a test rig. (`0C`/`0D` are listen-only announce frames — don't probe
  their SET twin blind.)

## The one command that writes flash

- **`01 26 <slot14>` = preset STORE. It WRITES FLASH.** Never send it automatically, never
  unprompted, and never from a replayed or corrupted capture. It stores the edit buffer to the
  currently loaded slot — a real, persistent overwrite. Frame layout (FW 32.02):
  ```
  F0 00 01 74 10 01 26 00 00 00 00 00 <slotLo> <slotHi> 00 00 00 00 00 00 00 <ck> F7
  ```
  (slot is 14-bit LSB-first; checksum = XOR of F0..last data byte, & 0x7F). Treat this as
  never-send unless a human explicitly asked for it and you've backed up first.

## Persistent (autosaved) settings — no undo

- **The GLOBAL settings block and the CONTROL block are NOT edit-buffer state.** Writes to them are
  immediate and autosaved — there is **no reload-to-revert**. The only way back is writing the old
  value in again, so **read and record the current value before you write.**
- In those blocks, some parameters are **read-only display state** and some ranges are reserved
  "set-all" action pids — don't blind-probe-write into them.
- Regular parameter writes (to effect blocks) only change the **edit buffer** and are reversible by
  reloading the preset (send a Program Change). That's the safe place to experiment.

## Rule of thumb

Read with the passive commands, write only to the edit buffer, keep a backup, pace everything, and
never send `01 26` unless you mean it.
