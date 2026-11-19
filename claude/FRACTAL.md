# Fractal Audio – MIDI Reference

Everything about the Fractal side (devices, MIDI features, protocol). This is the only place for this information; other files link here.
How this protocol maps to PySwitch and how it compares to Kemper: [FRACTAL_ANALYSIS.md](FRACTAL_ANALYSIS.md).
Source documents: section 6.


## 1. Devices

| Device     | Model byte | Presets          | Scenes | Channels/block | USB MIDI | 3rd-party SysEx     | Realtime push  |
|------------|------------|------------------|--------|----------------|----------|---------------------|----------------|
| Axe-Fx III | 0x10       | 1024 (Mk I: 512) | 8      | 4              | yes      | official, fw ≥ 1.13 | yes            |
| FM9        | 0x12       | 512              | 8      | 4              | yes      | yes (1)             | yes            |
| FM3        | 0x11       | 512              | 8      | 4              | **no**   | yes (2)             | yes            |
| AM4        | 0x15       | 104 (A1..Z4)     | 4      | 4              | yes (3)  | not confirmed       | not documented |
| VP4        | 0x14       | 104              | 4      | 4              | yes (3)  | private spec only   | not documented |

(1) Status dump since fw 3.00. (2) Status dump fixed in fw 1.06; MIDI only via DIN. (3) MIDI DIN replaced by TRS jacks.

- Model bytes: 0x10 is official; 0x11/0x12 are from the wiki and community code (tested on hardware), 0x14/0x15 from the wiki and user captures.
- The model **cannot be queried** with the 3rd-party commands (official statement).
- Block instance counts per device: `fractal_spec/Fractal-Audio-Blocks-Guide.pdf` p.3 (e.g. FM3: 1 Amp, 1 Cab, 2 Drive, 2 Delay, 1 Reverb, 1 Pitch; Axe-Fx III: 2 Amp, 2 Cab, 4 Drive, 4 Delay, 2 Reverb).
- AM4/VP4 (not in the alpha, see SPEC section 1): undocumented fn **0x12 = mode/page select** (`48` Presets, `49` Scenes, `4A` Effects, `18` Tuner/Tap, `58` Amp – AM4 only); officially also via "Mode Via CC Value". The AM4 reportedly uses its own slot-based block addressing.


## 2. What can be controlled externally via MIDI

Overview of all external control options of Axe-Fx III / FM9 / FM3. "CC" functions must be assigned to a CC number by the user in *Setup > MIDI/Remote* (global, there are no defaults a controller can rely on). The SysEx commands (section 3) work without any setup on the device.

| Function                             | Standard MIDI                        | 3rd-party SysEx  | State readable by controller          |
|--------------------------------------|--------------------------------------|------------------|---------------------------------------|
| Preset select                        | CC0 (bank) + PC                      | –                | yes: number + name (`0D`)             |
| Preset increment / decrement         | CC (with start/stop range)           | –                | yes (`0D`)                            |
| Read any preset's name by number     | –                                    | `0D`             | yes                                   |
| Scene select                         | CC, value 0–7                        | `0C`             | yes (`0C`)                            |
| Scene increment / decrement          | CC, value > 63                       | –                | yes (`0C`)                            |
| Scene name                           | –                                    | `0E`             | yes, any scene                        |
| Block bypass (per block)             | CC (Value or Toggle mode)            | `0A`             | yes (`0A`, `13`)                      |
| Block channel A–D (per block)        | CC, value mod 4                      | `0B`             | yes (`0B`, `13`)                      |
| Blocks present in current preset     | –                                    | `13`             | yes, incl. bypass, channel, #channels |
| Tuner on/off                         | CC                                   | `11`             | only via tuner push data (DIN)        |
| Tuner note / string / cents          | –                                    | push only        | yes, push (DIN only)                  |
| Tap tempo                            | CC                                   | `10`             | –                                     |
| Tempo BPM                            | –                                    | `14`             | yes (`14`)                            |
| Tempo beat                           | –                                    | push only        | yes, push (DIN only)                  |
| Looper Rec/Play/Undo/Once/Rev/Half   | CC per function                      | `0F`             | yes (`0F`, incl. Overdub)             |
| External Controllers 1–16 (1)        | CC                                   | –                | –                                     |
| Input 1/2, Output 1/2 volume         | CC                                   | –                | –                                     |
| Output volume inc/dec (2)            | CC                                   | –                | –                                     |

(1) Modifier sources: any parameter of any block can be controlled this way (expression pedals etc.).
(2) Saves the preset, including all unsaved changes. Not used by PySwitch.

**Not possible via MIDI** (3rd-party scope): reading or setting block parameter values (only via the excluded editor protocol, see section 3.5), grid layout / block positions, user-defined block names, querying the tuner state or the device model.

Device settings that affect a controller (*Setup > MIDI/Remote > General*): MIDI channel (SysEx ignores it), Program Change on/off, Ignore Redundant PC, PC Mapping and PC Offset (change what a PC loads), Effect Bypass Mode (CC only), Display Offset (presets shown from 000 or 001; display only), **Send Realtime Sysex** (enables push data).

The FC controllers group presets into dynamic banks: *FC Controllers > Config > Bank Size* (1–12), "Preset in Bank" and "Bank Inc/Dec" switch functions.

Sources: FM3 Owner's Manual p.105–108 ("The MIDI/Remote Menu"), FM9 Owner's Manual "FC: Config Page", 3rd-party spec.


## 3. 3rd-party SysEx protocol

Official: "Axe-Fx III MIDI for 3rd Party Devices" rev 1.4 (also valid for FM9/FM3 with their model byte).

### 3.1 Message format
```
F0 00 01 74 <model> <function> <data...> <checksum> F7
```
- Manufacturer ID `00 01 74`. The `01` is NOT a MIDI channel; SysEx is accepted on every MIDI channel setting.
- Checksum: XOR of all bytes from `F0` up to the last data byte, `& 0x7F`.
- 14-bit values: two 7-bit bytes, **LS byte first**.
- Error answer (NAK): function `64`, data `<rejected function> <error code>` (e.g. on a wrong checksum).

### 3.2 Commands

| Fn   | Name              | Request (payload) | Response (payload)      |
|------|-------------------|-------------------|-------------------------|
| 0x0A | Set/Get bypass    | `0A idL idH dd`   | `0A idL idH dd`         |
| 0x0B | Set/Get channel   | `0B idL idH dd`   | `0B idL idH dd`         |
| 0x0C | Set/Get scene     | `0C dd`           | `0C dd`                 |
| 0x0D | Query preset name | `0D nL nH`        | `0D nL nH <32 chars>`   |
| 0x0E | Query scene name  | `0E dd`           | `0E nn <32 chars>`      |
| 0x0F | Set/Get looper    | `0F dd`           | `0F dd`                 |
| 0x10 | Tap tempo         | `10`              | –                       |
| 0x11 | Tuner on/off      | `11 dd`           | –                       |
| 0x13 | Status dump       | `13`              | `13` + n × `idL idH dd` |
| 0x14 | Set/Get tempo     | `14 tL tH`        | `14 tL tH`              |

Details:
- `7F` (or `7F 7F` for 14-bit fields) as value means "query / current".
- **0x0A** dd: 0 = engaged, 1 = bypassed.
- **0x0B** dd: channel 0–3 (0–5 for Multiplexer, errata).
- **0x0C** dd: scene 0–7.
- **0x0D** also returns the **current preset number** (0-based); any preset can be read by number. Cut the name at the first NUL, trim spaces.
- **0x0F** request dd: 0 Rec, 1 Play, 2 Undo, 3 Once, 4 Reverse, 5 Half. Response dd is a bit field: bit0 Rec, bit1 Play, bit2 Overdub, bit3 Once, bit4 Reverse, bit5 Half.
- **0x11** dd: 0 = off, 1 = on.
- **0x13** returns all blocks of the current preset; per block dd: bit0 = bypassed, bits1–3 = channel, bits4–6 = number of channels. Blocks not in the preset are not listed.
- What `0A`/`0B` queries return for a block that is not in the preset is undocumented (asked in the forum, never answered).

### 3.3 Push data
Only when *Setup > MIDI/Remote > Send Realtime Sysex* = ON, **only on the MIDI Out DIN jack, never over USB**, without checksum:
- Tempo beat (on every down beat): `F0 00 01 74 <model> 10 F7`
- Tuner (continuously while the tuner is on): `F0 00 01 74 <model> 11 nn ss cc F7` – note 0–11, string 0–5 (0 = low E), cents offset-binary (63 = 0).

The devices **never push** preset, scene, bypass, channel or looper changes (official: "It's a client's responsibility to poll").

### 3.4 Preset change
CC0 (bank) + PC, preset = 128 × CC0 + PC, 0-based. There is no SysEx command for it.

### 3.5 Editor protocol (excluded)
The Axe-Edit/FM3-Edit protocol (fn 0x01, 0x1F, 0x2E …) is undocumented and device-specific, partly writes flash, and bursts can lock up the device MIDI. It is not used.


## 4. Effect (block) IDs

Shared gen-3 enum (Appendix 1 of rev 1.4):
- `ID_CONTROL = 2`, `ID_TUNER = 35`, `ID_IRCAPTURE = 36`, `ID_INPUT1..5 = 37..41`, `ID_OUTPUT1..4 = 42..45`
- From 46 on, **4 IDs per block type** in this order: COMP, GRAPHEQ, PARAEQ, DISTORT (= **Amp**), CAB, REVERB, DELAY, MULTITAP, CHORUS, FLANGER, ROTARY, PHASER, WAH, FORMANT, VOLUME, TREMOLO, PITCH, FILTER, FUZZ (= **Drive**), ENHANCER, MIXER, SYNTH, VOCODER, MEGATAP, CROSSOVER, GATE, RINGMOD, MULTICOMP, TENTAP, RESONATOR, LOOPER, TONEMATCH, RTA, PLEX, FBSEND, FBRETURN
- Then `ID_MIDIBLOCK = 190`, `MULTIPLEXER1..4 = 191..194`, `IRPLAYER1..4 = 195..198`, `ID_FOOTCONTROLLER = 199`, `ID_PRESET_FC = 200`

Regular blocks: `id = 46 + 4 × type_index + (instance − 1)`. Example: Amp 1 = 58, Drive 1 = 118.

Not in the enum (unknown IDs, not supported in the alpha): Dynamic Distortion, NAM Player, ID 201 (seen in FM9 status dumps).


## 5. Behaviour notes from community code
- Tuner: the community FM3 firmware (nilkis) treats the tuner as on while tuner push data arrives, and as off on `11 00` or when the push data stops; after switching it off it ignores the push data that is still in flight for a short time.
- Polling: the same firmware polls every 150 ms (scene, preset, status dump, scene name, looper, tempo in rotation) without problems on the FM3.


## 6. Reference documents (`claude/fractal_spec/`)
- Official: `Axe-Fx III MIDI for 3rd Party Devices.pdf` (rev 1.4, still current; no other device-specific spec is published), owner's manuals (Axe-Fx III, FM3, FM9, AM4, VP4), `Fractal-Audio-Blocks-Guide.pdf`, current release notes of all five devices. Every PDF has a `.txt` extract next to it.
- Community: Fractal wiki pages "MIDI SysEx" and "MIDI" (Wayback copies), forum threads (3rd-party spec thread incl. answers from Fractal, DIY controller thread, VP4/AM4 threads, FM9 FAQ).
- `community_github/`: reverse-engineered notes (ToneCommand, forgefx-midi, BigSaurus, fractal-midi) and **nilkis/midicaptain_for_fm3** (MIT) – standalone CircuitPython FM3 firmware for the MIDI Captain. Used as a behaviour reference only; no code is taken over.
