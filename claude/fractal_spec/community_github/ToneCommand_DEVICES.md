# Supported devices

ToneCommand talks to a device through an adapter, and every adapter declares
what it can actually do rather than assuming. That declaration is not
decoration: the safety layer reads it, and a device that cannot verify a write
is never allowed to report one as verified. So this page is blunt about what each
device can and cannot do today.

When more than one of these is reachable at once, a picker appears in the
header and a build is refused until you say which device it is for.

| Device | Control | State read back | Notes |
|---|---|---|---|
| **Fractal FM9** | Full | From the unit | The reference implementation. Blocks, scenes, cabs, modifiers, stores, preset files |
| **BOSS IR-2** | Full, all 7 parameters, plus IR install | From the unit | Amp voicing, tone stack, ambience. Announces its own knob moves. Load your own cab IRs |
| **Fractal FM3** | Read-only, through a USB MIDI interface (unreleased after 1.5.9) | From the unit | No MIDI over USB: choose the interface on its 5-pin MIDI ports in the Devices FM3 card (#221). Unverified on a real FM3 |
| **HeadRush** | Rigs and parameters | From the unit | Core-verified. One verification rerun and one acked-too-early defect still open (#33, #166) |
| **Fractal Axe-Fx III** | Read-only (new in 1.6.0) | From the unit | Presets, scenes, firmware, block bypass and channels. Mark I, Mark II and Turbo. Verified on a Mark II against Axe-Edit |
| **IK Multimedia ToneX** | None, by design | Observed | Captures listed, nothing written. The upload path is undecoded (#27) and stays closed |

Wanted next, each with hardware as the only real blocker: full FM3 control
(#40), Axe-Fx III editing (#190), AM4 (#41), VP4 (#191), Kemper, Boss ES-5. A device
ToneCommand recognises but cannot drive yet is named when it is plugged in,
with a link to its issue, instead of being silently ignored. The picker is
device-agnostic, so an adapter that registers correctly appears in it with no
interface work at all.

## Fractal FM9

Developed and regression-tested on an FM9 Mk II Turbo across firmware 11.x and
12.00. Everything ToneCommand does on an FM9 is edit-buffer only unless you
explicitly whitelist a store slot, and every write is verified by reading the
unit back. The full capability matrix per firmware is in
[SETUP.md](SETUP.md#compatibility), and the protocol record with evidence per
claim is [PROTOCOL.md](PROTOCOL.md).

Other FM9 variants share the model byte and should behave identically but are
untested. The FM3 is a different case (below); the Axe-Fx III uses a different
model byte and has its own read-only adapter (below).

## Fractal FM3 (through a MIDI interface, read-only)

**The FM3 does not do MIDI over USB.** Its USB port carries only Fractal's own
channel (COM over USB) for FM3-Edit, Fractal-Bot and Cab-Lab; it never appears
as a MIDI device on Windows or macOS, and installing Fractal's USB driver does
not change that ([Fractal wiki: USB](https://wiki.fractalaudio.com/wiki/index.php?title=USB),
[MIDI](https://wiki.fractalaudio.com/wiki/index.php?title=MIDI)). The FM9 is
different: it does MIDI over USB, which is how ToneCommand reaches it, and its
USB and Windows driver guidance is unchanged.

ToneCommand reaches an FM3 through a **USB MIDI interface** connected to the
FM3's **5-pin MIDI IN and MIDI OUT**: interface OUT to FM3 IN, and FM3 OUT to
interface IN (#221, unreleased after 1.5.9). Open **Devices**, choose your
interface's port on the **Fractal FM3** card, and press **Save**. The name must
be available for both MIDI input and output. ToneCommand remembers it in
`fm3_port.json` beside its other local settings and uses that exact name; if
the port disappears it will not choose another interface. Saving a different
port while connected reconnects the FM3 through the new port. Without a saved
port, an FM3-named port is still found automatically.

For a fixed configuration, set `TONECOMMAND_FM3_PORT` to the exact interface
port name. It takes precedence over the saved choice. Devices shows that the
environment fixes the port and disables Save; change or remove that environment
setting to choose a different port.

Once connected, ToneCommand addresses the FM3 through the FM9's own code with
the FM3's model byte: it shows the loaded preset, the eight scenes and which
blocks are on, and switches presets and scenes. Read-only is enforced at the
FM3's MIDI port (only Fractal's documented queries plus preset and scene
switching), because the FM3's block and parameter map has only been proven on
an FM9.

**Not yet verified on a real FM3.** The interface route and the model byte
(taken from preset files) still need a hardware check by an FM3 owner;
simulator checks do not establish hardware support. Full support is #40.

## BOSS IR-2

Plug it in by USB and it appears. There is nothing to configure, no
environment variable and no port to choose.

ToneCommand controls all seven of the pedal's parameters:

| Parameter | Range |
|---|---|
| AMP | one of CLEAN, TWN, TWEED, DIAMOND, CRUNCH, BRIT, HI-GAIN, SLDN, BROWN, MODDED, RFIER |
| GAIN, BASS, MIDDLE, TREBLE, LEVEL, AMBIENCE | 0 to 127 |

Every write is followed by a read of the same address, and a write whose
read-back disagrees raises instead of reporting success. The pedal clamps an
out-of-range value silently rather than refusing it, which would look like a
successful write to a naive read-back, so ranges are checked before anything is
sent.

The IR-2 is also the most talkative device ToneCommand supports. It announces
every knob turn and footswitch press without being asked, so ToneCommand knows
when you have changed something on the pedal by hand. The FM9 cannot do that.

### Loading your own IRs

ToneCommand can write a cabinet IR from your own library into the pedal.

The eleven USER slots are not a free list: each one holds the cabinet for one
amp voicing, in order, so installing an IR replaces that amp's speaker.

| Slot | Voicing | | Slot | Voicing | | Slot | Voicing |
|---|---|---|---|---|---|---|---|
| USER 1 | CLEAN | | USER 5 | CRUNCH | | USER 9 | BROWN |
| USER 2 | TWN | | USER 6 | BRIT | | USER 10 | MODDED |
| USER 3 | TWEED | | USER 7 | HI-GAIN | | USER 11 | RFIER |
| USER 4 | DIAMOND | | USER 8 | SLDN | | | |

Because of that, **no slot is writable until you say so.** Set
`TONECOMMAND_IR2_SLOTS` to the slots you are willing to overwrite, for example
`9,10,11`. Asking for a slot that is not on the list tells you which voicing's
cabinet you were about to replace.

Any 16, 24 or 32-bit PCM wav works. It is resampled to 44.1 kHz, truncated to
the 37 ms the pedal holds with a short fade so the cut does not click, and
peak-normalised, because every factory cab peaks at exactly 1.0 and a hotter
one clips inside the pedal. Every sample is read back and compared before the
install reports success.

**The pedal loads its cabinets at power-on**, so a freshly installed IR is not
audible until you unplug the IR-2 and plug it back in. Switching voicings does
not do it. Every install says so in its result, because otherwise it reads as
a failure.

Removing an IR is refused: it would leave that voicing with no speaker at all,
which the pedal's own editor does not offer. Install something else over it.
The pedal has no scenes and no effect blocks, so those refuse too, by
declaration rather than by pretending. It reports no firmware version, so
ToneCommand reports none rather than inventing one.

The protocol was decoded on hardware on 2026-09-29. Frames, addresses,
evidence and the remaining unknowns are recorded in the project's protocol
ledger.

## Fractal Axe-Fx III (read-only)

New in 1.6.0, contributed by [@Axelman8](https://github.com/Axelman8). Choose
the Axe-Fx III in **Devices** and ToneCommand reads, from the unit:

- the current preset and scene;
- preset names and scene names;
- the firmware version;
- which blocks are on or bypassed, and their channels.

Pick your model in **Devices**: a Mark I has 512 presets, a Mark II or Turbo
has 1024. Mark I is the default, so a Mark II or Turbo owner picks theirs once
to see the upper 512. Preset numbers count from 0, matching Axe-Edit.

It is read-only by construction: every message to the III is checked against
an exact list of read requests before it leaves, and changing sounds,
switching presets, storing, NAM and firmware traffic are all refused. Editing
is tracked in #190.

Verified on a Mark II against Axe-Edit III. Not yet checked on a Mark I or a
Turbo, and the firmware readout shows a different number from Axe-Edit's on a
beta firmware. Details: [AXEFX3-READONLY.md](https://github.com/monzta1/ToneCommand/blob/main/docs/AXEFX3-READONLY.md).

## HeadRush

Contributed by @bschmalz81401 and on `main` since 1.3.0, reachable over the
network rather than USB. Set `TONECOMMAND_HEADRUSH_HOST` to its address. It is
supported and useful, and it is honest about being unfinished: #33 is held open
for one verification rerun and #166 records a real defect, where the device
acknowledges a rig load before the chain has actually been replaced.

## IK Multimedia ToneX

Read-only on purpose. ToneCommand lists what captures are loaded and reports
what the pedal announces over its serial port, and it has no code path that
writes. The capture-upload format is undecoded by anyone (#27), and until it is
proven, install and remove refuse before a frame exists rather than guessing at
a pedal's flash. Load captures with the TONEX Editor.

## Adding a device

An adapter is one class implementing the contract in
[ARCHITECTURE.md](../ARCHITECTURE.md), plus an honest capability declaration, a
parameter registry and a simulator so the suite runs without hardware. The
safety layer is inherited, not reimplemented. Declaring is deny-by-default, so
an unfinished adapter under-promises rather than over-promises, and a thin one
that only reports state is a legitimate contribution rather than a compromise.

If you own a device on the wanted list, comment on its issue and it is yours.
