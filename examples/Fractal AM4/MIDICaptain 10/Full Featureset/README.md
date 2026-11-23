## Example Description

Full example for the Fractal Audio **AM4** (experimental). Switch **Up** rotates through the pages, the page is shown in the middle of the display.

**Full example:** it shows all functions at once. It is not known yet whether it fits into the RAM of the controller; please report if it works on your device.

|             | Presets                              | Scenes + Effects     | Modes                |
|-------------|--------------------------------------|----------------------|----------------------|
| Switch 1–4  | Presets 1–4 of the bank              | Scene 1–4            | AM4 preset / scene / effects / amp mode |
| Switch A    | Previous bank (shows letter)         | Slot 1 on/off        | AM4 tuner/tempo mode |
| Switch B    | Next bank (shows letter)             | Slot 2 on/off        | Previous preset      |
| Switch C    | Previous preset (shows name)         | Slot 3 on/off        | Next preset          |
| Switch D    | Next preset (shows name)             | Slot 4 on/off        | Next scene           |
| Switch Up   | Next page                            |                      |                      |
| Switch Down | Tuner                                |                      |                      |

## Setup

- Connect the MIDI Out of the MIDI Captain to the MIDI In of the AM4 and vice versa (**two MIDI cables**). The AM4 has 3.5 mm TRS MIDI jacks (**Type A**): use TRS MIDI cables or DIN to TRS (Type A) cables/adapters, depending on the jacks of your MIDI Captain. No setup on the AM4 is needed for the SysEx communication.
- **Tuner**: assign **CC 15** to *SETUP > MIDI/Remote > Tuner* on the AM4 (MIDI channel 1). Pressing the tuner switch sends CC 15 = 127 (on) and = 0 (off) alternately.
- **Experimental**: the AM4 has no official MIDI spec for controllers. This client uses the AM4-Edit protocol as documented by the community (only messages confirmed on hardware). Please report your firmware version and what works.
