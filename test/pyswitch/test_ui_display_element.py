import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from lib.pyswitch.ui.ui import DisplayElement, DisplayBounds
    from .mocks_ui import MockDisplayElement, MockFontLoader



class TestDisplayElement(unittest.TestCase):

    def test_bounds(self):
        b = DisplayBounds(20, 40, 100, 400)
        el = MockDisplayElement(
            bounds = b
        )

        self.assertEqual(el.bounds, b)

        b.x = 10
        self.assertNotEqual(el.bounds, b)

        el.bounds = b
        self.assertEqual(el.bounds, b)

        el.init(None, None)


    def test_initialized(self):
        el = DisplayElement(
            id = "foo"
        )

        self.assertEqual(el.initialized(), False)

        el.init(None, None)

        self.assertEqual(el.initialized(), True)


    def test_make_splash(self):
        el = DisplayElement(
            id = "foo"
        )

        f = MockFontLoader()
        el.make_splash(f)

        self.assertEqual(el.font_loader, f)
        self.assertIsInstance(el.splash, MockDisplayIO.Group)

        spl = el.splash
        f2 = MockFontLoader()
        el.make_splash(f2)

        self.assertEqual(el.font_loader, f)
        self.assertEqual(spl, el.splash)


    def test_children(self):
        el = DisplayElement(
            id = "foo"
        )

        child_1 = DisplayElement(
            id = "bar"
        )

        child_2 = DisplayElement(
            id = "bat"
        )

        subchild_1 = DisplayElement(
            id = "tar"
        )

        el.add(child_1)
        el.add(child_2)

        child_1.add(None)
        child_1.add(subchild_1)
        child_1.add(None)

        # children
        self.assertEqual(el.children, [child_1, child_2])
        self.assertEqual(child_1.children, [None, subchild_1, None])
        self.assertEqual(child_2.children, None)
        self.assertEqual(subchild_1.children, None)

        # child(index)
        #self.assertEqual(el.child(0), child_1)
        #self.assertEqual(el.child(1), child_2)        
        #self.assertEqual(child_1.child(0), None)
        #self.assertEqual(child_1.child(1), subchild_1)

        #with self.assertRaises(Exception):
        #    el.child(-1)

        #with self.assertRaises(Exception):
        #    el.child(2)            

        # first_child / last_child
        #self.assertEqual(el.first_child, child_1)
        #self.assertEqual(el.last_child, child_2)

        #self.assertEqual(child_1.first_child, subchild_1)
        #self.assertEqual(child_1.last_child, subchild_1)        

        #self.assertEqual(child_2.first_child, None)
        #self.assertEqual(child_2.last_child, None)   


    def test_init(self):
        class Object:
            pass

        appl = Object()
        ui = Object()

        el = MockDisplayElement(
            id = "foo"
        )

        child_1 = MockDisplayElement(
            id = "bar"
        )

        child_2 = MockDisplayElement(
            id = "bat"
        )

        subchild_1 = MockDisplayElement(
            id = "tar"
        )

        el.add(child_1)
        el.add(child_2)

        child_1.add(None)
        child_1.add(subchild_1)

        self.assertEqual(el.initialized(), False)
        self.assertEqual(child_1.initialized(), False)
        self.assertEqual(child_2.initialized(), False)
        self.assertEqual(subchild_1.initialized(), False)

        el.init(ui, appl)

        self.assertEqual(el.initialized(), True)
        self.assertEqual(child_1.initialized(), True)
        self.assertEqual(child_2.initialized(), True)
        self.assertEqual(subchild_1.initialized(), True)

        self.assertEqual(el.num_init_calls, 1)
        self.assertEqual(child_1.num_init_calls, 1)
        self.assertEqual(child_2.num_init_calls, 1)
        self.assertEqual(subchild_1.num_init_calls, 1)


    def test_init_partially(self):
        class Object:
            pass

        appl = Object()
        ui = Object()

        el = MockDisplayElement(
            id = "foo"
        )

        child_1 = MockDisplayElement(
            id = "bar"
        )

        child_2 = MockDisplayElement(
            id = "bat"
        )

        subchild_1 = MockDisplayElement(
            id = "tar"
        )
        
        el.add(child_1)
        el.add(child_2)

        child_1.add(None)
        child_1.add(subchild_1)

        child_1.init(ui, appl)

        self.assertEqual(el.initialized(), False)
        self.assertEqual(child_1.initialized(), True)
        self.assertEqual(child_2.initialized(), False)
        self.assertEqual(subchild_1.initialized(), True)

        el.init(ui, appl)

        self.assertEqual(el.initialized(), True)
        self.assertEqual(child_1.initialized(), True)
        self.assertEqual(child_2.initialized(), True)
        self.assertEqual(subchild_1.initialized(), True)
        
        self.assertEqual(el.num_init_calls, 1)
        self.assertEqual(child_1.num_init_calls, 1)
        self.assertEqual(child_2.num_init_calls, 1)
        self.assertEqual(subchild_1.num_init_calls, 1)

        subchild_2 = MockDisplayElement(
            id = "tar2"
        )

        child_1.add(subchild_2)

        self.assertEqual(el.initialized(), False)
        self.assertEqual(child_1.initialized(), False)
        self.assertEqual(child_2.initialized(), True)
        self.assertEqual(subchild_1.initialized(), True)
        self.assertEqual(subchild_2.initialized(), False)

        el.init(ui, appl)

        self.assertEqual(el.initialized(), True)
        self.assertEqual(child_1.initialized(), True)
        self.assertEqual(child_2.initialized(), True)
        self.assertEqual(subchild_1.initialized(), True)
        self.assertEqual(subchild_2.initialized(), True)
        
        self.assertEqual(el.num_init_calls, 2)
        self.assertEqual(child_1.num_init_calls, 2)
        self.assertEqual(child_2.num_init_calls, 1)
        self.assertEqual(subchild_1.num_init_calls, 1)
        self.assertEqual(subchild_2.num_init_calls, 1)


