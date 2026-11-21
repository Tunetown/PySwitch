# Examples

Folder `examples/Fractal/<device>/FC Layouts/`, one example per device:
- `MIDICaptain 10/FC Layouts/`: 5 pages (Presets, Scenes, Effects, Channels, Looper) on switch Up; Down: Tuner, hold: Tap Tempo.
- `MIDICaptain Mini 6/FC Layouts/`: 4 pages (Presets, Scenes, Effects, Looper) on switch C, hold C: Tuner; holds on A/B: Bank −/+ (Presets page only).
- `MIDICaptain Nano 4/FC Layouts/`: 4 pages with 3 switches each like the FM3 views (Presets via Inc/Dec with destination names, Scenes, Effects, Channels) on switch B, hold B: Tuner.

Content is modelled on the FM3 factory layouts ([FRACTAL.md 7.4](../FRACTAL.md)): the layouts become PySwitch pages (`PagerAction`, page name shown on a label), FC Hold functions become hold actions. The main display shows preset number + name and scene number + name (like the FC main display); `FractalTunerDisplayCallback` shows the tuner. Hold actions that are not the main function of the switch use `use_leds = False` (the switch LEDs are shared by all LED-using actions of a switch, including hold actions).

All examples work with the default settings (FM3, bank size 5); each `README.md` has the switch table and the setup (DIN cables, *Send Realtime Sysex*, `config.py` options).

Each example has a `communication.py` that routes `PA_MIDICAPTAIN_DIN_MIDI` to and from the application and sets no protocol ([architecture.md 4](python/architecture.md)).

The emulator needs the examples to pick the client (`estimateClient()` checks for `pyswitch.clients.fractal` in `inputs.py`).

Verification (no hardware): each example has been run in CPython with a real `Controller`/`UiController`, mocked hardware modules and a fake device answering the 3rd-party commands (page switching, preset/bank/scene selection, labels, tuner hold).
