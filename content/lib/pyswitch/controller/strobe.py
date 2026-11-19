from ..misc import PeriodCounter
from ..colors import Colors

class StrobeController:

    def __init__(self,
                 mapping_state,                     # Mapping for tuner mode state (1 == enabled)
                 mapping_deviance,                  # Mapping for deviance [0..16383]
                 speed = 1000,                      # Higher values make the strobe tuner go slower. 1000 is the recommended speed to start from.
                 width = 0.3,                       # Width of the virtual moving highlight
                 color = Colors.WHITE,              # LED color for strobe tuner
                 dim_factor = 0.1,                  # Dim factor for strobe tuner in range [0..1]
                 max_fps = 120,                     # Maximum cumulative frame rate for update of strobe tuner LEDs. Reduce this to save processing power.
                                                    # The number will be divided by the amount of available switches to get the real max. frame rate (that's
                                                    # why it is called cumulative ;)
                 reverse = False                    # By default, the strobe is rotating clockwise when too high / ccw when too low. 
                                                    # Set this to True to reverse this.
        ):
        self.__mapping_state = mapping_state
        self.__mapping_deviance = mapping_deviance

        self.__speed = speed * 2000                 # Determined empirically
        self.__width = width
        self.__color = color
        self.__dim_factor = dim_factor
        self.__max_fps = max_fps
        
        self.__switches = None               # List of switches ordered for strobe
        self.__period = None        
        self.__strobe_pos = 0
        self.__last_deviance = 8192
        self.__reverse = reverse

        self.__enabled = False

    def init(self, appl):
        # Register mappings
        appl.client.register(self.__mapping_state, self)
        appl.client.register(self.__mapping_deviance, self)
        
        # Bring the switches into the correct order for strobe
        self.__switches = [s for s in appl.inputs if hasattr(s, "pixels")]
        self.__current_strobe_brightnesses = [0 for s in self.__switches]

        # Period counter for saving LED updates (restricts the updates to a certain frame rate)
        period = int(1000 / self.__max_fps * len(self.__switches))
        self.__period = PeriodCounter(period)

        def compare(sw):
            return sw.strobe_order

        self.__switches.sort(key = compare)

        # Numer of switches: If this equals the amount of switches, you get one dot
        # running in the circle. If this equals half the available switches, it will show
        # two dots and so on. 
        self.__num_switches = len(self.__switches)
        # if self.__num_switches > 4:
        #     self.__num_switches = self.__num_switches / 2

    # Listen to client value returns
    def parameter_changed(self, mapping):
        if self.__num_switches <= 1:
            self.__enabled = False
            return
        
        value = mapping.value

        if mapping == self.__mapping_state:
            if value == 1:
                # Tuner on
                self.__enabled = True
                self.__period.reset()
            else:
                # Tuner off
                self.__enabled = False

        if mapping == self.__mapping_deviance:
            if value != self.__last_deviance:
                self.__last_deviance = value               

            self.__update_strobe()

    # Called when the client is offline (requests took too long)
    def request_terminated(self, mapping):
        pass                                       # pragma: no cover

    # Update the strobe LEDs
    def __update_strobe(self):
        if not self.__enabled:
            return
        
        passed = self.__period.passed
        if not self.__period.exceeded:
            return

        speed = self.__speed
        width = self.__width

        # Accumulate deviances and restrict range
        delta = (8191 - self.__last_deviance) if self.__reverse else (self.__last_deviance - 8191)

        threshold = 100 * self.__period.interval
        if delta > threshold:
            delta = threshold
        if delta < -threshold:
            delta = -threshold
        
        self.__strobe_pos -= delta * passed

        while self.__strobe_pos > speed:
            self.__strobe_pos -= speed
        while self.__strobe_pos < -speed:
            self.__strobe_pos += speed
        
        # Put to range [0..1], regarding speed
        pos = (self.__strobe_pos % speed) / speed

        # Defines the period function in range [0..1] for inputs in range [0..1] 
        # (starts with 1, goes to zero in the middle and goes up to 1 again at the end)
        def b(p, width):
            if p <= width:
                return 1 - p * (1 / width)
            elif p >= 1 - width:
                return (p - 1 + width) * (1 / width)
            else:
                return 0

        # Color each switch
        for switch_num in range(len(self.__switches)):
            switch = self.__switches[switch_num]
            
            # Position inside the period [0..1]
            p = pos + switch_num / self.__num_switches

            while p > 1:
                p -= 1
            while p < 0:
                p += 1

            # Brightness [0..1]
            brightness = b(p, width)
            brightness = int(brightness * 16) / 16
            
            # Use the square of the calculated brightness to accomodate for the non-linear NeoPixels
            switch.color = self.__color
            brightness_out = (brightness * brightness) * self.__dim_factor

            if self.__current_strobe_brightnesses[switch_num] != brightness_out:
                self.__current_strobe_brightnesses[switch_num] = brightness_out

                switch.brightness = brightness_out