# Emulator – Client aware parser

Decision (TBC, 2026-11-21): the emulator parser is client aware, so actions and mappings of different clients may have the same name ([SPEC.md 9.6](../../SPEC.md): classes must still be unique). A configuration may use several clients ([multi_client.md](multi_client.md)), including same-named actions of different clients in one file.

Status: implemented (step 1 of [multi_client.md](multi_client.md)).


## Rules

- **Client functions** are all entries of `definitions/actions.json` and `definitions/mappings.json` without a dot in the name (actions, mappings, also classes like `PagerAction`). They are imported by `(client, name)` with the `importPath` of the definition.
- Entries with a dot (`FractalMappings.PRESET`, `KemperMappings.EFFECT_STATE`, `PagerAction.proxy`) import their class (`importName`), which is unique: handled by name as before. Same for all other names (callbacks, `FractalLabel`, `KemperEffectSlot`, `Colors`, display labels, ...).
- **Aliases**: if functions with the same name from several clients are used in one file, they are imported as `<CLIENT>_<NAME>`, e.g. `from pyswitch.clients.fractal.actions.tap_tempo import TAP_TEMPO as FRACTAL_TAP_TEMPO`, and the calls use the alias. A client whose function is already imported **without** alias keeps the plain name (existing code stays as it is). When only one client is left, the alias is removed again.
- **Reading**: an alias is resolved to the real name and the client of its import (the tree data always contains the real name, e.g. `name = "TAP_TEMPO"`, `client = "fractal"`). The client of an import is determined from the module path `pyswitch.clients.<client>[...]`.
- **Code strings** (values set as code, e.g. mappings selected in the UI, and all argument values the UI reads via `Parser.codeForNode()`): functions which exist in several clients are written with the **qualified name** `<CLIENT>_<NAME>` (same as the alias), e.g. `"FRACTAL_MAPPING_TEMPO_BPM()"`, so the client is not lost when the UI sets the actions again. When writing, qualified names count as calls of that client (import plan) and are replaced by the planned name (plain or alias). Client functions with a plain name which are used but not imported are imported from the clients used by the calls of the file first, then from `local`, then from the first client defining the name.
- Updating a configuration without changes never changes the client of an action (before, the order of the clients in the definitions decided).


## Implementation

| File (`web/htdocs/...`) | Content |
|---|---|
| `python/parser/misc/ClientImports.py` (new) | `plan()`: binding names (plain or alias) for all `(name, client)` calls of a file. `apply()`: replaces qualified names by the planned names, removes imports binding these names to something else, adds the missing imports, imports unresolved client functions (code strings). `code_string_name()`, `qualified_calls()`: qualified names in code strings. |
| `python/parser/PySwitchParser.py` | `set_inputs()`/`set_splashes()` create the plan from the tree data (including qualified names in code strings) and pass it to the `CodeGenerator`; `to_source()` applies it (`_apply_client_imports()`) before the name based imports of all other names (which no longer contain the client functions). Without set trees, the plan is created from the current code. `resolve_name()` returns `(real name, client)`. `code_for_data_node()` writes qualified names. |
| `python/parser/misc/CodeGenerator.py` | Optional `names(name, client)` callback for the name written for a call. |
| `python/parser/misc/ImportExtractor.py` | Also returns the real name and the module of the import. |
| `python/parser/InputsExtractor.py`, `SplashesExtractor.py` | Resolve aliases (`resolve_name()`). |
| `js/model/parser/ParserInput.js` | `setActions()` passes the `client` of the actions to the parser (was dropped before). |
| `js/PySwitchRunner.js` | Loads `ClientImports.py`. |

The UI side (action dialog, mapping selects with qualified names): [multi_client.md](multi_client.md).


## Tests

`test/spec/parser/ClientImportsTests.js` (spec "Client Imports"): single client, two clients with aliases (write and read), existing plain import keeps its name, changing the client of an action, removing an alias, unchanged configuration keeps the clients, code strings, qualified names in code strings (one and two clients), unchanged code strings keep their clients, mapping options, PySwitch run with same-named actions of two clients. The parser test "Auto-add imports (all actions)" puts the actions of all clients into one input and runs PySwitch with them.
