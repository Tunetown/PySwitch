# Tests

## Python
- `test/pyswitch/test_fractal_*.py`, unittest, same structure as the Kemper tests (mocks via `patch.dict(sys.modules, ...)`, imports from `lib.pyswitch...`), conventions: [SPEC.md 9](../SPEC.md).
- Covered: every mapping (message bytes, checksums, parsing incl. push messages without checksum and NAK answers, target name queries vs. current preset), every action and callback (FC LED states off/dim/bright, colors, labels, 2nd press, toggle, inc/dec, local feedback, timeouts, absent blocks), client settings incl. model byte patching.
- A Fractal mock helper may be added to the test folder if needed.
- The existing 427 tests must keep passing.

## Jasmine (emulator)
See [emulator/integration.md](emulator/integration.md). The user runs them.
