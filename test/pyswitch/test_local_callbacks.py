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
    # from lib.pyswitch.controller.callbacks import BinaryParameterCallback
    
    from .mocks_appl import *
    from .mocks_callback import *

    from lib.pyswitch.clients.local.callbacks.splashes import *
    

class TestLocalCallbackDefinitions(unittest.TestCase):

    def test_splashes_callback(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        cb = SplashesCallback(
            splashes = display
        )

        self.assertEqual(cb.get_root(), display)

