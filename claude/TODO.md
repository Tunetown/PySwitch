# Long-term TODOs

Things that are not part of the current alpha work. Current phase: [SPEC.md 11](SPEC.md).

- **DIN MIDI on the MIDI Captain models**: wiring confirmed by the user (GP16 in, GP17 out); the `PA_MIDICAPTAIN_DIN_MIDI` factory is fixed (LIB_CHANGES.md). Re-check with the Fractal client on real hardware (user).
- **README.md**: supported devices etc., done last, together with the user. Include multiple clients in one configuration: at most one bidirectional protocol, different MIDI channels per device ([spec/emulator/multi_client.md](spec/emulator/multi_client.md)).
- **AM4 / VP4**: not in the alpha. Research results: [FRACTAL.md 1](FRACTAL.md).
- **Unknown block IDs** (Dynamic Distortion, NAM Player, ID 201): collect from tester reports (they show up in the status dump).
- **Effect colors / abbreviations**: let alpha testers verify colors and the 3-letter block abbreviations (FRACTAL.md 7.3).
- **Expression pedals**: maybe add Fractal convenience mappings for External Controllers (generic CC mappings work already).
- **Editor protocol**: excluded for now ([FRACTAL.md 3.5](FRACTAL.md)).

