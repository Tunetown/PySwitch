import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):

    #from lib.pyswitch.controller.actions.actions import PushButtonAction
    from .mocks_appl import *
    from .mocks_callback import *
    from lib.pyswitch.controller.controller import Controller


class TestActionPushButton(unittest.TestCase):

    def test_set_reset(self):
        cb = MockPushButtonActionCallback()

        action_1 = MockPushButtonAction({
            "mode": PushButtonAction.LATCH,
            "callback": cb
        })

        self.assertEqual(cb.update_displays_calls, 0)
        self.assertEqual(cb.state_changed_calls, 0)
        self.assertEqual(action_1.state, False)

        action_1.state = True
        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 1)
        self.assertEqual(action_1.state, True)

        action_1.feedback_state(False)
        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 1)
        self.assertEqual(action_1.state, False)

        action_1.feedback_state(True)
        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 1)
        self.assertEqual(action_1.state, True)

        action_1.state = False
        self.assertEqual(cb.update_displays_calls, 2)
        self.assertEqual(cb.state_changed_calls, 2)
        self.assertEqual(action_1.state, False)

        action_1.state = True
        self.assertEqual(cb.update_displays_calls, 3)
        self.assertEqual(cb.state_changed_calls, 3)
        self.assertEqual(action_1.state, True)

        action_1.reset()
        self.assertEqual(cb.update_displays_calls, 4)
        self.assertEqual(cb.state_changed_calls, 3)
        self.assertEqual(action_1.state, False)
        
        
###################################################################################


    def test_latch(self):
        switch_1 = MockSwitch()
        action_1 = MockPushButtonAction({
            "mode": PushButtonAction.LATCH
        })

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
            ]
        )

        appl.init()

        # Build scene:
        # Step 1: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, True)
        
        # Step 2: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, True)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, False)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, False)
        
        
###################################################################################


    def test_enable(self):
        switch_1 = MockSwitch()
        action_1 = MockPushButtonAction({
            "mode": PushButtonAction.ENABLE
        })

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
            ]
        )

        appl.init()

        # Build scene:
        # Step 1: Button pushed        
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
        
        # Step 2: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, True)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)

        
###################################################################################


    def test_disable(self):
        switch_1 = MockSwitch()
        action_1 = MockPushButtonAction({
            "mode": PushButtonAction.DISABLE
        })
        action_1.state = True

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
            ]
        )

        # Build scene:
        # Step 1: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)

        # Step 2: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, False)

        
###################################################################################


    def test_momentary(self):
        switch_1 = MockSwitch()
        action_1 = MockPushButtonAction({
            "mode": PushButtonAction.MOMENTARY
        })

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
            ]
        )

        appl.init()

        # Build scene:
        # Step 1: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()
        
        self.assertEqual(action_1.state, True)
        
        # Step 2: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)

        
###################################################################################


    def test_momentary_inverse(self):
        switch_1 = MockSwitch()
        action_1 = MockPushButtonAction({
            "mode": PushButtonAction.MOMENTARY_INVERSE
        })
        action_1.state = True

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
            ]
        )

        appl.init()

        # Build scene:
        # Step 1: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)

        # Step 2: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)

        
###################################################################################


    def test_one_shot(self):
        switch_1 = MockSwitch()
        cb = MockPushButtonActionCallback()
        action_1 = MockPushButtonAction({
            "mode": PushButtonAction.ONE_SHOT,
            "callback": cb
        })

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
            ]
        )

        appl.init()

        # Build scene:
        # Step 1: Button pushed
        switch_1.shall_be_pushed = True
        cb.update_displays_calls = 0
        cb.state_changed_calls = 0

        appl.tick()

        self.assertEqual(cb.update_displays_calls, 2)
        self.assertEqual(cb.state_changed_calls, 1)

        # Step 2: Button released    
        switch_1.shall_be_pushed = False
        self.assertEqual(cb.update_displays_calls, 2)
        self.assertEqual(cb.state_changed_calls, 1)

        appl.tick()
        appl.tick()

        self.assertEqual(cb.update_displays_calls, 3)
        self.assertEqual(cb.state_changed_calls, 1)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(cb.update_displays_calls, 3)
        self.assertEqual(cb.state_changed_calls, 1)

        appl.tick()
        appl.tick()

        self.assertEqual(cb.update_displays_calls, 4)
        self.assertEqual(cb.state_changed_calls, 2)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(cb.update_displays_calls, 4)
        self.assertEqual(cb.state_changed_calls, 2)

        appl.tick()
        appl.tick()

        self.assertEqual(cb.update_displays_calls, 5)
        self.assertEqual(cb.state_changed_calls, 2)


###################################################################################


    def test_no_state_change(self):
        switch_1 = MockSwitch()
        cb = MockPushButtonActionCallback()

        action_1 = MockPushButtonAction({
            "mode": PushButtonAction.NO_STATE_CHANGE,
            "callback": cb
        })

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
            ]
        )

        appl.init()

        # Build scene:
        # Step 1: Button pushed
        switch_1.shall_be_pushed = True
        cb.update_displays_calls = 0
        cb.state_changed_calls = 0

        appl.tick()

        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 0)

        # Step 2: Button released    
        switch_1.shall_be_pushed = False
        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 0)

        appl.tick()
        appl.tick()

        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 0)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 0)

        appl.tick()
        appl.tick()

        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 0)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 0)

        appl.tick()
        appl.tick()

        self.assertEqual(cb.update_displays_calls, 1)
        self.assertEqual(cb.state_changed_calls, 0)

        
###################################################################################


    def test_hold_momentary_short_press(self):
        switch_1 = MockSwitch()
        period = MockPeriodCounter()        
        action_1 = MockPushButtonAction(
            {
                "mode": PushButtonAction.HOLD_MOMENTARY,
                "holdTimeMillis": 500
            },
            period
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
                },
                MockInputControllerDefinition()
            ]
        )

        appl.init()

        # Build scene:
        # Step 1: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, False)
        self.assertEqual(period.num_reset_calls, 0)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
        self.assertEqual(period.num_reset_calls, 1)

        # Step 2: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, True)
        self.assertEqual(period.num_reset_calls, 1)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
        self.assertEqual(period.num_reset_calls, 1)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, True)
        self.assertEqual(period.num_reset_calls, 1)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)
        self.assertEqual(period.num_reset_calls, 2)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, False)
        self.assertEqual(period.num_reset_calls, 2)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)
        self.assertEqual(period.num_reset_calls, 2)


###################################################################################


    def test_hold_momentary_long_press(self):
        switch_1 = MockSwitch()
        period = MockPeriodCounter()
        action_1 = MockPushButtonAction(
            {
                "mode": PushButtonAction.HOLD_MOMENTARY,
                "holdTimeMillis": 500
            },
            period
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
                },
                MockInputControllerDefinition()
            ]
        )

        appl.init()

        # Build scene:
        # Step 1: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
    
        # Step 2: Button released
        period.exceed_next_time = True
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, False)
        
        # Step 3: Button pushed
        switch_1.shall_be_pushed = True
        self.assertEqual(action_1.state, False)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
        
        # Step 4: Button released
        switch_1.shall_be_pushed = False
        self.assertEqual(action_1.state, True)

        appl.tick()
        appl.tick()

        self.assertEqual(action_1.state, True)
