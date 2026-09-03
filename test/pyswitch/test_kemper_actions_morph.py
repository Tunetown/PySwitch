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
    from lib.pyswitch.controller.callbacks import BinaryParameterCallback
    
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.kemper.actions.morph import *
    from lib.pyswitch.clients.kemper.mappings.morph import *
    

class TestKemperActionMorph(unittest.TestCase):

    def test_morph_button(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = MORPH_BUTTON(
            display = display, 
            text = "foo",
            id = 67, 
            color = (3, 4, 5),
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_MORPH_BUTTON())
        self.assertEqual(cb._text, "foo")
        #self.assertEqual(cb._color, (3, 4, 5))
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)


    def test_morph_button_with_display(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = MORPH_BUTTON(
            display = display, 
            text = "foo",
            id = 67, 
            use_leds = True, 
            enable_callback = ecb,
            color = "kemper"
        )

        cb = action.callback
        self.assertIsInstance(cb, KemperMorphCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_MORPH_BUTTON())
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._value_enable, 1)
        self.assertEqual(cb._value_disable, 0)

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)
        self.assertEqual(action._PushButtonAction__mode, PushButtonAction.MOMENTARY)


    def test_morph_display(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = MORPH_DISPLAY(
            display = display, 
            text = "foo",
            id = 67, 
            use_leds = True, 
            enable_callback = ecb
        )

        appl = MockController()
        action.init(appl, None)

        cb = action.callback
        self.assertIsInstance(cb, KemperMorphCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_MORPH_PEDAL())
        self.assertEqual(cb._text, "foo")
        self.assertEqual(cb._BinaryParameterCallback__comparison_mode, BinaryParameterCallback.NO_STATE_CHANGE)
        self.assertEqual(cb._led_brightness_off, 0.3)

        self.assertEqual(cb._BinaryParameterCallback__display_dim_factor_off, 1)
        self.assertEqual(cb._KemperMorphCallback__suppress_send, True)
        
        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)


#################################################################################

    def test_midi_channels(self):
        for c in range(16):
            self._test_morph_button_midi_channel(c)
            self._test_morph_display_midi_channel(c)
            

    def _test_morph_button_midi_channel(self, channel):
        action = MORPH_BUTTON(
            midi_channel = channel + 1
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_MORPH_BUTTON(channel))


    def _test_morph_display_midi_channel(self, channel):
        action = MORPH_DISPLAY(
            midi_channel = channel + 1
        )

        appl = MockController()
        action.init(appl, None)

        cb = action.callback
        self.assertEqual(cb.mapping, MAPPING_MORPH_PEDAL(channel))
