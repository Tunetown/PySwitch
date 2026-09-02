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
    from .mocks_misc import MockMisc
    from .mocks_callback import *

    with patch.dict(sys.modules, {
        "lib.pyswitch.misc": MockMisc
    }):
        
        from lib.pyswitch.controller.inputs import ContinuousController
        from .mocks_appl import *


##################################################################################################################################


class TestControllerInput(unittest.TestCase):

    def test_potentiometer(self):
        pot = MockPotentiometer()
        
        action_1 = MockAnalogAction()
        action_2 = MockAnalogAction()

        appl = MockController()

        input = ContinuousController(appl, {
            "assignment": {
                "model": pot,
            },
            "actions": [
                action_1,
                action_2,
            ]
        })

        self.assertEqual(action_1.init_calls, [appl])
        self.assertEqual(action_2.init_calls, [appl])

        pot.output = 100
        input.process()

        self.assertEqual(action_1.process_calls, [100])
        self.assertEqual(action_2.process_calls, [100])

        pot.output = 101
        input.process()

        self.assertEqual(action_1.process_calls, [100, 101])
        self.assertEqual(action_2.process_calls, [100, 101])

        # Disable
        pot.output = 102
        action_1.enabled = False
        input.process()

        self.assertEqual(action_1.process_calls, [100, 101])
        self.assertEqual(action_2.process_calls, [100, 101, 102])

        pot.output = 103
        action_1.enabled = True
        action_2.enabled = False
        input.process()

        self.assertEqual(action_1.process_calls, [100, 101, 103])
        self.assertEqual(action_2.process_calls, [100, 101, 102])

        pot.output = 104
        input.process()

        self.assertEqual(action_1.process_calls, [100, 101, 103, 104])
        self.assertEqual(action_2.process_calls, [100, 101, 102])
        

    def test_encoder(self):
        encoder = MockRotaryEncoder()
        
        action_1 = MockEncoderAction()
        action_2 = MockEncoderAction()

        appl = MockController()

        input = ContinuousController(appl, {
            "assignment": {
                "model": encoder,
            },
            "actions": [
                action_1,
                action_2,
            ]
        })

        self.assertEqual(action_1.init_calls, [appl])
        self.assertEqual(action_2.init_calls, [appl])

        encoder.output = 100
        input.process()

        self.assertEqual(action_1.process_calls, [100])
        self.assertEqual(action_2.process_calls, [100])

        encoder.output = 101
        input.process()

        self.assertEqual(action_1.process_calls, [100, 101])
        self.assertEqual(action_2.process_calls, [100, 101])

        # Disable
        encoder.output = 102
        action_1.enabled = False
        input.process()

        self.assertEqual(action_1.process_calls, [100, 101])
        self.assertEqual(action_2.process_calls, [100, 101, 102])

        encoder.output = 103
        action_1.enabled = True
        action_2.enabled = False
        input.process()

        self.assertEqual(action_1.process_calls, [100, 101, 103])
        self.assertEqual(action_2.process_calls, [100, 101, 102])

        encoder.output = 104
        input.process()

        self.assertEqual(action_1.process_calls, [100, 101, 103, 104])
        self.assertEqual(action_2.process_calls, [100, 101, 102])
        

    def test_actions_deep(self):
        pot = MockPotentiometer()
        
        action_1 = MockAnalogAction()
        action_2 = MockAnalogAction()
        action_3 = MockAnalogAction()
        action_4 = MockAnalogAction()

        appl = MockController()

        input = ContinuousController(appl, {
            "assignment": {
                "model": pot,
            },
            "actions": [
                [ 
                    action_1,
                    action_2,
                    action_3
                ],
                action_4
            ]
        })

        self.assertEqual(input.actions, [
            action_1,
            action_2,
            action_3,
            action_4
        ])