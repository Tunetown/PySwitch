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
    from lib.pyswitch.controller.inputs import SwitchController, ContinuousController
    from .mocks_appl import *


class TestControllerActions(unittest.TestCase):

    def test_switches_and_inputs(self):
        switch_1 = MockSwitch()
        switch_2 = MockSwitch()

        pot_3 = MockPotentiometer()
        pot_4 = MockPotentiometer()
        
        action_1 = MockAction()
        action_2 = MockAction()
        action_3 = MockAnalogAction()
        action_4 = MockEncoderAction()

        period = MockPeriodCounter()

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
                },
                {
                    "assignment": {
                        "model": switch_2
                    },
                    "actions": [
                        action_2
                    ]
                },
                {
                    "assignment": {
                        "model": pot_3
                    },
                    "actions": [
                        action_3
                    ]
                },
                {
                    "assignment": {
                        "model": pot_4
                    },
                    "actions": [
                        action_4
                    ]
                }
            ],
            period_counter = period
        )

        appl.init()

        period.exceed_next_time = True
        
        switch_ctrl_1 = appl.inputs[0]
        switch_ctrl_2 = appl.inputs[1]
        input_ctrl_3 = appl.inputs[2]
        input_ctrl_4 = appl.inputs[3]

        self.assertIsInstance(switch_ctrl_1, SwitchController)
        self.assertIsInstance(switch_ctrl_2, SwitchController)
        self.assertIsInstance(input_ctrl_3, ContinuousController)
        self.assertIsInstance(input_ctrl_4, ContinuousController)


    def test_update_period(self):
        switch_1 = MockSwitch()
        switch_2 = MockSwitch()
        
        action_1 = MockAction()
        action_2 = MockAction()
        action_3 = MockAction()

        period = MockPeriodCounter()

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
                },
                MockInputControllerDefinition(),
                {
                    "assignment": {
                        "model": switch_2
                    },
                    "actions": [
                        action_2,
                        action_3
                    ]
                }
            ],
            period_counter = period
        )

        appl.init()

        # Build scene:
        # Step 1: Not exceeded
        self.assertEqual(period.exceed_next_time, False)
        self.assertEqual(action_1.num_update_calls_overall, 0)
        self.assertEqual(action_2.num_update_calls_overall, 0)
        self.assertEqual(action_3.num_update_calls_overall, 0)

        appl.tick()
        appl.tick()
        
        self.assertEqual(period.exceed_next_time, False)
        self.assertEqual(action_1.num_update_calls_overall, 0)
        self.assertEqual(action_2.num_update_calls_overall, 0)
        self.assertEqual(action_3.num_update_calls_overall, 0)
        
        # Step 2: Exceeded the first time
        period.exceed_next_time = True
        self.assertEqual(action_1.num_update_calls_overall, 0)
        self.assertEqual(action_2.num_update_calls_overall, 0)
        self.assertEqual(action_3.num_update_calls_overall, 0)

        appl.tick()
        appl.tick()
        
        self.assertEqual(period.exceed_next_time, False)
        self.assertEqual(action_1.num_update_calls_overall, 1)
        self.assertEqual(action_2.num_update_calls_overall, 1)
        self.assertEqual(action_3.num_update_calls_overall, 1)
        
        # Step 3: Not exceeded
        self.assertEqual(period.exceed_next_time, False)
        self.assertEqual(action_1.num_update_calls_overall, 1)
        self.assertEqual(action_2.num_update_calls_overall, 1)
        self.assertEqual(action_3.num_update_calls_overall, 1)

        appl.tick()
        appl.tick()
        
        self.assertEqual(period.exceed_next_time, False)
        self.assertEqual(action_1.num_update_calls_overall, 1)
        self.assertEqual(action_2.num_update_calls_overall, 1)
        self.assertEqual(action_3.num_update_calls_overall, 1)
        
        # Step 4: Exceeded again
        period.exceed_next_time = True
        self.assertEqual(action_1.num_update_calls_overall, 1)
        self.assertEqual(action_2.num_update_calls_overall, 1)
        self.assertEqual(action_3.num_update_calls_overall, 1)

        appl.tick()
        appl.tick()
        
        self.assertEqual(period.exceed_next_time, False)
        self.assertEqual(action_1.num_update_calls_overall, 2)
        self.assertEqual(action_2.num_update_calls_overall, 2)
        self.assertEqual(action_3.num_update_calls_overall, 2)
        
    def test_reset_actions(self):
        switch_1 = MockSwitch()
        switch_2 = MockSwitch()
        
        action_1 = MockAction()
        action_2 = MockAction()
        action_3 = MockAction()

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
                },
                MockInputControllerDefinition(),
                {
                    "assignment": {
                        "model": switch_2
                    },
                    "actions": [
                        action_2,
                        action_3
                    ]
                }
            ]
        )

        appl.init()

        appl.reset_actions()

        self.assertEqual(action_1.num_reset_calls, 1)
        self.assertEqual(action_2.num_reset_calls, 1)
        self.assertEqual(action_3.num_reset_calls, 1)

        appl.reset_actions()

        self.assertEqual(action_1.num_reset_calls, 2)
        self.assertEqual(action_2.num_reset_calls, 2)
        self.assertEqual(action_3.num_reset_calls, 2)