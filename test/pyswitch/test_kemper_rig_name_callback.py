import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_midi.midi_message": MockAdafruitMIDIMessage(),
    "adafruit_midi.control_change": MockAdafruitMIDIControlChange(),
    "adafruit_midi.system_exclusive": MockAdafruitMIDISystemExclusive(),
    "adafruit_midi.program_change": MockAdafruitMIDIProgramChange(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.clients.kemper import *
    
    from lib.pyswitch.ui.elements import DisplayLabel
    from .mocks_appl import *
    from .mocks_ui import MockUiController
          

class TestKemperRigNameCallback(unittest.TestCase):

    def test(self):
        self._test(False, False)
        self._test(False, True)
        self._test(False, 'rig')
        self._test(False, 'bank')
        self._test(True, False)
        self._test(True, True)
        self._test(True, 'rig')
        self._test(True, 'bank')
        

    def _test(self, show_name, show_rig_id):
        self._do_test(
            show_name = show_name,
            show_rig_id = show_rig_id,
            preselect = False
        )

        if show_name or show_rig_id:
            self._do_test(
                show_name = show_name,
                show_rig_id = show_rig_id,
                preselect = True
            )


    def _do_test(self, show_name, show_rig_id, preselect):
        cb = KemperRigNameCallback(
            show_name = show_name,
            show_rig_id = show_rig_id
        )

        if show_name:
            self.assertIn(KemperMappings.RIG_NAME(), cb._Callback__mappings)

        if show_rig_id:
            self.assertIn(KemperMappings.RIG_ID(), cb._Callback__mappings)

        label = DisplayLabel(
            layout = {
                "font": "foo"
            },
            callback = cb
        )

        appl = MockController()
        ui = MockUiController()
        label.init(ui, appl)

        if show_name:
            mapping_name = [m for m in cb._Callback__mappings if m == KemperMappings.RIG_NAME()][0]
            mapping_name.value = "foo"

        if show_rig_id:
            mapping_id = [m for m in cb._Callback__mappings if m == KemperMappings.RIG_ID()][0]
            mapping_id.value = 13

        if preselect:
            appl.shared["preselectedBank"] = 2
            cb.update()

            self.assertEqual(label.text, "Bank 3")

            del appl.shared["preselectedBank"]

            cb.update()

        cb.update_label(label)

        if show_name:
            if show_rig_id == 'rig':
                self.assertEqual(label.text, "4 foo")
            elif show_rig_id == 'bank':
                self.assertEqual(label.text, "3 foo")
            elif show_rig_id:
                self.assertEqual(label.text, "3-4 foo")
            else:
                self.assertEqual(label.text, "foo")
        else:
            if show_rig_id == 'rig':
                self.assertEqual(label.text, "4")
            elif show_rig_id == 'bank':
                self.assertEqual(label.text, "3")
            elif show_rig_id:
                self.assertEqual(label.text, "3-4")


