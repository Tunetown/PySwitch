from ....controller.callbacks import Callback
from ....controller.actions import Action

class PagerAction(Callback, Action):
    class _EnableCallback(Callback):
        def __init__(self, pager):
            super().__init__()
            self.__pager = pager

        def enabled(self, action):
            return (action.id == self.__pager.current_page_id)

    # The PagerAction is used to control multiple other actions to provide paging. Define this action for one switch which will by default rotate through the defined pages.
    # For the actions you want to be part of pages, just assign them using the paging buttons (which will set the id and enable_callback parameters for you).
    # Also, it is possible to have more than one pager in a configuration.
    # 
    # <b>Rotate Through Pages:</b>
    # If you want to rotate through pages, just use this action with select_page set to None, which is the default. The switch will then rotate through the pages. 
    # 
    # <b>Directly Select Pages:</b>
    # If you want to have one switch dedicated to select each page, set select_page here to the page you want to select with the switch this pager is assigned to, and use the "Select Page" action (assigned to this pager) for the other switches to select the further pages directly.
    def __init__(self, 
                 pages,                         # This has to be a list of dicts like follows:
                                                # {
                                                #      "id": Page ID. All actions with this ID will be enabled
                                                #      "color": Page color. LEDs and label will be colored this way (for the brightness, there is a separate parameter)
                                                #      "text": Label text for the page
                                                # }

                 select_page = None,            # If None, the pages will be rotated. If set to a page ID, the action will select the passed page (use a 
                                                # "Select Page" action for directly selecting the other pages)

                 led_brightness = 0.15,         # LED brightness for the pager in range [0..1]. Only used when selet_page is None (rotate mode).
                 led_brightness_off = 0.02,     # LED brightness for the pager when select_page is set and the page is not currently selected. Range [0..1].
                 led_brightness_on = 0.3,       # LED brightness for the pager when select_page is set and the page is currently selected. Range [0..1].
                 mappings = [],                 # List of mappings the paging depends on (optional)
                 use_leds = True,
                 id = None,
                 display = None,
                 enable_callback = None
        ):
        Callback.__init__(self, mappings)
        Action.__init__(self, {
            "useSwitchLeds": use_leds,
            "id": id,
            "display": display,
            "enableCallback": enable_callback
        })

        self.pages = pages
        self.led_brightness = led_brightness
        self.led_brightness_on = led_brightness_on
        self.led_brightness_off = led_brightness_off
        self.__proxies = []

        self.current_page_index = -1
        self.current_page_id = None
        self.__select_page_index = self._get_page_index(select_page) if select_page else None

        self.enable_callback = PagerAction._EnableCallback(self)

    # This controls a Pager Action from another switch, making it possible to directly select pages with dedicated switches.
    # 
    # You always need to have a Pager Action which defines the pages, which also MUST be assigned to a switch. Set "select_page" on this pager to the first page, and for selecting the other pages, create "Select Page" actions for other switches. For example, to have 3 pages and 3 switches:
    # <ul>
    #     <li>Switch 1: Pager Action with "select_page" set to the first page</li>
    #     <li>Switch 2: Select Page action set to page 2</li>
    #     <li>Switch 3: Select Page action set to page 3</li>
    # </ul>
    # The LED and display brightness settings are determined from the connected pager and can be set there if needed.
    def proxy(self, 
              page_id,                    # Sets the page to be selected with this action
              use_leds = True, 
              id = None, 
              enable_callback = None
        ):
        from .pager_direct import DirectPagerProxy

        proxy = DirectPagerProxy(self, 
                                 page_index = self._get_page_index(page_id),
                                 use_leds = use_leds,
                                 id = id,
                                 enable_callback = enable_callback)
        
        self.__proxies.append(proxy)
        return proxy

    # Determines the page index for a given page ID
    def _get_page_index(self, page_id):
        for index in range(len(self.pages)):
            if self.pages[index]["id"] == page_id:
                return index
        return None

    # Must be called before usage
    def init(self, appl, switch):
        Action.init(self, appl, switch)

        self.current_page_index = 0
        self.current_page_id = self.pages[self.current_page_index]["id"] if len(self.pages) > 0 else None

    # Called when the switch is pushed down
    def push(self):
        if not len(self.pages):
            return
        
        if self.current_page_index < 0:
            return 
        
        if self.__select_page_index != None:
            # Direct select
            self.current_page_index = self.__select_page_index
        else:
            # Next page
            self.current_page_index += 1
            while self.current_page_index >= len(self.pages):
                self.current_page_index = 0

        self.current_page_id = self.pages[self.current_page_index]["id"] if len(self.pages) > 0 else None

        self.appl.reset_actions()
        self.update_displays()

    def update_displays(self):
        if not len(self.pages):
            return

        if self.current_page_index < 0:
            return 
        
        if not self.enabled:
            return
        
        page_current = self.pages[self.current_page_index]
        
        # LEDs
        if self.__select_page_index != None:
            # Direct select
            page_select = self.pages[self.__select_page_index]
            
            if "color" in page_select:
                self.switch_color = page_select["color"]
            else:
                self.switch_color = (255, 255, 255)

            is_current = self.__select_page_index == self.current_page_index                
            self.switch_brightness = self.led_brightness_on if is_current else self.led_brightness_off                     
        else:
            # Rotating
            if "color" in page_current:                
                self.switch_color = page_current["color"]
            else:
                self.switch_color = (255, 255, 255)
            
            self.switch_brightness = self.led_brightness

        # Label (doing the same thing for rotary or direct modes)
        if self.label:
            self.label.text = page_current["text"] if "text" in page_current else ""
            
            if self.label.back_color:
                if "color" in page_current:                
                    self.label.back_color = page_current["color"]
                else:
                    self.label.back_color = (255, 255, 255)
        
        # Update all proxies, too
        for proxy in self.__proxies:
            proxy.update_displays()

