# TBC – Open points

Answer below each item after **Answer:**. "Recommendation" is what I do if you just say "ok". Add your own wishes at the end.

--- 

## 1. Architecture: please confirm
Your question from #4 ("do I get changes made on the device?"): yes, within one update interval. Explanation: [FRACTAL_ANALYSIS.md 3](FRACTAL_ANALYSIS.md).
Resulting design: no protocol class, plain `Client`, all effect switches share one status dump mapping, local feedback after set ([spec/python/architecture.md](spec/python/architecture.md) 2–3). OK?

**Answer:**
ok

## 2. Device model and other client settings
Without a protocol class, the model byte (part of every SysEx message) needs another home. The same place would hold the bank size (#4) and the number display offset.
The mapping messages are built while `inputs.py` is imported, where the config is not available.
- (a) Module constant in `fractal/__init__.py` like Kemper `PRODUCT_TYPE`. Users edit one line in the lib. No overhead, but not changeable in the emulator.
- (b) Option in `config.py`, e.g. `"fractalModel": 0x11`. The Fractal package reads it once at the first callback `init()` and patches model byte + checksum of all Fractal messages (one-time, no RAM cost). Per configuration, editable like other config options. Is a client-specific key in `config.py` OK for you (and the emulator config editor)?
- (c) Auto-detect: query with all model bytes, use the first answer. Undocumented whether devices ignore foreign model bytes → risky, more code.

Recommendation: (b).

**Answer:**
(b) If not set in config.py, default to AM4

## 3. DIN MIDI on dev_midi (follow-up #6)
Checked again:
- `MIDIBuffer.send()` → `write(bytes, len)` **is fine** on UART (CircuitPython stream `write` accepts an optional length; adafruit_midi does the same). My earlier concern was wrong.
- `PA_MIDICAPTAIN_DIN_MIDI()` in `hardware/devices/pa_midicaptain.py` **is definitely broken**: it passes `in_channel`, `out_channel`, `in_buf_size` to `AdafruitDinMidiDevice.__init__()`, which no longer accepts them → `TypeError` on construction. Commit `993406c` ("Raw MIDI almost finished") migrated the USB factory but not the DIN one. The emulator loads this file too, so all DIN examples fail there as well (including the Fractal ones).
- Fix: signature `PA_MIDICAPTAIN_DIN_MIDI(receive_chunk_size = 50)`, passed through. All existing callers use it without arguments.

Shall I make this fix (logged in LIB_CHANGES.md), or do you?

**Answer:**
please fix it

## 4. Bank concept (follow-up #9)
Proposal, mirroring Fractal's own FC concept (Bank Size 1–12, "Preset in Bank", "Bank Inc/Dec"; FRACTAL.md 2):
- One global **bank size N** (any N ≥ 1, default 5), set in the same place as the model (#2). All bank actions use it, so they cannot get out of sync.
- `PRESET_SELECT(preset, preset_off)`: absolute preset number, independent of banks.
- `PRESET_IN_BANK(slot, bank = None, slot_off, bank_off)`: slot 1..N in the current (or a fixed) bank. Same logic as Kemper `RIG_SELECT`, with N instead of 5.
- `BANK_UP` / `BANK_DOWN` (with preselect), `BANK_SELECT(bank)`, `PRESET_UP` / `PRESET_DOWN`, `ENCODER_PRESET_SELECT`.
- Current bank = current preset // N. Number of banks = number of presets of the model / N, rounded up; slots after the last preset of a partial last bank are shown dimmed and do nothing.
- Bank colors cycle like the Kemper bank colors.
- Numbers: presets 0-based with 3 digits ("000") by default, like the devices; option for offset 1 (like the device's "Display Offset"). Banks and slots 1-based.

OK?

**Answer:**
ok

## 5. Effect slots like Kemper (your wish)
Switching blocks on/off is possible and planned (`EFFECT_STATE`, block + instance; [features/effects.md](spec/python/features/effects.md)).
Kemper switches are bound to **slots**, whose effect type changes with the rig. Fractal has no slots, but this can be emulated with the status dump: `EFFECT_SLOT(slot = n)` = the n-th switchable block of the current preset; label and color follow that block.
- Switchable = all blocks except Input, Output, Control, Tuner, IR Capture, MIDI block, Foot Controller, Preset FC; optional `types` parameter to restrict it (e.g. only Drive/Delay/Reverb).
- Limitation: the order is the order of the status dump (most likely ID order, not the grid position; the grid is not accessible via MIDI). A preset change can move blocks to other switches.

Include `EFFECT_SLOT` in the alpha?
Recommendation: yes (little code, as the status dump is there anyway).

**Answer:**
please dont "emulate" the old kemper stuff. All features should closely alogn to the fractal designs. Please propose something.

---


## Your wishes
