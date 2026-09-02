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
    from lib.pyswitch.colors import Colors
    from lib.pyswitch.controller.callbacks import BinaryParameterCallback
    
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.kemper.actions.fixed_fx import *
    from lib.pyswitch.clients.kemper.mappings.fixed_fx import *

class TestKemperActionDefinitionsFixed(unittest.TestCase):

    def test(self):
        self._test_slot(FIXED_SLOT_ID_TRANSPOSE, MAPPING_FIXED_TRANSPOSE(), "Transpose", Colors.WHITE)
        self._test_slot(FIXED_SLOT_ID_GATE, MAPPING_FIXED_GATE(), "Gate", Colors.LIGHT_BLUE)
        self._test_slot(FIXED_SLOT_ID_COMP, MAPPING_FIXED_COMP(), "Comp", Colors.BLUE)
        self._test_slot(FIXED_SLOT_ID_BOOST, MAPPING_FIXED_BOOST(), "Boost", Colors.RED)
        self._test_slot(FIXED_SLOT_ID_WAH, MAPPING_FIXED_WAH(), "Wah", Colors.ORANGE)
        self._test_slot(FIXED_SLOT_ID_CHORUS, MAPPING_FIXED_CHORUS(), "Chorus", Colors.BLUE)

        self._test_slot(FIXED_SLOT_ID_AIR, MAPPING_FIXED_AIR(), "Air", Colors.BLUE)
        self._test_slot(FIXED_SLOT_ID_DBL_TRACKER, MAPPING_FIXED_DBL_TRACKER(), "Doubler", Colors.BLUE)


    def _test_slot(self, slot, exp_mapping, exp_text, exp_color):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = FIXED_EFFECT_STATE(
            slot = slot,
            display = display, 
            id = 67, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)

        self.assertEqual(cb.mapping, exp_mapping)
        self.assertEqual(cb._text, exp_text)
        self.assertEqual(cb._color, exp_color)
