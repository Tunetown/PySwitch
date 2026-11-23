## Example Description

Simple example for the Fractal Audio **FM9**: scene selection, four effect blocks, presets and tuner, no pages.

|           | Press                    | Long press |
|-----------|--------------------------|------------|
| Switch 1  | Scene 1                  |            |
| Switch 2  | Scene 2                  |            |
| Switch 3  | Scene 3                  |            |
| Switch 4  | Scene 4                  |            |
| Switch A  | Drive 1 on/off  |            |
| Switch B  | Delay 1 on/off  |            |
| Switch C  | Reverb 1 on/off  |            |
| Switch D  | Amp 2 on/off  |            |
| Switch Up | Preset +1                |            |
| Switch Down | Preset −1              | Tuner      |

The effect switches are lit brightly when the block is engaged, dimmed when it is bypassed, and off when the block is not in the current preset. The display shows the preset number and name and the scene number and name, and the tuner when it is engaged.

## Setup

- Connect the MIDI Captain to the FM9 with **two DIN MIDI cables** (MIDI Out to MIDI In and vice versa).
- On the FM9, set *Setup > MIDI/Remote > Send Realtime Sysex* to **ON** (needed for the tuner).
- In `config.py`, set the model:
  ```
  "fractalModel": 0x12,             # FM9
  ```
