from .inputs import SwitchController
from .callbacks import Callback
from .actions import Action
from ..ui.layout import remove_from_bottom
from ..ui.elements import DisplayLabel, DisplayElement
from ..ui.DisplaySplitContainer import DisplaySplitContainer
from ..misc import Updater, do_print
from ..colors import Colors

# Action to explore switch GPIO assignments (used internally only in explore mode!)
# Also used to examine neopixel addressing.
class ExploreAction(Action):
    
    def __init__(self, config = {}):
        super().__init__(config)

        self.__name = config["name"]
        self.__step = config["step"]
           
    # Must be called before usage
    def init(self, appl, switch):
        self.appl = appl
        self.switch = switch

        self.__label = self.appl.get_next_port_label()

        if self.__label:
            self.__label.text = self.__name

    def push(self):
        pixel_out = self.__trigger_pixel_search()
        do_print(f"board.{ self.__name } { pixel_out }")

        if self.appl.ui:
            self.appl.pixel_display.text = pixel_out

        if self.__label:
            self.appl.set_latest_port_marker(self.__label)
            # self.appl.reset_port_markers()
            # self.__label.back_color = Colors.RED
            
    # Enlighten the next available switch LEDs and returns a report string.
    def __trigger_pixel_search(self):
        current = self.appl.show_next_switch(self.__step)
        if not current:
            return
        
        # Get output for pixel exploration
        num_switch_leds = len(self.appl.switches) * len(self.switch.pixels)
        pxstr = ", ".join([repr(current[i]) for i in range(self.appl.num_pixels_per_switch)])
        return f"Pixels: ({pxstr}) of {repr(num_switch_leds)}"


###########################################################################################################################


# Must be implemented by switch_factory
#class ExploreModeSwitchFactory:
#    def create_switch(self, port):
#        raise Exception("Must be implemented in child classes")


###########################################################################################################################


# Main application class for Explore Mode
class ExploreModeController(Updater):

    def __init__(self, board, switch_factory, led_driver = None, ui = None, num_pixels_per_switch = 3, num_port_columns = 5):
        Updater.__init__(self)

        self.ui = ui
        self.config = {}  # Dummy for other classes

        self.num_pixels_per_switch = num_pixels_per_switch
        self.__currently_shown_switch_index = -1
        self.__switch_factory = switch_factory
        self.__num_port_columns = num_port_columns
        self.__board = board

        class FakeClient:
            def register(self, mapping, listener):
                pass
            def request(self, mapping, listener):
                pass
        
        self.client = FakeClient()
        self.latest_marker = None

        # Get list of available ports
        available_ports = self.__get_available_ports()

        # NeoPixel driver, initialized to the maximum possible amount of LEDs
        self.led_driver = led_driver
        if self.led_driver:
            self.led_driver.init(len(available_ports) * self.num_pixels_per_switch)

        if self.ui:
            self.__setup_ui()

            # Try to initialize all available ports. This gets us the list of ports successfully assigned.
            ports_assigned = self.__init_switches(available_ports)

            do_print(f"Explore mode: Assigned { repr(len(ports_assigned)) } ports")

            self.reset_port_markers()
        else:
            # Try to initialize all available ports. This gets us the list of ports successfully assigned.
            ports_assigned = self.__init_switches(available_ports)

            do_print("+------------------+")
            do_print("|   EXPLORE MODE   |")
            do_print("+------------------+")
            do_print("")
            do_print("Listening to: ")
            do_print(self.__get_ports_string(ports_assigned))            
            do_print("")

    # Set up user interface
    def __setup_ui(self):
        bounds = self.ui.bounds.clone()

        root = DisplayElement(
            bounds = bounds
        )

        # Display for currently enlightened pixels
        self.pixel_display = DisplayLabel(
            bounds = remove_from_bottom(bounds, 40),
            layout = {
                "font": "/fonts/A12.pcf",
                "backColor": Colors.DARK_GREEN
            }
        )
        root.add(self.pixel_display)

        # Display for ports
        self.__ports_display_rows = DisplaySplitContainer(
            bounds = bounds,
            direction = DisplaySplitContainer.VERTICAL
        )
        root.add(self.__ports_display_rows)

        class EMCallback(Callback):
            def get_root(self):
                return root

        self.ui.set_callback(EMCallback())

        self.ui.init(self)

    # Prepare to run the processing loop
    def init(self):
        # Show user interface    
        if self.ui:    
            self.ui.show()

    # Single tick in the processing loop. Must return True to keep the loop alive. Call this in an endless loop.
    def tick(self):
        # Update switch states
        for switch in self.switches:
            switch.process()

        # Update actions
        self.update()

        return True

    # Called by ExplorePixelAction: Enlightens the next switch according to the passed step value. 
    # Returns the pixels tuple of the switch currently enlightened.
    def show_next_switch(self, step):
        # Add step and regard bounds
        self.__currently_shown_switch_index = self.__currently_shown_switch_index + step
        
        if self.__currently_shown_switch_index >= len(self.switches):
            self.__currently_shown_switch_index = 0
        
        if self.__currently_shown_switch_index < 0:
            self.__currently_shown_switch_index = len(self.switches) - 1

        # Show the currently selected switch, and for all others, indicate
        # whether they increase or decrease.
        ret = None
        for switch in self.switches:
            if switch.em_index == self.__currently_shown_switch_index:
                switch.color = Colors.WHITE
                switch.brightness = 1
                ret = switch.pixels
            else:
                switch.color = Colors.BLUE
                switch.brightness = 0.05
                
                #self._indicate_action_color(switch)

        return ret
    
    # Returns a small representation of the ports passed
    def __get_ports_string(self, ports_assigned):
        return ", ".join([port for port in ports_assigned])

    # Initialize switches. Returns a list of port names initialized
    def __init_switches(self, available_ports):
        self.switches = []
        self._next_label_index = 0

        ret = []

        for port_def in available_ports:
            try:                                
                ret.append(
                    self.__init_switch(
                        port_def,
                        len(ret)
                    )
                )

            except ValueError:
                # This is no error as not all pins can be assigned to switches
                pass

            except Exception as ex:
                do_print(f"Error assigning port { port_def["name"] }:")
                raise ex 

        return ret

    # Initializes a explore port switch. Returns the short ID of the port
    def __init_switch(self, port_def, index):
        if index % 2 == 0:
            scan_step = 1
        else:
            scan_step = -1
        
        switch = SwitchController(
            self,
            {
                "assignment": {
                    "model": self.__switch_factory.create_switch(port_def["port"]),
                    "pixels": self.__calculate_pixels(index)
                },
                "actions": [
                    ExploreAction({
                        "name": port_def["name"],
                        "step": scan_step
                    })
                ],
                "initialColors": [Colors.WHITE for i in range(self.num_pixels_per_switch)],
                "initialBrightness": 0
            }
        )

        switch.em_index = index              # This is a custom attribute not parsed by FootSwitch, but used internally in this class only

        self.switches.append(switch)
        return port_def["name"]

    # Returns the next available label (used by the ExploreAction)
    def get_next_port_label(self):
        if not self.ui:
            return None
        
        row = self.__ports_display_rows.children[len(self.__ports_display_rows.children) - 1] if self.__ports_display_rows.children else None
        if not row or len(row.children) >= self.__num_port_columns:
            row = DisplaySplitContainer(
                direction = DisplaySplitContainer.HORIZONTAL
            )
            self.__ports_display_rows.add(row)

        label = DisplayLabel(
            layout = {
                "font": "/fonts/A12.pcf",
                "backColor": Colors.BLACK,
                "stroke": 1
            }
        )

        row.add(label)

        return label

    # Resets all ports markers
    def reset_port_markers(self):
        for row in self.__ports_display_rows.children:
            for col in row.children:
                col.back_color = Colors.DARK_BLUE

    def set_latest_port_marker(self, label):
        if self.latest_marker:
            self.latest_marker.back_color = Colors.LIGHT_BLUE

        for row in self.__ports_display_rows.children:
            for col in row.children:
                if label == col:
                    self.latest_marker = col
                    col.back_color = Colors.RED

    # Determine pixel addressing for a switch index, assuming they are linear
    def __calculate_pixels(self, index):
        if not self.led_driver:
            return []
        
        i = index * self.num_pixels_per_switch

        return [i + j for j in range(self.num_pixels_per_switch)]

    # Determines all available GP* ports
    def __get_available_ports(self):
        names = dir(self.__board)
        ret = []
        for name in names:
            if not name.startswith("GP"):
                continue

            ret.append({
                "name": name,
                "port": getattr(self.__board, name)
            })

        return ret
    
