import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
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

    def test_wait_for_initial_bank_feedback(self):
        action = ENCODER_BANK_SELECT()
        mapping = action._mapping
        previous_value = mapping.value
        self.addCleanup(setattr, mapping, "value", previous_value)
        mapping.value = None
        appl = MockController()
        action.init(appl)

        action.process(0)
        action.process(8)
        action.process(12)
        action.update()

        self.assertIsNone(mapping.value)
        self.assertEqual(appl.client.set_calls, [])
        self.assertEqual(appl.shared, {})
        self.assertEqual(appl.client.request_calls, [{
            "mapping": mapping,
            "listener": None
        }])

        mapping.value = 40
        action.process(12)
        self.assertEqual(appl.client.set_calls, [])

        action.process(14)
        self.assertEqual(appl.client.set_calls, [{
            "mapping": mapping,
            "value": 9
        }])
        self.assertEqual(mapping.value, 45)
        self.assertEqual(appl.shared["preselectedBank"], 9)

    def test_feedback_loss_does_not_replay_unknown_motion(self):
        action = ENCODER_BANK_SELECT()
        mapping = action._mapping
        previous_value = mapping.value
        self.addCleanup(setattr, mapping, "value", previous_value)
        mapping.value = 10
        appl = MockController()
        action.init(appl)

        action.process(0)
        action.process(2)
        self.assertEqual(appl.client.last_sent_message["value"], 3)

        mapping.value = None
        action.process(10)
        action.process(18)
        self.assertIsNone(mapping.value)
        self.assertEqual(len(appl.client.set_calls), 1)

        mapping.value = 45
        action.process(20)
        self.assertEqual(appl.client.last_sent_message["value"], 10)
        self.assertEqual(mapping.value, 50)
        self.assertEqual(len(appl.client.set_calls), 2)

    def test_shared_preview_can_cancel_before_bank_feedback(self):
        from lib.pyswitch.controller.preview import ValuePreview

        display = DisplayLabel(layout = {"font": "foo"})
        action = ENCODER_BANK_SELECT(preview_display = display)
        mapping = action._mapping
        previous_value = mapping.value
        self.addCleanup(setattr, mapping, "value", previous_value)
        mapping.value = 10
        appl = MockController()
        action.init(appl)

        action.process(0)
        action.process(2)
        self.assertEqual(display.text, "Bank 4")

        mapping.value = None
        ValuePreview.get(display).preview(text = "Another value")
        self.assertEqual(display.text, "Another value")
        self.assertIsNone(mapping.value)
        self.assertEqual(len(appl.client.set_calls), 1)
