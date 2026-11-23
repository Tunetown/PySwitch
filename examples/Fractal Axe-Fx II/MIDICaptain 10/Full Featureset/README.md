## Example Description

Full example for the Fractal Audio **Axe-Fx II** (experimental), with pages like the gen-3 Fractal examples. Switch **Up** rotates through the pages, the page is shown in the middle of the display.

**Full example:** it shows all functions at once. It is not known yet whether it fits into the RAM of the controller; please report if it works on your device.

|             | Presets                       | Scenes    | Effects                 | Channels                                  |
|-------------|-------------------------------|-----------|-------------------------|-------------------------------------------|
| Switch 1–4  | Presets 1–4 of the bank       | Scene 1–4 | Compressor 1, Wah 1, Drive 1, Amp 1 on/off | Drive 1, Amp 1, Cab 1, Delay 1 X/Y |
| Switch A    | Preset 5 of the bank          | Scene 5   | Chorus 1 on/off         | Reverb 1 X/Y                              |
| Switch B    | Previous bank                 | Scene 6   | Delay 1 on/off          | Chorus 1 X/Y                              |
| Switch C    | Next bank                     | Scene 7   | Reverb 1 on/off         | Amp 2 X (pressed again: on/off)           |
| Switch D    | Next preset (shows its name)  | Scene 8   | Amp 2 on/off            | Amp 2 Y (pressed again: on/off)           |
| Switch Up   | Next page                     |           |                         |                                           |
| Switch Down | Tap tempo (shows the BPM), long press: tuner |  |                     |                                           |

## Setup

- Connect the MIDI Captain to the Axe-Fx II with **two DIN MIDI cables** (MIDI Out to MIDI In and vice versa).
- On the Axe-Fx II, set *I/O > MIDI > SEND REALTIME SYSEX* to **ALL** (needed for the tuner display and the tap tempo LED).
- The tuner is switched with **CC 15** on MIDI channel 1, the defaults of *I/O > CTRL > Tuner* and *I/O > MIDI > Channel*, tap tempo with **CC 14** (*I/O > CTRL > Tap Tempo*). If you changed them on the device, pass `cc` and `midi_channel` to the actions (and `tuner_cc` and `midi_channel` to FractalIITunerDisplayCallback in display.py, which switches the tuner off when a switch is pressed).
- In `config.py`, set the model (default is the XL+):
  ```
  "fractalIIModel": 7,              # 3 = Axe-Fx II (Mark I/II), 6 = XL, 7 = XL+
  ```
- Presets and scenes are selected with SysEx messages, so no program change setup is needed on the device.
- **Experimental**: this client is based on Fractal's MIDI spec for the Axe-Fx II and community reports, but has not been tested on a real Axe-Fx II by the PySwitch developers. Please report your model, firmware version and what works.
