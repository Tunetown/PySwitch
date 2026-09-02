import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

with patch.dict(sys.modules, {
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "gc": MockGC()
}):
    from lib.pyswitch.ui.ui import DisplayBounds
    from lib.pyswitch.ui.layout import *



class TestDisplayBoundsLayout(unittest.TestCase):

    def test_remove_top(self):
        b = DisplayBounds(20, 40, 100, 400)
        
        self.assertEqual(remove_from_top(b, 20), DisplayBounds(20, 40, 100, 20))
        self.assertEqual(b, DisplayBounds(20, 60, 100, 380))

    def test_remove_bottom(self):
        b = DisplayBounds(20, 40, 100, 400)
        
        self.assertEqual(remove_from_bottom(b, 20), DisplayBounds(20, 420, 100, 20))
        self.assertEqual(b, DisplayBounds(20, 40, 100, 380))

    def test_remove_left(self):
        b = DisplayBounds(20, 40, 100, 400)
        
        self.assertEqual(remove_from_left(b, 20), DisplayBounds(20, 40, 20, 400))
        self.assertEqual(b, DisplayBounds(40, 40, 80, 400))

    def test_remove_right(self):
        b = DisplayBounds(20, 40, 100, 400)
        
        self.assertEqual(remove_from_right(b, 20), DisplayBounds(100, 40, 20, 400))
        self.assertEqual(b, DisplayBounds(20, 40, 80, 400))

    def test_translate(self):
        b = DisplayBounds(20, 40, 100, 400)

        translate(b, -2, 4)
        self.assertEqual(b, DisplayBounds(18, 44, 100, 400))

        translate(b, 20, -10)
        self.assertEqual(b, DisplayBounds(38, 34, 100, 400))

    def test_translated(self):
        b = DisplayBounds(20, 40, 100, 400)

        self.assertEqual(translated(b, -2, 4), DisplayBounds(18, 44, 100, 400))
        self.assertEqual(b, DisplayBounds(20, 40, 100, 400))

    def test_with_position(self):
        b = DisplayBounds(20, 40, 100, 400)

        self.assertEqual(with_position(b, 3, 5), DisplayBounds(3, 5, 100, 400))
        self.assertEqual(b, DisplayBounds(20, 40, 100, 400))

    def test_top(self):
        b = DisplayBounds(20, 40, 100, 400)
        
        self.assertEqual(top(b, 20), DisplayBounds(20, 40, 100, 20))
        self.assertEqual(b, DisplayBounds(20, 40, 100, 400))

    def test_bottom(self):
        b = DisplayBounds(20, 40, 100, 400)
        
        self.assertEqual(bottom(b, 20), DisplayBounds(20, 420, 100, 20))
        self.assertEqual(b, DisplayBounds(20, 40, 100, 400))

    def test_left(self):
        b = DisplayBounds(20, 40, 100, 400)
        
        self.assertEqual(left(b, 20), DisplayBounds(20, 40, 20, 400))
        self.assertEqual(b, DisplayBounds(20, 40, 100, 400))

    def test_right(self):
        b = DisplayBounds(20, 40, 100, 400)
        
        self.assertEqual(right(b, 20), DisplayBounds(100, 40, 20, 400))
        self.assertEqual(b, DisplayBounds(20, 40, 100, 400))