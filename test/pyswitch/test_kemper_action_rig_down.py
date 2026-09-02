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
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.kemper import *
    from lib.pyswitch.ui.elements import DisplayLabel
    from lib.pyswitch.colors import DEFAULT_LABEL_COLOR, DEFAULT_SWITCH_COLOR

    from lib.pyswitch.clients.kemper.actions.rig_up_down import *
    from lib.pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_CURRENT_RIG, RIG_SELECT_DISPLAY_TARGET_RIG

    from lib.pyswitch.clients.kemper.mappings.select import *


####################################################################################################


class TestKemperActionDefinitionsRigDown(unittest.TestCase):

    def test_bank_colors(self):
        # Current (no keeping bank)
        self._test_bank_colors(mapping_value = None,  keep_bank = False, exp_color = None, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = None, exp_text_rig = None)
        
        self._test_bank_colors(mapping_value = 0,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 1,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 2)
        self._test_bank_colors(mapping_value = 2,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 3)
        self._test_bank_colors(mapping_value = 3,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 4)
        self._test_bank_colors(mapping_value = 4,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 5)
        
        self._test_bank_colors(mapping_value = 5,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 6,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 2)
        self._test_bank_colors(mapping_value = 7,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 3)
        self._test_bank_colors(mapping_value = 8,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 4)
        self._test_bank_colors(mapping_value = 9,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 5)

        self._test_bank_colors(mapping_value = 10,    keep_bank = False, exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 3, exp_text_rig = 1)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,  keep_bank = False, exp_color = BANK_COLORS[4], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 125, exp_text_rig = 5)

        # Target (no keeping bank)
        self._test_bank_colors(mapping_value = None,  keep_bank = False, exp_color = None, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = None, exp_text_rig = None)
        
        self._test_bank_colors(mapping_value = 0,     keep_bank = False, exp_color = BANK_COLORS[4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 125, exp_text_rig = 5)
        self._test_bank_colors(mapping_value = 1,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 2,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 2)
        self._test_bank_colors(mapping_value = 3,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 3)
        self._test_bank_colors(mapping_value = 4,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 4)
        
        self._test_bank_colors(mapping_value = 5,     keep_bank = False, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 5)
        self._test_bank_colors(mapping_value = 6,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 7,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 2)
        self._test_bank_colors(mapping_value = 8,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 3)
        self._test_bank_colors(mapping_value = 9,     keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 4)

        self._test_bank_colors(mapping_value = 10,    keep_bank = False, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 5)
        self._test_bank_colors(mapping_value = 11,    keep_bank = False, exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 3, exp_text_rig = 1)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,    keep_bank = False, exp_color = BANK_COLORS[4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 125, exp_text_rig = 4)

        # Current (keeping bank)
        self._test_bank_colors(mapping_value = None,  keep_bank = True, exp_color = None, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = None, exp_text_rig = None)
        
        self._test_bank_colors(mapping_value = 0,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 1,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 2)
        self._test_bank_colors(mapping_value = 2,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 3)
        self._test_bank_colors(mapping_value = 3,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 4)
        self._test_bank_colors(mapping_value = 4,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 1, exp_text_rig = 5)
        
        self._test_bank_colors(mapping_value = 5,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 6,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 2)
        self._test_bank_colors(mapping_value = 7,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 3)
        self._test_bank_colors(mapping_value = 8,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 4)
        self._test_bank_colors(mapping_value = 9,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 2, exp_text_rig = 5)

        self._test_bank_colors(mapping_value = 10,    keep_bank = True, exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 3, exp_text_rig = 1)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,  keep_bank = False, exp_color = BANK_COLORS[4], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, exp_text_bank = 125, exp_text_rig = 5)

        # Target (keeping bank)
        self._test_bank_colors(mapping_value = None,  keep_bank = True, exp_color = None, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = None, exp_text_rig = None)
        
        self._test_bank_colors(mapping_value = 0,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 1,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 2,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 2)
        self._test_bank_colors(mapping_value = 3,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 3)
        self._test_bank_colors(mapping_value = 4,     keep_bank = True, exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 1, exp_text_rig = 4)
        
        self._test_bank_colors(mapping_value = 5,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 6,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 7,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 2)
        self._test_bank_colors(mapping_value = 8,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 3)
        self._test_bank_colors(mapping_value = 9,     keep_bank = True, exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 2, exp_text_rig = 4)

        self._test_bank_colors(mapping_value = 10,    keep_bank = True, exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 3, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 11,    keep_bank = True, exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 3, exp_text_rig = 1)
        self._test_bank_colors(mapping_value = 12,    keep_bank = True, exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 3, exp_text_rig = 2)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,    keep_bank = True, exp_color = BANK_COLORS[4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, exp_text_bank = 125, exp_text_rig = 4)


    def _test_bank_colors(self, mapping_value, keep_bank, exp_color, display_mode, exp_text_bank, exp_text_rig):
        # With label but no text callback 
        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode,
            exp_text_bank = exp_text_bank,
            exp_text_rig = exp_text_rig,
            keep_bank = keep_bank
        )

        # Without text callback and label
        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode,
            keep_bank = keep_bank
        )

        # With text callback and label
        if mapping_value != None:
            self._test_bank_colors_with_label_and_cb(
                mapping_value = mapping_value,
                exp_color = exp_color,
                display_mode = display_mode,
                exp_text_bank = exp_text_bank,
                exp_text_rig = exp_text_rig,
                keep_bank = keep_bank
            )


    def _do_test_bank_colors_without_label(self, mapping_value, keep_bank, display_mode, exp_color):    
        ecb = MockEnabledCallback(output = True)

        action = RIG_DOWN(
            display_mode = display_mode, 
            keep_bank = keep_bank,
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )
        
        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigChangeCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color if exp_color else DEFAULT_SWITCH_COLOR)
        self.assertEqual(switch.brightness, 0.3)
        

    def _do_test_bank_colors_with_label(self, mapping_value, keep_bank, display_mode, exp_color, exp_text_bank, exp_text_rig):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = RIG_DOWN(
            keep_bank = keep_bank,
            display = display,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigChangeCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color if exp_color else DEFAULT_SWITCH_COLOR)
        self.assertEqual(switch.brightness, 0.3)

        self.assertEqual(display.back_color, exp_color if exp_color else DEFAULT_LABEL_COLOR)

        if mapping_value != None:
            self.assertEqual(display.text, "Rig " + repr(exp_text_bank) + "-" + repr(exp_text_rig))
            

    def _test_bank_colors_with_label_and_cb(self, mapping_value, keep_bank, display_mode, exp_color, exp_text_bank, exp_text_rig):
        self._do_test_bank_colors_with_label_and_text_cb(
            mapping_value = mapping_value,
            display_mode = display_mode,
            exp_color = exp_color,
            exp_text_bank = exp_text_bank, 
            exp_text_rig = exp_text_rig,
            keep_bank = keep_bank
        )

        self._do_test_bank_colors_with_label_and_color_cb(
            mapping_value = mapping_value,
            display_mode = display_mode
        )


    def _do_test_bank_colors_with_label_and_text_cb(self, mapping_value, keep_bank, display_mode, exp_color, exp_text_bank, exp_text_rig):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        def text_cb(action_paramater, bank, rig):
            self.assertEqual(action, action_paramater)
            return repr(bank) + "|" + repr(rig)

        action = RIG_DOWN(
            display = display,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb,
            text_callback = text_cb,
            keep_bank = keep_bank
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigChangeCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.3)

        self.assertEqual(display.back_color, exp_color)

        if mapping_value != None:
            self.assertEqual(display.text, repr(exp_text_bank-1) + "|" + repr(exp_text_rig-1))
            

    def _do_test_bank_colors_with_label_and_color_cb(self, mapping_value, display_mode):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        def color_cb(action_paramater, bank, rig):
            self.assertEqual(action, action_paramater)
            self.assertEqual(rig, mapping_value % 5)
            self.assertEqual(bank, int(mapping_value / 5))

            return (3, 4, 5)

        action = RIG_DOWN(
            display = display,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb,
            color_callback = color_cb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigChangeCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, (3, 4, 5))
        self.assertEqual(switch.brightness, 0.3)

        self.assertEqual(display.back_color, (3, 4, 5))
            

 ###################################################################################################################


    def test_overrides(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = RIG_DOWN(
            display = display,
            id = 45, 
            use_leds = True, 
            display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
            enable_callback = ecb,
            text = "foo",
            color = (5, 6, 7)
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigChangeCallback__mapping 
        
        # On state
        mapping.value = 100
        action.update_displays()
        
        self.assertEqual(switch.color, (5, 6, 7))
        self.assertEqual(switch.brightness, 0.3)

        self.assertEqual(display.back_color, (5, 6, 7))

        self.assertEqual(display.text, "foo")


###################################################################################################################


    def test_invalid_display_mode(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = RIG_DOWN(
            display = display,
            display_mode = self,                   # Invalid value ;)
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigChangeCallback__mapping 
        mapping.value = 0

        with self.assertRaises(Exception):            
            action.update_displays()


############################################################################################################


    def test_messages(self):
        self._test_messages(False)
        self._test_messages(True)

    def _test_messages(self, keep_bank):
        action = RIG_DOWN(
            keep_bank = keep_bank
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperRigChangeCallback__mapping 
        
        mapping.value = 8
        action.update_displays()
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 0
        })

        mapping.value = 6
        action.update_displays()
        
        # Select rig the first time
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 4)
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        mapping.value = 5
        action.update_displays()
        # Select rig on next bank
        action.push()
        action.release()

        if keep_bank:
            self.assertEqual(len(appl.client.set_calls), 4)    
        else:
            self.assertEqual(len(appl.client.set_calls), 7)
            self.assertEqual(appl.client.set_calls[4], {
                "mapping": MAPPING_BANK_SELECT(),
                "value": 0
            })
            self.assertEqual(appl.client.set_calls[5], {
                "mapping": MAPPING_RIG_SELECT(4),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[6], {
                "mapping": MAPPING_RIG_SELECT(4),
                "value": 0
            })

        action.update_displays()

        
############################################################################################################


    def test_get_next_rig(self):
        action = RIG_DOWN(
            keep_bank = False
        )

        get_next_rig = action.callback._KemperRigChangeCallback__get_next_rig

        self.assertEqual(get_next_rig(0, 0), NUM_BANKS * NUM_RIGS_PER_BANK - 1)
        self.assertEqual(get_next_rig(1, 1), 0)
        self.assertEqual(get_next_rig(2, 2), 1)
        self.assertEqual(get_next_rig(3, 3), 2)
        self.assertEqual(get_next_rig(4, 4), 3)
        
        self.assertEqual(get_next_rig(0, 5), 4)
        self.assertEqual(get_next_rig(1, 6), 5)
        self.assertEqual(get_next_rig(2, 7), 6)
        self.assertEqual(get_next_rig(3, 8), 7)
        self.assertEqual(get_next_rig(4, 9), 8)


    def test_get_next_rig_keep_bank(self):
        action = RIG_DOWN(
            keep_bank = True
        )

        get_next_rig = action.callback._KemperRigChangeCallback__get_next_rig

        self.assertEqual(get_next_rig(0, 0), 0)
        self.assertEqual(get_next_rig(1, 1), 0)
        self.assertEqual(get_next_rig(2, 2), 1)
        self.assertEqual(get_next_rig(3, 3), 2)
        self.assertEqual(get_next_rig(4, 4), 3)
        
        self.assertEqual(get_next_rig(0, 5), 5)
        self.assertEqual(get_next_rig(1, 6), 5)
        self.assertEqual(get_next_rig(2, 7), 6)
        self.assertEqual(get_next_rig(3, 8), 7)
        self.assertEqual(get_next_rig(4, 9), 8)
        
        
        