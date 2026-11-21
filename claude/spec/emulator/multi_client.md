# Multiple clients in one configuration

Decision (TBC, 2026-11-21): a configuration can control several clients (e.g. Kemper and Fractal at the same time). Done in two steps:

1. **Client aware parser with import aliases** – done: [parser.md](parser.md).
2. **Emulator** (virtual clients, real devices, UI) – open. Before starting, the UI question in [TBC.md](../../TBC.md) has to be decided.


## PySwitch on the device

No library change needed:
- There is one `Client` for all actions; it handles any mapping, regardless of the client. With a bidirectional protocol (Kemper), only the protocol's parameters use it, all other mappings (Fractal) are polled as usual (`BidirectionalClient`, `KemperBidirectionalProtocol.is_bidirectional()`).
- At most **one** bidirectional protocol per configuration (`Communication["protocol"]`). Today only Kemper has one, so Kemper + Fractal is possible.
- `MidiController.send()` sends every message to all outputs (no routing per client). SysEx is harmless (different manufacturer IDs), but CC/PC messages reach all devices (e.g. a Fractal preset change, CC0 + PC, also switches the Kemper rig). **The devices must use different MIDI channels** (all actions have `midi_channel`). To be documented in the README/examples.
- RAM: all used clients are loaded (~200 kB usable). To be checked on the device with a real configuration.


## Step 2: emulator (planned)

| # | Area / file(s) (`web/htdocs/...`) | Change |
|---|-----------------------------------|--------|
| 1 | `clients/ClientFactory.js` `estimateClient()` → `estimateClients()` | All clients used in the configuration (today: the first one). Used in `ClientController`, `PySwitchRunner`, `test/spec/misc/ConfigRunner.js`. |
| 2 | Virtual clients (`ClientController`, `PySwitchRunner.setMidiWrapper()`, `ConfigRunner`) | A combined MIDI wrapper: sends every message to all virtual clients and merges their answers (like the MIDI routing on the device). |
| 3 | Real devices (`ClientController` scanning/connecting) | One connection per client (each client detected on its own port), messages sent to all connections. |
| 4 | Protocol (`python/PySwitchRunner.py`: `client.getProtocolCode()`) | Protocol code of the one client that has a protocol. |
| 5 | UI: action list (`ParserFrontendInput`, `ActionsProvider`), mapping selects (`MappingOptions`: same-named mappings must be distinguishable and carry their client), virtual client tabs (`PySwitchUI`), MIDI monitor | Actions/mappings of all clients (grouped by client), one tab per virtual client, MIDI monitor names the messages of all clients. How a client is added to a configuration: [TBC.md](../../TBC.md). |
| 6 | Tests (Jasmine) | Kemper + Fractal example configuration with an example test (both virtual clients), detection of several clients. |
| 7 | README/examples | One protocol at most, different MIDI channels per device. |
