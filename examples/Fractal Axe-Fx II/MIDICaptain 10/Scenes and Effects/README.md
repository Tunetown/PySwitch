## Example Description

Simple example for the Fractal Audio **Axe-Fx II** (experimental): scenes on the upper row, effects on the lower row.

|             | Press                | Long press |
|-------------|----------------------|------------|
| Switch 1–4  | Scene 1–4            |            |
| Switch A    | Drive 1 on/off       |            |
| Switch B    | Delay 1 on/off       |            |
| Switch C    | Reverb 1 on/off      |            |
| Switch D    | Amp 2 on/off         |            |
| Switch Up   | Next preset          |            |
| Switch Down | Previous preset      | Tuner      |

The effect switches are bright when the block is engaged, dim when it is bypassed and off when the block is not in the preset. The display shows the preset number and name and the scene, and the tuner when it is engaged.

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
