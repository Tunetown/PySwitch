import time as _time
import board as _board
import digitalio as _digitalio

# No switch pushed -> PySwitch
# Switch 2 pushed -> original FW

_switch2 = _digitalio.DigitalInOut(_board.GP25)
_switch2.direction = _digitalio.Direction.INPUT
_switch2.pull = _digitalio.Pull.UP

_time.sleep(0.05)

_firmware_id = 1
 
# Evaluate switches
if _switch2.value is False:
    _firmware_id = 2

# Clean up
_switch2.deinit()
del _switch2

# Load firmware according to the current ID
if _firmware_id == 2:
    import midicaptain
else:
    # PySwitch (default)
    import  lib.pyswitch.process
