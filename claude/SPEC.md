# PySwitch Fractal Audio Client – Specification

Status: **Spec phase.** No code is generated until the Go is given (section 11). Open points: [TBC.md](TBC.md).


## 1. Goal

Extend PySwitch (https://github.com/Tunetown/PySwitch, branch `dev_midi`) to support Fractal Audio devices:

| Device                     | Priority       | Alpha        |
|----------------------------|----------------|--------------|
| FM3                        | most important | yes          |
| FM9                        | high           | yes          |
| Axe-Fx III (Mk I/II/Turbo) | high           | yes          |
| AM4                        | low            | no (TODO.md) |
| VP4                        | low            | no (TODO.md) |

When it runs well in the emulator, it is published as an **alpha** for forum members who own Fractal devices.


## 2. Deliverables

1. **Virtual Fractal client** in the emulator, built FIRST (no real device available): [spec/emulator/virtual_client.md](spec/emulator/virtual_client.md).
2. **Python client** `content/lib/pyswitch/clients/fractal/`: [spec/python/architecture.md](spec/python/architecture.md), features in [spec/python/features/](spec/python/features/).
3. **Python unit tests**: [spec/tests.md](spec/tests.md).
4. **Emulator integration, definitions, Jasmine tests**: [spec/emulator/integration.md](spec/emulator/integration.md).
5. **Examples**: [spec/examples.md](spec/examples.md).
6. **Version and changelog**: PySwitch 2.4.11 (`content/lib/pyswitch/misc.py`, `PYSWITCH_VERSION` in `web/htdocs/js/Controller.js`), emulator 2.4.11.18 (`VERSION` suffix `.18` in `Controller.js`), new entry in `CHANGELOG.md` in the existing format.

### Constraints
- **No changes to the core library or other clients.** Local mappings/actions may be added, never changed. Approved exceptions are listed in the deliverable specs; every change to a file that exists on `dev_midi` is logged in [LIB_CHANGES.md](LIB_CHANGES.md) (file, class and method, description).
- `README.md` is not touched (done last, together with the user).
- **RAM**: the controllers have ~200 kB usable RAM. Memory efficiency has priority. Follow the existing PySwitch principles (section 9), not generic internet advice.
- Not in the alpha: AM4/VP4, Fractal convenience mappings for expression pedals (the generic CC mappings already work), the editor protocol, blocks with unknown IDs.


## 3. Working environment

- Project folder: WebDAV mount `.../git/PySwitch Fractal`. It contains the working tree of `dev_midi` at commit `955fdd0` without `.git` (771 files, checksums verified). **No git is used for now**; the user manages version control.
- Python tests: the existing suite (427 tests) passes on `dev_midi` (run in a local copy because the host Python has a stdlib `test` package; in the project's Docker setup `test/run` works as-is).


## 4. Documents

All Claude-related files are in `claude/`:

| File                                                     | Content                                              |
|----------------------------------------------------------|------------------------------------------------------|
| `SPEC.md`                                                | this file: goal, rules, architecture principles, conventions, status |
| `TBC.md`                                                 | open points and the user's wishes                    |
| `TODO.md`                                                | long-term TODOs (after the alpha)                    |
| `LIB_CHANGES.md`                                         | log of all changes to files existing on `dev_midi`   |
| `FRACTAL.md`                                             | Fractal devices, MIDI features, protocol reference   |
| `FRACTAL_ANALYSIS.md`                                    | communication model, comparison with Kemper          |
| `spec/python/architecture.md`                            | Python client architecture                           |
| `spec/python/features/*.md`                              | presets, scenes, effects, tuner, tempo, looper       |
| `spec/emulator/virtual_client.md`, `integration.md`      | virtual client, emulator integration, Jasmine tests  |
| `spec/examples.md`, `spec/tests.md`                      | examples, Python tests                               |
| `fractal_spec/`                                          | downloaded reference documents (FRACTAL.md 6)        |


## 5. Architecture principles

### 5.1 General rule for mappings
A mapping describes everything about one value:
- **Request message** → the value is polled (requested in every update interval by the callbacks using it).
- **Response message** → incoming values are received and parsed. A mapping with a response but no request receives passively (push data, or a value contained in another mapping's answer).
- **Set message** → the value can be set from PySwitch.

A protocol class is only used when the device has a real bidirectional protocol (like Kemper). Fractal has none ([FRACTAL_ANALYSIS.md](FRACTAL_ANALYSIS.md)), so the Fractal client uses the plain `Client` and mappings only.

### 5.2 Timing
There is no own poll interval: polling happens with the general `updateInterval` of `config.py` (CPU is limited too).

### 5.3 Transport
The controller connects to the Fractal device via DIN MIDI ([spec/python/architecture.md 4](spec/python/architecture.md)).


## 6. Feature scope (alpha)

| Topic   | Spec                                                                  |
|---------|-----------------------------------------------------------------------|
| Presets | [features/presets.md](spec/python/features/presets.md)                |
| Scenes  | [features/scenes.md](spec/python/features/scenes.md)                  |
| Effects | [features/effects.md](spec/python/features/effects.md)                |
| Tuner   | [features/tuner.md](spec/python/features/tuner.md)                    |
| Tempo   | [features/tempo.md](spec/python/features/tempo.md)                    |
| Looper  | [features/looper.md](spec/python/features/looper.md)                  |


## 7. Emulator
See [spec/emulator/](spec/emulator/).


## 8. Prior art
`nilkis/midicaptain_for_fm3` (MIT) is used as a behaviour reference only; no code is taken over (FRACTAL.md 5).


## 9. Code conventions (extracted from the existing code)

### Python
1. 4 spaces indentation. Spaces around `=` in keyword arguments **and** defaults: `def FOO(display = None, id = False)`, `foo(slot_id = slot_id)`.
2. f-strings with spaces inside braces: `f"Slot State { name } ({channel})"`.
3. No docstrings. A `#` comment line above every function/class; parameter documentation as aligned trailing comments in the signature.
4. Section separators: long `####...####` lines between classes/sections.
5. Action factories are UPPER_SNAKE_CASE functions returning `Action`/`PushButtonAction` (e.g. `EFFECT_STATE(...)`). Mapping factories are `MAPPING_XXX()` functions or static UPPER_SNAKE methods of a `<Client>Mappings` class. Mappings are created via `get(name = ...)` (singletons, unique names including all parameters).
6. Callback classes: `<Client>XxxCallback`; module-private ones prefixed `_`. Private members `self.__x`, protected `self._x`.
7. Constants via `micropython.const()`; numeric enums as `const` class attributes; parallel tuples for names/colors indexed by the enum (order must match).
8. Standard action parameters, in this order after the specific ones: `display`, `midi_channel = 1` (range 1..16, converted internally to `channel = midi_channel - 1`), `mode`, `id`, `use_leds`, `enable_callback`, then `color`/`text` and their callbacks.
9. Relative imports inside `lib/pyswitch` (`from ....controller.actions import Action`). Optional heavy modules are imported lazily inside the branch that needs them (e.g. strobe controller).
10. MIDI bytes as lowercase hex (`0xf0`); messages as tuples.
11. Exceptions: errors that are likely to happen (typically wrong parameters in the user's configuration) are raised with a short message text, e.g. `raise Exception("Invalid scene: 9")`. Errors that are very unlikely (internal misuse) are raised as `raise Exception()` without text, with the reason as a trailing comment (saves RAM).
12. Debug-only code is marked `# pragma: no cover`. `do_print()` is only used where it already exists; new code adds no debug output.
13. Keep the call stack short: inline small base-class logic where it is called in hot paths (comment it as such).
14. Memory: no large dicts/tables of strings; compute where possible; no per-instance data that could be shared; precompute message bytes at construction.

### Python tests
15. One `TestXxx(unittest.TestCase)` per file/topic; imports inside `with patch.dict(sys.modules, {...})` using the mocks from `mocks_lib`/`mocks_appl`/`mocks_callback`; private members checked via name mangling (`action._PushButtonAction__mode`).

### JavaScript (emulator)
16. ES classes, private members `#x`, a `/** ... */` comment on every method, 4 spaces, `const that = this` in closures, jQuery for DOM, `try { ... } catch (e) { console.error(e); }` in UI and MIDI callbacks.
17. One class per file; client files under `clients/<client>/`, virtual client under `clients/<client>/virtual/`; every new file is registered in `index.html` and `test/index.html`.


## 10. Collaboration rules

- SPEC.md and the files it references are the only valid spec. On every change request they are updated and outdated content is removed.
- **Single source of truth**: every piece of information exists in one place only; other places link to it.
- All open points are in `TBC.md`; the user answers there and adds wishes there. On "reprocess", answered items are moved into the spec and removed from TBC.md.
- Long-term TODOs go to `TODO.md`.
- Chat answers only give a short overview of what changed where; all real information is in the files.


## 11. TODO (current phase)

1. ~~Check out `dev_midi` into this folder~~ – done (section 3).
2. ~~Analyse PySwitch and the Fractal MIDI specs~~ – done (FRACTAL.md, FRACTAL_ANALYSIS.md).
3. Iterate the spec with `TBC.md` until TBC.md is empty – **in progress**.
4. Wait for the Go, then: virtual client → Python client → unit tests → examples, meta.json → user runs the Jasmine tests to regenerate the definitions.
