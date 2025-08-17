import sys
from unittest.mock import patch
import traceback

from pyodide.ffi.wrappers import set_timeout
from js import externalRefs

from mocks import *
from wrappers.WrapDisplayDriver import *
from wrappers.wrap_io import *
from wrappers.wrap_adafruit_display import *
from wrappers.wrap_adafruit_led import *
from wrappers.wrap_adafruit_midi import *
from wrappers.wrap_time import *
from wrappers.wrap_hid import *

from lib.pyswitch.misc import get_option

class PySwitchRunner:
    def __init__(self, container_id, dom_namespace, coverage, tickInterval = 10):
        self.container_id = container_id

        self.dom_namespace = dom_namespace
        self.coverage = coverage

        self.running = False
        self.triggerStop = False

        self.protocol = None
        self.frontend = None
        self.tickInterval = tickInterval

    # Set up a PySwitch controller and let it run
    def run(self, display_width, display_height, client, config_py, comm_settings):
        self.running = True
        self.triggerStop = False

        self.init(display_width, display_height, client, config_py, comm_settings)

    def init(self, display_width, display_height, client, config_py, comm_settings):
        config_py = config_py.to_py()

        if self.coverage:
            import coverage

            cov = coverage.Coverage()
            cov.start()

        if get_option(config_py, "exploreMode", False):
            self._init_explore_mode(display_width, display_height)
        else:
            self._init_default(display_width, display_height, client, config_py, comm_settings)

        # Local callback for set_timeout
        def tick():            
            if not self.triggerStop:
                set_timeout(tick, self.tickInterval)

                self.tick()
            else:
                self.running = False

        if self.running:
            tick()

        if self.coverage:
            cov.stop()
            cov.save()
            # print(cov.get_data())

    def _init_default(self, display_width, display_height, client, config_py, comm_settings):
        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC(),
            "board": WrapBoard,
            "displayio": WrapDisplayIO(),
            "adafruit_display_text": WrapAdafruitDisplayText(self.dom_namespace),
            "adafruit_display_shapes.rect": WrapDisplayShapes().rect(),
            "busio": MockBusIO(),
            "adafruit_misc.adafruit_st7789": MockAdafruit_ST7789,
            "adafruit_misc.neopixel": MockNeoPixel,
            "adafruit_bitmap_font": MockAdafruitBitmapFont,
            "fontio": MockFontIO(),
            "digitalio": WrapDigitalIO(self.dom_namespace),
            "analogio": WrapAnalogIO(self.dom_namespace),
            "rotaryio": WrapRotaryIO(self.dom_namespace),
            "time": WrapTime(),
            "usb_hid": WrapUsbHid(),
            "adafruit_hid.keyboard": WrapUsbHidKeyboard
        }):
            self.display_driver = WrapDisplayDriver(
                width = display_width,
                height = display_height,
                dom_namespace = self.dom_namespace
            )
            self.display_driver.init()

            from lib.pyswitch.controller.controller import Controller
            from lib.pyswitch.controller.midi import MidiController, MidiRouting
            from lib.pyswitch.ui.UiController import UiController
            from lib.pyswitch.hardware.adafruit.AdafruitUsbMidiDevice import AdafruitUsbMidiDevice

            # from lib.pyswitch.clients.kemper import KemperBidirectionalProtocol

            from display import Splashes
            from inputs import Inputs

            midi_in = WrapMidiInput()
            midi_out = WrapMidiOutput()

            in_channel = comm_settings.inChannel if hasattr(comm_settings, "inChannel") else None
            out_channel = comm_settings.outChannel if hasattr(comm_settings, "outChannel") else 0

            if hasattr(comm_settings, "debug") and comm_settings.debug:
                print(f"Connecting to MIDI (Input channel(s): { in_channel if in_channel != None else "All" }, Output channel: { out_channel })")

            midi = AdafruitUsbMidiDevice(
                port_in = midi_in,
                port_out = midi_out,
                in_buf_size = 100,
                in_channel = in_channel,
                out_channel = out_channel,
            )

            protocol_generator_code = client.getProtocolCode()
            if protocol_generator_code:
                exec(protocol_generator_code)
                
                if not self.protocol:
                    raise Exception("Protocol has not been generated")

            # Controller instance (runs the processing loop and keeps everything together)
            self.controller = Controller(
                led_driver = WrapNeoPixelDriver(self.dom_namespace), 
                protocol = self.protocol,
                midi = MidiController(
                    routings = {
                        # Application: Receive MIDI messages from USB
                        MidiRouting(
                            source = midi,
                            target = MidiRouting.APPLICATION
                        ),

                        # Application: Send MIDI messages to USB
                        MidiRouting(
                            source = MidiRouting.APPLICATION,
                            target = midi
                        ),
                    }
                ),
                config = config_py,
                inputs = Inputs,
                ui = UiController(
                    display_driver = self.display_driver,
                    font_loader = WrapFontLoader(),
                    splash_callback = Splashes
                )
            )

            # Prepare to run the processing loop
            self.controller.init()

    def _init_explore_mode(self, display_width, display_height):
        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC(),
            "board": WrapBoard,
            "displayio": WrapDisplayIO(),
            "adafruit_display_text": WrapAdafruitDisplayText(self.dom_namespace),
            "adafruit_display_shapes.rect": WrapDisplayShapes().rect(),
            "busio": MockBusIO(),
            "adafruit_misc.adafruit_st7789": MockAdafruit_ST7789,
            "adafruit_misc.neopixel": MockNeoPixel,
            "adafruit_bitmap_font": MockAdafruitBitmapFont,
            "fontio": MockFontIO(),
            "digitalio": WrapDigitalIO(self.dom_namespace),
            "time": WrapTime()
        }):
            self.display_driver = WrapDisplayDriver(
                width = display_width,
                height = display_height,
                dom_namespace = self.dom_namespace
            )
            self.display_driver.init()

            from lib.pyswitch.controller.explore import ExploreModeController
            from lib.pyswitch.ui.UiController import UiController
            from lib.pyswitch.hardware.adafruit.AdafruitSwitch import AdafruitSwitch
            
            import board as _board

            # Switch factory
            class _SwitchFactory:
                def create_switch(self, port):
                    return AdafruitSwitch(port)

            self.controller = ExploreModeController(
                board = _board, 
                switch_factory = _SwitchFactory(), 
                led_driver = WrapNeoPixelDriver(self.dom_namespace),
                ui = UiController(
                    display_driver = self.display_driver,
                    font_loader = WrapFontLoader(),
                )
            )

            # Prepare to run the processing loop
            self.controller.init()

    # One tick of the controller
    def tick(self):
        try:
            self.controller.tick()
        
        except Exception as exc:
            self.stop()

            if hasattr(externalRefs, "errorHandler"):
                externalRefs.errorHandler.handle("".join(traceback.format_exception(exc)))
            
            raise exc
        
        self.display_driver.update()

        if self.protocol:
            externalRefs.protocolState = self.protocol.state
        else:
            externalRefs.protocolState = -10   # No protocol

    # Stop execution of the set_timeout handler by just not renewing it
    def stop(self):        
        self.triggerStop = True


    

