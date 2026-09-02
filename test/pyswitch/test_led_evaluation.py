import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "gc": MockGC()
}):
    from lib.pyswitch.controller.controller import Controller
    from .mocks_appl import *


class TestLedEvaluation(unittest.TestCase):

    #################################################################################################

    # Minimal call: Must not throw anything
    def test_no_switches(self):
        led_driver = MockNeoPixelDriver()

        appl = Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
        )

        self.assertEqual(len(led_driver.leds), 0)
        self.assertEqual(len(appl.inputs), 0)
        
    #################################################################################################

    def test_1_switch(self):
        led_driver = MockNeoPixelDriver()
        switch_1 = MockSwitch()

        Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": (0, 1, 2, 3, 8)
                    }
                },
                MockInputControllerDefinition()
            ]
        )

        self.assertEqual(len(led_driver.leds), 9)

    #################################################################################################

    def test_2_switches(self):
        led_driver = MockNeoPixelDriver()
        switch_1 = MockSwitch()
        switch_2 = MockSwitch()
        switch_3 = MockSwitch()

        Controller(
            led_driver = led_driver,
            midi = MockMidiController(),
            inputs = [
                {
                    "assignment": {
                        "model": switch_1,
                        "pixels": (0, 1, 2, 3, 8)
                    }
                },
                {
                    "assignment": {
                        "model": switch_2
                    }
                },
                MockInputControllerDefinition(),
                {
                    "assignment": {
                        "model": switch_3,
                        "pixels": (111, 2, 3)
                    }
                }
            ]
        )

        self.assertEqual(len(led_driver.leds), 112)
