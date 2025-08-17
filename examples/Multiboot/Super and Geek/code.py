import time as _time
import board as _board
import digitalio as _digitalio

# No switch pushed -> PySwitch
# Switch 2 pushed -> original FW (super mode ?)
# Switch 3 pushed -> original FW (geek mode)

_switch2 = _digitalio.DigitalInOut(_board.GP25)
_switch2.direction = _digitalio.Direction.INPUT
_switch2.pull = _digitalio.Pull.UP

_switch3 = _digitalio.DigitalInOut(_board.GP24)
_switch3.direction = _digitalio.Direction.INPUT
_switch3.pull = _digitalio.Pull.UP

_time.sleep(0.05)

_firmware_id = 1
 
# Evaluate switches
if _switch2.value is False:
    _firmware_id = 2
elif _switch3.value is False:
    _firmware_id = 3

# Clean up
_switch2.deinit()
_switch3.deinit()
del _switch2
del _switch3

# Load firmware according to the current ID
if _firmware_id == 2:
    # Super Mode
    import midicaptain10s

elif _firmware_id == 3:
    # Geek Mode
    import midigeek

else:
    # PySwitch (default)
    import  lib.pyswitch.process
