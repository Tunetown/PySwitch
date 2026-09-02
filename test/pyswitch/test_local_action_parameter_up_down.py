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
    from lib.pyswitch.ui.elements import DisplayLabel
    # from lib.pyswitch.misc import Updater
    
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.local.actions.param_change import *
    

class TestLocalActionParameterUpDown(unittest.TestCase):

    def test(self):
        # Up
        self._test_offset(
            offset = 100, 
            start_value = 10,
            max_value = 1000,
            data = (110, 210, 310, 410, 510, 610, 710, 810, 910, 1000, 1000)
        )

        # Down
        self._test_offset(
            offset = -100, 
            start_value = 620,
            max_value = 1000,
            data = (520, 420, 320, 220, 120, 20, 0, 0)
        )


    def _test_offset(self, offset, start_value, max_value, data):
        mapping = MockParameterMapping(
            name = "PB",
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0)
            }
        )

        ecb = MockEnabledCallback(output = True)

        action = PARAMETER_UP_DOWN(
            mapping = mapping,
            offset = offset,
            repeat_interval_millis = None,
            max_value = max_value,
            display = display, 
            color = (100, 100, 100),
            led_brightness = 0.5,
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        self.assertIsInstance(action, Action)

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 45)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping.value = start_value

        for exp_value in data:
            appl.client.set_calls = []

            appl.update()
            action.push()
            action.release()

            self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": exp_value }])
        
            mapping.value = exp_value
            action.update_displays()

            # Label
            exp_perc = int(100 * (exp_value / max_value))
            exp_comp = exp_perc if offset > 0 else 100 - exp_perc
            self.assertEqual(display.back_color, (exp_comp, exp_comp, exp_comp), exp_value)
            self.assertEqual(display.text, str(exp_perc) + "%", exp_value)
            
            # LEDs
            self.assertEqual(switch.color, (100, 100, 100), exp_value)
            self.assertEqual(switch.brightness, (exp_value * 0.5 / max_value) if offset > 0 else (1 - (exp_value / max_value)) * 0.5, exp_value)

    
    ##############################################################################################


    def test_text_override(self):
        mapping = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0)
            }
        )

        action = PARAMETER_UP_DOWN(
            mapping = mapping,
            text = "foo {val}",
            offset = 100,
            max_value = 1000,
            display = display, 
            color = (100, 100, 100),
            use_leds = False
        )

        self.assertEqual(action.uses_switch_leds, False)

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        # None value
        mapping.value = None
        action.update_displays()

        self.assertEqual(display.text, "foo ?")

        # Real value
        mapping.value = 10

        appl.client.set_calls = []

        appl.update()
        action.push()
        action.release()

        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 110 }])
        
        mapping.value = 110
        action.update_displays()

        # Label
        self.assertEqual(display.back_color, (11, 11, 11))
        self.assertEqual(display.text, "foo 11")
            
        # LEDs
        self.assertEqual(switch.color, (0, 0, 0))
        self.assertEqual(switch.brightness, 0)


    ##############################################################################################


    def test_change_display(self):
        mapping = MockParameterMapping(
            name = "PP",
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        display = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (0, 0, 0)
            }
        )

        action = PARAMETER_UP_DOWN(
            mapping = mapping,
            offset = 100,
            max_value = 1000,
            change_display = display,
            change_timeout_millis = 124
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping.value = 10

        appl.client.set_calls = []

        appl.update()
        action.push()
        action.release()

        self.assertEqual(appl.client.set_calls, [{ "mapping": mapping, "value": 110 }])
        
        mapping.value = 110

        self.assertEqual(display.text, "PP: 11%")


    ##############################################################################################


    def test_auto_range_sysex(self):
        mapping = MockParameterMapping(
            set = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        display = DisplayLabel(
            layout = {
                "font": "foo"
            }
        )

        action = PARAMETER_UP_DOWN(
            mapping = mapping,
            offset = 100,
            display = display
        )

        self.assertEqual(action.callback._max_value, 16383)


    def test_auto_range_cc(self):
        mapping = MockParameterMapping(
            set = (176, 8, 0)
            # ControlChange(
            #     control = 8,
            #     value = 0
            # )
        )

        display = DisplayLabel(
            layout = {
                "font": "foo"
            }
        )

        action = PARAMETER_UP_DOWN(
            mapping = mapping,
            offset = 100,
            display = display
        )

        self.assertEqual(action.callback._max_value, 127)


    #######################################################################################


    def test_repeat(self):
        mapping = MockParameterMapping(
            name = "PP",
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        action = PARAMETER_UP_DOWN(
            repeat_interval_millis = 101,
            mapping = mapping,
            offset = 100,
            max_value = 1000
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        self.assertEqual(action.callback._ParameterChangeCallback__repeat_period.interval, 101)
        action.callback._ParameterChangeCallback__repeat_period = MockPeriodCounter()
        period = action.callback._ParameterChangeCallback__repeat_period

        mapping.value = 10

        appl.client.set_calls = []

        action.push()
        action.release()

        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 110 })
        
        mapping.value = 110

        # Long push
        action.push()

        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 210 })

        mapping.value = 210
        period.exceed_next_time = True
        action.callback.update()

        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 310 })

        mapping.value = 310
        period.exceed_next_time = True
        action.callback.update()

        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 410 })

        mapping.value = 410

        # Release again
        action.release()
        period.exceed_next_time = True
        action.callback.update()

        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 410 })

        period.exceed_next_time = True
        action.callback.update()

        self.assertEqual(appl.client.last_sent_message, { "mapping": mapping, "value": 410 })
