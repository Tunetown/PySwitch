import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "adafruit_midi": MockAdafruitMIDI(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "gc": MockGC()
}):
    from .mocks_misc import MockMisc
    from .mocks_callback import *

    with patch.dict(sys.modules, {
        "lib.pyswitch.misc": MockMisc
    }):
        
        from lib.pyswitch.controller.inputs import SwitchController
        from lib.pyswitch.colors import Colors
        from .mocks_appl import *



##################################################################################################################################


class TestControllerSwitch(unittest.TestCase):

    def test_actions(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()
        
        action_1 = MockAction()
        action_2 = MockAction()

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1,
                "pixels": (2, 4)                
            },
            "actions": [
                action_1,
                action_2,
            ]
        })

        switch_1.shall_be_pushed = True
        fs.process()

        self.assertEqual(action_1.num_push_calls, 1)
        self.assertEqual(action_2.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)

        switch_1.shall_be_pushed = False
        fs.process()

        self.assertEqual(action_1.num_push_calls, 1)
        self.assertEqual(action_2.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 1)
        self.assertEqual(action_2.num_release_calls, 1)


    def test_actions_deep(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()
        
        action_1 = MockAction()
        action_2 = MockAction()
        action_3 = MockAction()
        action_4 = MockAction()
        action_5 = MockAction()
        action_6 = MockAction()

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1,
                "pixels": (2, 4)                
            },
            "actions": [
                action_1,
                [ 
                    action_2, 
                    action_3 
                ],
                action_4
            ],
            "actionsHold": [
                [ 
                    action_5, 
                    action_6 
                ]
            ]
        })

        self.assertEqual(fs.actions, [
            action_1,
            action_2,
            action_3,
            action_4,
            action_5,
            action_6
        ])

    ####################################################################

    def test_actions_disabled(self):
        appl = MockController()
        switch_1 = MockSwitch()

        cb_1 = MockEnabledCallback(output = True)
        cb_2 = MockEnabledCallback(output = True)

        action_1 = MockAction({ "enableCallback": cb_1 })
        action_2 = MockAction({ "enableCallback": cb_2 })

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1
            },
            "actions": [
                action_1,
                action_2,
            ]
        })

        # Both enabled
        switch_1.shall_be_pushed = True
        fs.process()

        self.assertEqual(action_1.num_push_calls, 1)
        self.assertEqual(action_2.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)

        switch_1.shall_be_pushed = False
        fs.process()

        self.assertEqual(action_1.num_push_calls, 1)
        self.assertEqual(action_2.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 1)
        self.assertEqual(action_2.num_release_calls, 1)

        # Only 1 enabled 
        action_1.reset_mock()
        action_2.reset_mock()

        cb_2.output = False

        switch_1.shall_be_pushed = True
        fs.process()

        self.assertEqual(action_1.num_push_calls, 1)
        self.assertEqual(action_2.num_push_calls, 0)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)

        switch_1.shall_be_pushed = False
        fs.process()

        self.assertEqual(action_1.num_push_calls, 1)
        self.assertEqual(action_2.num_push_calls, 0)
        self.assertEqual(action_1.num_release_calls, 1)
        self.assertEqual(action_2.num_release_calls, 0)

        # Only 2 enabled 
        action_1.reset_mock()
        action_2.reset_mock()

        cb_1.output = False
        cb_2.output = True

        switch_1.shall_be_pushed = True
        fs.process()

        self.assertEqual(action_1.num_push_calls, 0)
        self.assertEqual(action_2.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)

        switch_1.shall_be_pushed = False
        fs.process()

        self.assertEqual(action_1.num_push_calls, 0)
        self.assertEqual(action_2.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 1)

        # All disabled
        action_1.reset_mock()
        action_2.reset_mock()

        cb_1.output = False
        cb_2.output = False

        switch_1.shall_be_pushed = True
        fs.process()

        self.assertEqual(action_1.num_push_calls, 0)
        self.assertEqual(action_2.num_push_calls, 0)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)

        switch_1.shall_be_pushed = False
        fs.process()

        self.assertEqual(action_1.num_push_calls, 0)
        self.assertEqual(action_2.num_push_calls, 0)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)


    ##############################################################################

    def test_minimal(self):
        appl = MockController()
        switch_1 = MockSwitch()

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1
            },
        })

        self.assertEqual(fs.color, None)
        self.assertEqual(fs.brightness, None)

        self.assertEqual(fs.colors, [])
        self.assertEqual(fs.brightnesses, [])

    ##############################################################################

    def test_default_color_and_brightness(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1,
                "pixels": (2, 4)
            }
        })

        self.assertEqual(fs.color, Colors.WHITE)
        self.assertEqual(fs.brightness, 0)

        for c in fs.colors:
            self.assertEqual(c, Colors.WHITE)

        self.assertEqual(len(fs.colors), 2)
        self.assertEqual(fs.brightnesses, [0, 0])

    ##############################################################################

    def test_set_color_and_brightness(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1,
                "pixels": (0, 1, 2, 3, 4)
            }
        })

        # Set color
        fs.color = (4, 6, 5)

        self.assertEqual(fs.color, (4, 6, 5))
        self.assertEqual(fs.colors, [(4, 6, 5) for i in range(5)])

        fs.colors = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15)]

        self.assertEqual(fs.color, (1, 2, 3))
        self.assertEqual(fs.colors, [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15)])
        
        # Brightnesses
        fs.color = (50, 100, 200)
        fs.brightness = 0.4
        
        self.assertAlmostEqual(fs.brightness, 0.4)
        for b in fs.brightnesses:
            self.assertAlmostEqual(b, 0.4)

        self.assertEqual(appl.led_driver.leds, [(20, 40, 80) for i in range(5)])

        fs.brightnesses = [0, 0.1, 0.4, 1, 1]

        self.assertEqual(fs.brightness, 0)
        for i in range(len(fs.brightnesses)):
            b = fs.brightnesses[i]
            self.assertAlmostEqual(b, [0, 0.1, 0.4, 1, 1][i])
        
        self.assertEqual(appl.led_driver.leds, [(0, 0, 0), (5, 10, 20), (20, 40, 80), (50, 100, 200), (50, 100, 200)])

    ##############################################################################

    def test_invalid_colors_and_brightnesses(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()        

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1,
                "pixels": (2, 4)
            }
        })

        with self.assertRaises(Exception):
            fs.colors = [(0, 0, 0)]

        with self.assertRaises(Exception):
            fs.colors = ((0, 0, 0), (0, 0, 0))

        with self.assertRaises(Exception):
            fs.brightnesses = [1]

    ##############################################################################

    def test_no_pixels(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()        

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1
            }
        })

        fs.brightnesses = [0, 1]
        self.assertEqual(fs.brightnesses, [])

    ##############################################################################

    def test_strobe_order(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()

        for order in range(0, 10):
            fs = SwitchController(appl, {
                "assignment": {
                    "model": switch_1,
                    "pixels": (2, 4),
                    "strobeOrder": order
                }
            })

            self.assertEqual(fs.strobe_order, order)

    ##############################################################################

    def test_default_strobe_order(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1,
                "pixels": (2, 4)                
            }
        })

        self.assertEqual(fs.strobe_order, 0)

    ##############################################################################

    def test_override_action(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()
        
        action_1 = MockAction()
        action_2 = MockAction()
        action_o = MockAction()

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1,
                "pixels": (2, 4)                
            },
            "actions": [
                action_1,
                action_2,
            ]
        })

        fs.override_action = action_o

        switch_1.shall_be_pushed = True
        fs.process()

        self.assertEqual(action_1.num_push_calls, 0)
        self.assertEqual(action_2.num_push_calls, 0)
        self.assertEqual(action_o.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)
        self.assertEqual(action_o.num_release_calls, 0)

        switch_1.shall_be_pushed = False
        fs.process()

        self.assertEqual(action_1.num_push_calls, 0)
        self.assertEqual(action_2.num_push_calls, 0)
        self.assertEqual(action_o.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)
        self.assertEqual(action_o.num_release_calls, 1)

    ##############################################################################

    def test_override_action_process_normal(self):
        appl = MockController(num_leds=5)
        switch_1 = MockSwitch()
        
        action_1 = MockAction()
        action_2 = MockAction()
        action_o = MockAction()

        action_o.output_push = True
        action_o.output_release = True

        fs = SwitchController(appl, {
            "assignment": {
                "model": switch_1,
                "pixels": (2, 4)                
            },
            "actions": [
                action_1,
                action_2,
            ]
        })

        fs.override_action = action_o

        switch_1.shall_be_pushed = True
        fs.process()

        self.assertEqual(action_1.num_push_calls, 1)
        self.assertEqual(action_2.num_push_calls, 1)
        self.assertEqual(action_o.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 0)
        self.assertEqual(action_2.num_release_calls, 0)
        self.assertEqual(action_o.num_release_calls, 0)

        switch_1.shall_be_pushed = False
        fs.process()

        self.assertEqual(action_1.num_push_calls, 1)
        self.assertEqual(action_2.num_push_calls, 1)
        self.assertEqual(action_o.num_push_calls, 1)
        self.assertEqual(action_1.num_release_calls, 1)
        self.assertEqual(action_2.num_release_calls, 1)
        self.assertEqual(action_o.num_release_calls, 1)
