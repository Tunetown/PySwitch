# PySwitch build report

Built 2026-11-25 17:20 by `build`.

## Sources

| Item             | Value                                                       |
|------------------|-------------------------------------------------------------|
| Origin           | fetched from https://github.com/Tunetown/PySwitch.git       |
| Branch           | main                                                        |
| Commit           | 955fdd0                                                     |
| PySwitch version | 2.4.10                                                      |
| Firmware         | CircuitPython 7.3.1 (raspberry_pi_pico) with frozen modules |

## Unit tests

OK, 427 tests, coverage 98%

Coverage report: [test_report/index.html](test_report/index.html)

## Firmware

| Item       | Value                        |
|------------|------------------------------|
| File       | `PySwitch.uf2`               |
| Flash used | 939372 B of 1044480 B (89 %) |
| Flash free | 105108 B                     |

## Frozen modules

PySwitch and every library of `content/lib` it imports; libraries from their sources in the versions of the `.mpy` files. Details: `logs/frozen_modules.json`.

| Package                   | Files | Source                                                                                                                                                                             |
|---------------------------|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `adafruit_bitmap_font`    | 6     | content/lib/adafruit_bitmap_font/__init__.py, https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font.git 1.5.11                                                            |
| `adafruit_display_shapes` | 8     | content/lib/adafruit_display_shapes/__init__.py, https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes.git 2.5.6                                                       |
| `adafruit_display_text`   | 4     | https://github.com/adafruit/Adafruit_CircuitPython_Display_Text.git 2.22.12                                                                                                        |
| `adafruit_hid`            | 8     | https://github.com/adafruit/Adafruit_CircuitPython_HID.git 5.3.3                                                                                                                   |
| `adafruit_misc`           | 3     | content/lib/adafruit_misc/__init__.py, https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel.git 6.3.6, https://github.com/adafruit/Adafruit_CircuitPython_ST7789.git 1.5.14 |
| `pymidibridge`            | 4     | content/lib/pymidibridge/__init__.py, https://github.com/Tunetown/PyMidiBridge.git 0.6.0 (default branch (tag 0.6.0 not found))                                                    |
| `pyswitch`                | all   | content/lib/pyswitch                                                                                                                                                               |

## Drive files (`drive/`)

Copy to the device drive (MIDI Captain: `MIDICAPTAIN`, other boards: `CIRCUITPY`):

- `boot.py`
- `code.py`
- `communication.py`
- `config.py`
- `display.py`
- `fonts/`
- `inputs.py`
- `lib/`
- `lib/functools.py`

## RAM measurement

Not measured (switched on with `./build --measure`; needs the memory monitoring lines in `lib/pyswitch/process.py`).
