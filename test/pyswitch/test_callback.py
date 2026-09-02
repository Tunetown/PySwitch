import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    # "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    # "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    # "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    # "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from .mocks_appl import *
    from .mocks_callback import *
    from lib.pyswitch.misc import Updater


class TestCallback(unittest.TestCase):

    def test_init(self):
        mapping_1 = MockParameterMapping()
        mapping_2 = MockParameterMapping()

        cb = MockCallback(mappings = [
            mapping_1,
            mapping_2
        ])

        appl = MockController()
        cb.init(appl)

        self.assertEqual(len(appl.client.register_calls), 2)
        self.assertIn(mapping_1, [x["mapping"] for x in appl.client.register_calls])
        self.assertIn(mapping_2, [x["mapping"] for x in appl.client.register_calls])

        self.assertEqual(appl.updateables, [cb])

        # Not call init again when already initialized
        other = Updater()
        cb.init(appl, other)

        self.assertEqual(len(appl.client.register_calls), 2)


    def test_update(self):
        mapping_1 = MockParameterMapping()
        mapping_2 = MockParameterMapping()

        cb = MockCallback(mappings = [
            mapping_1,
            mapping_2
        ])

        appl = MockController()
        cb.init(appl)

        cb.update()

        self.assertIn(mapping_1, [x["mapping"] for x in appl.client.request_calls])
        self.assertIn(mapping_2, [x["mapping"] for x in appl.client.request_calls])


    def test(self):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_2 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x11, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        cb = MockCallback(mappings = [
            mapping_1,
            mapping_2
        ])

        appl = MockController()

        listener = MockClientRequestListener()
        cb.init(appl, listener)

        # mapping_value_2 = MockParameterMapping(
        #     response = SystemExclusive(
        #         manufacturer_id = [0x00, 0x11, 0x20],
        #         data = [0x00, 0x00, 0x09]
        #     )
        # )
        mapping_2.value = 456

        cb.parameter_changed(mapping_2)

        self.assertEqual(mapping_1.value, None)
        self.assertEqual(mapping_2.value, 456)

        self.assertEqual(listener.parameter_changed_calls, [mapping_2])

        # mapping_value_1 = MockParameterMapping(
        #     response = SystemExclusive(
        #         manufacturer_id = [0x00, 0x10, 0x20],
        #         data = [0x00, 0x00, 0x09]
        #     )
        # )
        mapping_1.value = 654

        cb.parameter_changed(mapping_1)

        self.assertEqual(mapping_1.value, 654)
        self.assertEqual(mapping_2.value, 456)

        self.assertEqual(listener.parameter_changed_calls, [mapping_2, mapping_1])

        # Terminate
        cb.request_terminated(mapping_2)

        self.assertEqual(mapping_1.value, 654)
        self.assertEqual(mapping_2.value, None)

        self.assertEqual(listener.request_terminated_calls, [mapping_2])

        
    def test_no_listener(self):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        cb = MockCallback(mappings = [
            mapping_1
        ])

        appl = MockController()

        cb.init(appl)

        mapping_1.value = 654

        cb.parameter_changed(mapping_1)

        self.assertEqual(mapping_1.value, 654)

        cb.request_terminated(mapping_1)

        self.assertEqual(mapping_1.value, None)

