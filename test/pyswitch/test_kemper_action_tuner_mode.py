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
    
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.kemper.actions.tuner import *



class TestKemperActionTunerMode(unittest.TestCase):

    def test_tuner_mode(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        ecb = MockEnabledCallback(output = True)

        action = TUNER_MODE(
            display = display, 
            mode = PushButtonAction.ONE_SHOT, 
            color = (4, 5, 6), 
            id = 67, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, KemperMappings.TUNER_MODE_STATE())
        self.assertEqual(cb._text, "Tuner")
        self.assertEqual(cb._color, (4, 5, 6))

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)


    def test_state_change_by_user(self):
        action = TUNER_MODE()

        switch = MockFootswitch(
            actions = [
                action
            ]
        )

        appl = MockController()
        action.init(appl, switch)

        cb = action.callback
        mapping = cb.mapping
        self.assertEqual(action.state, False)

        mapping.value = 1
        action.state = True
        self.assertEqual(action.state, True)
        self.assertEqual(appl.client.set_calls, [
            {
                "mapping": cb.mapping,
                "value": 1
            }
        ])

        appl.client.set_calls = []
        mapping.value = 3
        action.state = False
        self.assertEqual(action.state, False)
        self.assertEqual(appl.client.set_calls, [
            {
                "mapping": cb.mapping,
                "value": 0
            }
        ])

