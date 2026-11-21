# TBC – Open points

Answer below each item after **Answer:**. "Recommendation" is what I do if you just say "ok". Add your own wishes at the end.

--- 

## 1. Multiple clients: how is a client added to a configuration in the emulator UI?

Step 1 (client aware parser, aliases) is done: [spec/emulator/parser.md](spec/emulator/parser.md). Step 2 (emulator: virtual clients, real devices, UI) is planned in [spec/emulator/multi_client.md](spec/emulator/multi_client.md). Before starting it, this has to be decided. Today the emulator determines the one client of a configuration from the code (`ClientFactory.estimateClient()`: the first client imported in `inputs.py`), and the "add action" dialog only offers the actions of that client plus the local ones.

Options:
- **A**: Derived from the code, no setting. The "add action" dialog offers the actions of **all** clients (grouped by client, the sorting by client already exists). Adding the first action of a client adds the client (the imports follow automatically), removing its last action removes it. The emulator shows a virtual client tab for every client used.
- **B**: Explicit list of clients per configuration (e.g. a setting "Clients: Kemper, Fractal"); the "add action" dialog only offers the actions of these clients. Needs a place to store the list (e.g. a comment or option in `inputs.py`/`config.py`) that has to be kept in sync with the code.

Recommendation: **A** (no additional setting to keep in sync; the code stays the only source of truth, as today).

**Answer:**

---


## Your wishes
