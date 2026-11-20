## Example Description

Controls a Fractal Audio FM3, FM9 or Axe-Fx III. The pages are modelled on the Fractal FC layouts (Presets, Scenes, Effects, Channels, Looper): switch **Up** rotates through them, the page is shown in the middle of the display.

|            | Presets      | Scenes  | Effects      | Channels          | Looper       | Long press |
|------------|--------------|---------|--------------|-------------------|--------------|------------|
| Switch 1   | P1 in bank   | Scene 1 | Drive 1      | Amp 1 channel A   | Record       |            |
| Switch 2   | P2 in bank   | Scene 2 | Delay 1      | Amp 1 channel B   | Play/Stop    |            |
| Switch 3   | P3 in bank   | Scene 3 | Reverb 1     | Amp 1 channel C   | Undo         |            |
| Switch 4   | P4 in bank   | Scene 4 | Chorus 1     | Amp 1 channel D   | Once         |            |
| Switch Up  | Next page    |         |              |                   |              |            |
| Switch A   | P5 in bank   | Scene 5 | Compressor 1 | Drive 1 A/B       | Reverse      |            |
| Switch B   | Bank -1      | Scene 6 | Phaser 1     | Drive 2 A/B       | Half Speed   |            |
| Switch C   | Bank +1      | Scene 7 | Pitch 1      | Delay 1 channel + | Looper block |            |
| Switch D   | Preset +1    | Scene 8 | Wah 1        | Reverb 1 channel +| Tap Tempo    |            |
| Switch Dn  | Tuner        |         |              |                   |              | Tap Tempo  |

Bank -1/+1 only select the bank: the P1-P5 switches show the presets of the new bank, the preset is loaded when you press one of them.

## Setup

- Connect the MIDI Captain to the Fractal device with **two DIN MIDI cables** (MIDI Out to MIDI In and vice versa).
- On the Fractal device, set *Setup > MIDI/Remote > Send Realtime Sysex* to **ON** (needed for the tuner and the tempo display).
- In `config.py`, set the model of your device (the default is the FM3), and optionally the bank size and number display:
  ```
  "fractalModel": 0x11,                # 0x11 = FM3, 0x12 = FM9, 0x10 = Axe-Fx III
  "fractalBankSize": 5,                # Presets per bank (5 "P in bank" switches in this example)
  "fractalPresetDisplayOffset": 0,     # 1 to show preset numbers starting at 001
  ```
