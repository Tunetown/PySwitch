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
    from lib.pyswitch.ui.UiController import UiController
    # from lib.pyswitch.misc import Updater

    from .mocks_ui import *
    from .mocks_appl import *
    from .mocks_callback import *



class MockUiController(UiController):
    def __init__(self, display_driver, font_loader, splash_callback = None):
        super().__init__(display_driver, font_loader, splash_callback)

        self.num_show_calls = 0

    def show(self):
        super().show()

        self.num_show_calls += 1


#########################################################################


class TestUiController(unittest.TestCase):

    def test(self):
        display_driver = MockDisplayDriver(300, 400)
        display_driver.init()

        font_loader = MockFontLoader()

        display = DisplayElement(id = 1)
        cb = MockSplashCallback(output = display)

        ui = UiController(display_driver, font_loader, cb)        

        appl = MockController()
        display.init(display, appl)
        ui.init(appl)

        ui.show()

        self.assertEqual(ui._UiController__current_splash_element, display)
        self.assertEqual(display.font_loader, font_loader)
        self.assertEqual(ui.bounds, DisplayBounds(0, 0, 300, 400))

        self.assertEqual(display.initialized(), True)
        self.assertEqual(display_driver.tft.show_calls, [display.splash])

        display_2 = DisplayElement(id = 2)
        cb.output = display_2

        ui.show()

        self.assertEqual(ui._UiController__current_splash_element, display_2)
        self.assertEqual(display_2.font_loader, font_loader)

        self.assertEqual(display_2.initialized(), True)
        self.assertEqual(display_driver.tft.show_calls, [display.splash, display_2.splash])


    def test_mappings(self):
        mapping_1 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x20, 0x00, 0x00, 0x09, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x20],
            #     data = [0x00, 0x00, 0x09]
            # )
        )

        mapping_2 = MockParameterMapping(
            response = (0xf0, 0x00, 0x10, 0x22, 0x00, 0x00, 0xe9, 0xf7)
            # SystemExclusive(
            #     manufacturer_id = [0x00, 0x10, 0x22],
            #     data = [0x00, 0x00, 0xe9]
            # )
        )

        display_driver = MockDisplayDriver(300, 400, init = True)
        font_loader = MockFontLoader()

        display = DisplayElement(id = 1)
        ui = MockUiController(
            display_driver = display_driver, 
            font_loader = font_loader
        )

        cb = MockSplashCallback(
            output = display,
            mappings = [
                mapping_1,
                mapping_2
            ]
        )

        ui.set_callback(cb)

        appl = MockController()
        ui.init(appl)

        ui.show()

        self.assertEqual(ui._UiController__current_splash_element.font_loader, font_loader)
        self.assertEqual(ui._UiController__current_splash_element, display)
        self.assertEqual(ui.bounds, DisplayBounds(0, 0, 300, 400))

        self.assertEqual(ui._UiController__current_splash_element.initialized(), True)
        self.assertEqual(display_driver.tft.show_calls, [ui._UiController__current_splash_element.splash])

        self.assertEqual(appl.client.register_calls, [
            {
                "mapping": mapping_1,
                "listener": cb
            },
            {
                "mapping": mapping_2,
                "listener": cb
            }
        ])

        appl.update()

        self.assertEqual(appl.client.request_calls, [
            {
                "mapping": mapping_1,
                "listener": cb
            },
            {
                "mapping": mapping_2,
                "listener": cb
            }
        ])

        self.assertEqual(ui.num_show_calls, 1)
        
        ui.parameter_changed(None)

        self.assertEqual(ui.num_show_calls, 2)


    def test_add_updateables(self):
        display_driver = MockDisplayDriver(w = 300, h = 400, init = True)

        element_1 = DisplayElement(id = 1)
        element_2 = DisplayElement(id = 2)

        element_3 = MockUpdateableDisplayElement(id = 3)
        element_2.add(element_3)

        display = DisplayElement(
            children = [
                None,
                element_1,
                None,
                element_2,
                None
            ]
        )

        ui = UiController(display_driver, MockFontLoader(), MockSplashCallback(output = display))
        appl = MockController()
        appl.add_updateable(ui)
        ui.init(appl)
        
        self.assertEqual(element_1.initialized(), False)
        self.assertEqual(element_2.initialized(), False)
        self.assertEqual(element_3.initialized(), False)

        ui.show()

        self.assertEqual(element_1.initialized(), True)
        self.assertEqual(element_2.initialized(), True)
        self.assertEqual(element_3.initialized(), True)

        appl.update()

        self.assertEqual(element_3.num_update_calls, 1)


    def test_error_show_before_init(self):
        display_driver = MockDisplayDriver(300, 400)
        display_driver.init()

        font_loader = MockFontLoader()

        element_1 = DisplayElement(id = 1)

        ui = UiController(display_driver, font_loader, MockSplashCallback(output = element_1))

        with self.assertRaises(Exception):
            ui.show()


    def test_terminated_request(self):
        display_driver = MockDisplayDriver(300, 400)
        display_driver.init()

        font_loader = MockFontLoader()

        element_1 = DisplayElement(id = 1)

        ui = UiController(display_driver, font_loader, MockSplashCallback(output = element_1))

        # Method must exist
        ui.request_terminated(None)


