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

    from lib.pyswitch.clients.kemper.actions.amp import *

    from lib.pyswitch.clients.local.actions.encoder_button import *
    from lib.pyswitch.controller.actions.EncoderAction import EncoderAction
    

class TestKemperActionsRig(unittest.TestCase):

   
    def test_amp_gain(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        accept = ENCODER_BUTTON()
        cancel = ENCODER_BUTTON()

        action = AMP_GAIN(
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

        self.assertEqual(action._mapping, MAPPING_AMP_GAIN())
        self.assertEqual(action.id, 45)
        self.assertEqual(action._EncoderAction__enable_callback, ecb)
        self.assertEqual(action._EncoderAction__step_width, 1)
        self.assertEqual(action._EncoderAction__preselect, True)
        self.assertEqual(action._EncoderAction__preview.label, display)
        # self.assertEqual(action._EncoderAction__preview._ValuePreview__blink_color, (3, 4, 5))
        # self.assertEqual(action._EncoderAction__preview._ValuePreview__period.interval, 345)

        appl = MockController()
        action.init(appl)

        switch = MockSwitch()
        accept.init(appl, switch)
        cancel.init(appl, switch)

        action.process(0)
        action.process(8192)
        action.update()

        self.assertEqual(display.text, "Gain: 5.0")