## Example Description

Simple example for the Fractal Audio **FM9**: scene selection and tuner, no pages.

|          | Press   | Long press |
|----------|---------|------------|
| Switch 1 | Scene 1 |            |
| Switch 2 | Scene 2 |            |
| Switch A | Scene 3 |            |
| Switch B | Scene 4 | Tuner      |

The display shows the preset number and name and the scene number and name, and the tuner when it is engaged.

## Setup

- Connect the MIDI Captain to the FM9 with **two DIN MIDI cables** (MIDI Out to MIDI In and vice versa).
- On the FM9, set *Setup > MIDI/Remote > Send Realtime Sysex* to **ON** (needed for the tuner).
- In `config.py`, set the model:
  ```
  "fractalModel": 0x12,             # FM9
  ```
