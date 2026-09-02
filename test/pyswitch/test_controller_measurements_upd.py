import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

class TestControllerMeasurementsUpdate(unittest.TestCase):

    def test_runtime_measurement_tick_time(self):
        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "usb_midi": MockUsbMidi(),
            "gc": MockGC()
        }):
            from .mocks_misc import MockMisc
            from gc import gc_mock_data

            with patch.dict(sys.modules, {
                "lib.pyswitch.misc": MockMisc
            }):
                from .mocks_appl import MockNeoPixelDriver, MockMidiController, MockSwitch, MockAction, MockPeriodCounter
                
                from lib.pyswitch.controller.measure import RuntimeMeasurement
                from lib.pyswitch.controller.controller import Controller

                action_1 = MockAction()
                period = MockPeriodCounter()

                gc_mock_data().reset()
                MockMisc.reset_mock()

                appl = Controller(
                    led_driver = MockNeoPixelDriver(),
                    midi = MockMidiController(),
                    inputs = [
                        {
                            "assignment": {
                                "model": MockSwitch()
                            },
                            "actions": [
                                action_1                        
                            ]
                        }
                    ],
                    period_counter = period,
                    config = {
                        "debugStats": True
                    }
                )

                appl.init()

                m = appl._Controller__measurement_process_jitter
                self.assertIsInstance(m, RuntimeMeasurement)

                gc_mock_data().output_mem_free = 1024 * 566

                # Build scene
                period.exceed_next_time = True
                
                appl.tick()
                appl.tick()
                
                self.assertGreaterEqual(gc_mock_data().collect_calls, 1)
                self.assertIn(MockMisc.format_size(gc_mock_data().output_mem_free), MockMisc.msgs_str)
                