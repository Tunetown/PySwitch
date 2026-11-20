# Emulator – Virtual Fractal Client

Built **first** (no real device available), analog to the Virtual Kemper Client (`web/htdocs/clients/kemper/`).
Protocol it simulates: [FRACTAL.md](../../FRACTAL.md). Integration into the emulator: [integration.md](integration.md).


## Files (`web/htdocs/clients/fractal/`)

| File                                  | Content                                                                            |
|---------------------------------------|------------------------------------------------------------------------------------|
| `FractalClient.js`                    | display name, `getProtocolCode()`, `getVirtualClient()`, `getClientDetector()`, `resolveValueToken()` (e.g. `NUM_PRESETS`), meta factories |
| `FractalClientDetector.js`            | sends a scene query with each model byte (FM3, FM9, Axe-Fx III); a valid answer identifies the device and its model |
| `virtual/VirtualFractalClient.js`     | main class (based on `VirtualClient`: `doSend`, `queueMessage`, `update`, `getUserInterface`) |
| `virtual/VirtualFractalProtocol.js`   | parses incoming SysEx (checksum check, NAK `64` on errors) and CC0/PC, builds answers |
| `virtual/VirtualFractalPresets.js`    | preset model: presets with names; per preset 8 scenes with names; blocks with bypass/channel per scene |
| `virtual/VirtualFractalTempo.js`      | tempo, tap, beat push                                                              |
| `virtual/VirtualFractalTuner.js`      | tuner on/off, push data simulation                                                 |
| `virtual/VirtualFractalLooper.js`     | looper state machine (Rec/Play/Overdub/Once/Reverse/Half, Undo)                    |
| `virtual/VirtualFractalStats.js`      | traffic statistics                                                                 |
| `virtual/VirtualFractalClientUI.js`   | UI (see below)                                                                     |


## Behaviour

- Behaves like a real device: answers queries and never pushes state changes. Only tempo beat and tuner data are pushed (simulates DIN with *Send Realtime Sysex* = ON).
- Model selector: FM3 (default, like `fractalModel`), FM9, Axe-Fx III. The model sets the model byte it answers to, the number of presets and the block counts.
- Dummy content is generated per preset (names, block set matching the model's block counts).
- Changes made in the UI (preset, scene, bypass, channel, looper) behave like changes on the device: PySwitch only sees them through its polling.


## UI

Model selector, preset and scene selectors with names, block grid with bypass checkbox and channel select per block, tuner (on/off, note/cents input), tempo (BPM, beat indicator), looper buttons with state, traffic indicators.
