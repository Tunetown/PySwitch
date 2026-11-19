# Tests

## Python
- `test/pyswitch/test_fractal_*.py`, unittest, same structure as the Kemper tests (mocks via `patch.dict(sys.modules, ...)`, imports from `lib.pyswitch...`), conventions: [SPEC.md 9](../SPEC.md).
- Covered: every mapping (message bytes, checksums, parsing incl. push messages without checksum and NAK answers), every action and callback (states, LEDs, labels, local feedback, timeouts, absent blocks).
- A Fractal mock helper may be added to the test folder if needed.
- The existing 427 tests must keep passing.

## Jasmine (emulator)
See [emulator/integration.md](emulator/integration.md). The user runs them.
