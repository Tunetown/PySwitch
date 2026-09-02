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
    "gc": MockGC()
}):
    from .mocks_ui import *
    from .mocks_appl import *
    from .mocks_callback import *


class MockAction(Action):
    def __init__(self, config = {}, use_leds = False):
        super().__init__(config = config)

        self.uses_switch_leds = use_leds

        self.num_update_displays_calls = 0

    def update_displays(self):
        super().update_displays()
        
        self.num_update_displays_calls += 1


#################################################################################


class TestAction(unittest.TestCase):

    def test_enabled_callback(self):
        cb = MockEnabledCallback(output = True)

        action_1 = MockAction(config = {
            "enableCallback": cb
        })

        self.assertEqual(action_1.enabled, True)

        cb.output = False

        self.assertEqual(action_1.enabled, False)


    def test_enabled_callback_mappings(self):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_2 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0xe9, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x22],
            #     data = [0x00, 0x00, 0xe9]
            # )
        )

        cb = MockEnabledCallback(
            output = True,
            mappings = [
                mapping_1,
                mapping_2
            ]
        )

        action_1 = MockAction(
            config = {
                "enableCallback": cb
            }
        )

        appl = MockController()

        action_1.init(appl, MockFootswitch())

        self.assertEqual([x["mapping"] for x in appl.client.register_calls], [mapping_1, mapping_2])

        appl.update()

        self.assertEqual([x["mapping"] for x in appl.client.request_calls], [mapping_1, mapping_2])

        listener_1 = appl.client.register_calls[0]["listener"]
        self.assertEqual(appl.client.register_calls[1]["listener"], listener_1)
        
        cb.output = False

        self.assertEqual(action_1.num_update_displays_calls, 0)  # Is updated in update()!

        action_1.update()

        self.assertEqual(action_1.num_update_displays_calls, 1)


    #######################################################################################################


    def test_callback(self):
        cb = MockActionCallback()

        action_1 = MockAction(config = {
            "callback": cb
        })

        self.assertEqual(cb.update_displays_calls, 0)

        action_1.update_displays()

        self.assertEqual(cb.update_displays_calls, 1)
        

    def test_callback_mappings(self):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_2 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0xe9, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x22],
            #     data = [0x00, 0x00, 0xe9]
            # )
        )

        cb = MockActionCallback(
            mappings = [
                mapping_1,
                mapping_2
            ]
        )

        action_1 = MockAction(
            config = {
                "callback": cb
            }
        )

        appl = MockController()

        action_1.init(appl, MockFootswitch())

        self.assertEqual([x["mapping"] for x in appl.client.register_calls], [mapping_1, mapping_2])
        
        listener_1 = appl.client.register_calls[0]["listener"]
        self.assertEqual(appl.client.register_calls[1]["listener"], listener_1)

        listener_1.parameter_changed(mapping_1)

        self.assertEqual(action_1.num_update_displays_calls, 1)
        self.assertEqual(cb.update_displays_calls, 1)

        listener_1.parameter_changed(mapping_1)

        self.assertEqual(action_1.num_update_displays_calls, 2)
        self.assertEqual(cb.update_displays_calls, 2)

        listener_1.request_terminated(mapping_1)

        self.assertEqual(action_1.num_update_displays_calls, 3)
        self.assertEqual(cb.update_displays_calls, 3)


    def test_callback_mappings_disabled(self):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        cb_enabled = MockEnabledCallback(
            output = True
        )

        cb = MockActionCallback(
            mappings = [mapping_1]
        )

        action_1 = MockAction(
            config = {
                "callback": cb,
                "enableCallback": cb_enabled
            }
        )

        appl = MockController()

        action_1.init(appl, MockFootswitch())

        listener_1 = appl.client.register_calls[0]["listener"]
        
        listener_1.parameter_changed(mapping_1)

        self.assertEqual(action_1.num_update_displays_calls, 1)
        self.assertEqual(cb.update_displays_calls, 1)

        cb_enabled.output = False

        listener_1.parameter_changed(mapping_1)

        self.assertEqual(action_1.num_update_displays_calls, 1)
        self.assertEqual(cb.update_displays_calls, 1)

        listener_1.request_terminated(mapping_1)

        self.assertEqual(action_1.num_update_displays_calls, 1)
        self.assertEqual(cb.update_displays_calls, 1)


    #######################################################################################################

    def test_led_segments_one_action(self):
        appl = MockController()
        switch = MockFootswitch()
        
        action_1 = MockAction()
        action_2 = MockAction()
        action_3 = MockAction()
        action_4 = MockAction(use_leds = True)
        action_5 = MockAction()

        with self.assertRaises(Exception):           
            action_4._Action__get_led_segments()

        action_1.init(appl, switch)
        action_2.init(appl, switch)
        action_3.init(appl, switch)
        action_4.init(appl, switch)
        action_5.init(appl, switch)

        ### 5 Actions
        switch.actions = [
            action_1,
            action_2,
            action_3,
            action_4,
            action_5
        ]

        # One pixel
        switch.pixels = [11]
        self.assertEqual(list(action_4._Action__get_led_segments()), [0])
        self.assertEqual(list(action_1._Action__get_led_segments()), [])
        self.assertEqual(list(action_2._Action__get_led_segments()), [])
        self.assertEqual(list(action_3._Action__get_led_segments()), [])
        self.assertEqual(list(action_5._Action__get_led_segments()), [])

        # Two pixels
        switch.pixels = [11, 13]
        self.assertEqual(list(action_4._Action__get_led_segments()), [0, 1])

        # Three pixels
        switch.pixels = [11, 13, 15]
        self.assertEqual(list(action_4._Action__get_led_segments()), [0, 1, 2])

        # Four pixels
        switch.pixels = [11, 13, 15, 19]
        self.assertEqual(list(action_4._Action__get_led_segments()), [0, 1, 2, 3])

        # Five pixels
        switch.pixels = [11, 13, 15, 19, 20]
        self.assertEqual(list(action_4._Action__get_led_segments()), [0, 1, 2, 3, 4])

        # Six pixels
        switch.pixels = [11, 13, 15, 19, 20, 23]
        self.assertEqual(list(action_4._Action__get_led_segments()), [0, 1, 2, 3, 4, 5])


#################################################################################


    def test_led_segments_three_actions(self):
        appl = MockController()
        switch = MockFootswitch()
        
        cb_1 = MockEnabledCallback(output = True)
        cb_2 = MockEnabledCallback(output = True)

        action_1 = MockAction(use_leds = True, config = { "enableCallback": cb_1 })
        action_2 = MockAction(use_leds = True, config = { "enableCallback": cb_2 })
        action_3 = MockAction()
        action_4 = MockAction(use_leds = True)
        action_5 = MockAction()

        action_1.init(appl, switch)
        action_2.init(appl, switch)
        action_3.init(appl, switch)
        action_4.init(appl, switch)
        action_5.init(appl, switch)

        ### 5 Actions
        switch.actions = [
            action_1,
            action_2,
            action_3,
            action_4,
            action_5
        ]

        # One pixel
        switch.pixels = [11]
        self.assertEqual(list(action_1._Action__get_led_segments()), [0])
        self.assertEqual(list(action_2._Action__get_led_segments()), [])
        self.assertEqual(list(action_4._Action__get_led_segments()), [])
        self.assertEqual(list(action_3._Action__get_led_segments()), [])
        self.assertEqual(list(action_5._Action__get_led_segments()), [])

        # Two pixels
        switch.pixels = [11, 13]
        self.assertEqual(list(action_1._Action__get_led_segments()), [0])
        self.assertEqual(list(action_2._Action__get_led_segments()), [1])
        self.assertEqual(list(action_4._Action__get_led_segments()), [])

        # Three pixels
        switch.pixels = [11, 13, 15]
        self.assertEqual(list(action_1._Action__get_led_segments()), [0])
        self.assertEqual(list(action_2._Action__get_led_segments()), [1])
        self.assertEqual(list(action_4._Action__get_led_segments()), [2])

        # Four pixels
        switch.pixels = [11, 13, 15, 19]
        self.assertEqual(list(action_1._Action__get_led_segments()), [0, 1])
        self.assertEqual(list(action_2._Action__get_led_segments()), [2])
        self.assertEqual(list(action_4._Action__get_led_segments()), [3])

        # Five pixels
        switch.pixels = [11, 13, 15, 19, 20]
        self.assertEqual(list(action_1._Action__get_led_segments()), [0, 1, 2])
        self.assertEqual(list(action_2._Action__get_led_segments()), [3])
        self.assertEqual(list(action_4._Action__get_led_segments()), [4])

        # Six pixels
        switch.pixels = [11, 13, 15, 19, 20, 23]
        self.assertEqual(list(action_1._Action__get_led_segments()), [0, 1, 2, 3])
        self.assertEqual(list(action_2._Action__get_led_segments()), [4])
        self.assertEqual(list(action_4._Action__get_led_segments()), [5])

        # Disable action 1
        cb_1.output = False
        self.assertEqual(list(action_1._Action__get_led_segments()), [])
        self.assertEqual(list(action_2._Action__get_led_segments()), [0, 1, 2, 3, 4])
        self.assertEqual(list(action_4._Action__get_led_segments()), [5])

        # Disable action 2
        cb_1.output = True
        cb_2.output = False
        self.assertEqual(list(action_1._Action__get_led_segments()), [0, 1, 2, 3, 4])
        self.assertEqual(list(action_2._Action__get_led_segments()), [])
        self.assertEqual(list(action_4._Action__get_led_segments()), [5])

        # No LED actions at all but action 1 but this is disabled        
        cb_1.output = False
        action_2.uses_switch_leds = False
        action_4.uses_switch_leds = False
        self.assertEqual(list(action_1._Action__get_led_segments()), [])
        

########################################################################################


    def test_property_set_switch_colors_brightness(self):
        appl = MockController()
        switch = MockFootswitch()
        
        action_1 = MockAction()
        action_2 = MockAction(use_leds = True)
        action_3 = MockAction()
        action_4 = MockAction(use_leds = True)
        action_5 = MockAction(use_leds = True)

        action_1.init(appl, switch)
        action_2.init(appl, switch)
        action_3.init(appl, switch)
        action_4.init(appl, switch)
        action_5.init(appl, switch)

        ### 5 Actions
        switch.actions = [
            action_1,
            action_2,
            action_3,
            action_4,
            action_5
        ]

        # One pixel
        switch.pixels = [11]
        switch.colors = [(0, 0, 0)]
        switch.brightnesses = [0]

        action_2.switch_color = (2, 3, 4)
        action_2.switch_brightness = 1

        self.assertEqual(switch.colors, [(2, 3, 4)])
        self.assertEqual(switch.brightnesses, [1])
        self.assertEqual(action_2.switch_brightness, 1)

        # Two pixels
        switch.pixels = [11, 12]
        switch.colors = [(0, 0, 0), (0, 0, 0)]
        switch.brightnesses = [0, 0]

        action_2.switch_color = (2, 30, 4)
        action_4.switch_color = (2, 30, 40)
        action_5.switch_color = (2, 30, 400)
        action_2.switch_brightness = 0.2
        action_4.switch_brightness = 0.3
        action_5.switch_brightness = 0.4
        
        self.assertEqual(switch.colors, [(2, 30, 4), (2, 30, 40)])
        self.assertEqual(switch.brightnesses, [0.2, 0.3])
        
        self.assertEqual(action_2.switch_brightness, 0.2)
        self.assertEqual(action_4.switch_brightness, 0.3)
        self.assertEqual(action_5.switch_brightness, None)

        # Three pixels
        switch.pixels = [11, 12, 34]
        switch.colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        switch.brightnesses = [0, 0, 0]

        action_2.switch_color = (2, 30, 4)
        action_4.switch_color = (2, 30, 40)
        action_5.switch_color = (2, 30, 400)
        action_2.switch_brightness = 0.2
        action_4.switch_brightness = 0.3
        action_5.switch_brightness = 0.4
        
        self.assertEqual(switch.colors, [(2, 30, 4), (2, 30, 40), (2, 30, 400)])
        self.assertEqual(switch.brightnesses, [0.2, 0.3, 0.4])

        self.assertEqual(action_2.switch_brightness, 0.2)
        self.assertEqual(action_4.switch_brightness, 0.3)
        self.assertEqual(action_5.switch_brightness, 0.4)


########################################################################################


    def test_property_set_switch_color_brightness_tuples(self):
        appl = MockController()
        switch = MockFootswitch()
        
        cb_4 = MockEnabledCallback(output = True)
        cb_5 = MockEnabledCallback(output = True)

        action_1 = MockAction()
        action_2 = MockAction(use_leds = True)
        action_3 = MockAction()
        action_4 = MockAction(use_leds = True, config = { "enableCallback": cb_4 })
        action_5 = MockAction(use_leds = True, config = { "enableCallback": cb_5 })

        action_1.init(appl, switch)
        action_2.init(appl, switch)
        action_3.init(appl, switch)
        action_4.init(appl, switch)
        action_5.init(appl, switch)

        ### 5 Actions
        switch.actions = [
            action_1,
            action_2,
            action_3,
            action_4,
            action_5
        ]

        # One pixel
        switch.pixels = [11]
        switch.colors = [(0, 0, 0)]
        switch.brightnesses = [0]

        action_2.switch_color = [(2, 3, 4), (3, 4, 5)]
        action_2.switch_brightness = 0.2
        
        self.assertEqual(switch.colors, [(3, 4, 5)])
        self.assertEqual(switch.brightnesses, [0.2])

        # Two pixels
        switch.pixels = [11, 12]
        switch.colors = [(0, 0, 0), (0, 0, 0)]
        switch.brightnesses = [0, 0]

        action_2.switch_color = [(2, 3, 4), (3, 4, 5)]
        action_4.switch_color = [(2, 30, 40), (3, 40, 5)]
        action_5.switch_color = [(2, 3, 400), (3, 4, 5)]
        action_2.switch_brightness = 0.2
        action_4.switch_brightness = 0.4
        action_5.switch_brightness = 0.6

        self.assertEqual(switch.colors, [(3, 4, 5), (3, 40, 5)])
        self.assertEqual(switch.brightnesses, [0.2, 0.4])

        # Three pixels
        switch.pixels = [11, 12, 34]
        switch.colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        switch.brightnesses = [0, 0, 0]

        action_2.switch_color = [(2, 3, 4), (3, 4, 5)]
        action_4.switch_color = [(2, 30, 40), (30, 4, 5)]
        action_5.switch_color = [(2, 30, 400), (31, 4, 5)]

        action_2.switch_brightness = 0.2
        action_4.switch_brightness = 0.4
        action_5.switch_brightness = 0.6

        self.assertEqual(switch.colors, [(3, 4, 5), (30, 4, 5), (31, 4, 5)])
        self.assertEqual(switch.brightnesses, [0.2, 0.4, 0.6])

        ### Only action 2 is enabled ##############################################
        cb_4.output = False
        cb_5.output = False

        # One pixel
        switch.pixels = [11]
        switch.colors = [(0, 0, 0)]
        switch.brightnesses = [0]

        action_2.switch_color = [(2, 3, 4), (3, 4, 5)]
        action_2.switch_brightness = 0.2

        self.assertEqual(switch.colors, [(3, 4, 5)])
        self.assertEqual(switch.brightnesses, [0.2])

        # Two pixels
        switch.pixels = [11, 12]
        switch.colors = [(0, 0, 0), (0, 0, 0)]
        switch.brightnesses = [0, 0]

        action_2.switch_color = [(2, 3, 4), (3, 4, 5)]
        action_4.switch_color = [(2, 30, 40), (3, 4, 5)]
        action_5.switch_color = [(2, 3, 400), (3, 4, 5)]

        action_2.switch_brightness = 0.2
        action_4.switch_brightness = 0.4
        action_5.switch_brightness = 0.6

        self.assertEqual(switch.colors, [(2, 3, 4), (3, 4, 5)])
        self.assertEqual(switch.brightnesses, [0.2, 0.2])

        # Three pixels
        switch.pixels = [11, 12, 34]
        switch.colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        switch.brightnesses = [0, 0, 0]

        action_2.switch_color = [(2, 3, 4), (3, 4, 5), (6, 7, 8)]
        action_4.switch_color = [(2, 30, 40), (3, 4, 5), (4, 5, 78)]
        action_5.switch_color = [(2, 30, 400), (3, 4, 5), (2, 34, 56)]

        action_2.switch_brightness = 0.2
        action_4.switch_brightness = 0.4
        action_5.switch_brightness = 0.6

        self.assertEqual(switch.colors, [(2, 3, 4), (3, 4, 5), (6, 7, 8)])
        self.assertEqual(switch.brightnesses, [0.2, 0.2, 0.2])