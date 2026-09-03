from ...kemper import NUM_RIGS_PER_BANK, BANK_COLORS
from ....controller.actions import Action
from ....controller.callbacks import Callback
from ....misc import get_option, PeriodCounter
from ....colors import Colors, dim_color

from ..mappings.select import MAPPING_BANK_SELECT, MAPPING_RIG_SELECT
from .rig_select import RIG_SELECT_DISPLAY_CURRENT_RIG, RIG_SELECT_DISPLAY_TARGET_RIG

# Selects a specific bank, keeping the current rig, or toggles between two banks (if bank_off is also provided). 
def BANK_SELECT(bank,                                           # Bank to select. Banks are indexed starting from one, range: [1..126].
                bank_off = None,                                # "off" bank, to toggle between banks. Will be ignored when preselect is enabled.
                preselect = False,                              # Preselect mode. If enabled, the bank is only pre-selected, the change will only take effect when you select a rig next time. Ignores the parameter "bank_off".
                display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,  # Display mode
                display = None,                                 # Reference to a DisplayLabel
                midi_channel = 1,                               # MIDI Channel in range [1..16]
                id = False,                                     # ID for paging / enable callbacks
                use_leds = True,                                # Use the switch LEDs
                enable_callback = None,                         # Optional callback to enable/disable the action depeinding on things
                color_callback = None,                          # Optional callback for setting the color. Scheme: 
                                                                # def callback(action, bank, rig) -> (r, g, b) where bank and rig are integers starting from 0.
                color = None,                                   # Static color (if no color callback is passed)
                text_callback = None,                           # Callback for setting the text. Scheme: 
                                                                # def callback(action, bank, rig) -> String where bank and rig are integers starting from 0.
                text = None                                     # Static text (if no text callback is passed)
    ):
    
    return Action({
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "callback": KemperBankSelectCallback(
            bank = bank,
            bank_off = bank_off,
            text = text,
            text_callback = text_callback,
            color = color,
            color_callback = color_callback,
            display_mode = display_mode,
            preselect = preselect,
            channel = midi_channel - 1
        ),
        "enableCallback": enable_callback
    })


# Callback implementation for Bank Select, showing bank colors and rig/bank info
class KemperBankSelectCallback(Callback):
    def __init__(self,
                 bank,
                 bank_off,
                 text, 
                 text_callback,
                 color,
                 color_callback,
                 display_mode,
                 preselect,
                 channel,
                 preselect_blink_interval = 400
        ):
        super().__init__()

        self.__mapping = MAPPING_BANK_SELECT(channel)
        self._channel = channel
        self.register_mapping(self.__mapping)

        self.__bank = bank
        self.__bank_off = bank_off if not preselect else None
        self.__text = text
        self.__text_callback = text_callback
        self.__color = color
        self.__color_callback = color_callback
        self.__display_mode = display_mode

        self.__current_value = -1
        self.__last_state = -1
        self.__sent_rig_mapping = None

        self.__preselect = preselect
        if preselect:
            self.__preselect_blink_period = PeriodCounter(preselect_blink_interval)

    @property
    def state(self):
        if self.__mapping.value == None:
            return False
        
        curr_bank = int(self.__mapping.value / NUM_RIGS_PER_BANK)
        
        return (curr_bank == (self.__bank - 1))

    def reset(self):
        self.__current_value = -1
        self.__last_state = -1

        # if self.action.enabled:
        #     self.update_displays()

    def init(self, appl, listener = None):
        super().init(appl, listener)

        self.__default_dim_factor_off = get_option(appl.config, "displayDimFactorOff", 0.2)
        self.__default_led_brightness_off = get_option(appl.config, "ledBrightnessOff", 0.02)
        self.__default_led_brightness_on = get_option(appl.config, "ledBrightnessOn", 0.3)
        self.__appl = appl

        if self.__preselect:
            self.__appl.shared["preselectBlinkState"] = False

    def update(self):
        Callback.update(self)

        if self.__preselect and "preselectedBank" in self.__appl.shared and self.__appl.shared["preselectedBank"] == self.__bank - 1 and self.__preselect_blink_period.exceeded:
            self.__appl.shared["preselectBlinkState"] = not self.__appl.shared["preselectBlinkState"]
            self.update_displays()

    def push(self):
        if self.__mapping.value == None:
            return
        
        curr_bank = int(self.__mapping.value / NUM_RIGS_PER_BANK)         
        
        if self.__preselect and ( "preselectedBank" in self.__appl.shared or curr_bank != self.__bank - 1 ):
            self.__appl.shared["preselectedBank"] = self.__bank - 1
            self.__appl.shared["preselectCallback"] = self

        for input in self.__appl.inputs:
            if hasattr(input, "pixels"):
                for a in input.actions:
                    a.update_displays()

        # Send bank preselect
        if self.__bank_off != None:
            if curr_bank != self.__bank - 1:
                self.__appl.client.set(MAPPING_BANK_SELECT(channel = self._channel), self.__bank - 1)
            else:
                self.__appl.client.set(MAPPING_BANK_SELECT(channel = self._channel), self.__bank_off - 1)
        else:        
            self.__appl.client.set(MAPPING_BANK_SELECT(channel = self._channel), self.__bank - 1)

        # Also send rig select when not in preselect mode
        if not self.__preselect:
            curr_rig = self.__mapping.value % NUM_RIGS_PER_BANK

            self.__sent_rig_mapping = MAPPING_RIG_SELECT(curr_rig, channel = self._channel)
            self.__appl.client.set(self.__sent_rig_mapping, 1)

            # End preselect display
            if "preselectedBank" in self.__appl.shared:
                del self.__appl.shared["preselectedBank"]

            # Reset morph state override
            self.__appl.shared["morphStateOverride"] = 0

    def release(self):
        # Send release (0) value if necessary
        if not self.__sent_rig_mapping:
            return
        
        self.__appl.client.set(self.__sent_rig_mapping, 0)
        self.__sent_rig_mapping = None

    def update_displays(self):
        if self.__mapping.value == None:
            if self.action.label:
                self.action.label.text = ""
                self.action.label.back_color = dim_color(Colors.WHITE, self.__default_dim_factor_off)

            self.action.switch_color = Colors.WHITE
            self.action.switch_brightness = self.__default_led_brightness_off
            return
        
        if self.__preselect and "preselectedBank" in self.__appl.shared and self.__appl.shared["preselectedBank"] == self.__bank - 1:
            is_current = self.__appl.shared["preselectBlinkState"]            
        else:
            is_current = self.state

        # Calculate bank and rig numbers in range [0...]
        curr_bank = int(self.__mapping.value / NUM_RIGS_PER_BANK)
        curr_rig = self.__mapping.value % NUM_RIGS_PER_BANK                
        
        if self.__mapping.value == self.__current_value and is_current == self.__last_state:
            return
        
        self.__current_value = self.__mapping.value
        self.__last_state = is_current
            
        if self.__color != None:
            bank_color = self.__color
        elif self.__color_callback:
            bank_color = self.__color_callback(self.action, curr_bank, curr_rig)
        else:
            bank_color = self._get_bank_color(curr_bank, self.__bank, self.__bank_off, self.__display_mode)
                        
        # Label text
        if self.action.label:
            if self.__display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
                self.action.label.text = self._get_text(curr_bank, curr_rig) 
                self.action.label.back_color = dim_color(bank_color, self.__default_dim_factor_off)

            elif self.__display_mode == RIG_SELECT_DISPLAY_TARGET_RIG:
                self.action.label.back_color = bank_color if is_current else dim_color(bank_color, self.__default_dim_factor_off) 

                if is_current and self.__bank_off != None:
                    self.action.label.text = self._get_text(self.__bank_off - 1, curr_rig)
                else:
                    self.action.label.text = self._get_text(self.__bank - 1, curr_rig)

            else:
                raise Exception()  #"Invalid display mode: " + repr(display_mode))

        # LEDs
        self.action.switch_color = bank_color

        if self.__display_mode == RIG_SELECT_DISPLAY_TARGET_RIG:
            if is_current:
                self.action.switch_brightness = self.__default_led_brightness_on
            else:
                self.action.switch_brightness = self.__default_led_brightness_off
        else:
            self.action.switch_brightness = self.__default_led_brightness_off

    # Get text for the label
    def _get_text(self, bank, rig):
        if self.__text:
            return self.__text
        elif self.__text_callback:
            return self.__text_callback(self.action, bank, rig)
        else:
            return "Bank " + repr(bank + 1)
            
    # Default color callback for bank color
    def _get_bank_color(self, curr_bank, bank, bank_off, display_mode):
        is_current = (curr_bank == (bank - 1))

        if display_mode == RIG_SELECT_DISPLAY_TARGET_RIG:
            if is_current and bank_off != None:
                return BANK_COLORS[(bank_off - 1) % len(BANK_COLORS)]
            else:
                return BANK_COLORS[(bank - 1) % len(BANK_COLORS)]

        elif display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
            return BANK_COLORS[curr_bank % len(BANK_COLORS)]

        else:
            raise Exception() #"Invalid display mode: " + repr(display_mode))         