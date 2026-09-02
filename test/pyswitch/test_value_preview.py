import sys
import unittest
from unittest.mock import patch   # Necessary workaround! Needs to be separated.

from .mocks_lib import *

# Import subject under test
with patch.dict(sys.modules, {
    "micropython": MockMicropython,
    "usb_midi": MockUsbMidi(),
    "displayio": MockDisplayIO(),
    "adafruit_display_text": MockAdafruitDisplayText(),
    "adafruit_display_shapes.rect": MockDisplayShapes().rect(),
    "gc": MockGC()
}):
    from .mocks_callback import *

    from lib.pyswitch.controller.preview import ValuePreview
    from lib.pyswitch.ui.elements import DisplayLabel
    from .mocks_appl import *


class MockPreviewClient:
    def __init__(self):
        self.cancel_calls = 0

    def cancel(self):
        self.cancel_calls += 1

##################################################################################################################################


class TestValuePreview(unittest.TestCase):

    def test_private_init(self):
        with self.assertRaises(Exception):
            ValuePreview(
                create_key = None, 
                label = None
            )

    def test_singleton(self):
        display_1 = DisplayLabel(layout = {
            "font": "foo"
        })
        display_2 = DisplayLabel(layout = {
            "font": "foo"
        })

        vp_1 = ValuePreview.get(label = display_1)
        vp_2 = ValuePreview.get(label = display_2)

        self.assertEqual(ValuePreview.get(label = display_1), vp_1)
        self.assertEqual(ValuePreview.get(label = display_2), vp_2)

        self.assertEqual(ValuePreview.get(label = display_1), vp_1)
        self.assertEqual(ValuePreview.get(label = display_2), vp_2)


    #########################################################################################


    def test_stay(self):
        display = DisplayLabel(
            layout = {
                "font": "foo"
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )
        display.update_label()

        self.assertEqual(display.text, "foo")
        
        vp = ValuePreview.get(
            label = display
        )

        vp.preview(
            text = "text",
            stay = True,
            timeout_millis = None
        )

        self.assertEqual(display.text, "text")
        
        vp.update()

        self.assertEqual(display.text, "text")

        vp.reset()

        self.assertEqual(display.text, "foo")


    def test_timeout(self):
        display = DisplayLabel(
            layout = {
                "font": "foo"
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )
        display.update_label()

        self.assertEqual(display.text, "foo")
        
        vp = ValuePreview.get(
            label = display
        )

        vp.preview(
            text = "text",
            timeout_millis = 123
        )

        self.assertEqual(vp._ValuePreview__period.interval, 123)
        vp._ValuePreview__period = MockPeriodCounter()
        period = vp._ValuePreview__period

        self.assertEqual(display.text, "text")
        
        vp.update()

        self.assertEqual(display.text, "text")
        
        period.exceed_next_time = True
        vp.update()

        self.assertEqual(display.text, "foo")


    def test_timeout_stay(self):
        display = DisplayLabel(
            layout = {
                "font": "foo"
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )
        display.update_label()

        self.assertEqual(display.text, "foo")
        
        vp = ValuePreview.get(display)

        vp.preview(
            text = "text",
            stay = True,
            timeout_millis = 123
        )

        vp._ValuePreview__period = MockPeriodCounter()
        period = vp._ValuePreview__period

        self.assertEqual(display.text, "text")
        
        vp.update()

        self.assertEqual(display.text, "text")
        
        period.exceed_next_time = True
        vp.update()

        self.assertEqual(display.text, "text")

        vp.reset()

        self.assertEqual(display.text, "text")

        period.exceed_next_time = True
        vp.update()

        self.assertEqual(display.text, "foo")


    def test_timeout_reset_immediately(self):
        display = DisplayLabel(
            layout = {
                "font": "foo"
            },
            callback = MockDisplayLabelCallback(label_text = "foo")
        )
        display.update_label()

        self.assertEqual(display.text, "foo")
        
        vp = ValuePreview.get(
            label = display
        )

        vp.preview(
            text = "text",
            stay = True,
            timeout_millis = 123
        )

        vp._ValuePreview__period = MockPeriodCounter()
        period = vp._ValuePreview__period

        self.assertEqual(display.text, "text")
        
        vp.update()

        self.assertEqual(display.text, "text")
        
        period.exceed_next_time = True
        vp.update()

        self.assertEqual(display.text, "text")

        vp.reset(immediately = True)

        self.assertEqual(display.text, "foo")


    def test_clients(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "text": "foo"
        })
        display.update_label()

        self.assertEqual(display.text, "foo")
        
        vp = ValuePreview.get(label = display)

        client_1 = MockPreviewClient()
        client_2 = MockPreviewClient()

        vp.preview(
            text = "text",
            client = client_1
        )

        self.assertEqual(display.text, "text")
        self.assertEqual(client_1.cancel_calls, 0)
        self.assertEqual(client_2.cancel_calls, 0)

        vp.preview(
            text = "text2",
            client = client_2
        )

        self.assertEqual(display.text, "text2")
        self.assertEqual(client_1.cancel_calls, 1)
        self.assertEqual(client_2.cancel_calls, 0)

        vp.preview(
            text = "text3",
            client = client_1
        )

        self.assertEqual(display.text, "text3")
        self.assertEqual(client_1.cancel_calls, 1)
        self.assertEqual(client_2.cancel_calls, 1)
