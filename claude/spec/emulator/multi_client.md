# Multiple clients in one configuration

Decision (TBC, 2026-11-21): a configuration can control several clients (e.g. Kemper and Fractal at the same time). Done in two steps:

1. **Client aware parser with import aliases** – done: [parser.md](parser.md).
2. **Emulator** (virtual clients, real devices, UI) – done (2026-11-22), this file.


## PySwitch on the device

No library change needed:
- There is one `Client` for all actions; it handles any mapping, regardless of the client. With a bidirectional protocol (Kemper), only the protocol's parameters use it, all other mappings (Fractal) are polled as usual (`BidirectionalClient`, `KemperBidirectionalProtocol.is_bidirectional()`).
- At most **one** bidirectional protocol per configuration (`Communication["protocol"]`). Today only Kemper has one, so Kemper + Fractal is possible.
- `MidiController.send()` sends every message to all outputs (no routing per client). SysEx is harmless (different manufacturer IDs), but CC/PC messages reach all devices (e.g. a Fractal preset change, CC0 + PC, also switches the Kemper rig). **The devices must use different MIDI channels** (all actions have `midi_channel`). Documented in the example README; README.md: [TODO.md](../../TODO.md).
- RAM: all used clients are loaded (~200 kB usable). To be checked on the device with a real configuration.


## Emulator

### Rules
- **Clients of a configuration** are derived from the code, there is no setting (TBC decision 2026-11-22, option A): every client imported in `inputs.py` or `display.py` (`pyswitch.clients.<client>`) is used. Without any client import, Kemper is assumed (as before). The first client in the order Kemper, Boomerang, Fractal is the main client.
- **Adding/removing clients**: the "add action" dialog offers the actions of all clients (grouped by client, sorted by client). Adding the first action of a client adds the client (the imports follow automatically, [parser.md](parser.md)), removing its last action removes it. After every change of the configuration, the client connection is initialized again if the clients have changed.
- **Virtual clients**: one virtual client per client, each in its own tab. Like the MIDI routing on the device, every message of PySwitch is sent to all virtual clients, and the messages of all of them are received. Each virtual client also receives the messages of the other clients (like a real device); unknown messages are logged as "Unparsed" in the console and the client statistics.
- **Real devices** ("Auto-detect client device"): each client is searched on its own port with its detector (in parallel). Clients found on a port are connected to that port, clients not found are connected to their virtual client (so a real Kemper can be combined with a virtual Fractal). Selecting a single port or virtual client manually connects only that one.
- **Protocol**: the protocol of the one client which has a protocol code (`Client.getProtocolCode()`), else none.
- **Mapping selects**: mappings with the same name in several clients are listed once per client (name with the client's display name, value with the qualified name `<CLIENT>_<NAME>`, [parser.md](parser.md)). Parameters whose range has too many values (`ParameterRange.getValues()` returns `null`, e.g. Fractal `effect_id` 0..255) offer only the first 10 values of the range (TBC decision 2026-11-23); other values can be entered in the code. For Fractal `effect_id`, these are 0..9, which are no effect blocks (regular blocks start at 46); left as it is for now (TBC decision 2026-11-23, [TODO.md](../../TODO.md)).
- **MIDI monitor**: names the messages of all clients (unchanged: it always asks the virtual clients of all available clients).

### Implementation (`web/htdocs/...`)

| File | Change |
|------|--------|
| `clients/ClientFactory.js` | `estimateClient()` replaced by `estimateClients()` (all clients, see rules); new `getProtocolClient()` |
| `js/midi/CombinedMidiWrapper.js` (new) | MIDI wrapper combining several wrappers (virtual clients and `PythonMidiWrapper`s): sends to all, shares one message queue with all of them, `run()`/`update()`/`detach()`/`getMessageProperties()` for all. Used only for more than one wrapper. |
| `js/ClientController.js` | `#scan()` scans per client (`#scanClient()`), `#scanPort()` takes the client ID, `#connectAll()` connects ports and virtual clients, `#connect()` uses it for manual selections; new `update()` |
| `js/Controller.js` | `restart()` calls `ClientController.update()` after the changes |
| `js/PySwitchRunner.js` | protocol client via `ClientFactory.getProtocolClient()` (`python/PySwitchRunner.py` is unchanged) |
| `js/ui/PySwitchUI.js` | `showVirtualClient()` → `showVirtualClients()` (one tab per virtual client) |
| `js/ui/parser/ActionProperties.js` | `createActionDefinition()` returns the client of the action |
| `js/ui/parser/ActionsProvider.js`, `ParserFrontendInput.js` | editing an action preselects the action of its client (same-named actions of several clients) |
| `js/model/parser/MappingOptions.js` | qualified values and client names for same-named mappings; first 10 values for parameters with too many values |
| `test/spec/misc/ConfigRunner.js` | one virtual client per client: `clients` (by client ID), `client` is the MIDI wrapper (the virtual client, or a `CombinedMidiWrapper`) |
| `test/spec/examples/fractal/FractalTestBase.js` | `client` is `runner.clients.fractal` |
| `index.html`, `test/index.html` | `CombinedMidiWrapper.js`; test page: `MappingOptions.js` and the new tests |

### Tests (Jasmine)
- `test/spec/misc/MultiClientTests.js` (spec "Multiple Clients"): client detection, protocol client, `CombinedMidiWrapper`, PySwitch run with two virtual clients.
- `test/spec/parser/ClientImportsTests.js`: qualified names in code strings, unchanged code strings keep their clients, mapping options incl. parameters with too many values ([parser.md](parser.md)).
- `test/spec/test_config_parser.js`: timeout of "Display name: Bank Select" raised to 60 s (parses the configuration 8 times; TBC decision 2026-11-23).
- Example `examples/Kemper and Fractal/MIDICaptain Nano 4/Rigs and Scenes/` ([examples.md](../examples.md)) with an example test: Fractal scenes and scene name display, Kemper rig selection, both virtual clients.
