import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    # "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    # "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    # "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    # "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.controller.callbacks.parameter_display import ParameterDisplayCallback
    
    from lib.pyswitch.ui.elements import DisplayLabel

    from .mocks_appl import *
    from .mocks_ui import MockUiController
    


class TestParameterDisplayCallback(unittest.TestCase):

    def test(self):
        mapping = MockParameterMapping()
         
        cb = ParameterDisplayCallback(
            mapping = mapping,
            default_text = "default"
        )

        self.assertIn(mapping, cb._Callback__mappings)

        label = DisplayLabel(
            layout = {
                "font": "foo"
            },
            callback = cb
        )

        appl = MockController()
        ui = MockUiController()
        label.init(ui, appl)

        cb.update_label(label)
        
        self.assertEqual(label.text, "default")

        # Set a value
        mapping.value = "heythere"

        cb.update_label(label)

        self.assertEqual(label.text, "heythere")
        
        # Set another value
        mapping.value = "yes?"

        cb.update_label(label)

        self.assertEqual(label.text, "yes?")
        

    def test_value_conversion(self):
        mapping = MockParameterMapping()
         
        def convert_value(value):
            if value == None:
                return None
            return str(value * value) + " dings"

        cb = ParameterDisplayCallback(
            mapping = mapping,
            default_text = "default",
            convert_value = convert_value
        )

        self.assertIn(mapping, cb._Callback__mappings)

        label = DisplayLabel(
            layout = {
                "font": "foo"
            },
            callback = cb
        )

        appl = MockController()
        ui = MockUiController()
        label.init(ui, appl)

        cb.update_label(label)
        
        self.assertEqual(label.text, "default")

        # Set a value
        mapping.value = 4

        cb.update_label(label)

        self.assertEqual(label.text, "16 dings")
        
        # Set another value
        mapping.value = 3

        cb.update_label(label)

        self.assertEqual(label.text, "9 dings")
        