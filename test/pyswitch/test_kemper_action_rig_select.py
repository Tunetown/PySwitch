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
    from lib.pyswitch.colors import Colors

    from lib.pyswitch.clients.kemper.actions.rig_select import *
    from lib.pyswitch.clients.kemper.actions.rig_select_and_morph_state import *
    
    from lib.pyswitch.clients.kemper.mappings.select import *


####################################################################################################


class TestKemperActionDefinitionsRigSelect(unittest.TestCase):

    def test_bank_colors(self):
        # Current
        self._test_bank_colors(mapping_value = None,  exp_color = Colors.WHITE, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        
        self._test_bank_colors(mapping_value = 0,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 1,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 2,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 3,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 4,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        
        self._test_bank_colors(mapping_value = 5,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 6,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 7,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 8,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 9,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        self._test_bank_colors(mapping_value = 10,    exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,  exp_color = BANK_COLORS[4], display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        # Target
        self._test_bank_colors(mapping_value = None,  exp_color = Colors.WHITE, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        
        self._test_bank_colors(mapping_value = 0,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 1,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 2,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 3,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 4,     exp_color = BANK_COLORS[0], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        
        self._test_bank_colors(mapping_value = 5,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 6,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 7,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 8,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 9,     exp_color = BANK_COLORS[1], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)

        self._test_bank_colors(mapping_value = 10,    exp_color = BANK_COLORS[2], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,    exp_color = BANK_COLORS[4], display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)


    def _test_bank_colors(self, mapping_value, exp_color, display_mode):
        # With label but no text callback 
        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode,
            rig = mapping_value % 5 + 2 if mapping_value != None else 0,
            rig_off = None,
            exp_enlightened = False
        )

        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode,
            rig = mapping_value % 5 + 1 if mapping_value != None else 0,
            rig_off = None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode,
            rig = mapping_value % 5 + 1 if mapping_value != None else 0,
            rig_off = mapping_value % 5 + 2 if mapping_value != None else None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        # Without text callback and label
        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode,
            rig = mapping_value % 5 + 2 if mapping_value != None else 0,
            rig_off = None,
            exp_enlightened = False
        )

        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode,
            rig = mapping_value % 5 + 1 if mapping_value != None else 0,
            rig_off = None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            exp_color = exp_color,
            display_mode = display_mode,
            rig = mapping_value % 5 + 1 if mapping_value != None else 0,
            rig_off = mapping_value % 5 + 2 if mapping_value != None else None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        # With text callback and label
        if mapping_value != None:
            self._test_bank_colors_with_label_and_cb(
                mapping_value = mapping_value,
                exp_color = exp_color,
                display_mode = display_mode,
                rig = mapping_value % 5 + 2 if mapping_value != None else 0,
                rig_off = None,
                exp_enlightened = False
            )

            self._test_bank_colors_with_label_and_cb(
                mapping_value = mapping_value,
                exp_color = exp_color,
                display_mode = display_mode,
                rig = mapping_value % 5 + 1 if mapping_value != None else 0,
                rig_off = None,
                exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
            )

            self._test_bank_colors_with_label_and_cb(
                mapping_value = mapping_value,
                exp_color = exp_color,
                display_mode = display_mode,
                rig = mapping_value % 5 + 1 if mapping_value != None else 0,
                rig_off = mapping_value % 5 + 2 if mapping_value != None else None,
                exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
            )


    def _do_test_bank_colors_without_label(self, mapping_value, rig, rig_off, display_mode, exp_color, exp_enlightened):    
        ecb = MockEnabledCallback(output = True)

        action = RIG_SELECT(
            rig = rig, 
            rig_off = rig_off,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )
        
        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.3 if exp_enlightened else 0.02)
        

    def _do_test_bank_colors_with_label(self, mapping_value, rig, rig_off, display_mode, exp_color, exp_enlightened):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = RIG_SELECT(
            display = display,
            rig = rig, 
            rig_off = rig_off,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.3 if exp_enlightened else 0.02)

        factor = 1 if exp_enlightened else 0.2

        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor),
            int(exp_color[1] * factor),
            int(exp_color[2] * factor)
        ))

        if mapping_value != None:
            if display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
                self.assertEqual(display.text, "Rig " + repr(int(mapping_value / 5) + 1) + "-" + repr(mapping_value % 5 + 1))
            else:
                if rig_off != None and mapping_value % 5 + 1 != rig_off:                
                    self.assertEqual(display.text, "Rig " + repr(int(mapping_value / 5) + 1) + "-" + repr(rig_off))
                else:
                    self.assertEqual(display.text, "Rig " + repr(int(mapping_value / 5) + 1) + "-" + repr(rig))                


    def _test_bank_colors_with_label_and_cb(self, mapping_value, rig, rig_off, display_mode, exp_color, exp_enlightened):
        self._do_test_bank_colors_with_label_and_text_cb(
            mapping_value = mapping_value,
            rig = rig,
            rig_off = rig_off,
            display_mode = display_mode,
            exp_color = exp_color,
            exp_enlightened = exp_enlightened
        )

        self._do_test_bank_colors_with_label_and_color_cb(
            mapping_value = mapping_value,
            rig = rig,
            rig_off = rig_off,
            display_mode = display_mode,
            exp_enlightened = exp_enlightened
        )


    def _do_test_bank_colors_with_label_and_text_cb(self, mapping_value, rig, rig_off, display_mode, exp_color, exp_enlightened):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        def text_cb(action_paramater, bank, rig):
            self.assertEqual(action, action_paramater)
            return repr(bank) + "|" + repr(rig)

        action = RIG_SELECT(
            display = display,
            rig = rig, 
            rig_off = rig_off,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb,
            text_callback = text_cb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.3 if exp_enlightened else 0.02)

        factor = 1 if exp_enlightened else 0.2

        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor),
            int(exp_color[1] * factor),
            int(exp_color[2] * factor)
        ))

        if mapping_value != None:
            if display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
                self.assertEqual(display.text, repr(int(mapping_value / 5)) + "|" + repr(mapping_value % 5))
            else:
                if rig_off != None and mapping_value % 5 + 1 != rig_off:                
                    self.assertEqual(display.text, repr(int(mapping_value / 5)) + "|" + repr(rig_off - 1))
                else:
                    self.assertEqual(display.text, repr(int(mapping_value / 5)) + "|" + repr(rig - 1))    
 

    def _do_test_bank_colors_with_label_and_color_cb(self, mapping_value, rig, rig_off, display_mode, exp_enlightened):
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

        action = RIG_SELECT(
            display = display,
            rig = rig, 
            rig_off = rig_off,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb,
            color_callback = color_cb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, (3, 4, 5))
        self.assertEqual(switch.brightness, 0.3 if exp_enlightened else 0.02)

        factor = 1 if exp_enlightened else 0.2

        self.assertEqual(display.back_color, (
            int((3, 4, 5)[0] * factor),
            int((3, 4, 5)[1] * factor),
            int((3, 4, 5)[2] * factor)
        ))
            

 ###################################################################################################################


    def test_overrides(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = RIG_SELECT(
            display = display,
            rig = 1, 
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

        mapping = action.callback._KemperRigSelectCallback__mapping 
        
        # On state
        mapping.value = NUM_RIGS_PER_BANK * 2
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        self.assertEqual(switch.color, (5, 6, 7))
        self.assertEqual(switch.brightness, 0.3)

        self.assertEqual(display.back_color, (5, 6, 7))

        self.assertEqual(display.text, "foo")

        # Off state
        mapping.value = 2
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        self.assertEqual(switch.color, (5, 6, 7))
        self.assertEqual(switch.brightness, 0.02)

        self.assertEqual(display.back_color, (
            int((5, 6, 7)[0] * 0.2),
            int((5, 6, 7)[1] * 0.2),
            int((5, 6, 7)[2] * 0.2)
        ))

        self.assertEqual(display.text, "foo")


###################################################################################################################

    def test_rig_btn_morph(self):
        self._test_rig_btn_morph(preselect = False)
        self._test_rig_btn_morph(preselect = True)

    def _test_rig_btn_morph(self, preselect):
        action = RIG_SELECT(
            rig = 1,
            rig_btn_morph = True
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperRigSelectCallback__mapping 

        self.assertNotIn("morphStateOverride", appl.shared)
        
        # Select rig the first time
        mapping.value = 1   # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 16383)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 16383)

        # Select rig the first time
        mapping.value = 1   # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 16383)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        if preselect:
            appl.shared["preselectedBank"] = 56

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()        
        self.assertEqual(action.callback.state, True)

        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 16383 if not preselect else 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0 if not preselect else 16383)


###################################################################################################################

    def test_rig_btn_morph_momentary(self):
        action = RIG_SELECT(
            rig = 1,
            rig_btn_morph = True,
            momentary_morph = True
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperRigSelectCallback__mapping 

        self.assertNotIn("morphStateOverride", appl.shared)
        
        # Select rig the first time
        mapping.value = 1   # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        action.push()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()

        self.assertEqual(appl.shared["morphStateOverride"], 16383)

        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()

        self.assertEqual(appl.shared["morphStateOverride"], 16383)

        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()
        
        self.assertEqual(appl.shared["morphStateOverride"], 16383)

        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig the first time
        mapping.value = 1   # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        action.push()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()

        self.assertEqual(appl.shared["morphStateOverride"], 16383)

        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        # Select rig again 
        mapping.value = 0   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        action.push()

        self.assertEqual(appl.shared["morphStateOverride"], 16383)

        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)


###################################################################################################################


    def test_invalid_display_mode(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = RIG_SELECT(
            display = display,
            rig = 1,
            display_mode = self,                   # Invalid value ;)
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping 
        mapping.value = 0

        with self.assertRaises(Exception):            
            action.update_displays()


###################################################################################################################


    def test_bank_colors_with_preselect(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = RIG_SELECT(
            display = display,
            rig = 3, 
            display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
        )        

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping 

        # Normal        
        mapping.value = 5 # Off rig
        exp_color = BANK_COLORS[1]

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.02)

        factor = 0.2
        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor),
            int(exp_color[1] * factor),
            int(exp_color[2] * factor)
        ))

        # With preselect
        exp_color = BANK_COLORS[0]
        appl.shared = { "preselectedBank": 0 }
        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.02)

        factor = 0.2
        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor),
            int(exp_color[1] * factor),
            int(exp_color[2] * factor)
        ))

        # With preselect (other bank)
        exp_color = BANK_COLORS[4]
        appl.shared = { "preselectedBank": 9 }
        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.02)

        factor = 0.2
        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor),
            int(exp_color[1] * factor),
            int(exp_color[2] * factor)
        ))
        
###################################################################################################################


    def test_messages(self):
        for rig in range(NUM_RIGS_PER_BANK):
            self._test_messages(rig)

    def _test_messages(self, rig):
        action = RIG_SELECT(
            rig = rig + 1
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperRigSelectCallback__mapping 
        
        mapping.value = None
        self.assertEqual(action.callback.state, False)

        mapping.value = rig + 1   # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        # Select rig the first time
        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 0
        })

        mapping.value = rig   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select rig again 
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 4)
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 0
        })

        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Receive other rig
        mapping.value = rig + 11  # Not matching
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 4)


###################################################################################################################

    def test_messages_rig_off(self):
        for bank in range(NUM_BANKS):
            self._test_messages_rig_off(bank)

    def _test_messages_rig_off(self, bank):
        action = RIG_SELECT(
            rig = 1,   
            rig_off = 3
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping   

        mapping.value = bank * NUM_RIGS_PER_BANK + 3   # Not matching (Rig 3)
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        # Select on rig
        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 4)
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK + 2  # Off rig
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        # Select on rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[4], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[5], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK  # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Receive any other rigs
        mapping.value = bank * NUM_RIGS_PER_BANK + 1
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        mapping.value = 1
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 6)


###################################################################################################################

    def test_messages_rig_none(self):
        for curr_bank in range(NUM_BANKS):
            for curr_rig in range(NUM_RIGS_PER_BANK):
                self._test_messages_rig_none(curr_bank, curr_rig, RIG_SELECT_DISPLAY_CURRENT_RIG, None)
                self._test_messages_rig_none(curr_bank, curr_rig, RIG_SELECT_DISPLAY_TARGET_RIG, None)

                self._test_messages_rig_none(curr_bank, curr_rig, RIG_SELECT_DISPLAY_CURRENT_RIG, 2)
                self._test_messages_rig_none(curr_bank, curr_rig, RIG_SELECT_DISPLAY_TARGET_RIG, 2)

    def _test_messages_rig_none(self, curr_bank, curr_rig, display_mode, bank):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = RIG_SELECT(
            display = display,
            display_mode = display_mode,
            rig = None,
            bank = bank
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping

        mapping.value = curr_bank * NUM_RIGS_PER_BANK + curr_rig
        action.update_displays()

        self.assertEqual(action.callback.state, False)
        self.assertEqual(display.text, "Rig " + repr((curr_bank + 1) if bank == None or display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG else bank) + "-" + repr(curr_rig + 1), f"{ curr_bank }-{ curr_rig }")
        
        appl.update()

        # Trigger
        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        if bank == None:
            self.assertEqual(len(appl.client.set_calls), 2)
            self.assertEqual(appl.client.set_calls[0], {
                "mapping": MAPPING_RIG_SELECT(curr_rig),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[1], {
                "mapping": MAPPING_RIG_SELECT(curr_rig),
                "value": 0
            })
        else:
            self.assertEqual(len(appl.client.set_calls), 3)
            self.assertEqual(appl.client.set_calls[0], {
                "mapping": MAPPING_BANK_SELECT(),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[1], {
                "mapping": MAPPING_RIG_SELECT(curr_rig),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[2], {
                "mapping": MAPPING_RIG_SELECT(curr_rig),
                "value": 0
            })

        action.update_displays()

        self.assertEqual(action.callback.state, False)
        self.assertEqual(display.text, "Rig " + repr((curr_bank + 1) if bank == None or display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG else bank) + "-" + repr(curr_rig + 1), f"{ curr_bank }-{ curr_rig }")

        # Trigger again
        action.push()
        action.release()

        if bank == None:
            self.assertEqual(len(appl.client.set_calls), 4)
            self.assertEqual(appl.client.set_calls[2], {
                "mapping": MAPPING_RIG_SELECT(curr_rig),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[3], {
                "mapping": MAPPING_RIG_SELECT(curr_rig),
                "value": 0
            })
        else:
            self.assertEqual(len(appl.client.set_calls), 6)
            self.assertEqual(appl.client.set_calls[3], {
                "mapping": MAPPING_BANK_SELECT(),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[4], {
                "mapping": MAPPING_RIG_SELECT(curr_rig),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[5], {
                "mapping": MAPPING_RIG_SELECT(curr_rig),
                "value": 0
            })

        mapping.value = curr_bank * NUM_RIGS_PER_BANK + 2  # Off rig
        action.update_displays()

        self.assertEqual(action.callback.state, False)
        self.assertEqual(display.text, "Rig " + repr((curr_bank + 1) if bank == None or display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG else bank) + "-3")

        # Trigger again
        action.push()
        action.release()

        if bank == None:
            self.assertEqual(len(appl.client.set_calls), 6)
            self.assertEqual(appl.client.set_calls[4], {
                "mapping": MAPPING_RIG_SELECT(2),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[5], {
                "mapping": MAPPING_RIG_SELECT(2),
                "value": 0
            })
        else:
            self.assertEqual(len(appl.client.set_calls), 9)
            self.assertEqual(appl.client.set_calls[6], {
                "mapping": MAPPING_BANK_SELECT(),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[7], {
                "mapping": MAPPING_RIG_SELECT(2),
                "value": 1
            })
            self.assertEqual(appl.client.set_calls[8], {
                "mapping": MAPPING_RIG_SELECT(2),
                "value": 0
            })

        if display_mode == RIG_SELECT_DISPLAY_TARGET_RIG:            
            appl.shared["preselectedBank"] = 4

            action.update_displays()

            self.assertEqual(action.callback.state, False)
            self.assertEqual(display.text, "Rig 5-3")


############################################################################################################


    def test_rig_select_and_morph_enabled(self):
        self._test_rig_select_and_morph_enabled(False)
        self._test_rig_select_and_morph_enabled(True)


    def _test_rig_select_and_morph_enabled(self, morph_only_when_enabled):
        ecb = MockEnabledCallback()

        action_select, action_morph = RIG_SELECT_AND_MORPH_STATE(
            rig = 1,
            rig_off = 2,
            use_leds = True, 
            enable_callback = ecb,     
            color = (2, 4, 6),
            morph_only_when_enabled = morph_only_when_enabled        
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action_select])
        action_select.init(appl, switch)

        mapping_rig = action_select.callback._KemperRigSelectCallback__mapping 
        
        mapping_rig.value = 4  # off value
        ecb.output = False
        action_select.push()
        action_select.release()

        self.assertEqual(action_select.enabled, False)
        self.assertEqual(action_morph.enabled, False)

        ecb.output = True
        action_select.push()
        action_select.release()

        self.assertEqual(action_select.enabled, True)
        self.assertEqual(action_morph.enabled, False if morph_only_when_enabled else True)

        mapping_rig.value = 0  # on value
        action_select.push()
        action_select.release()

        self.assertEqual(action_select.enabled, True)
        self.assertEqual(action_morph.enabled, True)

        mapping_rig.value = 4  # off value
        action_select.push()
        action_select.release()
        
        self.assertEqual(action_select.enabled, True)
        self.assertEqual(action_morph.enabled, False if morph_only_when_enabled else True)

        ecb.output = False
        action_select.push()
        action_select.release()

        self.assertEqual(action_select.enabled, False)
        self.assertEqual(action_morph.enabled, False)


############################################################################################################

    def test_auto_rig_off(self):
        bank = 0
        action = RIG_SELECT(
            rig = 3,
            rig_off = "auto"
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping   

        mapping.value = bank * NUM_RIGS_PER_BANK + 1   # Not matching (Rig 2)
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        # Select on rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK + 2   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 4)
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK + 4  # Off rig
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        # Select on rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[4], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[5], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK + 2 # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 8)
        self.assertEqual(appl.client.set_calls[6], {
            "mapping": MAPPING_RIG_SELECT(4),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[7], {
            "mapping": MAPPING_RIG_SELECT(4),
            "value": 0
        })

############################################################################################################

    def test_auto_rig_off_with_exclude_rigs(self):
        self._test_auto_rig_off_with_exclude_rigs((3, 4))
        self._test_auto_rig_off_with_exclude_rigs((8, 3, 99, 4))
        self._test_auto_rig_off_with_exclude_rigs([4, 3])
        self._test_auto_rig_off_with_exclude_rigs([3, 4, 9, 10])


    def _test_auto_rig_off_with_exclude_rigs(self, exclude_rigs):
        bank = 0
        action = RIG_SELECT(
            rig = 3,
            rig_off = "auto",
            auto_exclude_rigs = exclude_rigs
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperRigSelectCallback__mapping   

        mapping.value = bank * NUM_RIGS_PER_BANK + 1   # Not matching (Rig 2)
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        # Select on rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 0
        })
        
        mapping.value = bank * NUM_RIGS_PER_BANK + 2   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()
        
        self.assertEqual(len(appl.client.set_calls), 4)
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK + 3  # Off rig (excluded)
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        # Select on rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[4], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[5], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK + 2 # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 8)
        self.assertEqual(appl.client.set_calls[6], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[7], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 0
        })

        mapping.value = bank * NUM_RIGS_PER_BANK + 3  # Off rig (excluded)
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        # Select on rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 10)
        self.assertEqual(appl.client.set_calls[8], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[9], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 0
        })


#################################################################################################


    def test_mapping_none(self):
        action = RIG_SELECT(
            rig = 1
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperRigSelectCallback__mapping 
        
        mapping.value = None
        self.assertEqual(action.callback.state, False)

        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        # Select rig the first time
        action.push()
        action.release()

        self.assertEqual(action.callback.state, False)
        self.assertEqual(appl.shared["morphStateOverride"], 0)

        self.assertEqual(len(appl.client.set_calls), 2)
