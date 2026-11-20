## Example Description

Controls a Fractal Audio FM3, FM9 or Axe-Fx III. The pages are modelled on the Fractal FC layouts (Presets, Scenes, Effects, Looper): switch **C** rotates through them and shows the current page.

|          | Presets    | Scenes    | Effects      | Looper    | Long press                     |
|----------|------------|-----------|--------------|-----------|--------------------------------|
| Switch 1 | P1 in bank | Scene 1   | Drive 1      | Record    |                                |
| Switch 2 | P2 in bank | Scene 2   | Delay 1      | Play/Stop |                                |
| Switch 3 | P3 in bank | Scene 3   | Reverb 1     | Undo      |                                |
| Switch A | P4 in bank | Scene 4   | Chorus 1     | Once      | Presets page: Bank -1          |
| Switch B | P5 in bank | Scene +1  | Compressor 1 | Reverse   | Presets page: Bank +1          |
| Switch C | Next page  |           |              |           | Tuner                          |

Bank -1/+1 only select the bank: the P1-P5 switches show the presets of the new bank, the preset is loaded when you press one of them.

## Setup

- Connect the MIDI Captain to the Fractal device with **two DIN MIDI cables** (MIDI Out to MIDI In and vice versa).
- On the Fractal device, set *Setup > MIDI/Remote > Send Realtime Sysex* to **ON** (needed for the tuner).
- In `config.py`, set the model of your device (the default is the FM3), and optionally the bank size and number display:
  ```
  "fractalModel": 0x11,                # 0x11 = FM3, 0x12 = FM9, 0x10 = Axe-Fx III
  "fractalBankSize": 5,                # Presets per bank (5 "P in bank" switches in this example)
  "fractalPresetDisplayOffset": 0,     # 1 to show preset numbers starting at 001
  ```
