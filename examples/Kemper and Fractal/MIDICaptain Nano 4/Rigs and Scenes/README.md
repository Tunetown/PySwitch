## Example Description

Controls a Kemper Profiler and a Fractal Audio FM3, FM9 or Axe-Fx III at the same time.

|          | Press                                                  |
|----------|--------------------------------------------------------|
| Switch 1 | Kemper: Rig 1                                          |
| Switch 2 | Kemper: Rig 2                                          |
| Switch A | Fractal: Scene 1, again: Scene 2                       |
| Switch B | Tap Tempo for **both** devices (shows the Fractal BPM) |

The display shows the Kemper rig name and the Fractal scene name. The tuner display shows the Kemper tuner.

## Setup

- Connect the Kemper via **USB**, and the Fractal device via **two DIN MIDI cables** (MIDI Out to MIDI In and vice versa).
- All MIDI messages are sent to both devices. SysEx messages are ignored by the other device, but **CC and PC messages reach both devices**, so the devices must use **different MIDI channels** as soon as you add actions sending CC or PC messages to the Fractal device (for example preset or bank selection, which have a `midi_channel` parameter). The actions of this example do not conflict.
- At most one bidirectional protocol can be used per configuration (here: Kemper). The Fractal device is polled as usual.
- On the Fractal device, set *Setup > MIDI/Remote > Send Realtime Sysex* to **ON** (needed for the tempo display).
- In `config.py`, set the model of your Fractal device (the default is the FM3):
  ```
  "fractalModel": 0x11,                # 0x11 = FM3, 0x12 = FM9, 0x10 = Axe-Fx III
  ```
