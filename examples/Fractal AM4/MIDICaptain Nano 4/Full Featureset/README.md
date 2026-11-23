## Example Description

Full example for the Fractal Audio **AM4** (experimental): the AM4's footswitch modes as pages. Switch **B** rotates through the pages and shows the current page.

**Full example:** it shows all functions at once. It is not known yet whether it fits into the RAM of the controller; please report if it works on your device.

|          | Presets                 | Scenes                   | Effects   | Modes                      | Long press |
|----------|-------------------------|--------------------------|-----------|----------------------------|------------|
| Switch 1 | Preset 1 of the bank    | Scene 1                  | Slot 1    | AM4 preset mode            | Presets page: previous bank |
| Switch 2 | Preset 2 of the bank    | Scene 2                  | Slot 2    | AM4 scene mode             | Presets page: next bank |
| Switch A | Preset 3 of the bank    | Next scene (shows name)  | Slot 3    | AM4 effects mode           |            |
| Switch B | Next page               |                          |           |                            | Tuner      |

## Setup

- Connect the MIDI Out of the MIDI Captain to the MIDI In of the AM4 and vice versa (**two MIDI cables**). The AM4 has 3.5 mm TRS MIDI jacks (**Type A**): use TRS MIDI cables or DIN to TRS (Type A) cables/adapters, depending on the jacks of your MIDI Captain. No setup on the AM4 is needed for the SysEx communication.
- **Tuner**: assign **CC 15** to *SETUP > MIDI/Remote > Tuner* on the AM4 (MIDI channel 1). Pressing the tuner switch sends CC 15 = 127 (on) and = 0 (off) alternately.
- **Experimental**: the AM4 has no official MIDI spec for controllers. This client uses the AM4-Edit protocol as documented by the community (only messages confirmed on hardware). Please report your firmware version and what works.
