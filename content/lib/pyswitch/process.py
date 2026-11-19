#################################################################################################################################
# 
# Custom Firmware for CircuitPy based devices such as the PaintAudio MIDICaptain series, to control devices like 
# the Kemper Profiler Player, including display of Rig Name, Effect type feedback etc. which is not implemented by the PaintAudio 
# Kemper firmware (yet). The firmware has been created for Kemper devices but can easily be adapted to others (all Kemper
# specific definitions and code is located in the files beneath this one, the src folder is generic)
#
#################################################################################################################################


# Uncomment these two lines to enable memory monitoring
# from pyswitch.stats import Memory as _Memory
# _Memory.start()

from pyswitch.hardware.adafruit import AdafruitST7789DisplayDriver as _DisplayDriver, AdafruitNeoPixelDriver as _NeoPixelDriver, AdafruitFontLoader as _FontLoader
from pyswitch.misc import get_option as _get_option

# Initialize Display first to get console output on setup/config errors (for users who do not connect to the serial console)
_display_driver = _DisplayDriver()
_display_driver.init()

# Load global config
from config import Config as _Config

if not _get_option(_Config, "exploreMode"):
    # Normal operation
    from pyswitch.controller.controller import Controller as _Controller
    from pyswitch.controller.midi import MidiController as _MidiController
    from pyswitch.ui.UiController import UiController as _UiController

    # Load communication configuration
    from communication import Communication as _Communication  

    # Optional Wrapper to include the PyMidiBridge for transfering files.
    # Disable this to save memory.
    if _get_option(_Config, "enableMidiBridge"):
        from pymidibridge.MidiBridgeWrapper import MidiBridgeWrapper as _MidiBridgeWrapper

        _midi = _MidiBridgeWrapper(
            midi = _MidiController(
                routings = _Communication["midi"]["routings"]
            ),
            temp_file_path = '/.bridge_tmp'
        )
    else:
        _midi = _MidiController(
            routings = _Communication["midi"]["routings"]
        )

    try:
        # Load configuration files
        from display import Splashes as _Splashes
        from inputs import Inputs as _Inputs

        # Controller instance (runs the processing loop and keeps everything together)
        _controller = _Controller(
            led_driver = _NeoPixelDriver(), 
            protocol = _get_option(_Communication, "protocol", None),
            midi = _midi,
            config = _Config, 
            inputs = _Inputs,
            ui = _UiController(
                display_driver = _display_driver,
                font_loader = _FontLoader(),
                splash_callback = _Splashes
            )
        )

        # Prepare to run the processing loop
        _controller.init()

        # Start processing loop (done here to keep the call stack short)
        while _controller.tick():
            pass

    except Exception as e:
        if _get_option(_Config, "enableMidiBridge"):
            _midi.error(e)
        else:
            raise e

else:
    # Explore mode: Just shows the pressed GPIO port. This can be used to determine switch assignment 
    # on unknown devices, to create layouts for the configuration.
    from pyswitch.controller.explore import ExploreModeController as _ExploreModeController
    from pyswitch.ui.UiController import UiController as _UiController
    from pyswitch.hardware.adafruit.AdafruitSwitch import AdafruitSwitch as _Switch
    
    import board as _board

    # Switch factory
    class _SwitchFactory:
        def create_switch(self, port):
            return _Switch(port)

    _controller = _ExploreModeController(
        board = _board, 
        switch_factory = _SwitchFactory(), 
        led_driver = _NeoPixelDriver(), 
        ui = _UiController(
            display_driver = _display_driver,
            font_loader = _FontLoader()
        )
    )

    # Prepare to run the processing loop
    _controller.init()

    # Start processing loop (done here to keep the call stack short)
    while _controller.tick():
        pass

    
