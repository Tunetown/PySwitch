import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.kemper import *
    from lib.pyswitch.ui.elements import DisplayLabel
    from lib.pyswitch.colors import Colors

    from lib.pyswitch.clients.kemper.actions.bank_up_down import *
    from lib.pyswitch.clients.kemper.actions.rig_select import *
    from lib.pyswitch.clients.kemper.mappings.bank import *
    from lib.pyswitch.clients.kemper.mappings.select import *


####################################################################################################


class TestKemperActionDefinitionsBankChange(unittest.TestCase):

    def test_bank_colors(self):
        self.assertEqual(NUM_RIGS_PER_BANK, 5)
        self.assertEqual(len(BANK_COLORS), NUM_RIGS_PER_BANK)

        self._test_bank_colors_dir(True)
        self._test_bank_colors_dir(False)


    def _test_bank_colors_dir(self, up):
        # Current
        self._test_bank_colors(up = up, mapping_value = None,  exp_color = Colors.WHITE, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        
        self._test_bank_colors(up = up, mapping_value = 0,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(up = up, mapping_value = 1,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(up = up, mapping_value = 2,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(up = up, mapping_value = 3,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(up = up, mapping_value = 4,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        
        self._test_bank_colors(up = up, mapping_value = 5,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(up = up, mapping_value = 6,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(up = up, mapping_value = 7,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(up = up, mapping_value = 8,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(up = up, mapping_value = 9,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        self._test_bank_colors(up = up, mapping_value = 10,    exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        self._test_bank_colors(up = up, mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,  exp_color = BANK_COLORS[4], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        # Target
        self._test_bank_colors(up = up, mapping_value = None,  exp_color = Colors.WHITE, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        
        self._test_bank_colors(up = up, mapping_value = 0,     exp_color = BANK_COLORS[1 if up else 4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(up = up, mapping_value = 1,     exp_color = BANK_COLORS[1 if up else 4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(up = up, mapping_value = 2,     exp_color = BANK_COLORS[1 if up else 4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(up = up, mapping_value = 3,     exp_color = BANK_COLORS[1 if up else 4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(up = up, mapping_value = 4,     exp_color = BANK_COLORS[1 if up else 4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        
        self._test_bank_colors(up = up, mapping_value = 5,     exp_color = BANK_COLORS[2 if up else 0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(up = up, mapping_value = 6,     exp_color = BANK_COLORS[2 if up else 0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(up = up, mapping_value = 7,     exp_color = BANK_COLORS[2 if up else 0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(up = up, mapping_value = 8,     exp_color = BANK_COLORS[2 if up else 0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(up = up, mapping_value = 9,     exp_color = BANK_COLORS[2 if up else 0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)

        self._test_bank_colors(up = up, mapping_value = 10,    exp_color = BANK_COLORS[3 if up else 1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)

        self._test_bank_colors(up = up, mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,    exp_color = BANK_COLORS[0 if up else 3], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)


    def _test_bank_colors(self, up, mapping_value, exp_color, display_mode):
        # Without text callback and label
        self._do_test_bank_colors_with_label(
            up = up,
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode
        )

        # With label but no text callback (which makes no sense there anyway)
        self._do_test_bank_colors_without_label(
            up = up,
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode
        )

        # With text callback and label
        if mapping_value != None:
            self._do_test_bank_colors_with_label_and_text_cb(
                up = up,
                mapping_value = mapping_value,
                display_mode = display_mode,
                exp_color = exp_color
            )

        # With color callback and label
        if mapping_value != None:
            self._do_test_bank_colors_with_label_and_color_cb(
                up = up,
                mapping_value = mapping_value,
                display_mode = display_mode,
                exp_color = exp_color
            )


    def _do_test_bank_colors_without_label(self, up, mapping_value, display_mode, exp_color):    
        ecb = MockEnabledCallback(output = True)

        if up:
            action = BANK_UP(
                display_mode = display_mode, 
                id = 45, 
                use_leds = True, 
                enable_callback = ecb
            )
        else:
            action = BANK_DOWN(
                display_mode = display_mode, 
                id = 45, 
                use_leds = True, 
                enable_callback = ecb
            )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = appl.client.register_calls[0]["mapping"]
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.02)


    def _do_test_bank_colors_with_label(self, up, mapping_value, display_mode, exp_color):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        if up:
            action = BANK_UP(
                display = display, 
                text = "foo", 
                display_mode = display_mode, 
                id = 45, 
                use_leds = True, 
                enable_callback = ecb,
                led_brightness = 0.5,
                dim_factor = 0.4,
            )
        else:
            action = BANK_DOWN(
                display = display, 
                text = "foo", 
                display_mode = display_mode, 
                id = 45, 
                use_leds = True, 
                enable_callback = ecb,
                led_brightness = 0.5,
                dim_factor = 0.4,
            )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = appl.client.register_calls[0]["mapping"]
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.back_color, (
            int(exp_color[0] * 0.4),
            int(exp_color[1] * 0.4),
            int(exp_color[2] * 0.4)
        ))

        self.assertEqual(display.text, "foo")        


    def _do_test_bank_colors_with_label_and_text_cb(self, up, mapping_value, display_mode, exp_color):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        if display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
            exp_bank = int(mapping_value / 5) 
            exp_rig = mapping_value % 5
        else:
            exp_bank = int(mapping_value / 5) 

            if up:
                exp_bank += 1
                if exp_bank >= NUM_BANKS:
                    exp_bank = 0
            else:
                exp_bank -= 1
                if exp_bank < 0:
                    exp_bank = NUM_BANKS - 1

            exp_rig = mapping_value % 5

        def text_cb(action_parameter, bank, rig):
            self.assertEqual(bank, exp_bank)
            self.assertEqual(rig, exp_rig)
            self.assertEqual(action, action_parameter)
            
            return repr(bank) + "|" + repr(rig)

        if up:
            action = BANK_UP(
                display = display, 
                text = "foo2", 
                display_mode = display_mode, 
                id = 45, 
                use_leds = True, 
                enable_callback = ecb,
                text_callback = text_cb
            )
        else:
            action = BANK_DOWN(
                display = display, 
                text = "foo2", 
                display_mode = display_mode, 
                id = 45, 
                use_leds = True, 
                enable_callback = ecb,
                text_callback = text_cb
            )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = appl.client.register_calls[0]["mapping"]
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.02)

        self.assertEqual(display.back_color, (
            int(exp_color[0] * 0.2),
            int(exp_color[1] * 0.2),
            int(exp_color[2] * 0.2)
        ))

        self.assertEqual(display.text, repr(exp_bank) + "|" + repr(exp_rig))


    def _do_test_bank_colors_with_label_and_color_cb(self, up, mapping_value, display_mode, exp_color):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        exp_bank = int(mapping_value / 5) 
        exp_rig = mapping_value % 5

        def color_cb(action_parameter, bank, rig):
            self.assertEqual(bank, exp_bank)
            self.assertEqual(rig, exp_rig)
            self.assertEqual(action, action_parameter)

            return (3, 4, 5)

        if up:
            action = BANK_UP(
                display = display, 
                display_mode = display_mode, 
                id = 45, 
                use_leds = True, 
                enable_callback = ecb,
                color_callback = color_cb,
                led_brightness = 0.5,
                dim_factor = 0.4,

            )
        else:
            action = BANK_DOWN(
                display = display, 
                display_mode = display_mode, 
                id = 45, 
                use_leds = True, 
                enable_callback = ecb,
                color_callback = color_cb,
                led_brightness = 0.5,
                dim_factor = 0.4,
            )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = appl.client.register_calls[0]["mapping"]
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, (3, 4, 5))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.back_color, (
            int((3, 4, 5)[0] * 0.4),
            int((3, 4, 5)[1] * 0.4),
            int((3, 4, 5)[2] * 0.4)
        ))

        self.assertEqual(display.text, "Bank up" if up else "Bank dn")


####################################################################################################


    def test_overrides(self):
        self._test_overrides(False)
        self._test_overrides(True)


    def _test_overrides(self, up):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        if up:
            action = BANK_UP(
                display = display, 
                text = "foo", 
                color = (3, 5, 7),
                id = 45, 
                use_leds = True,
                led_brightness = 0.5,
                dim_factor = 0.4,
                enable_callback = ecb
            )
        else:
            action = BANK_DOWN(
                display = display, 
                text = "foo", 
                color = (3, 5, 7),
                id = 45, 
                use_leds = True,
                led_brightness = 0.5,
                dim_factor = 0.4, 
                enable_callback = ecb
            )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = appl.client.register_calls[0]["mapping"]

        # Off state (always)
        mapping.value = 1
        action.update_displays()

        self.assertEqual(switch.color, (3, 5, 7))
        self.assertEqual(switch.brightness, 0.5)

        self.assertEqual(display.back_color, (
            int((3, 5, 7)[0] * 0.4),
            int((3, 5, 7)[1] * 0.4),
            int((3, 5, 7)[2] * 0.4)
        ))

        self.assertEqual(display.text, "foo")     


####################################################################################################


    def test_invalid_display_mode(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)
        
        def text_cb(bank, rig):
            pass

        action = BANK_UP(
            display = display, 
            display_mode = self,   # Just some value guaranteed to not be equal to one of the valid modes ;)
            id = 45, 
            use_leds = True, 
            enable_callback = ecb,
            text_callback = text_cb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = appl.client.register_calls[0]["mapping"]
        mapping.value = 1

        with self.assertRaises(Exception):            
            action.update_displays()


#########################################################################################################

    def test_reset_morph_state(self):
        self._test_reset_morph_state(False)
        self._test_reset_morph_state(True)

    def _test_reset_morph_state(self, up):
        if up:
            action = BANK_UP()
        else:
            action = BANK_DOWN()

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)


#########################################################################################################


    def test_messages(self):
        self._test_messages(False)
        self._test_messages(True)

    def _test_messages(self, up):
        if up:
            action = BANK_UP()
        else:
            action = BANK_DOWN()

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperBankChangeCallback__mapping 
        mapping.value = 8
        
        action.push()
        action.release()
        
        self.assertEqual(len(appl.client.set_calls), 1)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_NEXT_BANK() if up else MAPPING_PREVIOUS_BANK(),
            "value": 0
        })
        self.assertEqual(appl.client.set_calls[0]["mapping"].name, MAPPING_NEXT_BANK().name if up else MAPPING_PREVIOUS_BANK().name)

        action.push()
        action.release()
        
        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_NEXT_BANK() if up else MAPPING_PREVIOUS_BANK(),
            "value": 0
        })
        self.assertEqual(appl.client.set_calls[1]["mapping"].name, MAPPING_NEXT_BANK().name if up else MAPPING_PREVIOUS_BANK().name)


#########################################################################################################


    def test_messages_preselect(self):
        self._test_messages_preselect(display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, up = False)
        self._test_messages_preselect(display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, up = True)
        self._test_messages_preselect(display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, up = False)
        self._test_messages_preselect(display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, up = True)

    def _test_messages_preselect(self, display_mode, up):
        if up:
            action = BANK_UP(
                preselect = True
            )
        else:
            action = BANK_DOWN(
                preselect = True
            )

        action_rig_select = RIG_SELECT(
            rig = 2,
            display_mode = display_mode
        )

        switch = MockFootswitch(actions = [action])
        switch_2 = MockFootswitch(actions = [action_rig_select])

        appl = MockController(inputs = [
            switch,
            MockInputControllerDefinition(),
            switch_2,
            MockInputControllerDefinition()
        ])

        action.init(appl, switch)
        action_rig_select.init(appl, switch_2)

        mapping = action.callback._KemperBankChangeCallback__mapping 
        mapping_rigsel = action_rig_select.callback._KemperRigSelectCallback__mapping 

        mapping.value = 14  # Bank 2
        mapping_rigsel.value = mapping.value
        
        action.update_displays()
        action_rig_select.update_displays()
        
        action.push()
        action.release()

        self._check_blinking(
            action = action, 
            switch = switch, 
            should_blink = True, 
            action_rig_select = action_rig_select,
            switch_rig_select = switch_2,
            rig_switch_should_blink = True
        )
        
        self.assertEqual(appl.shared["preselectedBank"], 3 if up else 1)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)

        self.assertEqual(len(appl.client.set_calls), 1)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 3 if up else 1
        })
        
        action.push()
        action.release()

        self._check_blinking(
            action = action, 
            switch = switch, 
            should_blink = True, 
            action_rig_select = action_rig_select,
            switch_rig_select = switch_2,
            rig_switch_should_blink = True
        )
        
        self.assertEqual(appl.shared["preselectedBank"], 4 if up else 0)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)

        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 4 if up else 0
        })
        
        action.push()
        action.release()

        self._check_blinking(
            action = action, 
            switch = switch, 
            should_blink = True, 
            action_rig_select = action_rig_select,
            switch_rig_select = switch_2,
            rig_switch_should_blink = True
        )
        
        self.assertEqual(appl.shared["preselectedBank"], 5 if up else 124)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)

        self.assertEqual(len(appl.client.set_calls), 3)
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 5 if up else 124
        })

        appl.shared = {}  # Remove preselect mark

        self._check_blinking(
            action = action, 
            switch = switch, 
            should_blink = False, 
            action_rig_select = action_rig_select,
            switch_rig_select = switch_2,
            rig_switch_should_blink = False
        )

    def test_messages_preselect_max_bank(self):
        self._test_messages_preselect_max_bank(up = False)
        self._test_messages_preselect_max_bank(up = True)

    def _test_messages_preselect_max_bank(self, up):
        if up:
            action = BANK_UP(
                preselect = True,
                max_bank = 10
            )
        else:
            action = BANK_DOWN(
                preselect = True,
                max_bank = 10
            )

        switch = MockFootswitch(actions = [action])
        
        appl = MockController(inputs = [
            switch,
        ])

        action.init(appl, switch)
        
        mapping = action.callback._KemperBankChangeCallback__mapping 
        
        mapping.value = 14  # Bank 2
        
        action.update_displays()
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["preselectedBank"], 3 if up else 1)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)

        action.push()
        action.release()

        self.assertEqual(appl.shared["preselectedBank"], 4 if up else 0)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)

        action.push()
        action.release()

        self.assertEqual(appl.shared["preselectedBank"], 5 if up else 9)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["preselectedBank"], 6 if up else 8)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["preselectedBank"], 7 if up else 7)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["preselectedBank"], 8 if up else 6)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["preselectedBank"], 9 if up else 5)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["preselectedBank"], 0 if up else 4)
        self.assertEqual(appl.shared["preselectCallback"], action.callback)
        
    # Checks if the LEDs are blinking
    def _check_blinking(self, 
                        action, 
                        switch, 
                        should_blink, 
                        action_rig_select = None, 
                        switch_rig_select = None, 
                        rig_switch_should_blink = False
        ):
        cb = action.callback

        if action_rig_select:
            cb_rigsel = action_rig_select.callback

        brightness_off = cb._KemperBankChangeCallback__led_brightness_off
        brightness_on = cb._KemperBankChangeCallback__led_brightness

        exp_brightness_off = brightness_on
        exp_brightness_on = brightness_off if should_blink else brightness_on

        # factor_off = 0.2
        # factor_on = 1 if should_blink else factor_off

        rig_brightness_on = action_rig_select.callback._KemperRigSelectCallback__default_led_brightness_on
        rig_brightness_off = action_rig_select.callback._KemperRigSelectCallback__default_led_brightness_off

        rig_exp_brightness_off = rig_brightness_off
        rig_exp_brightness_on = rig_brightness_on if rig_switch_should_blink else rig_brightness_off

        period = MockPeriodCounter()
        cb._KemperBankChangeCallback__preselect_blink_period = period

        def update():
            cb.update()
            if action_rig_select:
                if rig_switch_should_blink:
                    cb_rigsel.update()
                else:
                    cb_rigsel.update_displays()

        # Off state (initial)
        update()

        while switch.brightness != exp_brightness_off:
            period.exceed_next_time = True
            update()

        self.assertEqual(switch.brightness, exp_brightness_off)
        # self.assertEqual(display.back_color, (
        #     int(exp_color[0] * factor_off),
        #     int(exp_color[1] * factor_off),
        #     int(exp_color[2] * factor_off)
        # ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_on)

        # Blink on
        period.exceed_next_time = True
        
        update()
        
        self.assertEqual(switch.brightness, exp_brightness_on)
        # self.assertEqual(display.back_color, (
        #     int(exp_color[0] * factor_on),
        #     int(exp_color[1] * factor_on),
        #     int(exp_color[2] * factor_on)
        # ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_off)

        # Blink off
        period.exceed_next_time = True
                
        update()

        self.assertEqual(switch.brightness, exp_brightness_off)
        # self.assertEqual(display.back_color, (
        #     int(exp_color[0] * factor_off),
        #     int(exp_color[1] * factor_off),
        #     int(exp_color[2] * factor_off)
        # ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_on)

        # Blink on
        period.exceed_next_time = True
        
        update()

        self.assertEqual(switch.brightness, exp_brightness_on)
        # self.assertEqual(display.back_color, (
        #     int(exp_color[0] * factor_on),
        #     int(exp_color[1] * factor_on),
        #     int(exp_color[2] * factor_on)
        # ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_off)

        # Blink off
        period.exceed_next_time = True
        
        update()

        self.assertEqual(switch.brightness, exp_brightness_off)
        # self.assertEqual(display.back_color, (
        #     int(exp_color[0] * factor_off),
        #     int(exp_color[1] * factor_off),
        #     int(exp_color[2] * factor_off)
        # ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_on)



