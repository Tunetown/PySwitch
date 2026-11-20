# Emulator – Virtual Fractal Client

Built **first** (no real device available), analog to the Virtual Kemper Client (`web/htdocs/clients/kemper/`).
Protocol it simulates: [FRACTAL.md](../../FRACTAL.md). Integration into the emulator: [integration.md](integration.md).


## Files (`web/htdocs/clients/fractal/`)

| File                                  | Content                                                                            |
|---------------------------------------|------------------------------------------------------------------------------------|
| `FractalClient.js`                    | model table, SysEx helpers (checksum, 14-bit), display name, `getVirtualClient()`, `getClientDetector()`, `resolveValueToken()` (`NUM_PRESETS`, `NUM_SCENES`) |
| `FractalClientDetector.js`            | sends a scene query with each model byte (FM3, FM9, Axe-Fx III); a valid answer identifies the device and its model |
| `virtual/VirtualFractalClient.js`     | main class (based on `VirtualClient`: `doSend`, `queueMessage`, `update`, `getUserInterface`) |
| `virtual/VirtualFractalBlocks.js`     | block IDs, names, abbreviations, instance counts per model, channel counts (Blocks Guide) |
| `virtual/VirtualFractalProtocol.js`   | parses incoming SysEx (checksum check, NAK `64` on errors) and CC0/PC, builds answers |
| `virtual/VirtualFractalPresets.js`    | preset model: presets with names; per preset 8 scenes with names; blocks with bypass/channel per scene |
| `virtual/VirtualFractalTempo.js`      | tempo, tap, beat push                                                              |
| `virtual/VirtualFractalTuner.js`      | tuner on/off, push data simulation                                                 |
| `virtual/VirtualFractalLooper.js`     | looper state machine (Rec/Play/Overdub/Once/Reverse/Half, Undo)                    |
| `virtual/VirtualFractalStats.js`      | traffic statistics                                                                 |
| `virtual/VirtualFractalClientUI.js`   | UI (see below)                                                                     |


## Behaviour

- Behaves like a real device: answers queries and never pushes state changes. Only tempo beat and tuner data are pushed (simulates DIN with *Send Realtime Sysex* = ON).
- Model selector: FM3, FM9, Axe-Fx III. The model sets the model byte it answers to, the number of presets and the block counts. When the emulator UI creates the virtual client (no options passed), the model is taken from the emulator settings (`fractalModel`), else FM3 (tests pass options, so they are independent of the user's settings).
- Dummy content is generated per preset (names, scene names, block set matching the model's block counts, per scene bypass/channel). Loading a preset copies it to a working buffer; bypass/channel changes are kept per scene until the next preset change, like on the device.
- Undocumented device behaviour, chosen here: NAK error code `01` for checksum errors; bypass/channel queries for blocks not in the preset are not answered; messages with a foreign model byte, malformed messages and out of range values are ignored; PC is accepted on all MIDI channels.
- Looper: state machine after the Blocks Guide (Record, Play, Undo/Erase, Once, Reverse, Half, Overdub, layers), "Record 2nd Press" selectable; it only reacts while the preset contains a Looper block.
- Tap tempo averages the last up to 10 taps (device default); BPM range 24–250.
- Changes made in the UI (preset, scene, bypass, channel, looper) behave like changes on the device: PySwitch only sees them through its polling.


## UI

Model selector, Send Realtime Sysex switch, preset number and scene selectors with editable names, block list of the current preset (engaged checkbox, channel select, remove; add block), tuner (on/off, note, cents, string), tempo (BPM, beat indicator), looper buttons with state and Record 2nd Press, traffic indicators (click for details).
