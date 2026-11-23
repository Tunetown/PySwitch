## Example Description

Full example for the Fractal Audio **Axe-Fx II** (experimental), with pages like the gen-3 Fractal examples. Switch **C** rotates through the pages and shows the current page.

**Full example:** it shows all functions at once. It is not known yet whether it fits into the RAM of the controller; please report if it works on your device.

|          | Presets                         | Scenes         | Effects            | Channels    | Long press |
|----------|---------------------------------|----------------|--------------------|-------------|------------|
| Switch 1 | Preset 1 of the bank            | Scene 1        | Drive 1 on/off     | Amp 1 X/Y   |            |
| Switch 2 | Preset 2 of the bank            | Scene 2        | Delay 1 on/off     | Drive 1 X/Y |            |
| Switch 3 | Preset 3 of the bank            | Scene 3        | Reverb 1 on/off    | Delay 1 X/Y |            |
| Switch A | Previous bank (first preset)    | Previous scene | Chorus 1 on/off    | Reverb 1 X/Y |           |
| Switch B | Next bank (first preset)        | Next scene     | Compressor 1 on/off | Cab 1 X/Y  |            |
| Switch C | Next page                       |                |                    |             | Tuner      |

## Setup

- Connect the MIDI Captain to the Axe-Fx II with **two DIN MIDI cables** (MIDI Out to MIDI In and vice versa).
- On the Axe-Fx II, set *I/O > MIDI > SEND REALTIME SYSEX* to **ALL** (needed for the tuner display).
- The tuner is switched with **CC 15** on MIDI channel 1, the defaults of *I/O > CTRL > Tuner* and *I/O > MIDI > Channel*. If you changed them on the device, pass `cc` and `midi_channel` to the actions (and `tuner_cc` and `midi_channel` to FractalIITunerDisplayCallback in display.py, which switches the tuner off when a switch is pressed).
- In `config.py`, set the model (default is the XL+):
  ```
  "fractalIIModel": 7,              # 3 = Axe-Fx II (Mark I/II), 6 = XL, 7 = XL+
  ```
- Presets and scenes are selected with SysEx messages, so no program change setup is needed on the device.
- **Experimental**: this client is based on Fractal's MIDI spec for the Axe-Fx II and community reports, but has not been tested on a real Axe-Fx II by the PySwitch developers. Please report your model, firmware version and what works.
