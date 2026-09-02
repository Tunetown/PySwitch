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
    from lib.pyswitch.ui.ui import DisplayBounds
    from lib.pyswitch.ui.elements import DisplayLabel, DisplayLabelLayout    
    from lib.pyswitch.misc import Updater

    from .mocks_appl import *
    from .mocks_ui import *
    from .mocks_callback import *


class TestDisplayLabel(unittest.TestCase):

    def test_layout_no_font(self):
        with self.assertRaises(Exception):
            DisplayLabel(
                layout = {},
                bounds = DisplayBounds(20, 21, 200, 210)
            )


    def test_layout_defaults(self):
        label = DisplayLabel(
            layout = {
                "font": "foo"
            },
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        self.assertTrue(
            self._compare_layouts(
                label._DisplayLabel__layout,
                DisplayLabelLayout({
                    "font": "foo",
                    "maxTextWidth": False,
                    "lineSpacing": 1,
                    "text": "",
                    "textColor": None,
                    "backColor": None,
                    "stroke": 0
                })
            )
        )

    # Helper to compare two layouts
    def _compare_layouts(self, a, b):
        return (a.font_path == b.font_path and 
                a.max_text_width == b.max_text_width and
                a.line_spacing == b.line_spacing and
                #a.text == b.text and
                a.text_color == b.text_color and
                a.back_color == b.back_color and 
                a.stroke == b.stroke)
    
    
    #def _stringify_layout(self, layout):
    #    return repr(layout.__dict__)
    

###############################################################################################


    def test(self):
        self._test_label(20, 21, 200, 210, None, 0, "hey", (255, 255, 255), None)
        self._test_label(20, 221, 20, 210, None, 0, "hey", (200, 255, 255), (200, 255, 255))

        self._test_label(20, 21, 100, 210, (3, 4, 5), 0, "hey", (255, 200, 255), (255, 200, 255))
        self._test_label(20, 21, 200, 210, (3, 4, 5), 0, "", (255, 255, 255), None)
        self._test_label(20, 21, 300, 210, (3, 4, 5), 2, "bar", (255, 255, 200), (255, 255, 200))
        self._test_label(20, 21, 400, 210, (3, 4, 5), 3, "foo", (255, 255, 255), None)

        self._test_label(20, 23, 200, 210, (200, 240, 250), 3, "foo", (0, 0, 0), None)
        self._test_label(20, 25, 200, 210, (200, 140, 250), 3, "foo", (0, 0, 0), None)
        self._test_label(20, 28, 200, 210, (0, 0, 0), 3, "foo", (255, 255, 255), None)
        self._test_label(20, 31, 10000, 210, (30, 50, 100), 3, "foo", (255, 255, 255), None)


    def _test_label(self, x, y, w, h, fill, stroke, text, text_color_exp, text_color_set):
        layout_def_1 = {
            "font": "foo",
            "backColor": fill,
            "textColor": text_color_set,
            "text": text,
            "stroke": stroke
        }

        label = DisplayLabel(
            layout = layout_def_1,
            bounds = DisplayBounds(x, y, w, h)
        )

        ui = DisplayElement()
        ui.make_splash(MockFontLoader())

        u = Updater()
        u.low_memory_warning = False

        label.init(ui, u)
        
        index = 0

        if fill:
            rect = ui.splash.mock_content[index]
            index += 1

            self.assertIsInstance(rect, MockDisplayShapes.rect.Rect)

            self.assertEqual(rect.x, x + stroke)
            self.assertEqual(rect.y, y + stroke)
            self.assertEqual(rect.width, w - stroke * 2)
            self.assertEqual(rect.height, h - stroke * 2)
            self.assertEqual(rect.fill, fill)
            self.assertEqual(rect.outline, None)
            self.assertEqual(rect.stroke, 0)
            
        group = ui.splash.mock_content[index]
        label = ui.splash.mock_content[index].mock_content[0]

        self.assertIsInstance(group, MockDisplayIO.Group)
        self.assertIsInstance(label, MockAdafruitDisplayText.label.Label)

        self.assertEqual(group.x, x)
        self.assertEqual(group.y, y)
        self.assertEqual(group.scale, 1)

        self.assertEqual(label.text, text)
        self.assertEqual(label.color, text_color_exp)


###############################################################################################


    def test_callback(self):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        cb = MockDisplayLabelCallback(
            mappings = [mapping_1]
        )
        label = DisplayLabel(
            layout = {
                "font": "foo"            
            },
            bounds = DisplayBounds(20, 30, 400, 777),
            callback = cb
        )

        ui = DisplayElement()
        ui.make_splash(MockFontLoader())

        u = Updater()
        u.client = MockClient()
        u.low_memory_warning = False

        label.init(ui, u)

        cb.label_text = "foobar"
        cb.parameter_changed(mapping_1)

        self.assertEqual(label.text, "foobar")

        cb.label_text = "terminated"
        cb.request_terminated(mapping_1)
        self.assertEqual(label.text, "terminated")


###############################################################################################
 

    def test_back_color(self):
        label = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (3, 4, 6)
            },
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        self.assertEqual(label.back_color, (3, 4, 6))

        label.back_color = (200, 230, 240)
        self.assertEqual(label.back_color, (200, 230, 240))

        # Check background(s)
        ui = DisplayElement()
        ui.make_splash(MockFontLoader())

        u = Updater()
        u.low_memory_warning = False

        label.init(ui, u)
        
        self.assertEqual(ui.splash.mock_content[0].fill, (200, 230, 240))

        label.back_color = (200, 220, 250)
        self.assertEqual(label.back_color, (200, 220, 250))

        self.assertEqual(ui.splash.mock_content[0].fill, (200, 220, 250))


###############################################################################################


    def test_back_color_error_back2none(self):
        label = DisplayLabel(
            layout = {
                "font": "foo",
                "backColor": (3, 4, 6)
            },
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        with self.assertRaises(Exception):        
            label.back_color = None


###############################################################################################


    def test_back_color_error_none2back(self):
        label = DisplayLabel(
            layout = {
                "font": "foo"
            },
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        with self.assertRaises(Exception):        
            label.back_color = (3, 4, 6)


###############################################################################################


    def test_text_color(self):
        label = DisplayLabel(
            layout = {
                "font": "foo",
                "textColor": (3, 4, 6)
            },
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        self.assertEqual(label.text_color, (3, 4, 6))

        label.text_color = (5, 6, 7)
        self.assertEqual(label.text_color, (5, 6, 7))

        # Check elements
        ui = DisplayElement()
        ui.make_splash(MockFontLoader())

        u = Updater()
        u.low_memory_warning = False

        label.init(ui, u)
        
        self.assertEqual(ui.splash.mock_content[0].mock_content[0].color, (5, 6, 7))

        label.text_color = None
        self.assertEqual(ui.splash.mock_content[0].mock_content[0].color, (255, 255, 255))

        label.text_color = (5, 6, 7)
        self.assertEqual(label.text_color, (5, 6, 7))


###############################################################################################


    def test_text(self):
        label = DisplayLabel(
            layout = {
                "font": "foo",
                "text": "foo"
            },
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        self.assertEqual(label.text, "foo")

        label.text = "bar"
        self.assertEqual(label.text, "bar")

        # Check elements
        ui = DisplayElement()
        ui.make_splash(MockFontLoader())

        u = Updater()
        u.low_memory_warning = False

        label.init(ui, u)
        
        self.assertEqual(ui.splash.mock_content[0].mock_content[0].text, "bar")

        label.text = "foo"
        self.assertEqual(label.text, "foo")
        self.assertEqual(ui.splash.mock_content[0].mock_content[0].text, "foo")

        label.text = "bar1"
        self.assertEqual(label.text, "bar1")
        self.assertEqual(ui.splash.mock_content[0].mock_content[0].text, "bar1")


    def test_text_wrapped(self):
        label = DisplayLabel(
            layout = {
                "font": "foo",
                "text": "foo",
                "maxTextWidth": 12
            },
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        # Check elements
        ui = DisplayElement()
        ui.make_splash(MockFontLoader())

        u = Updater()
        u.low_memory_warning = False

        label.init(ui, u)
        
        self.assertEqual(ui.splash.mock_content[0].mock_content[0].text, "foo\n(wrapped to 12 and font 'foo')")

        label.text = "bar1"
        self.assertEqual(label.text, "bar1")
        self.assertEqual(ui.splash.mock_content[0].mock_content[0].text, "bar1\n(wrapped to 12 and font 'foo')")        


    def test_text_low_memory_warning(self):
        label = DisplayLabel(
            layout = {
                "font": "foo",
                "text": "foo"
            },
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        ui = DisplayElement()
        ui.make_splash(MockFontLoader())

        u = Updater()
        u.low_memory_warning = True

        label.init(ui, u)
        
        self.assertIn("Memory", ui.splash.mock_content[0].mock_content[0].text)
        self.assertIn("Memory", label.text)

        label.text = "foo2"
        self.assertIn("Memory", ui.splash.mock_content[0].mock_content[0].text)
        self.assertIn("Memory", label.text)


    def test_text_override(self):
        cb = MockDisplayLabelCallback()
        cb.label_text = "abc"

        label = DisplayLabel(
            layout = {
                "font": "foo"
            },
            callback = cb,
            bounds = DisplayBounds(20, 21, 200, 210)
        )

        label.update_label()
        self.assertEqual(label.text, "abc")

        label.override_text = "bar"
        label.update_label()
        self.assertEqual(label.text, "bar")

        label.override_text = None
        label.update_label()
        self.assertEqual(label.text, "abc")


