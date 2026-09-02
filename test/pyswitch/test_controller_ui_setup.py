import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "usb_midi": MockUsbMidi(),
    "gc": MockGC()
}):
    from .mocks_misc import MockMisc

    with patch.dict(sys.modules, {
        "lib.pyswitch.misc": MockMisc
    }):
       
        from lib.pyswitch.ui.ui import DisplayElement
        from lib.pyswitch.ui.UiController import UiController
        from lib.pyswitch.controller.controller import Controller

        from gc import gc_mock_data
        from .mocks_appl import *
        from .mocks_ui import MockDisplayDriver, MockFontLoader, MockUpdateableDisplayElement
        from .mocks_callback import MockSplashCallback


class MockUiController(UiController):
    def __init__(self, 
                 display_driver = MockDisplayDriver(init = True), 
                 font_loader = MockFontLoader(), 
                 splash_callback = None
        ):
        super().__init__(display_driver, font_loader, splash_callback)

        self.num_show_calls = 0

    def show(self):
        super().show()

        self.num_show_calls += 1


class TestControllerUiSetup(unittest.TestCase):

    def test_setup(self):
        switch_1 = MockSwitch()        
        action_1 = MockAction()
        period = MockPeriodCounter()

        element_1 = DisplayElement(id = 1)
        element_2 = DisplayElement(id = 2)
        element_3 = MockUpdateableDisplayElement(id = 3)

        ui = MockUiController(
            splash_callback = MockSplashCallback(
                output = DisplayElement(
                    children = [
                        element_1,
                        element_2,
                        element_3
                    ]
                )
            )
        )

        appl = Controller(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1
                    },
                    "actions": [
                        action_1                        
                    ]
                }
            ],
            period_counter = period,
            ui = ui
        )

        appl.init()

        # Build scene
        period.exceed_next_time = True      
        
        appl.tick()
        appl.tick()

        self.assertEqual(element_3.num_update_calls, 1)
        
        self.assertEqual(ui.num_show_calls, 1)


    def test_low_mem_warning_above(self):
        gc_mock_data().reset()
        gc_mock_data().output_mem_free_override(20)

        appl = Controller(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            config = {
                "memoryWarnLimitBytes": 1024
            }
        )

        appl.init()        
        appl.tick()
        
        self.assertEqual(appl.low_memory_warning, True)


    def test_low_mem_warning_below(self):
        gc_mock_data().reset()
        gc_mock_data().output_mem_free_override(2048)

        appl = Controller(
            led_driver = MockNeoPixelDriver(),
            midi = MockMidiController(),
            config = {
                "memoryWarnLimitBytes": 1024
            }
        )

        appl.init()
        appl.tick()
        
        self.assertEqual(appl.low_memory_warning, False)

