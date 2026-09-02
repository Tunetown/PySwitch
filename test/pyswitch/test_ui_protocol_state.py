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
    from lib.pyswitch.ui.elements import BidirectionalProtocolState
    from lib.pyswitch.controller.client import BidirectionalClient
    
    from .mocks_appl import MockBidirectionalProtocol, MockMidiController, MockClient, MockController
    from .mocks_ui import *
    

class TestProtocolState(unittest.TestCase):

    def test(self):
        display = BidirectionalProtocolState(
            bounds = DisplayBounds(200, 200, 400, 500)
        )

        self.assertEqual(display.bounds, DisplayBounds(600 - 4 - 2, 200 + 2, 4, 4))

        protocol = MockBidirectionalProtocol()        

        appl = MockController(
            client = BidirectionalClient(
                midi = MockMidiController(), 
                config = {}, 
                protocol = protocol
            )
        )

        ui = DisplayElement()
        ui.make_splash(None)

        display.init(ui, appl)

        protocol.output_color = (2, 5, 6)
        display.update()
        self.assertEqual(display._BidirectionalProtocolState__dot.fill, (2, 5, 6))

        protocol.output_color = (11, 45, 66)
        display.update()
        self.assertEqual(display._BidirectionalProtocolState__dot.fill, (11, 45, 66))

        display.update()
        self.assertEqual(display._BidirectionalProtocolState__dot.fill, (11, 45, 66))
    
    
    def test_no_protocol(self):
        display = BidirectionalProtocolState(
            bounds = DisplayBounds(22, 33, 44, 55)
        )

        appl = MockController()

        ui = DisplayElement()
        ui.make_splash(None)

        display.init(ui, appl)

        display.update()
        




