import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *
from .mocks_midi import test_mapping

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.clients.local.mappings.generic import *
    

class TestLocal(unittest.TestCase):

    def test_mappings(self):
        test_mapping(self, MAPPING_SEND_PROGRAM_CHANGE(), exp_name = "PC", exp_midi_channel = 0)
        test_mapping(self, MAPPING_SEND_PROGRAM_CHANGE(channel = 8), exp_name = "PC", exp_midi_channel = 8)


