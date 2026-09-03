from ...kemper import NUM_RIGS_PER_BANK, BANK_COLORS, NUM_BANKS, KemperMappings
from ....controller.actions import Action
from ....controller.callbacks import Callback
from ....misc import get_option
from ....colors import DEFAULT_SWITCH_COLOR, DEFAULT_LABEL_COLOR

from ..mappings.select import MAPPING_RIG_SELECT, MAPPING_BANK_SELECT
from .rig_select import RIG_SELECT_DISPLAY_CURRENT_RIG, RIG_SELECT_DISPLAY_TARGET_RIG

# Select next rig
def RIG_UP(keep_bank = True,                               # If enabled, the bank is not changed when at the first and last rigs of a bank. If disabled, 
                                                           # the banks are stepped up/down after the last/first rigs of a bank.
           display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,   # Display mode (see definitions above)
           display = None, 
           midi_channel = 1,                               # MIDI Channel in range [1..16]
           id = False, 
           use_leds = True, 
           enable_callback = None,
           color_callback = None,                          # Optional callback for setting the color. Footprint: def callback(action, bank, rig) -> (r, g, b) where bank and rig are int starting from 0.
           color = None,                                   # Color override (if no text callback is passed)
           text_callback = None,                           # Optional callback for setting the text. Footprint: def callback(action, bank, rig) -> String where bank and rig are int starting from 0.
           text = None,                                    # Text override (if no text callback is passed)
    ):
    
    # Finally we can create the action definition ;)
    return Action({
        "callback": _KemperRigChangeCallback(            
            color = color,
            color_callback = color_callback,
            display_mode = display_mode,
            text = text,
            text_callback = text_callback,
            keep_bank = keep_bank,
            channel = midi_channel - 1,
            direction_up = True
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })  

# Select previous rig
def RIG_DOWN(keep_bank = True,                               # If enabled, the bank is not changed when at the first and last rigs of a bank. If disabled, 
                                                             # the banks are stepped up/down after the last/first rigs of a bank.
             display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,   # Display mode (see definitions above)
             display = None, 
             midi_channel = 1,                               # MIDI Channel in range [1..16]
             id = False, 
             use_leds = True, 
             enable_callback = None,
             color_callback = None,                          # Optional callback for setting the color. Footprint: def callback(action, bank, rig) -> (r, g, b) where bank and rig are int starting from 0.
             color = None,                                   # Color override (if no text callback is passed)
             text_callback = None,                           # Optional callback for setting the text. Footprint: def callback(action, bank, rig) -> String where bank and rig are int starting from 0.
             text = None,                                    # Text override (if no text callback is passed)
    ):
    
    # Finally we can create the action definition ;)
    return Action({
        "callback": _KemperRigChangeCallback(            
            color = color,
            color_callback = color_callback,
            display_mode = display_mode,
            text = text,
            text_callback = text_callback,
            keep_bank = keep_bank,
            channel = midi_channel - 1,
            direction_up = False
        ),
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback
    })  


############################################################################################


# Callback implementation for Rig Select, showing bank colors and rig/bank info
class _KemperRigChangeCallback(Callback):
    def __init__(self,
                 color,
                 color_callback,
                 display_mode,
                 text,
                 text_callback,
                 keep_bank,
                 channel,
                 direction_up = True
        ):
        
        mapping = KemperMappings.RIG_ID(channel)
    
        super().__init__(mappings = [mapping])

        self._channel = channel
        self.__mapping = mapping
        
        self.__color_callback = color_callback
        self.__color = color

        self.__text_callback = text_callback
        self.__text = text

        self.__display_mode = display_mode
        self.__direction_up = direction_up
        self.__keep_bank = keep_bank

        self.__sent_rig_mapping = None

    def init(self, appl, listener = None):
        super().init(appl, listener)

        self.__led_brightness = get_option(appl.config, "ledBrightnessOn", 0.3)
        self.__appl = appl

    def push(self):
        if self.__mapping.value == None:
            return
        
        curr_bank = int(self.__mapping.value / NUM_RIGS_PER_BANK)
        curr_rig = self.__mapping.value % NUM_RIGS_PER_BANK
        
        next_rig_id = self.__get_next_rig(curr_rig, self.__mapping.value)
        if next_rig_id == self.__mapping.value:
            return
        next_bank = int(next_rig_id / NUM_RIGS_PER_BANK)
        next_rig = next_rig_id % NUM_RIGS_PER_BANK
        
        if next_bank != curr_bank:
            self.__appl.client.set(MAPPING_BANK_SELECT(channel = self._channel), next_bank)
            
        self.__sent_rig_mapping = MAPPING_RIG_SELECT(next_rig, channel = self._channel)
        self.__appl.client.set(self.__sent_rig_mapping, 1)
        
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
                self.action.label.back_color = DEFAULT_LABEL_COLOR

            self.action.switch_color = DEFAULT_SWITCH_COLOR
            self.action.switch_brightness = self.__led_brightness
            return
        
        # Calculate bank and rig numbers in range [0...]
        curr_bank = int(self.__mapping.value / NUM_RIGS_PER_BANK)
        curr_rig = self.__mapping.value % NUM_RIGS_PER_BANK
        
        bank_color = self._get_color(curr_bank, curr_rig, self.__mapping.value)

        # Label text
        if self.action.label:
            self.action.label.back_color = bank_color

            if self.__display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
                self.action.label.text = self.__get_text(curr_bank, curr_rig) 
            
            elif self.__display_mode == RIG_SELECT_DISPLAY_TARGET_RIG:
                next_rig_id = self.__get_next_rig(curr_rig, self.__mapping.value)
                next_bank = int(next_rig_id / NUM_RIGS_PER_BANK)
                next_rig = next_rig_id % NUM_RIGS_PER_BANK
        
                self.action.label.text = self.__get_text(next_bank, next_rig)

            else:
                raise Exception()  #"Invalid display mode: " + repr(display_mode))

        # LEDs
        self.action.switch_color = bank_color
        self.action.switch_brightness = self.__led_brightness
        
    def _get_color(self, curr_bank, curr_rig, curr_rig_id):
        if self.__color:
            return self.__color
        
        if self.__color_callback:
            return self.__color_callback(self.action, curr_bank, curr_rig)

        if self.__display_mode == RIG_SELECT_DISPLAY_TARGET_RIG:
            next_rig_id = self.__get_next_rig(curr_rig, curr_rig_id)
            next_bank = int(next_rig_id / NUM_RIGS_PER_BANK)
        
            return BANK_COLORS[next_bank % len(BANK_COLORS)]
            
        elif self.__display_mode == RIG_SELECT_DISPLAY_CURRENT_RIG:
            return BANK_COLORS[curr_bank % len(BANK_COLORS)]

        else:
            raise Exception() #"Invalid display mode: " + repr(display_mode))
        
    def __get_text(self, bank, rig):
        if self.__text_callback:
            return self.__text_callback(self.action, bank, rig)
        
        if self.__text:
            return self.__text
            
        return f"Rig { repr(bank + 1) }-{ repr(rig + 1) }"
    
    def __get_next_rig(self, curr_rig, curr_rig_id):
        if self.__direction_up:
            if self.__keep_bank:
                if curr_rig < NUM_RIGS_PER_BANK - 1:
                    return curr_rig_id + 1
                else:
                    return curr_rig_id
            else:
                if curr_rig_id < NUM_RIGS_PER_BANK * NUM_BANKS - 1:
                    return curr_rig_id + 1
                else:
                    return 0
        else:
            if self.__keep_bank:
                if curr_rig > 0:
                    return curr_rig_id - 1
                else:
                    return curr_rig_id
            else:
                if curr_rig_id > 0:
                    return curr_rig_id - 1
                else:
                    return NUM_RIGS_PER_BANK * NUM_BANKS - 1
    