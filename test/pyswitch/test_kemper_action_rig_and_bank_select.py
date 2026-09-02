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


class TestKemperActionDefinitionsRigAndBankSelect(unittest.TestCase):

    def test_display_mode_invalid(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = RIG_SELECT(
            display = display,
            rig = 1,
            display_mode = "ggg",                   # Invalid value ;)
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


    def test_bank_colors(self):
        # Current
        self._test_bank_colors(mapping_value = None,  display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        
        self._test_bank_colors(mapping_value = 0, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 1, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 2, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 3, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 4, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        
        self._test_bank_colors(mapping_value = 5, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 6, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 7, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 8, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)
        self._test_bank_colors(mapping_value = 9, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        self._test_bank_colors(mapping_value = 10, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1, display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG)

        # Target
        self._test_bank_colors(mapping_value = None, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        
        self._test_bank_colors(mapping_value = 0, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 1, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 2, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 3, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 4, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        
        self._test_bank_colors(mapping_value = 5, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 6, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 7, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 8, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)
        self._test_bank_colors(mapping_value = 9, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)

        self._test_bank_colors(mapping_value = 10, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)

        self._test_bank_colors(mapping_value = NUM_BANKS * NUM_RIGS_PER_BANK - 1, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG)


    def _test_bank_colors(self, mapping_value, display_mode):        
        # With label but no text callback 
        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            rig = mapping_value % 5 + 2 if mapping_value != None else 0,
            rig_off = None,
            bank = int(mapping_value / 5) + 2 if mapping_value != None else 0,
            bank_off = None,
            exp_enlightened = False
        )

        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            rig = mapping_value % 5 + 2 if mapping_value != None else 0,
            rig_off = None,
            bank = int(mapping_value / 5) + 1 if mapping_value != None else 0,
            bank_off = None,
            exp_enlightened = False
        )

        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            rig = mapping_value % 5 + 1 if mapping_value != None else 0,
            rig_off = None,
            bank = int(mapping_value / 5) + 1 if mapping_value != None else 0,
            bank_off = None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        self._do_test_bank_colors_with_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            rig = mapping_value % 5 + 1 if mapping_value != None else 0,
            rig_off = mapping_value % 5 + 2 if mapping_value != None else None,
            bank = int(mapping_value / 5) + 1 if mapping_value != None else 0,
            bank_off = int(mapping_value / 5) + 2 if mapping_value != None else 0,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        # Without text callback and label 
        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            rig = mapping_value % 5 + 2 if mapping_value != None else 0,
            rig_off = None,
            bank = int(mapping_value / 5) + 2 if mapping_value != None else 0,
            bank_off = None,            
            exp_enlightened = False
        )

        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            rig = mapping_value % 5 + 1 if mapping_value != None else 0,
            rig_off = None,
            bank = int(mapping_value / 5) + 1 if mapping_value != None else 0,
            bank_off = None,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        self._do_test_bank_colors_without_label(
            mapping_value = mapping_value,
            display_mode = display_mode,
            rig = mapping_value % 5 + 1 if mapping_value != None else 0,
            rig_off = mapping_value % 5 + 2 if mapping_value != None else None,
            bank = int(mapping_value / 5) + 1 if mapping_value != None else 0,
            bank_off = int(mapping_value / 5) + 2 if mapping_value != None else 0,
            exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
        )

        # With text callback and label
        if mapping_value != None:
            self._test_bank_colors_with_label_and_cbs(
                mapping_value = mapping_value,
                display_mode = display_mode,
                rig = mapping_value % 5 + 2 if mapping_value != None else 0,
                rig_off = None,
                bank = int(mapping_value / 5) + 2 if mapping_value != None else 0,
                bank_off = None,            
                exp_enlightened = False
            )

            self._test_bank_colors_with_label_and_cbs(
                mapping_value = mapping_value,
                display_mode = display_mode,
                rig = mapping_value % 5 + 1 if mapping_value != None else 0,
                rig_off = None,
                bank = int(mapping_value / 5) + 1 if mapping_value != None else 0,
                bank_off = None,            
                exp_enlightened = (mapping_value != None) and (display_mode == RIG_SELECT_DISPLAY_TARGET_RIG)
            )

            self._test_bank_colors_with_label_and_cbs(
                mapping_value = mapping_value,
                display_mode = display_mode,
                rig = mapping_value % 5 + 1 if mapping_value != None else 0,
                rig_off = mapping_value % 5 + 2 if mapping_value != None else None,
                bank = int(mapping_value / 5) + 2 if mapping_value != None else 0,
                bank_off = int(mapping_value / 5) + 3 if mapping_value != None else 0,
                exp_enlightened = False
            )

            self._test_bank_colors_with_label_and_cbs(
                mapping_value = mapping_value,
                display_mode = display_mode,
                rig = mapping_value % 5 + 1 if mapping_value != None else 0,
                rig_off = mapping_value % 5 + 2 if mapping_value != None else None,
                bank = int(mapping_value / 5) + 1 if mapping_value != None else 0,
                bank_off = int(mapping_value / 5) + 2 if mapping_value != None else 0,
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


    def _do_test_bank_colors_without_label(self, mapping_value, rig, bank, rig_off, bank_off, display_mode, exp_enlightened):
        ecb = MockEnabledCallback(output = True)

        exp_color = self._get_exp_color(mapping_value, display_mode, bank, bank_off)

        action = RIG_SELECT(
            rig = rig, 
            rig_off = rig_off,
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

        mapping = action.callback._KemperRigSelectCallback__mapping
        mapping.value = mapping_value

        action.update_displays()

        self.assertEqual(switch.color, exp_color)
        self.assertEqual(switch.brightness, 0.3 if exp_enlightened else 0.02)
        

    def _do_test_bank_colors_with_label(self, mapping_value, rig, bank, rig_off, bank_off, display_mode, exp_enlightened):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        exp_color = self._get_exp_color(mapping_value, display_mode, bank, bank_off)

        ecb = MockEnabledCallback(output = True)

        action = RIG_SELECT(
            display = display,
            rig = rig, 
            rig_off = rig_off,
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
                    self.assertEqual(display.text, "Rig " + repr(bank_off) + "-" + repr(rig_off))
                else:
                    self.assertEqual(display.text, "Rig " + repr(bank) + "-" + repr(rig))                


    def _test_bank_colors_with_label_and_cbs(self, mapping_value, rig, bank, rig_off, bank_off, display_mode, exp_enlightened):
        self._do_test_bank_colors_with_label_and_text_cb(
            mapping_value = mapping_value,
            rig = rig,
            bank = bank,
            rig_off = rig_off,
            bank_off = bank_off,
            display_mode = display_mode,
            exp_enlightened = exp_enlightened
        )

        self._do_test_bank_colors_with_label_and_color_cb(
            mapping_value = mapping_value,
            rig = rig,
            bank = bank,
            rig_off = rig_off,
            bank_off = bank_off,
            display_mode = display_mode,
            exp_enlightened = exp_enlightened
        )


    def _do_test_bank_colors_with_label_and_text_cb(self, mapping_value, rig, bank, rig_off, bank_off, display_mode, exp_enlightened):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        exp_color = self._get_exp_color(mapping_value, display_mode, bank, bank_off)

        ecb = MockEnabledCallback(output = True)

        def text_cb(action_parameter, bank, rig):
            self.assertEqual(action, action_parameter)

            return repr(bank) + "|" + repr(rig)

        action = RIG_SELECT(
            display = display,
            rig = rig, 
            rig_off = rig_off,
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
                if rig_off != None and ( mapping_value % 5 == rig - 1 and int(mapping_value / 5) == bank - 1 ):
                    self.assertEqual(display.text, repr(bank_off - 1) + "|" + repr(rig_off - 1))
                else:
                    self.assertEqual(display.text, repr(bank - 1) + "|" + repr(rig - 1))    
 

    def _do_test_bank_colors_with_label_and_color_cb(self, mapping_value, rig, bank, rig_off, bank_off, display_mode, exp_enlightened):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        exp_color = (4, 5, 6)

        ecb = MockEnabledCallback(output = True)

        def color_cb(action_parameter, bank, rig):
            self.assertEqual(action, action_parameter)
            self.assertEqual(bank, int(mapping_value / 5))
            self.assertEqual(rig, mapping_value % 5)

            return exp_color

        action = RIG_SELECT(
            display = display,
            rig = rig, 
            rig_off = rig_off,
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
            bank = 2,
            id = 45, 
            use_leds = True, 
            display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
            enable_callback = ecb,
            color = (7, 8, 9),
            text = "foobar"
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping
        
        # On rig
        mapping.value = 5  
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        self.assertEqual(switch.color, (7, 8, 9))
        self.assertEqual(switch.brightness, 0.3)

        self.assertEqual(display.back_color, (7, 8, 9))

        self.assertEqual(display.text, "foobar")

        # Off rig
        mapping.value = 6  
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        self.assertEqual(switch.color, (7, 8, 9))
        self.assertEqual(switch.brightness, 0.02)

        self.assertEqual(display.back_color, (
            int((7, 8, 9)[0] * 0.2),
            int((7, 8, 9)[1] * 0.2),
            int((7, 8, 9)[2] * 0.2)
        ))

        self.assertEqual(display.text, "foobar")


###################################################################################################################


    def test_messages(self):
        self._test_messages(0)
        self._test_messages(1)
        self._test_messages(2)
        self._test_messages(3)
        self._test_messages(4)


    def _test_messages(self, rig):
        action = RIG_SELECT(
            rig = rig + 1,
            bank = 3
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping        

        mapping.value = rig + 1  # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        # Select rig the first time 
        action.push()
        action.release()

        self.assertEqual(appl.shared["morphStateOverride"], 0)

        self.assertEqual(len(appl.client.set_calls), 3)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 2
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(rig),
            "value": 0
        })

        mapping.value = rig + 10  # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select rig again        
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 2
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
        mapping.value = rig + 11  # Not matching
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 6)


###################################################################################################################


    def test_messages_rig_off(self):
        action = RIG_SELECT(
            rig = 1,
            bank = 2,
            rig_off = 2,
            bank_off = 4
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping
        
        mapping.value = 33   # Not matching
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
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        mapping.value = 5  # On rig
        action.update_displays()

        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 3
        })
        self.assertEqual(appl.client.set_calls[4], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[5], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 0
        })

        mapping.value = 16  # Off rig
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        # Select rig again
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 9)
        self.assertEqual(appl.client.set_calls[6], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[7], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[8], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        mapping.value = 5  # On rig
        action.update_displays()

        self.assertEqual(action.callback.state, True)

        # Select off rig again
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 12)
        self.assertEqual(appl.client.set_calls[9], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 3
        })
        self.assertEqual(appl.client.set_calls[10], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[11], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 0
        })

        action.update_displays()

        self.assertEqual(action.callback.state, True)

        # Other rig selected
        mapping.value = 172  # Not matching
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 12)


###################################################################################################################


    def test_messages_rig_off_with_preselect(self):
        action = RIG_SELECT(
            rig = 1,       # ID 5
            bank = 2,
            rig_off = 2,   # ID 16
            bank_off = 4
        )

        appl = MockController()              
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping
        #mapping_disable = action.callback.mapping_disable

        mapping.value = 33   # Not matching
        action.update_displays()
        self.assertEqual(action.callback.state, False)            

        # Select rig the first time
        appl.shared = { "preselectedBank": 4 }  
        action.push()
        action.release()
        self.assertNotIn("preselectedBank", appl.shared)

        self.assertEqual(len(appl.client.set_calls), 2)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        mapping.value = 5  # On rig
        action.update_displays()

        self.assertEqual(action.callback.state, True)

        # Select off rig
        appl.shared = { "preselectedBank": 4 }  
        action.push()
        action.release()
        self.assertNotIn("preselectedBank", appl.shared)

        self.assertEqual(len(appl.client.set_calls), 4)
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        mapping.value = 16  # Off rig
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        # Select rig again
        appl.shared = { "preselectedBank": 4 }  
        action.push()
        action.release()
        self.assertNotIn("preselectedBank", appl.shared)

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[4], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[5], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        mapping.value = 5  # On rig
        action.update_displays()

        self.assertEqual(action.callback.state, True)

        # Select off rig again
        appl.shared = { "preselectedBank": 4 }  
        action.push()
        action.release()
        self.assertNotIn("preselectedBank", appl.shared)

        self.assertEqual(len(appl.client.set_calls), 8)
        self.assertEqual(appl.client.set_calls[6], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[7], {
            "mapping": MAPPING_RIG_SELECT(0),
            "value": 0
        })

        action.update_displays()

        self.assertEqual(action.callback.state, True)

        # Other rig selected
        mapping.value = 172  # Not matching
        action.update_displays()

        self.assertEqual(action.callback.state, False)

        self.assertEqual(len(appl.client.set_calls), 8)


###################################################################################################################


    def test_invalid_display_mode(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        action = RIG_SELECT(
            display = display,
            rig = 1,
            bank = 3,
            display_mode = self   # Invalid value ;)
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping                
        mapping.value = 3

        with self.assertRaises(Exception):                        
            action.update_displays()


    def test_error_no_bank_off(self):
        with self.assertRaises(Exception):        
            RIG_SELECT(
                rig = 1,
                bank = 3,
                rig_off = 5
            )


############################################################################################################


    def test_rig_select_and_morph_enabled(self):
        self._test_rig_select_and_morph_enabled(False)
        self._test_rig_select_and_morph_enabled(True)


    def _test_rig_select_and_morph_enabled(self, morph_only_when_enabled):
        ecb = MockEnabledCallback()

        action_select, action_morph = RIG_SELECT_AND_MORPH_STATE(
            rig = 1,
            bank = 2,
            rig_off = 2,
            bank_off = 1,
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

        mapping_rig.value = 5  # on value
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
        action = RIG_SELECT(
            rig = 3,
            bank = 2,
            rig_off = "auto",
            bank_off = "auto"
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        mapping = action.callback._KemperRigSelectCallback__mapping   

        mapping.value = 0 * NUM_RIGS_PER_BANK + 1   # Not matching (Rig 1-2)
        action.update_displays()
        self.assertEqual(action.callback.state, False)
        
        # Select on rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 3)
        self.assertEqual(appl.client.set_calls[0], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[1], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[2], {
            "mapping": MAPPING_RIG_SELECT(2),
            "value": 0
        })

        mapping.value = 1 * NUM_RIGS_PER_BANK + 2   # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 6)
        self.assertEqual(appl.client.set_calls[3], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 0
        })
        self.assertEqual(appl.client.set_calls[4], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[5], {
            "mapping": MAPPING_RIG_SELECT(1),
            "value": 0
        })

        mapping.value = 6 * NUM_RIGS_PER_BANK + 4  # Off rig
        action.update_displays()
        self.assertEqual(action.callback.state, False)

        # Select on rig
        action.push()
        action.release()

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

        mapping.value = 1 * NUM_RIGS_PER_BANK + 2 # On rig
        action.update_displays()
        self.assertEqual(action.callback.state, True)

        # Select off rig
        action.push()
        action.release()

        self.assertEqual(len(appl.client.set_calls), 12)
        self.assertEqual(appl.client.set_calls[9], {
            "mapping": MAPPING_BANK_SELECT(),
            "value": 6
        })
        self.assertEqual(appl.client.set_calls[10], {
            "mapping": MAPPING_RIG_SELECT(4),
            "value": 1
        })
        self.assertEqual(appl.client.set_calls[11], {
            "mapping": MAPPING_RIG_SELECT(4),
            "value": 0
        })
