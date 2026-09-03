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

    from lib.pyswitch.clients.kemper.actions.tempo import *
    from lib.pyswitch.clients.kemper.actions.tempo_bpm import *

    from lib.pyswitch.clients.kemper.mappings.tempo_bpm import *
    from lib.pyswitch.clients.kemper.mappings.tempo import *
    
    from lib.pyswitch.clients.local.actions.encoder_button import *
    from lib.pyswitch.controller.actions.EncoderAction import EncoderAction


class TestKemperActionsTempo(unittest.TestCase):

    def test_tap_tempo(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = TAP_TEMPO(
            display = display, 
            color = (4, 5, 6), 
            id = 67, 
            use_leds = True, 
            enable_callback = ecb
        )

        cb = action.callback
        self.assertIsInstance(cb, BinaryParameterCallback)
        self.assertIsInstance(action, PushButtonAction)

        self.assertEqual(cb.mapping, MAPPING_TAP_TEMPO())
        self.assertEqual(cb._text, "Tap")
        self.assertEqual(cb._color, (4, 5, 6))

        self.assertEqual(action.label, display)
        self.assertEqual(action.id, 67)
        self.assertEqual(action.uses_switch_leds, True)
        self.assertEqual(action._Action__enable_callback, ecb)


    def test_tempo_bpm(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        accept = ENCODER_BUTTON()
        cancel = ENCODER_BUTTON()

        action = ENCODER_BPM(
            step_width = 1,
            accept_action = accept,
            cancel_action = cancel,
            preview_display = display,
            preview_blink_color = (3, 4, 5),
            preview_timeout_millis = 345,
            id = 45, 
            enable_callback = ecb
        )

        self.assertIsInstance(action, EncoderAction)

        self.assertEqual(action._mapping, MAPPING_TEMPO_BPM())
        self.assertEqual(action.id, 45)
        self.assertEqual(action._EncoderAction__enable_callback, ecb)
        self.assertEqual(action._EncoderAction__step_width, 1)
        self.assertEqual(action._EncoderAction__preselect, True)
        self.assertEqual(action._EncoderAction__preview.label, display)

        appl = MockController()
        action.init(appl)

        switch = MockSwitch()
        accept.init(appl, switch)
        cancel.init(appl, switch)

        action.process(0)
        action.process(131 * 64)
        action.update()

        self.assertEqual(display.text, "131 bpm")

