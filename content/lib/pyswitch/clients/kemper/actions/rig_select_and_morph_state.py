from ....colors import Colors
from ....controller.actions import PushButtonAction
from ....controller.callbacks import BinaryParameterCallback, Callback

from .morph import KemperMorphCallback
from .rig_select import RIG_SELECT, RIG_SELECT_DISPLAY_TARGET_RIG

from ..mappings.morph import MAPPING_MORPH_PEDAL
from .. import KemperMappings


# Adds morph state display on one LED to the rig select action. The morph display will only be enabled when the rig in question is currently selected.
def RIG_SELECT_AND_MORPH_STATE(rig,                                            # Rig to select. Range: [1..5]
                               rig_off = None,                                 # If set, this defines the "off" rig chosen when the action is disabled. Set to "auto" to always remember the current rig as "off" rig
                               bank = None,                                    # If set, a specific bank is selected. If None, the current bank is kept
                               bank_off = None,                                # If set, this defines the "off" bank to be chosen when the action is disabled. Set to "auto" to always remember the current bank as "off" bank
                               midi_channel = 1,                               # MIDI Channel in range [1..16]
                               display = None, 
                               id = False, 
                               use_leds = True, 
                               enable_callback = None,
                               color_callback = None,                          # Optional callback for setting the color. Footprint: def callback(action, bank, rig) -> (r, g, b) where bank and rig are int starting from 0.
                               color = None,                                   # Color override (if no text callback is passed)
                               text_callback = None,                           # Optional callback for setting the text. Footprint: def callback(action, bank, rig) -> String where bank and rig are int starting from 0.
                               text = None,                                    # Text override (if no text callback is passed)
                               display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,   # Display mode (show color/text for current or target rig)
                               morph_display = None,                           # Optional DisplayLabel to show morph color
                               morph_use_leds = True,                          # Use the LEDs to show morph state?
                               morph_id = None,                                # Separate ID for the morph action. Default is the same id as specified with the "id" parameter.
                               morph_only_when_enabled = True,                 # Only show the morph state when the "on" rig is selected
                               morph_color_base = Colors.RED,                  # See MORPH_DISPLAY
                               morph_color_morphed = Colors.BLUE,              # See MORPH_DISPLAY
                               rig_btn_morph = False,                          # If set True, second press will trigger toggling the internal morphing state (no command is sent, just the displays are toggled). Only if no rig_off or bank_off are specified.
                               momentary_morph = False                         # If set true, the simulated morph state will operate in momentary mode. Use this if you have use momentary morph mode in your rigs.

):
    rig_select = RIG_SELECT(
        rig = rig,
        rig_off = rig_off,
        bank = bank,
        bank_off = bank_off,
        display_mode = display_mode,
        display = display,
        id = id,
        use_leds = use_leds,
        enable_callback = enable_callback,  
        color_callback = color_callback,
        color = color,
        text_callback = text_callback,
        text = text,
        rig_btn_morph = rig_btn_morph,
        momentary_morph = momentary_morph,
        midi_channel = midi_channel
    )        
    
    return [
        # Rig select action
        rig_select,

        # Use a separate action to show morph state
        PushButtonAction({
            "callback": KemperMorphCallback(
                mapping = MAPPING_MORPH_PEDAL(midi_channel - 1),
                comparison_mode = BinaryParameterCallback.NO_STATE_CHANGE,
                led_brightness_off = "on",
                display_dim_factor_off = "on",
                suppress_send = True,
                color_base = morph_color_base,
                color_morph = morph_color_morphed
            ),
            "useSwitchLeds": morph_use_leds,
            "display": morph_display,
            "id": morph_id if morph_id != None else id,
            "enableCallback": KemperMorphDisplayEnableCallback(
                action_rig_select = rig_select, 
                morph_only_when_enabled = morph_only_when_enabled,
                channel = midi_channel - 1
            )
        })            
    ]


# Callback to enable the morph state display only when the rig is selected
class KemperMorphDisplayEnableCallback(Callback):
    def __init__(self, 
                 action_rig_select, 
                 morph_only_when_enabled,
                 channel = 0
        ):
        Callback.__init__(self)
        
        self.__action_rig_select = action_rig_select
        self.__morph_only_when_enabled = morph_only_when_enabled

        self.register_mapping(KemperMappings.RIG_ID(channel))
        self.__last_enabled = None

    def enabled(self, action):
        if self.__morph_only_when_enabled:
            ret = self.__action_rig_select.callback.state and self.__action_rig_select.enabled
        else:
            ret = self.__action_rig_select.enabled

        if self.__last_enabled == None:
            self.__last_enabled = ret

        elif self.__last_enabled != ret:
            self.__last_enabled = ret
            
            # Tell the callback to not take the first morph value from the Kemper as override.
            action.callback.ignore_next_value = True

        return ret

