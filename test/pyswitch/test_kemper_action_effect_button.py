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

    from lib.pyswitch.clients.kemper.actions.effect_button import *
    


class TestKemperActionEffectButton(unittest.TestCase):

    def test_effect_button(self):
        self._test_effect_button(1, None, "FX I")
        self._test_effect_button(2, None, "FX II")
        self._test_effect_button(3, None, "FX III")
        self._test_effect_button(4, None, "FX IIII")
        self._test_effect_button(5, None, None)

        self._test_effect_button(1, "foo", "foo")
        self._test_effect_button(4, "foo", "foo")

    def _test_effect_button(self, num, text, exp_text):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = EFFECT_BUTTON(
            num = num,
            display = display, 
            color = (4, 5, 6), 
            text = text,
            id = 67, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_EFFECT_BUTTON(num))
        self.assertEqual(cb._text, exp_text)
        self.assertEqual(cb._color, (4, 5, 6))

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)


    def test_reset_on_rig_change(self):
        action = EFFECT_BUTTON(
            num = 1            
        )

        appl = MockController()
        switch = MockFootswitch(actions = [action])
        action.init(appl, switch)

        cb = action.callback
        mapping = cb.mapping
        mapping_rig = cb._KemperEffectButtonCallback__rig_mapping

        cb.parameter_changed(mapping_rig)  # Trigger condition for False state
        cb.parameter_changed(mapping)      # Trigger condition for wrong mapping_rig

        mapping.value = 0
        mapping_rig.value = 8

        self.assertEqual(action.state, False)

        action.push()
        action.release()
        
        self.assertEqual(action.state, True)

        action.push()
        action.release()

        self.assertEqual(action.state, False)

        action.push()
        action.release()
        
        self.assertEqual(action.state, True)

        cb.parameter_changed(mapping_rig)

        self.assertEqual(action.state, False)

        action.push()
        action.release()
        
        self.assertEqual(action.state, True)

        mapping_rig.value = 11
        cb.parameter_changed(mapping_rig)

        self.assertEqual(action.state, False)

#################################################################################

    def test_midi_channels(self):
        for c in range(16):
            self._test_midi_channel(c)

    def _test_midi_channel(self, channel):
        action = EFFECT_BUTTON(
            num = 1,
            midi_channel = channel + 1
        )

        cb = action.callback
        self.assertEqual(cb.mapping, MAPPING_EFFECT_BUTTON(1, channel))
