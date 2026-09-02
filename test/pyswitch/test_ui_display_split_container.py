import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "usb_midi": MockUsbMidi(),
    "gc": MockGC()
}):
    from lib.pyswitch.ui.ui import DisplayBounds, DisplayElement
    from lib.pyswitch.ui.DisplaySplitContainer import DisplaySplitContainer

    from .mocks_appl import *
    from .mocks_ui import *


###############################################################################################


class TestDisplaySplitContainer(unittest.TestCase):

    def test_split_horizontal(self):
        cont = DisplaySplitContainer(
            bounds = DisplayBounds(20, 30, 600, 500),
            direction = DisplaySplitContainer.HORIZONTAL
        )

        el_1 = DisplayElement()
        el_2 = DisplayElement()
        el_3 = DisplayElement()

        cont.add(el_1)
        cont.init(None, None)
        self.assertEqual(el_1.bounds, DisplayBounds(20, 30, 600, 500))

        cont.add(el_2)
        cont.init(None, None)
        self.assertEqual(el_1.bounds, DisplayBounds(20, 30, 300, 500))        
        self.assertEqual(el_2.bounds, DisplayBounds(320, 30, 300, 500))        

        cont.add(el_3)
        cont.init(None, None)
        self.assertEqual(el_1.bounds, DisplayBounds(20, 30, 200, 500))        
        self.assertEqual(el_2.bounds, DisplayBounds(220, 30, 200, 500))        
        self.assertEqual(el_3.bounds, DisplayBounds(420, 30, 200, 500))        


    def test_split_vertical(self):
        cont = DisplaySplitContainer(
            bounds = DisplayBounds(20, 30, 500, 600),
            direction = DisplaySplitContainer.VERTICAL
        )

        el_1 = DisplayElement()
        el_2 = DisplayElement()
        el_3 = DisplayElement()

        cont.add(el_1)
        cont.init(None, None)
        self.assertEqual(el_1.bounds, DisplayBounds(20, 30, 500, 600))

        cont.add(el_2)
        cont.init(None, None)
        self.assertEqual(el_1.bounds, DisplayBounds(20, 30, 500, 300))        
        self.assertEqual(el_2.bounds, DisplayBounds(20, 330, 500, 300))        

        cont.add(el_3)
        cont.init(None, None)
        self.assertEqual(el_1.bounds, DisplayBounds(20, 30, 500, 200))        
        self.assertEqual(el_2.bounds, DisplayBounds(20, 230, 500, 200))        
        self.assertEqual(el_3.bounds, DisplayBounds(20, 430, 500, 200))        


    def test_no_active_children(self):
        cont = DisplaySplitContainer(
            bounds = DisplayBounds(20, 30, 500, 600)
        )

        cont.init(None, None)

        # Must not throw
        cont.add(None)

        # Add an element for testing later lines
        el_1 = DisplayElement()

        cont.add(el_1)
        cont.init(None, None)

        

        