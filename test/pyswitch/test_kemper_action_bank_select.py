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

    from lib.pyswitch.clients.kemper.actions.bank_select import *
    from lib.pyswitch.clients.kemper.actions.rig_select import *
    from lib.pyswitch.clients.kemper.mappings.select import *
    

####################################################################################################


class TestKemperActionDefinitionsBankSelect(unittest.TestCase):

    def test_bank_colors(self):
        # Current
        self._test_bank_colors(mapping_value = None,  display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        
        self._test_bank_colors(mapping_value = 0,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 1,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 2,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 3,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 4,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        
        self._test_bank_colors(mapping_value = 5,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 6,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 7,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 8,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 9,     display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        self._test_bank_colors(mapping_value = 10,    display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,  display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        # Target
        self._test_bank_colors(mapping_value = None,  display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        
        self._test_bank_colors(mapping_value = 0,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 1,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 2,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 3,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 4,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        
        self._test_bank_colors(mapping_value = 5,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 6,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 7,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 8,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 9,     display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)

        self._test_bank_colors(mapping_value = 10,    display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1,    display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)


    def _test_bank_colors(self, mapping_value, display_mode):
        # With label but no text callback 
        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            bank = mapping_value // 5 + 2 if mapping_value != None else 0,
            bank_off = None,
            exp_enlightened = False
        )

        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            bank = mapping_value // 5 + 1 if mapping_value != None else 0,
            bank_off = None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            bank = mapping_value // 5 + 1 if mapping_value != None else 0,
            bank_off = mapping_value // 5 + 2 if mapping_value != None else None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        # Without text callback and label
        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            bank = mapping_value // 5 + 2 if mapping_value != None else 0,
            bank_off = None,
            exp_enlightened = False
        )

        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            bank = mapping_value // 5 + 1 if mapping_value != None else 0,
            bank_off = None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            bank = mapping_value // 5 + 1 if mapping_value != None else 0,
            bank_off = mapping_value // 5 + 2 if mapping_value != None else None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        # With text callback and label
        if mapping_value != None:
            self._test_bank_colors_with_label_and_cb(
                mapping_value = mapping_value,
                display_mode = display_mode,
                bank = mapping_value // 5 + 2 if mapping_value != None else 0,
                bank_off = None,
                exp_enlightened = False
            )

            self._test_bank_colors_with_label_and_cb(
                mapping_value = mapping_value,
                display_mode = display_mode,
                bank = mapping_value // 5 + 1 if mapping_value != None else 0,
                bank_off = None,
                exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
            )

            self._test_bank_colors_with_label_and_cb(
                mapping_value = mapping_value,
                display_mode = display_mode,
                bank = mapping_value // 5 + 1 if mapping_value != None else 0,
                bank_off = mapping_value // 5 + 2 if mapping_value != None else None,
                exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
            )


    def _get_exp_color(self, mapping_value, display_mode, bank, bank_off):
        if mapping_value == None:
            return Colors.WHITE
        
        if display_mode == RIG_SELECT_DISPLAY_TARGET_RIG:
            if bank_off != None and (int(mapping_value / 5) == bank - 1):
                return BANK_COLORS[(bank_off - 1) % 5]
            else:
                return BANK_COLORS[(bank - 1) % 5]
        
        return BANK_COLORS[int(mapping_value / 5) % 5]
    
        
    def _do_test_bank_colors_without_label(self, mapping_value, bank, bank_off, display_mode, exp_enlightened):    
        ecb = MockEnabledCallback(output = True)

        exp_color = self._get_exp_color(mapping_value, display_mode, bank, bank_off)

        action = BANK_SELECT(
            bank = bank, 
            bank_off = bank_off,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )
        
        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperBankSelectCallback__mapping 
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.3 if exp_enlightened else 0.02)
        

    def _do_test_bank_colors_with_label(self, mapping_value, bank, bank_off, display_mode, exp_enlightened):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        exp_color = self._get_exp_color(mapping_value, display_mode, bank, bank_off)

        ecb = MockEnabledCallback(output = True)

        action = BANK_SELECT(
            display = display,
            bank = bank, 
            bank_off = bank_off,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperBankSelectCallback__mapping 
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
                self.assertEqual(display.text, "Bank " + repr(int(mapping_value / 5) + 1))
            else:
                if bank_off != None and mapping_value // 5 + 1 != bank_off:                
                    self.assertEqual(display.text, "Bank " + repr(bank_off))
                else:
                    self.assertEqual(display.text, "Bank " + repr(bank))             


    def _test_bank_colors_with_label_and_cb(self, mapping_value, bank, bank_off, display_mode, exp_enlightened):
        self._do_test_bank_colors_with_label_and_text_cb(
            mapping_value = mapping_value,
            bank = bank, 
            bank_off = bank_off,
            display_mode = display_mode,
            exp_enlightened = exp_enlightened
        )

        self._do_test_bank_colors_with_label_and_color_cb(
            mapping_value = mapping_value,
            bank = bank, 
            bank_off = bank_off,
            display_mode = display_mode,
            exp_enlightened = exp_enlightened
        )


    def _do_test_bank_colors_with_label_and_text_cb(self, mapping_value, bank, bank_off, display_mode, exp_enlightened):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        exp_color = self._get_exp_color(mapping_value, display_mode, bank, bank_off)

        ecb = MockEnabledCallback(output = True)

        def text_cb(action_paramater, bank, rig):
            self.assertEqual(action, action_paramater)
            return repr(bank) + "|" + repr(rig)

        action = BANK_SELECT(
            display = display,
            bank = bank, 
            bank_off = bank_off,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb,
            text_callback = text_cb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperBankSelectCallback__mapping 
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
                if bank_off != None and mapping_value // 5 + 1 != bank_off:                
                    self.assertEqual(display.text, repr(int(bank_off - 1)) + "|" + repr(mapping_value % 5))
                else:
                    self.assertEqual(display.text, repr(int(bank - 1)) + "|" + repr(mapping_value % 5))    
 

    def _do_test_bank_colors_with_label_and_color_cb(self, mapping_value, bank, bank_off, display_mode, exp_enlightened):
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

        action = BANK_SELECT(
            display = display,
            bank = bank, 
            bank_off = bank_off,
            display_mode = display_mode, 
            id = 45, 
            use_leds = True, 
            enable_callback = ecb,
            color_callback = color_cb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperBankSelectCallback__mapping 
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

        action = BANK_SELECT(
            display = display,
            bank = 1, 
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

        mapping = action.callback._KemperBankSelectCallback__mapping 
        
        # On state
        mapping.value = 3
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        self.assertEqual(switch.color, (5, 6, 7))
        self.assertEqual(switch.brightness, 0.3)

        self.assertEqual(display.back_color, (5, 6, 7))

        self.assertEqual(display.text, "foo")

        # Off state
        mapping.value = 22
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


    def test_invalid_display_mode(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = BANK_SELECT(
            display = display,
            bank = 1,
            display_mode = self,                   # Invalid value ;)
            id = 45, 
            use_leds = True, 
            enable_callback = ecb
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperBankSelectCallback__mapping 
        mapping.value = 0

        with self.assertRaises(Exception):            
            action.update_displays()


###################################################################################################################


    def test_messages(self):
        self._test_messages(0)
        self._test_messages(1)
        self._test_messages(2)
        self._test_messages(3)
        self._test_messages(4)


    def _test_messages(self, rig):
        action = BANK_SELECT(
            bank = 1            
        )

        appl = MockController()
        appl.shared = { "preselectedBank": 667 }
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperBankSelectCallback__mapping 
        
        mapping.value = 10 + rig   # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        # Select rig the first time
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 3)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 0
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 0
        })

        mapping.value = rig   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select rig again 
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 0
        })
        self.assertEqual(appl.client.set_calls[4], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[5], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 0
        })

        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Receive other rig
        mapping.value = rig + 20  # Not matching
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 6)

        self.assertEqual(appl.shared["morphStateOverride"], 0)
        self.assertNotIn("preselectedBank", appl.shared)


###################################################################################################################


    def test_messages_bank_off(self):
        self._test_messages_bank_off(0)
        self._test_messages_bank_off(1)
        self._test_messages_bank_off(2)
        self._test_messages_bank_off(3)
        self._test_messages_bank_off(4)


    def _test_messages_bank_off(self, rig):
        action = BANK_SELECT(
            bank = 2,
            bank_off = 4           
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperBankSelectCallback__mapping 
        
        mapping.value = 10 + rig   # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        # Select rig the first time
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 3)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 0
        })

        mapping.value = 5 + rig   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Receive other rig
        mapping.value = rig + 20  # Not matching
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 3)

        # Select rig again 
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[4], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[5], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 0
        })

        mapping.value = 5 + rig   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 9)
        self.assertEqual(appl.client.set_calls[6], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 3
        })
        self.assertEqual(appl.client.set_calls[7], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[8], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 0
        })

        mapping.value = 15 + rig   # Off rig
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        action.update_displays()
        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 9)


###################################################################################################################

    def test_preselect(self):
        self._test_preselect(display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, bank_off = None)
        self._test_preselect(display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG, bank_off = 3)
        self._test_preselect(display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, bank_off = None)
        self._test_preselect(display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, bank_off = 5)


    def _test_preselect(self, display_mode, bank_off):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = BANK_SELECT(
            display = display,
            bank = 2,
            bank_off = bank_off,
            preselect = True,
            display_mode = display_mode        
        )

        action_other = MockAction()

        action_rig_select = RIG_SELECT(
            rig = 2,
            display_mode = display_mode
        )

        switch_1 = MockFootswitch(actions = [action_other, action_rig_select])
        switch_2 = MockFootswitch(actions = [action])
        appl = MockController(inputs = [
            switch_1,
            MockInputControllerDefinition(),
            switch_2,
            MockInputControllerDefinition()
        ])
        action.init(appl, switch_2)
        action_rig_select.init(appl, switch_1)
        
        mapping = action.callback._KemperBankSelectCallback__mapping 
        mapping_rigsel = action_rig_select.callback._KemperRigSelectCallback__mapping 
        
        mapping.value = 10   # Off rig
        mapping_rigsel.value = mapping.value

        exp_color = BANK_COLORS[2] if display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG else BANK_COLORS[1]
        action.update_displays()
        action_rig_select.update()
        self.assertEqual(action.callback.state, False)
        
        self._check_blinking(
            action = action, 
            switch = switch_2, 
            display = display, 
            exp_color = exp_color, 
            should_blink = False, 
            action_rig_select = action_rig_select,
            switch_rig_select = switch_1,
            rig_switch_should_blink = False
        )
        
        # Select rig the first time
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 1)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 1
        })
        
        self._check_blinking(
            action = action, 
            switch = switch_2, 
            display = display, 
            exp_color = exp_color, 
            should_blink = (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG),
            action_rig_select = action_rig_select,
            switch_rig_select = switch_1,
            rig_switch_should_blink = True
        )
        
        mapping.value = 6   # On rig 
        
        exp_color = BANK_COLORS[1]
        action.update_displays()
        action_rig_select.update()
        self.assertEqual(action.callback.state, True) 

        # Select rig again
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 1
        })

        self._check_blinking(
            action = action, 
            switch = switch_2, 
            display = display, 
            exp_color = exp_color, 
            should_blink = (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG),
            action_rig_select = action_rig_select,
            switch_rig_select = switch_1,
            rig_switch_should_blink = True
        )

        appl.shared = {}  # Remove preselect mark
                
        self._check_blinking(
            action = action, 
            switch = switch_2, 
            display = display, 
            exp_color = exp_color, 
            should_blink = False,
            action_rig_select = action_rig_select,
            switch_rig_select = switch_1,
            rig_switch_should_blink = False
        )
        
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Receive other rig
        mapping.value = 20  # Off rig
        
        exp_color = BANK_COLORS[4] if display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG else BANK_COLORS[1]
        action.update_displays()
        action_rig_select.update()

        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 2)

        self._check_blinking(
            action = action, 
            switch = switch_2, 
            display = display, 
            exp_color = exp_color, 
            should_blink = False,
            action_rig_select = action_rig_select,
            switch_rig_select = switch_1,
            rig_switch_should_blink = False
        )
        

###################################################################################################################


    def test_preselect_same(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = BANK_SELECT(
            display = display,
            bank = 2,
            preselect = True,
            display_mode = RIG_SELECT_DISPLAY_TARGET_RIG        
        )

        action_other = MockAction()

        switch_1 = MockFootswitch(actions = [action_other])
        switch_2 = MockFootswitch(actions = [action])
        appl = MockController(inputs = [
            switch_1,
            MockInputControllerDefinition(),
            switch_2,
            MockInputControllerDefinition()
        ])
        action.init(appl, switch_2)
        
        mapping = action.callback._KemperBankSelectCallback__mapping 
        
        mapping.value = 8   # On rig
        exp_color = BANK_COLORS[1]
        action.update_displays()
        self.assertEqual(action.callback.state, True)
        
        self._check_blinking(action, switch_2, display, exp_color, False, exp_state = True)

        # Select rig the first time
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 1)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 1
        })
        
        self._check_blinking(action, switch_2, display, exp_color, False, exp_state = True)
        
        # Receive other rig
        mapping.value = 20  # Off rig
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 1)

        self._check_blinking(action, switch_2, display, exp_color, False, exp_state = False)


###################################################################################################################


    def test_midi_channels(self):
        for channel in range(16):
            self._test_midi_channel(channel)


    def _test_midi_channel(self, channel):
        action = BANK_SELECT(
            bank = 1,
            midi_channel = channel + 1
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)
        
        mapping = action.callback._KemperBankSelectCallback__mapping 
        
        mapping.value = 1
        action.update_displays()
        
        # Select rig the first time
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 3)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_BANK_SELECT(channel),
            "value": 0
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(1, channel),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(1, channel),
            "value": 0
        })


#######################################################################################


    # Checks if the LEDs are blinking
    def _check_blinking(self, 
                        action, 
                        switch, 
                        display,
                        exp_color, 
                        should_blink, 
                        exp_state = None, 
                        action_rig_select = None, 
                        switch_rig_select = None, 
                        rig_switch_should_blink = False
        ):
        cb = action.callback

        if action_rig_select:
            cb_rigsel = action_rig_select.callback

        brightness_off = cb._KemperBankSelectCallback__default_led_brightness_off
        brightness_on = cb._KemperBankSelectCallback__default_led_brightness_on

        if exp_state:
            exp_brightness_off = brightness_on if exp_state else brightness_off
            exp_brightness_on = exp_brightness_off

            factor_off = 1 if exp_state else 0.2
            factor_on = factor_off
        else:
            exp_brightness_off = brightness_off
            exp_brightness_on = brightness_on if should_blink else brightness_off

            factor_off = 0.2
            factor_on = 1 if should_blink else factor_off

        rig_exp_brightness_off = brightness_off
        rig_exp_brightness_on = brightness_on if rig_switch_should_blink else brightness_off

        period = MockPeriodCounter()
        cb._KemperBankSelectCallback__preselect_blink_period = period

        def update():
            cb.update()
            if action_rig_select:
                if rig_switch_should_blink:
                    cb_rigsel.update()
                else:
                    cb_rigsel.update_displays()

        # Off state (initial)
        update()

        self.assertEqual(switch.brightness, exp_brightness_off)
        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor_off),
            int(exp_color[1] * factor_off),
            int(exp_color[2] * factor_off)
        ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_on)

        # Blink on
        period.exceed_next_time = True
        
        update()
        
        self.assertEqual(switch.brightness, exp_brightness_on)
        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor_on),
            int(exp_color[1] * factor_on),
            int(exp_color[2] * factor_on)
        ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_off)

        # Blink off
        period.exceed_next_time = True
                
        update()

        self.assertEqual(switch.brightness, exp_brightness_off)
        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor_off),
            int(exp_color[1] * factor_off),
            int(exp_color[2] * factor_off)
        ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_on)

        # Blink on
        period.exceed_next_time = True
        
        update()

        self.assertEqual(switch.brightness, exp_brightness_on)
        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor_on),
            int(exp_color[1] * factor_on),
            int(exp_color[2] * factor_on)
        ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_off)

        # Blink off
        period.exceed_next_time = True
        
        update()

        self.assertEqual(switch.brightness, exp_brightness_off)
        self.assertEqual(display.back_color, (
            int(exp_color[0] * factor_off),
            int(exp_color[1] * factor_off),
            int(exp_color[2] * factor_off)
        ))

        if action_rig_select:
            self.assertEqual(switch_rig_select.brightness, rig_exp_brightness_on)




