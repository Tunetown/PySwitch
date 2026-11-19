import time as _time
import board as _board
import digitalio as _digitalio

# No switch pushed -> Load last
# Switch 2 pushed -> PySwitch
# Switch 3 pushed -> original FW (super mode ?)
# Switch 4 pushed -> original FW (geek mode)

# File the firmware ID is being saved to
_FIRMWARE_FILE = '/boot_fw_id'    

_switch2 = _digitalio.DigitalInOut(_board.GP25)
_switch2.direction = _digitalio.Direction.INPUT
_switch2.pull = _digitalio.Pull.UP

_switch3 = _digitalio.DigitalInOut(_board.GP24)
_switch3.direction = _digitalio.Direction.INPUT
_switch3.pull = _digitalio.Pull.UP

_switch4 = _digitalio.DigitalInOut(_board.GP23)
_switch4.direction = _digitalio.Direction.INPUT
_switch4.pull = _digitalio.Pull.UP

_time.sleep(0.05)

# 1: Initial, when no switch has ever been pushed -> PySwitch
# 2: PySwitch
# 3: Super Mode
# 4: Geek Mode
_firmware_id = 1
 
# Save current FW id
def _save():
    try:
        with open(_FIRMWARE_FILE, 'w') as fp:            
            fp.write(str(_firmware_id))
    except OSError as ex:
        print(ex)

# Evaluate switches
if _switch2.value is False:
    _firmware_id = 2
    _save()
elif _switch3.value is False:
    _firmware_id = 3
    _save()
elif _switch4.value is False:
    _firmware_id = 4
    _save()
else:
    # Try to load FW id
    try:
        if _firmware_id == 1:
            with open(_FIRMWARE_FILE) as fp:
                _firmware_id = int(fp.read())
                del fp    
    except OSError as ex:
        print(ex)

# Clean up
_switch2.deinit()
_switch3.deinit()
_switch4.deinit()
del _switch2
del _switch3
del _switch4

# Load firmware according to the current ID
if _firmware_id == 3:
    # Super Mode
    import midicaptain10s

elif _firmware_id == 4:
    # Geek Mode
    import midigeek

else:
    # PySwitch (default)
    import pyswitch.process
