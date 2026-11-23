## Example Description

Simple example for the Fractal Audio **AM4** (experimental): scenes 1 and 2, and the effects in slots 1 and 2.

|          | Press                          | Long press |
|----------|--------------------------------|------------|
| Switch 1 | Scene 1                        |            |
| Switch 2 | Scene 2                        |            |
| Switch A | Effect in slot 1 on/off        |            |
| Switch B | Effect in slot 2 on/off        | Tuner      |

The effect switches show the name of the block in their slot: bright = engaged, dim = bypassed, off = slot empty. The display shows the preset (location and name) and the scene.

## Setup

- Connect the MIDI Out of the MIDI Captain to the MIDI In of the AM4 and vice versa (**two MIDI cables**). The AM4 has 3.5 mm TRS MIDI jacks (**Type A**): use TRS MIDI cables or DIN to TRS (Type A) cables/adapters, depending on the jacks of your MIDI Captain. No setup on the AM4 is needed for the SysEx communication.
- **Tuner**: assign **CC 15** to *SETUP > MIDI/Remote > Tuner* on the AM4 (MIDI channel 1). Pressing the tuner switch sends CC 15 = 127 (on) and = 0 (off) alternately.
- **Experimental**: the AM4 has no official MIDI spec for controllers. This client uses the AM4-Edit protocol as documented by the community (only messages confirmed on hardware). Please report your firmware version and what works.
