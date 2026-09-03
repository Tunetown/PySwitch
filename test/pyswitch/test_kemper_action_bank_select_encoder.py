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

    from lib.pyswitch.controller.actions.EncoderAction import EncoderAction

    from lib.pyswitch.clients.kemper.actions.bank_select_encoder import *
    from lib.pyswitch.clients.kemper.mappings.select import *
    
    from lib.pyswitch.clients.kemper import NUM_RIGS_PER_BANK, NUM_BANKS
    
    
class TestKemperActionBankSelectEncoder(unittest.TestCase):

    def test(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        ecb = MockEnabledCallback()

        action = ENCODER_BANK_SELECT(
            step_width = 0.5,
            preview_display = display,
            id = 45, 
            enable_callback = ecb
        )

        self.assertIsInstance(action, EncoderAction)

        self.assertEqual(action._mapping, MAPPING_BANK_SELECT())
        self.assertEqual(action.id, 45)
        self.assertEqual(action._EncoderAction__enable_callback, ecb)
        self.assertEqual(action._EncoderAction__step_width, 0.5)
        self.assertEqual(action._EncoderAction__preview.label, display)

        mapping = action._mapping
        mapping.value = 4 * NUM_RIGS_PER_BANK

        appl = MockController()
        action.init(appl)

        action.accept()
        
        action.process(0)
        action.process(2)
        action.update()

        self.assertEqual(display.text, "Bank 6")
        self.assertEqual(mapping.value, 5 * NUM_RIGS_PER_BANK)

        self.assertEqual(appl.client.set_calls, [
            {
                "mapping": mapping,
                "value": 5
            }
        ])

        action.process(4)
        action.update()

        self.assertEqual(display.text, "Bank 7")
        self.assertEqual(mapping.value, 6 * NUM_RIGS_PER_BANK)

        self.assertEqual(appl.client.set_calls, [
            {
                "mapping": mapping,
                "value": 5
            },
            {
                "mapping": mapping,
                "value": 6
            }
        ])

        action.process(400)
        action.update()

        self.assertEqual(display.text, f"Bank { NUM_BANKS }")
        self.assertEqual(mapping.value, (NUM_BANKS - 1) * NUM_RIGS_PER_BANK)

        self.assertEqual(appl.client.set_calls, [
            {
                "mapping": mapping,
                "value": 5
            },
            {
                "mapping": mapping,
                "value": 6
            },
            {
                "mapping": mapping,
                "value": 124
            }
        ])

        action.process(398)
        action.update()

        self.assertEqual(display.text, f"Bank { NUM_BANKS - 1 }")
        self.assertEqual(mapping.value, (NUM_BANKS - 2) * NUM_RIGS_PER_BANK)

        self.assertEqual(appl.client.set_calls, [
            {
                "mapping": mapping,
                "value": 5
            },
            {
                "mapping": mapping,
                "value": 6
            },
            {
                "mapping": mapping,
                "value": 124
            },
            {
                "mapping": mapping,
                "value": 123
            }
        ])


    def test_midi_channels(self):
        for channel in range(16):
            self._test_midi_channel(channel)

    def _test_midi_channel(self, channel):
        action = ENCODER_BANK_SELECT(
            midi_channel = channel + 1
        )

        self.assertIsInstance(action, EncoderAction)

        self.assertEqual(action._mapping, MAPPING_BANK_SELECT(channel = channel))
