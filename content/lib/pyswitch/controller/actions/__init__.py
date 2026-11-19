from micropython import const
from array import array
from math import floor
from ...misc import get_option, Updateable, PeriodCounter
#from ..stats import RuntimeStatistics


# Base class for actions. All functionality is encapsulated in a class for each, 
# inheriting from Action.
class Action(Updateable):
    
    class _CallbackListener:
        def __init__(self, cb):
            self.__cb = cb

        def parameter_changed(self, mapping):
            if self.__cb.enabled:
                self.__cb.update_displays()

        def request_terminated(self, mapping):
            if self.__cb.enabled:
                self.__cb.update_displays()

    # config: {
    #      "callback":             Callback instance to update the display and LEDs. Must contain an update_displays(action) function. Optional. 
    #
    #      "display":              Optional DisplayLabel instance
    #
    #      "enableCallback":       Callback to set enabled state (optional). Must contain an enabled(action) function.
    # 
    #      "id":                   Optional ID for debugging. If not set, an automatic ID is generated.
    #
    #      "useSwitchLeds":        Use LEDs to visualize state. Optional, default is False.
    #
    # }
    def __init__(self, config = {}):
        self.uses_switch_leds = get_option(config, "useSwitchLeds", False)

        self.label = get_option(config, "display", None)

        self.callback = get_option(config, "callback", None)
        if self.callback:
            self.callback.action = self

        self.id = get_option(config, "id", None)

        self.__enable_callback = get_option(config, "enableCallback", None)
        if self.__enable_callback:
            self.__enable_callback.action = self

        self.__last_enabled = -1

    # Must be called before usage
    def init(self, appl, switch):
        self.appl = appl
        self.switch = switch

        # Enable callback
        if self.__enable_callback:            
            self.__enable_callback.init(appl) 

        if self.callback:
            self.callback.init(appl, self._CallbackListener(self))

    @property
    def enabled(self):
        return self.__enable_callback.enabled(self) if self.__enable_callback else True
        
    # Color of the switch segment(s) for the action (Difficult to do with multicolor, 
    # but this property is just needed to have a setter so this is not callable)
    @property
    def switch_color(self):  # pragma: no cover
        raise Exception() #"Getter not implemented (yet)")

    # color can also be a tuple!
    @switch_color.setter
    def switch_color(self, color):
        segments = self.__get_led_segments()
        if len(segments) == 0:
            return
        
        tmp = self.switch.colors

        if isinstance(color[0], tuple):
            if len(segments) == len(color):
                # Fills all LEDs: Just pass colors
                for i in range(len(segments)):
                    tmp[segments[i]] = color[i]
            else:
                # Only fills some LEDs: Use a middle color
                for segment in segments:
                    tmp[segment] = color[floor(len(color) / 2)]
        else:
            # Single color: Fill all segments
            for segment in segments:
                tmp[segment] = color

        self.switch.colors = tmp

    # Brightness of the switch segment(s) for the action
    @property
    def switch_brightness(self):
        segments = self.__get_led_segments()
        if len(segments) > 0:
            return self.switch.brightnesses[segments[0]]  # Return the first segment as they are all equal
        return None

    @switch_brightness.setter
    def switch_brightness(self, brightness):
        segments = self.__get_led_segments()
        if len(segments) == 0:
            return
                
        tmp = self.switch.brightnesses
        for segment in segments:
            tmp[segment] = brightness

        self.switch.brightnesses = tmp

    # Called regularly every update interval to update status of effects etc.
    def update(self):
        if self.__last_enabled != self.enabled:
            self.__last_enabled = self.enabled
            
            if self.callback:
                self.callback.reset()

            self.update_displays()

    # Called when the switch is pushed down
    def push(self):
        if self.callback:
            self.callback.push()

    # Called when the switch is released
    def release(self):
        if self.callback:
            self.callback.release()

    # Called to update the displays (LEDs and label)
    #@RuntimeStatistics.measure
    def update_displays(self):
        if not self.enabled:
            return
        
        if self.callback:
            self.callback.update_displays()
    
    # Reset the action
    def reset(self):
        if self.callback:
            self.callback.reset()

    # Returns the switch LED segments to use
    def __get_led_segments(self):
        if not self.switch.pixels or not self.uses_switch_leds or not self.enabled:
            return array('i')
        
        actions_using_leds = [a for a in self.switch.actions if a.uses_switch_leds and a.enabled]

        ret = array('i')

        # Returns the index of this action inside the LED-using actions of the switch.
        def get_index_among_led_actions(actions_using_leds):
            for i in range(len(actions_using_leds)):
                if actions_using_leds[i] == self:
                    return i
            
            raise Exception() #"Action " + repr(self.id) + " not found in LED-using actions of switch " + repr(self.switch.id))

        index = get_index_among_led_actions(actions_using_leds)
        num_pixels = len(self.switch.pixels)

        if len(actions_using_leds) == 1:
            for i in range(num_pixels):
                ret.append(i)                
        
        elif len(actions_using_leds) < num_pixels:
            pixels_for_first = num_pixels - len(actions_using_leds) + 1

            if index == 0:
                for i in range(0, pixels_for_first):
                    ret.append(i)
            else:
                ret.append(pixels_for_first + index - 1)

        elif index < num_pixels:
            ret.append(index)

        return ret


##########################################################################################################


# Implements an abstraction layer for on/off parameters. Covers latch/momentary modes etc.
class PushButtonAction(Action):
    
    ENABLE = const(0)                      # Switch the functionality on
    DISABLE = const(10)                    # Switch the functionality off
    LATCH = const(20)                      # Toggle state on every button push
    MOMENTARY = const(30)                  # Enable on push, disable on release
    MOMENTARY_INVERSE = const(40)          # Disable on push, Enable on release
    HOLD_MOMENTARY = const(50)             # Combination of latch, momentary and momentary inverse: If pushed shortly, latch mode is 
                                           # used. If pushed longer than specified in the "holdTimeMillis" parameter, momentary mode is 
                                           # used (inverse or not: This depends on the current state of the functionality. When it is
                                           # on, it will momentarily be switched off and vice versa).
    ONE_SHOT = const(100)                  # Fire the SET command on every push (show as disabled)
    NO_STATE_CHANGE = const(200)           # Do not react on pushing the switch

    # Hold time for HOLD_MOMENTARY mode (milliseconds)
    DEFAULT_LATCH_MOMENTARY_HOLD_TIME = const(600)

    # config:
    # {
    #      "callback":        The callback has to additionally implement the function state_changed_by_user(action).
    #      "mode":            Mode of operation (see PushButtonModes). Optional, default is HOLD_MOMENTARY,
    #      "holdTimeMillis":  Optional hold time in milliseconds. Default is DEFAULT_LATCH_MOMENTARY_HOLD_TIME
    # }
    def __init__(self, config = {}, period_counter = None):
        super().__init__(config)

        self.__mode = get_option(config, "mode", self.HOLD_MOMENTARY)
        
        self.__period = period_counter
        if not self.__period:
            hold_time_ms = get_option(config, "holdTimeMillis", self.DEFAULT_LATCH_MOMENTARY_HOLD_TIME)
            self.__period = PeriodCounter(hold_time_ms)
        
        self.__state = False

    @property
    def state(self):
        return self.__state
    
    # Sets the state, also triggering the child class functionality. If you just 
    # want to set the state internally after feedback from the controlled device,
    # use feedback_state().
    @state.setter
    def state(self, state):
        if state == self.__state:
            return
        
        self.__state = state
        
        if self.callback:
            self.callback.state_changed_by_user()

        self.update_displays()

    # Update the state without functional changes. This is used to react to
    # parameters that have to be requested first. When the answer comes in, the state 
    # is set here again, but no functional update is done.
    def feedback_state(self, state):
        self.__state = state

    # Button pushed
    def push(self):
        mode = self.__mode

        if mode == self.ENABLE:
            # Enable
            self.state = True

        elif mode == self.DISABLE:
            # Disable
            self.state = False

        if mode == self.LATCH:
            # Latch mode: Simply toggle states
            self.state = not self.state

        elif mode == self.MOMENTARY:
            # Momentary mode: Enable on push
            self.state = True

        elif mode == self.MOMENTARY_INVERSE:
            # Momentary mode: Enable on push
            self.state = False

        elif mode == self.HOLD_MOMENTARY:
            # Hold Momentary: Toggle like latch, and remember the current timestamp
            self.__period.reset()
            self.state = not self.state

        elif mode == self.ONE_SHOT:
            self.__state = False    # Triggers that set() is called by the state property in the next line
            self.state = True            

    # Button released
    def release(self):
        mode = self.__mode

        if mode == self.MOMENTARY:
            self.state = False
        
        elif mode == self.MOMENTARY_INVERSE:
            self.state = True
        
        elif mode == self.HOLD_MOMENTARY:
            if self.__period.exceeded:
                # Momentary if the period exceeded
                self.state = not self.state

        elif mode == self.ONE_SHOT:
            # Do not use the child classes set() method: We do not want an "off" message to be sent here.
            self.__state = False
            self.update_displays()

    # Reset the action: Set False state without sending anything
    def reset(self):
        super().reset()
        self.__state = False
        self.update_displays()

