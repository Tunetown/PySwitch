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
    from lib.pyswitch.clients.local.actions.pager import *
    from lib.pyswitch.ui.elements import DisplayLabel
    
    from .mocks_appl import *

######################################################


class TestLocalPagerAction(unittest.TestCase):

    def test_without_label(self):
        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "color": (3, 4, 5),
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "color": (3, 6, 8),
                    "text": "bar"
                },
            ],
            led_brightness = 0.4
        )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        pager.init(appl, switch_pager)
        pager.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 4, 5))
        self.assertEqual(switch_pager.brightness, 0.4)

        # Select page 2
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (3, 6, 8))
        self.assertEqual(switch_pager.brightness, 0.4)

        # Select page 1 again
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 4, 5))
        self.assertEqual(switch_pager.brightness, 0.4)


    def test_no_leds(self):
        pager = PagerAction(
            pages = [
                {
                    "id": 1
                },
                {
                    "id": 2
                },
            ],
            use_leds = False
        )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        pager.init(appl, switch_pager)
        pager.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (0, 0, 0))
        self.assertEqual(switch_pager.brightness, 0)

        # Select page 2
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (0, 0, 0))
        self.assertEqual(switch_pager.brightness, 0)

        # Select page 1 again
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (0, 0, 0))
        self.assertEqual(switch_pager.brightness, 0)

        
    def test_with_label_and_leds(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "color": (3, 4, 5),
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "color": (3, 6, 8),
                    "text": "bar"
                },
            ],
            display = display,
            led_brightness = 0.4
        )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        # These calls shall do nothing before init!
        pager.push()
        pager.update_displays()

        pager.init(appl, switch_pager)
        pager.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 4, 5))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (3, 4, 5))

        # Select page 2
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (3, 6, 8))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "bar")
        self.assertEqual(pager.label.back_color, (3, 6, 8))

        # Select page 1 again
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 4, 5))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (3, 4, 5))


    def test_without_page_color(self):
        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "color": (3, 4, 5),
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "text": "bar"
                },
            ],
            led_brightness = 0.4
        )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        pager.init(appl, switch_pager)
        pager.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 4, 5))
        self.assertEqual(switch_pager.brightness, 0.4)

        # Select page 2
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (255, 255, 255))
        self.assertEqual(switch_pager.brightness, 0.4)

        # Select page 1 again
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 4, 5))
        self.assertEqual(switch_pager.brightness, 0.4)


    def test_display_no_back_color(self):
        display = DisplayLabel(layout = {
            "font": "foo"
        })

        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "color": (3, 4, 5),
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "color": (3, 6, 8),
                    "text": "bar"
                },
            ],
            display = display,
            led_brightness = 0.4
        )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        # These calls shall do nothing before init!
        pager.push()
        pager.update_displays()

        pager.init(appl, switch_pager)
        pager.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 4, 5))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, None)

        # Select page 2
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (3, 6, 8))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "bar")
        self.assertEqual(pager.label.back_color, None)

        # Select page 1 again
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 4, 5))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, None)

    
    ###########################################################################################################


    def test_select_page(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "color": (3, 4, 5),
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "text": "bar"
                },
            ],
            display = display,
            led_brightness_on = 0.4,
            led_brightness_off = 0.3,
            select_page = 2
        )

        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC()
        }):
            proxy = pager.proxy(
                page_id = 1,
                use_leds = True
            )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        # These calls shall do nothing before init!
        pager.push()
        pager.update_displays()

        pager.init(appl, switch_pager)
        pager.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (255, 255, 255))
        self.assertEqual(switch_pager.brightness, 0.3)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (3, 4, 5))

        # Select page 2
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (255, 255, 255))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "bar")
        self.assertEqual(pager.label.back_color, (255, 255, 255))

        # Select page 2 again
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (255, 255, 255))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "bar")
        self.assertEqual(pager.label.back_color, (255, 255, 255))

        # Use proxy to go back to page 1
        proxy.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (255, 255, 255))
        self.assertEqual(switch_pager.brightness, 0.3)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (3, 4, 5))


    def test_select_page_no_color_on_page_1(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "color": (3, 6, 8),
                    "text": "bar"
                },
            ],
            display = display,
            led_brightness_on = 0.4,
            led_brightness_off = 0.3,
            select_page = 2
        )

        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC()
        }):
            proxy = pager.proxy(
                page_id = 1,
                use_leds = True
            )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        # These calls shall do nothing before init!
        pager.push()
        pager.update_displays()

        pager.init(appl, switch_pager)
        pager.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 6, 8))
        self.assertEqual(switch_pager.brightness, 0.3)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (255, 255, 255))

        # Select page 2
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (3, 6, 8))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "bar")
        self.assertEqual(pager.label.back_color, (3, 6, 8))

        # Select page 2 again
        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_pager.color, (3, 6, 8))
        self.assertEqual(switch_pager.brightness, 0.4)

        self.assertEqual(pager.label.text, "bar")
        self.assertEqual(pager.label.back_color, (3, 6, 8))

        # Use proxy to go back to page 1
        proxy.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_pager.color, (3, 6, 8))
        self.assertEqual(switch_pager.brightness, 0.3)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (255, 255, 255))


    def test_no_pages(self):
        pager = PagerAction(
            pages = []
        )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC()
        }):
            proxy = pager.proxy(
                page_id = 10
            )

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )

        switch_proxy = MockFootswitch(
            actions = [
                proxy
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        pager.init(appl, switch_pager)
        proxy.init(appl, switch_proxy)
        
        pager.update_displays()
        proxy.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        proxy.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)


    ###########################################################################################


    def test_proxy(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "color": (3, 4, 5),
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "color": (3, 6, 8),
                    "text": "bar"
                },
            ],
            led_brightness_on = 0.4,
            led_brightness_off = 0.3,
            display = display
        )

        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC()
        }):
            proxy_1 = pager.proxy(
                page_id = 1,
                use_leds = True
            )

            proxy_2 = pager.proxy(
                page_id = 2,
                use_leds = True
            )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        switch_proxy_1 = MockFootswitch(
            pixels = [0],
            actions = [
                proxy_1
            ]
        )

        switch_proxy_2 = MockFootswitch(
            pixels = [0],
            actions = [
                proxy_2
            ]
        )

        appl = MockController(
            inputs = [
                switch, 
                switch_pager,
                switch_proxy_1,
                switch_proxy_2
            ]
        )
        
        pager.init(appl, switch_pager)
        proxy_1.init(appl, switch_proxy_1)
        proxy_2.init(appl, switch_proxy_2)

        pager.update_displays()
        proxy_1.update_displays()
        proxy_2.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_proxy_1.color, (3, 4, 5))
        self.assertEqual(switch_proxy_2.color, (3, 6, 8))
        self.assertEqual(switch_proxy_1.brightness, 0.4)
        self.assertEqual(switch_proxy_2.brightness, 0.3)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (3, 4, 5))

        # Select page 2
        proxy_2.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_proxy_1.color, (3, 4, 5))
        self.assertEqual(switch_proxy_2.color, (3, 6, 8))
        self.assertEqual(switch_proxy_1.brightness, 0.3)
        self.assertEqual(switch_proxy_2.brightness, 0.4)

        self.assertEqual(pager.label.text, "bar")
        self.assertEqual(pager.label.back_color, (3, 6, 8))

        # Select page 1
        proxy_1.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_proxy_1.color, (3, 4, 5))
        self.assertEqual(switch_proxy_2.color, (3, 6, 8))
        self.assertEqual(switch_proxy_1.brightness, 0.4)
        self.assertEqual(switch_proxy_2.brightness, 0.3)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (3, 4, 5))


    def test_proxy_no_color_on_page_1(self):
        display = DisplayLabel(layout = {
            "font": "foo",
            "backColor": (0, 0, 0)
        })

        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "color": (3, 6, 8),
                    "text": "bar"
                },
            ],
            led_brightness_on = 0.4,
            led_brightness_off = 0.3,
            display = display
        )

        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC()
        }):
            proxy_1 = pager.proxy(
                page_id = 1,
                use_leds = True
            )

            proxy_2 = pager.proxy(
                page_id = 2,
                use_leds = True
            )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        switch_proxy_1 = MockFootswitch(
            pixels = [0],
            actions = [
                proxy_1
            ]
        )

        switch_proxy_2 = MockFootswitch(
            pixels = [0],
            actions = [
                proxy_2
            ]
        )

        appl = MockController(
            inputs = [
                switch, 
                switch_pager,
                switch_proxy_1,
                switch_proxy_2
            ]
        )
        
        pager.init(appl, switch_pager)
        proxy_1.init(appl, switch_proxy_1)
        proxy_2.init(appl, switch_proxy_2)

        pager.update_displays()
        proxy_1.update_displays()
        proxy_2.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_proxy_1.color, (255, 255, 255))
        self.assertEqual(switch_proxy_2.color, (3, 6, 8))
        self.assertEqual(switch_proxy_1.brightness, 0.4)
        self.assertEqual(switch_proxy_2.brightness, 0.3)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (255, 255, 255))

        # Select page 2
        proxy_2.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), False)
        self.assertEqual(pager.enable_callback.enabled(action_2), True)

        self.assertEqual(switch_proxy_1.color, (255, 255, 255))
        self.assertEqual(switch_proxy_2.color, (3, 6, 8))
        self.assertEqual(switch_proxy_1.brightness, 0.3)
        self.assertEqual(switch_proxy_2.brightness, 0.4)

        self.assertEqual(pager.label.text, "bar")
        self.assertEqual(pager.label.back_color, (3, 6, 8))

        # Select page 1
        proxy_1.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        self.assertEqual(switch_proxy_1.color, (255, 255, 255))
        self.assertEqual(switch_proxy_2.color, (3, 6, 8))
        self.assertEqual(switch_proxy_1.brightness, 0.4)
        self.assertEqual(switch_proxy_2.brightness, 0.3)

        self.assertEqual(pager.label.text, "foo")
        self.assertEqual(pager.label.back_color, (255, 255, 255))

    
    def test_proxy_pager_not_initialized(self):
        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "color": (3, 4, 5),
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "color": (3, 6, 8),
                    "text": "bar"
                },
            ],
            led_brightness_on = 0.4,
            led_brightness_off = 0.3
        )

        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC()
        }):
            proxy_1 = pager.proxy(
                page_id = 1
            )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )
        
        switch_proxy_1 = MockFootswitch(
            pixels = [0],
            actions = [
                proxy_1
            ]
        )

        appl = MockController(
            inputs = [
                switch, 
                switch_proxy_1
            ]
        )
        
        proxy_1.init(appl, switch_proxy_1)

        with self.assertRaises(Exception):
            proxy_1.push()


    def test_proxy_invalid_page(self):
        pager = PagerAction(
            pages = [
                {
                    "id": 1, 
                    "color": (3, 4, 5),
                    "text": "foo"
                },
                {
                    "id": 2, 
                    "color": (3, 6, 8),
                    "text": "bar"
                }
            ],
            select_page = 1
        )

        action_1 = MockAction({ "enableCallback": pager.enable_callback, "id": 1 })
        action_2 = MockAction({ "enableCallback": pager.enable_callback, "id": 2 })

        with patch.dict(sys.modules, {
            "micropython": MockMicropython,
            "gc": MockGC()
        }):
            proxy = pager.proxy(
                page_id = 10
            )

        switch = MockFootswitch(
            actions = [
                action_1, 
                action_2
            ]
        )

        switch_proxy = MockFootswitch(
            actions = [
                proxy
            ]
        )
        
        switch_pager = MockFootswitch(
            pixels = [0],
            actions = [
                pager
            ]
        )
        
        appl = MockController(
            inputs = [
                switch, 
                switch_pager
            ]
        )
        
        pager.init(appl, switch_pager)
        proxy.init(appl, switch_proxy)
        
        pager.update_displays()
        proxy.update_displays()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        pager.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)

        proxy.push()

        self.assertEqual(pager.enable_callback.enabled(action_1), True)
        self.assertEqual(pager.enable_callback.enabled(action_2), False)