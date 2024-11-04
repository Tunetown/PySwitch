#################################################################################################################################
# 
# Custom Firmware for CircuitPi based devices such as the PaintAudio MIDICaptain series, to control devices like 
# the Kemper Profiler Player, including display of Rig Name, Effect type feedback etc. which is not implemented by the PaintAudio 
# Kemper firmware (yet). The firmware has been created for Kemper devices but can easily be adapted to others (all Kemper
# specific definitions and code is located in the files beneath this one, the src folder is generic)
#
#################################################################################################################################
# 
# v 2.0
# Changes @tunetown (Tom Weber):
# - Complete Rewrite (standalone firmware without dependency on PaintAudio Code, object oriented design etc.)
# - Customization by config script
# - Out-of-the-box Compatibility with PaintAudio MIDICaptain Nano (4 Switches) and Mini (6 Switches),
#   configurable easily for other devices using the new Explore mode (Detect IO addressing for new devices)
# - Activate auto-reload when switch 2 (GP25) is pressed during boot
# - Conditions in switch assignents an display layouts, to make the configuration depending on device 
#   parameters like the rig name
# - ...
#
# -------------------------------------------------------------------------------------------------------------------------------
#
# v 1.2
# Changes @gstrotmann:
# - Detect Rig changes via rig date
# - Change color for Compressor/Noise Gate to turquoise
#
#################################################################################################################################

#from pyswitch.Memory import Memory # type: ignore
#Memory.start(zoom = 10)

from pyswitch.hardware.adafruit import AdafruitST7789DisplayDriver, AdafruitNeoPixelDriver, AdafruitFontLoader, AdafruitSwitch
from pyswitch.ui.UserInterface import UserInterface
from pyswitch.misc import Tools

# Initialize Display first to get console output on setup/config errors (for users who do not connect to the serial console)
display_driver = AdafruitST7789DisplayDriver()
display_driver.init()

# Load global config
from config import Config

# NeoPixel driver 
led_driver = AdafruitNeoPixelDriver()

# Buffered font loader
font_loader = AdafruitFontLoader()

# Create User interface
gui = UserInterface(display_driver, font_loader)

if not Tools.get_option(Config, "exploreMode"):
    # Normal operation
    from pyswitch.controller.Controller import Controller

    # Load configuration files
    from displays import Displays
    from switches import Switches
    from communication import Communication

    # Controller instance (runs the processing loop and keeps everything together)
    appl = Controller(led_driver, Communication, Config, Switches, Displays, gui)
    appl.process()

else:
    # Explore mode: Just shows the pressed GPIO port. This can be used to determine switch assignment 
    # on unknown devices, to create layouts for the configuration.
    from pyswitch.controller.ExploreModeController import ExploreModeController
    import board

    # Switch factory
    class SwitchFactory:
        def create_switch(self, port):
            return AdafruitSwitch(port)

    appl = ExploreModeController(board, SwitchFactory(), led_driver, gui)
    appl.process()
    