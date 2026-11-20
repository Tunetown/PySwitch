# Examples

Folder `examples/Fractal/`, one basic example per device:
- `MIDICaptain 10/` (STD)
- `MIDICaptain Mini 6/`
- `MIDICaptain Nano 4/`

Content: modelled on the FM3 factory layouts ([FRACTAL.md 7.4](../FRACTAL.md)), adapted to the number of switches: the layouts become PySwitch pages (Presets, Scenes, Effects, Channels, Looper, Utilities), FC Hold functions become hold actions. Preset and scene name display like the FC main display.

Each example has a `communication.py` that routes `PA_MIDICAPTAIN_DIN_MIDI` to and from the application and sets no protocol ([architecture.md 4](python/architecture.md)).

The emulator needs the examples to pick the client (`estimateClient()` checks for `pyswitch.clients.fractal` in `inputs.py`).
