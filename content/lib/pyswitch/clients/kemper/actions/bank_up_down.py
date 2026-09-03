from ....controller.actions import Action
from ....controller.callbacks import Callback
from ...kemper import NUM_RIGS_PER_BANK, BANK_COLORS, NUM_BANKS
from ....misc import get_option, PeriodCounter
from ....colors import Colors, dim_color

from ..mappings.bank import MAPPING_NEXT_BANK, MAPPING_PREVIOUS_BANK
from ..mappings.select import MAPPING_BANK_SELECT

from .rig_select import RIG_SELECT_DISPLAY_CURRENT_RIG, RIG_SELECT_DISPLAY_TARGET_RIG

# Next bank (keeps rig index)
def BANK_UP(display = None,
            midi_channel = 1,                                 # MIDI Channel in range [1..16]
            id = False, 
            use_leds = True, 
            enable_callback = None,
            dim_factor = "off",                               # Can be "off", "on" or a value in range [0..1]
            led_brightness = "off",                           # Can be "off", "on" or a value in range [0..1]
            text = "Bank up",
            text_callback = None,                             # Optional callback for setting the text. Footprint: def callback(action, bank, rig) -> String where bank and rig are int starting from 0.
            color = None,                                     # Override color (if no color_callback is passed)
            color_callback = None,                            # Optional callback for setting the color. Footprint: def callback(action, bank, rig) -> (r, g, b) where bank and rig are int starting from 0.
            display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,    # Display mode (same as for RIG_SELECT, see definitions above)
            preselect = False,                                # Preselect mode. If enabled, the bank is only pre-selected, the change will only take effect when you select a rig next time.
            max_bank = None                                   # Highest bank available. Only relevant if preselct is enabled.
    ):
    return Action({
        "callback": KemperBankChangeCallback(
            mapping = MAPPING_NEXT_BANK(midi_channel - 1) if not preselect else MAPPING_BANK_SELECT(midi_channel - 1),
            offset = 1,
            dim_factor = dim_factor,
            display_mode = display_mode,
            led_brightness = led_brightness,
            color = color,
            color_callback = color_callback,
            text = text,
            text_callback = text_callback,
            preselect = preselect,
            max_bank = max_bank
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })

# Previous bank (keeps rig index)
def BANK_DOWN(display = None,                                   # Reference to a DisplayLabel
              midi_channel = 1,                                 # MIDI Channel in range [1..16]
              id = False, 
              use_leds = True, 
              enable_callback = None,
              dim_factor = "off",                               # Can be "off", "on" or a value in range [0..1]
              led_brightness = "off",                           # Can be "off", "on" or a value in range [0..1]
              text = "Bank dn", 
              text_callback = None,                             # Optional callback for setting the text. Footprint: def callback(action, bank, rig) -> String where bank and rig are int starting from 0.
              color = None,                                     # Override color (if no color_callback is passed)
              color_callback = None,                            # Optional callback for setting the color. Footprint: def callback(action, bank, rig) -> (r, g, b) where bank and rig are int starting from 0.
              display_mode = RIG_SELECT_DISPLAY_CURRENT_RIG,    # Display mode (same as for RIG_SELECT, see definitions above)
              preselect = False,                                # Preselect mode
              max_bank = None                                   # Highest bank available. Only relevant if preselct is enabled.
    ):
    return Action({        
        "callback": KemperBankChangeCallback(
            mapping = MAPPING_PREVIOUS_BANK(midi_channel - 1) if not preselect else MAPPING_BANK_SELECT(midi_channel - 1),
            offset = -1,
            dim_factor = dim_factor,
            display_mode = display_mode,
            led_brightness = led_brightness,
            color = color,
            color_callback = color_callback,
            text = text,
            text_callback = text_callback,
            preselect = preselect,
            max_bank = max_bank
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })


# Custom callback showing current bank color (only used by Bank up/down)
class KemperBankChangeCallback(Callback):
    def __init__(self, 
                 mapping, 
                 offset,
                 dim_factor,
                 display_mode,
                 led_brightness,
                 color,
                 color_callback,
                 text,
                 text_callback,
                 preselect,
                 max_bank,
                 preselect_blink_interval = 400
        ):            
        super().__init__(mappings = [mapping])

        self.__mapping = mapping
        self.__dim_factor_p = dim_factor
        self.__led_brightness_p = led_brightness
        self.__display_mode = display_mode

        self.__color = color
        self.__color_callback = color_callback
        self.__offset = offset

        self.__text = text
        self.__text_callback = text_callback
        self.__preselect = preselect
        self.__max_bank = max_bank

        if preselect:
            self.__preselect_blink_period = PeriodCounter(preselect_blink_interval)

    def init(self, appl, listener = None):
        super().init(appl, listener)
        self.__appl = appl

        if self.__dim_factor_p == "off":
            self.__dim_factor = get_option(appl.config, "displayDimFactorOff", 0.2)
        elif self.__display_mode == "on":
            self.__dim_factor = get_option(appl.config, "displayDimFactorOn", 1)
        else:
            self.__dim_factor = self.__dim_factor_p

        if self.__led_brightness_p == "off":
            self.__led_brightness = get_option(appl.config, "ledBrightnessOff", 0.02)
            self.__led_brightness_off = get_option(appl.config, "ledBrightnessOn", 0.3)
        elif self.__led_brightness_p == "on":
            self.__led_brightness = get_option(appl.config, "ledBrightnessOn", 0.3)
            self.__led_brightness_off = get_option(appl.config, "ledBrightnessOff", 0.02)
        else:
            self.__led_brightness = self.__led_brightness_p
            self.__led_brightness_off = self.__led_brightness_p * 0.1

        if self.__preselect:
            self.__appl.shared["preselectBlinkState"] = False
            self.__appl.shared["preselectCallback"] = None

    def push(self):
        if self.__preselect:
            if self.__mapping.value == None:
                return
            
            value = self.__get_next_bank()
            
            self.__appl.shared["preselectedBank"] = value
            self.__appl.shared["preselectCallback"] = self
        else:
            value = 0

        self.__appl.client.set(self.__mapping, value)
        
        self.__appl.shared["morphStateOverride"] = 0

    def release(self):
        pass

    def update(self):
        Callback.update(self)

        if self.__preselect and "preselectedBank" in self.__appl.shared and self.__appl.shared["preselectCallback"] == self and self.__preselect_blink_period.exceeded:
            self.__appl.shared["preselectBlinkState"] = not self.__appl.shared["preselectBlinkState"]
            
            self.update_displays()

    def reset(self):
        # TODO this should not be necessary: Normally this just resets the memory, which this class doesnt have.
        if self.action.enabled:
            self.update_displays()

    def update_displays(self):
        if self.__mapping.value == None:
            if self.action.label:
                self.action.label.text = self.__text
                self.action.label.back_color = dim_color(Colors.WHITE, self.__dim_factor)

            self.action.switch_color = Colors.WHITE
            self.action.switch_brightness = self.__led_brightness
            return
        
        # Calculate bank and rig numbers in range [0...]
        bank = int(self.__mapping.value / NUM_RIGS_PER_BANK)
        rig = self.__mapping.value % NUM_RIGS_PER_BANK
        target_bank = self.__get_next_bank(bank)

        if self.__color_callback:
            bank_color = self.__color_callback(self.action, bank, rig)
        elif self.__color:
            bank_color = self.__color
        else:
            if self.__display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
                bank_color = BANK_COLORS[bank % len(BANK_COLORS)]  
            else:
                bank_color = BANK_COLORS[target_bank % len(BANK_COLORS)]

        # Label text
        if self.action.label:
            self.action.label.back_color = dim_color(bank_color, self.__dim_factor)

            if self.__text_callback:
                if self.__display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
                    self.action.label.text = self.__text_callback(self.action, bank, rig)

                elif self.__display_mode == RIG_SELECT_DISPLAY_TARGET_RIG:                    
                    self.action.label.text = self.__text_callback(self.action, target_bank, rig)
                else:
                    raise Exception() #"Invalid display mode: " + repr(display_mode))
            else:
                self.action.label.text = self.__text

        self.action.switch_color = bank_color

        if self.__preselect and "preselectedBank" in self.__appl.shared and self.__appl.shared["preselectCallback"] == self: 
            self.action.switch_brightness = self.__led_brightness if not self.__appl.shared["preselectBlinkState"] else self.__led_brightness_off
        else:
            self.action.switch_brightness = self.__led_brightness

    def __get_next_bank(self, bank = None):
        if "preselectedBank" in self.__appl.shared:
            bank = self.__appl.shared["preselectedBank"]

        if bank == None:
            bank = int(self.__mapping.value / NUM_RIGS_PER_BANK)        

        value = bank + self.__offset
        _num_banks = NUM_BANKS if self.__max_bank == None else self.__max_bank
        
        while (value < 0):
            value += _num_banks
        while (value >= _num_banks):
            value -= _num_banks

        return value
