# Tests

## Python
- `test/pyswitch/test_fractal_*.py`, unittest, same structure as the Kemper tests (mocks via `patch.dict(sys.modules, ...)`, imports from `lib.pyswitch...`), conventions: [SPEC.md 9](../SPEC.md).
- Covered: every mapping (message bytes, checksums, parsing incl. push messages without checksum and NAK answers, target name queries vs. current preset), every action and callback (FC LED states off/dim/bright, colors, labels, 2nd press, toggle, inc/dec, local feedback, timeouts, absent blocks), client settings incl. model byte patching.
- Files (133 tests):

  | File                                  | Content                                                                 |
  |---------------------------------------|-------------------------------------------------------------------------|
  | `mocks_fractal.py`                    | `MockFractalClient` (adds `get_matching_request()`), `reset_fractal()` (shared state and mapping values, run in every `setUp()`), message builders, `setup_action()` |
  | `test_fractal_mappings.py`            | helpers, `FractalState`, all mappings (messages, checksums, parsing, set values, feedback, model patching, target names, tuner, beat) |
  | `test_fractal_actions_preset.py`      | preset and bank actions                                                 |
  | `test_fractal_actions_scene.py`       | scene actions                                                           |
  | `test_fractal_actions_effects.py`     | effect bypass and channel actions                                       |
  | `test_fractal_actions_utility.py`     | tuner, tap tempo, looper, encoders                                      |
  | `test_fractal_callbacks.py`           | name/tempo display callbacks, `FractalCallback`, `TunerDisplayCallback` |

- Every executable line of the Fractal package is run by these tests (line coverage; checked with the stdlib `trace` module, as `coverage` was not available locally).
- The existing 427 tests must keep passing (560 in total).
- Local run without Docker: a folder with the symlinks `lib` → `content/lib` and `tst` → `test` (not `test`, which collides with the stdlib package), then `python3 -m unittest discover -t <folder> -s <folder>/tst/pyswitch` with `PYTHONDONTWRITEBYTECODE=1`.

## Jasmine (emulator)
See [emulator/integration.md](emulator/integration.md). The user runs them.
