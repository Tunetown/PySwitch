import board

from storage import disable_usb_drive, remount
from digitalio import DigitalInOut, Direction, Pull
from time import sleep
from supervisor import disable_autoreload

############################################################################################

# Initializes a switch. Returns the switch instance.
def _init_switch(pin):
	switch = DigitalInOut(pin) 
	switch.direction = Direction.INPUT
	switch.pull = Pull.UP
	sleep(0.05)
	return switch

# Is a switch pressed? 
def _is_switch_pressed(switch):
	return switch.value == False   # Inverse logic!

############################################################################################
 
# When this switch is pressed during boot, the USB drive will be mounted
_switch_mount_usb = _init_switch(board.GP1)       

############################################################################################

# Disable autoreload
disable_autoreload()

# No USB drive in normal operation, but we need to write on the drive via MIDI bridge.
if not _is_switch_pressed(_switch_mount_usb):	
    disable_usb_drive()
    remount("/", readonly = False)

