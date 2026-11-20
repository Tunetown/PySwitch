## Example Description

Controls a Fractal Audio FM3, FM9 or Axe-Fx III. Like the views of the FM3 factory layouts, every page has three switches: switch **B** rotates through the pages and shows the current page.

|          | Presets                  | Scenes                 | Effects  | Channels                          | Long press                      |
|----------|--------------------------|------------------------|----------|-----------------------------------|---------------------------------|
| Switch 1 | Preset -1 (shows name)   | Scene 1                | Drive 1  | Amp 1 channel A/B                 | Presets page: Bank -1 (loads the first preset) |
| Switch 2 | Preset +1 (shows name)   | Scene 2                | Delay 1  | Drive 1 next channel              | Presets page: Bank +1 (loads the first preset) |
| Switch A | Tap Tempo (shows BPM)    | Scene +1 (shows name)  | Reverb 1 | Delay 1 channel B, again: on/off  |                                 |
| Switch B | Next page                |                        |          |                                   | Tuner                           |

## Setup

- Connect the MIDI Captain to the Fractal device with **two DIN MIDI cables** (MIDI Out to MIDI In and vice versa).
- On the Fractal device, set *Setup > MIDI/Remote > Send Realtime Sysex* to **ON** (needed for the tuner and the tempo display).
- In `config.py`, set the model of your device (the default is the FM3), and optionally the bank size and number display:
  ```
  "fractalModel": 0x11,                # 0x11 = FM3, 0x12 = FM9, 0x10 = Axe-Fx III
  "fractalBankSize": 5,                # Presets per bank
  "fractalPresetDisplayOffset": 0,     # 1 to show preset numbers starting at 001
  ```
