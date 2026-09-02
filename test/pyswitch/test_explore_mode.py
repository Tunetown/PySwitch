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
    "usb_midi": MockUsbMidi(),
    "gc": MockGC()
}):
    from .mocks_misc import MockMisc

    with patch.dict(sys.modules, {
        "lib.pyswitch.misc": MockMisc
    }):

        from .mocks_appl import *
        from .mocks_ui import *
        from lib.pyswitch.controller.explore import ExploreModeController
        from lib.pyswitch.colors import Colors


class MockSwitchFactory:
    def __init__(self):
        self.switches = []

    def create_switch(self, port):
        switch = MockSwitch(port)
        if port == "MockPort_23":
            switch.raise_on_init = ValueError()
        else:
            self.switches.append(switch)
        return switch
    
    def find_by_port(self, port):   
        for switch in self.switches:
            if switch.port != port:
                continue
            return switch
        return None          


class TestExploreMode(unittest.TestCase):

    def test_minimal(self):
        appl = ExploreModeController(MockBoard(), MockSwitchFactory())    # Must not throw
        appl.init()            
        appl.tick()
        appl.tick()
            

    def test_console_gpio_detect(self):
        MockMisc.reset_mock()
        led_driver = MockNeoPixelDriver()
        switch_factory = MockSwitchFactory()

        appl = ExploreModeController(
            board = MockBoard(), 
            switch_factory = switch_factory,
            led_driver = led_driver,
            num_pixels_per_switch = 2
        )

        appl.init()

        self.assertIn("EXPLORE MODE", MockMisc.msgs_str)
        self.assertIn("GP4", MockMisc.msgs_str)
        self.assertIn("GP6", MockMisc.msgs_str)
        self.assertIn("GP11", MockMisc.msgs_str)
        self.assertNotIn("Error", MockMisc.msgs_str)

        self.assertEqual(len(appl.switches), 3)
        
        # Build scenario
        switch_factory.find_by_port("MockPort_6").shall_be_pushed = True
        MockMisc.reset_mock()

        appl.tick()
        appl.tick()
            
        self.assertNotIn("GP4", MockMisc.msgs_str)
        self.assertIn("GP6", MockMisc.msgs_str)
        self.assertNotIn("GP11", MockMisc.msgs_str)
        
        # Next step
        switch_factory.find_by_port("MockPort_6").shall_be_pushed = False
        switch_factory.find_by_port("MockPort_11").shall_be_pushed = True
        MockMisc.reset_mock()

        appl.tick()
        appl.tick()
            
        self.assertNotIn("GP4", MockMisc.msgs_str)
        self.assertNotIn("GP6", MockMisc.msgs_str)
        self.assertIn("GP11", MockMisc.msgs_str)            
        

##################################################################################################


    def test_ui_gpio_detect_5rows(self):
        MockMisc.reset_mock()
        led_driver = MockNeoPixelDriver()
        switch_factory = MockSwitchFactory()
        ui = MockUiController(width = 999, height = 600)

        appl = ExploreModeController(
            board = MockBoard(), 
            switch_factory = switch_factory,
            led_driver = led_driver,
            num_pixels_per_switch = 2,
            ui = ui
        )

        appl.init()

        ui.show()

        self.assertNotIn("EXPLORE MODE", MockMisc.msgs_str)
        self.assertNotIn("GP4", MockMisc.msgs_str)
        self.assertNotIn("GP6", MockMisc.msgs_str)
        self.assertNotIn("GP11", MockMisc.msgs_str)
        self.assertNotIn("Error", MockMisc.msgs_str)

        self.assertEqual(len(appl.switches), 3)
        self.assertEqual(len(ui.shown_root.children), 2)
        self.assertEqual(len(ui.shown_root.children[1].children), 1)
        self.assertEqual(len(ui.shown_root.children[1].children[0].children), 3)
        
        label_0 = ui.shown_root.children[1].children[0].children[0]
        label_1 = ui.shown_root.children[1].children[0].children[1]
        label_2 = ui.shown_root.children[1].children[0].children[2]

        self.assertEqual(label_0.bounds, DisplayBounds(0, 0, 333, 560))
        self.assertEqual(label_1.bounds, DisplayBounds(333, 0, 333, 560))
        self.assertEqual(label_2.bounds, DisplayBounds(666, 0, 333, 560))

        self.assertEqual(label_0.text, "GP11")
        self.assertEqual(label_1.text, "GP4")
        self.assertEqual(label_2.text, "GP6")

        # Build scenario
        switch_factory.find_by_port("MockPort_6").shall_be_pushed = True
        MockMisc.reset_mock()

        appl.tick()
        appl.tick()
            
        self.assertNotIn("GP4", MockMisc.msgs_str)
        self.assertIn("GP6", MockMisc.msgs_str)
        self.assertNotIn("GP11", MockMisc.msgs_str)

        self.assertEqual(label_0.back_color, Colors.DARK_BLUE)
        self.assertEqual(label_1.back_color, Colors.DARK_BLUE)
        self.assertEqual(label_2.back_color, Colors.RED)
        
        # Next step
        switch_factory.find_by_port("MockPort_6").shall_be_pushed = False
        switch_factory.find_by_port("MockPort_11").shall_be_pushed = True
        MockMisc.reset_mock()

        appl.tick()
        appl.tick()
            
        self.assertNotIn("GP4", MockMisc.msgs_str)
        self.assertNotIn("GP6", MockMisc.msgs_str)
        self.assertIn("GP11", MockMisc.msgs_str)            

        self.assertEqual(label_0.back_color, Colors.RED)
        self.assertEqual(label_1.back_color, Colors.DARK_BLUE)
        self.assertEqual(label_2.back_color, Colors.LIGHT_BLUE)
        

##################################################################################################


    def test_ui_gpio_detect_2rows(self):
        MockMisc.reset_mock()
        ui = MockUiController(width = 1000, height = 600)

        appl = ExploreModeController(
            board = MockBoard(), 
            switch_factory = MockSwitchFactory(),
            led_driver = MockNeoPixelDriver(),
            num_pixels_per_switch = 2,
            ui = ui,
            num_port_columns = 2
        )

        appl.init()

        ui.show()

        self.assertEqual(len(appl.switches), 3)
        self.assertEqual(len(ui.shown_root.children), 2)
        self.assertEqual(len(ui.shown_root.children[1].children), 2)
        self.assertEqual(len(ui.shown_root.children[1].children[0].children), 2)
        self.assertEqual(len(ui.shown_root.children[1].children[1].children), 1)
        
        label_0 = ui.shown_root.children[1].children[0].children[0]
        label_1 = ui.shown_root.children[1].children[0].children[1]
        label_2 = ui.shown_root.children[1].children[1].children[0]

        self.assertEqual(label_0.bounds, DisplayBounds(0, 0, 500, 280))
        self.assertEqual(label_1.bounds, DisplayBounds(500, 0, 500, 280))
        self.assertEqual(label_2.bounds, DisplayBounds(0, 280, 1000, 280))

        self.assertEqual(label_0.text, "GP11")
        self.assertEqual(label_1.text, "GP4")
        self.assertEqual(label_2.text, "GP6")


##################################################################################################


    def test_console_pixel_scan(self):
        self._test_console_pixel_scan(0, "up")
        self._test_console_pixel_scan(1, "down")
        self._test_console_pixel_scan(2, "up")

    def _test_console_pixel_scan(self, switch_id, direction):
        MockMisc.reset_mock()
        led_driver = MockNeoPixelDriver()
        switch_factory = MockSwitchFactory()

        appl = ExploreModeController(
            board = MockBoard(), 
            switch_factory = switch_factory,
            led_driver = led_driver,
            num_pixels_per_switch = 4
        )

        appl.init()

        self.assertEqual(len(appl.switches), 3)
        
        # Build scenario
        switch_factory.switches[switch_id].shall_be_pushed = True
        MockMisc.reset_mock()
        
        appl.tick()
        appl.tick()
            
        if direction == "up":
            self.assertIn("(0, 1, 2, 3) of 12", MockMisc.msgs_str)            
            self._assert_enlightened(led_driver, (0, 1, 2, 3))
        else:
            self.assertIn("(8, 9, 10, 11) of 12", MockMisc.msgs_str)
            self._assert_enlightened(led_driver, (8, 9, 10, 11))
        
        # Next step
        switch_factory.switches[switch_id].shall_be_pushed = False

        appl.tick()
        appl.tick()
            
        # Next step
        switch_factory.switches[switch_id].shall_be_pushed = True
        MockMisc.reset_mock()            

        appl.tick()
        appl.tick()
            
        self.assertIn("(4, 5, 6, 7) of 12", MockMisc.msgs_str)    
        self._assert_enlightened(led_driver, (4, 5, 6, 7))        
    
        # Next step
        switch_factory.switches[switch_id].shall_be_pushed = False

        appl.tick()
        appl.tick()
            
        # Next step
        switch_factory.switches[switch_id].shall_be_pushed = True
        MockMisc.reset_mock()
        
        appl.tick()
        appl.tick()
        
        if direction == "up":
            self.assertIn("(8, 9, 10, 11) of 12", MockMisc.msgs_str)
            self._assert_enlightened(led_driver, (8, 9, 10, 11))
        else:
            self.assertIn("(0, 1, 2, 3) of 12", MockMisc.msgs_str)     
            self._assert_enlightened(led_driver, (0, 1, 2, 3))       
                
        # Next step        
        switch_factory.switches[switch_id].shall_be_pushed = False

        appl.tick()
        appl.tick()
            
        # Next step
        switch_factory.switches[switch_id].shall_be_pushed = True
        MockMisc.reset_mock()
        
        appl.tick()
        appl.tick()
            
        if direction == "up":
            self.assertIn("(0, 1, 2, 3) of 12", MockMisc.msgs_str)     
            self._assert_enlightened(led_driver, (0, 1, 2, 3))       
        else:
            self.assertIn("(8, 9, 10, 11) of 12", MockMisc.msgs_str)
            self._assert_enlightened(led_driver, (8, 9, 10, 11))                


##################################################################################################


    def test_ui_pixel_scan(self):
        self._test_ui_pixel_scan(0, "up")
        self._test_ui_pixel_scan(1, "down")
        self._test_ui_pixel_scan(2, "up")

    def _test_ui_pixel_scan(self, switch_id, direction):
        MockMisc.reset_mock()
        led_driver = MockNeoPixelDriver()
        switch_factory = MockSwitchFactory()
        ui = MockUiController()

        appl = ExploreModeController(
            board = MockBoard(), 
            switch_factory = switch_factory,
            led_driver = led_driver,
            num_pixels_per_switch = 3,
            ui = ui
        )

        appl.init()

        self.assertEqual(len(appl.switches), 3)        
        
        label = []  # Use a list to keep the field global (dirty hack)

        # Build scenario
        self.assertEqual(len(ui.shown_root.children), 2)
        label.append(ui.shown_root.children[0])

        switch_factory.switches[switch_id].shall_be_pushed = True
        MockMisc.reset_mock()
        
        appl.tick()
        appl.tick()
            
        if direction == "up":
            self.assertIn("(0, 1, 2) of 9", MockMisc.msgs_str)            
            self._assert_enlightened(led_driver, (0, 1, 2))
            self.assertIn("(0, 1, 2) of 9", label[0].text)
        else:
            self.assertIn("(6, 7, 8) of 9", MockMisc.msgs_str)
            self._assert_enlightened(led_driver, (6, 7, 8))
            self.assertIn("(6, 7, 8) of 9", label[0].text)
        
        # Next step        
        switch_factory.switches[switch_id].shall_be_pushed = False

        appl.tick()
        appl.tick()
            
        # Next step
        switch_factory.switches[switch_id].shall_be_pushed = True
        MockMisc.reset_mock()            

        appl.tick()
        appl.tick()
            
        self.assertIn("(3, 4, 5) of 9", MockMisc.msgs_str)    
        self._assert_enlightened(led_driver, (3, 4, 5))        
        self.assertIn("(3, 4, 5) of 9", label[0].text)
            
        # Next step    
        switch_factory.switches[switch_id].shall_be_pushed = False

        appl.tick()
        appl.tick()
            
        # Next step
        switch_factory.switches[switch_id].shall_be_pushed = True
        MockMisc.reset_mock()
        
        appl.tick()
        appl.tick()
            
        if direction == "up":
            self.assertIn("(6, 7, 8) of 9", MockMisc.msgs_str)
            self._assert_enlightened(led_driver, (6, 7, 8))
            self.assertIn("(6, 7, 8) of 9", label[0].text)
        else:
            self.assertIn("(0, 1, 2) of 9", MockMisc.msgs_str)     
            self._assert_enlightened(led_driver, (0, 1, 2))  
            self.assertIn("(0, 1, 2) of 9", label[0].text)     


##################################################################################################


    # Tool to check if the passed pixels are white and the others not
    def _assert_enlightened(self, led_driver, pixels):
        for i in range(len(led_driver.leds)):
            led = led_driver.leds[i]

            if i in pixels:
                self.assertEqual(led, (255, 255, 255))
            else:
                self.assertNotEqual(led, (255, 255, 255))

    
