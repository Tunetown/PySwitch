from ....controller.actions import PushButtonAction
from ....controller.callbacks import BinaryParameterCallback
from ....colors import Colors

from ..mappings.morph import MAPPING_MORPH_BUTTON, MAPPING_MORPH_PEDAL

# Morph button (faded change of morph state)
def MORPH_BUTTON(display = None, 
                 midi_channel = 1,                   # MIDI Channel in range [1..16]
                 text = "Morph", 
                 id = False, 
                 use_leds = True, 
                 enable_callback = None, 
                 color = "kemper",                   # Can be "kemper" or a fixed color
                 morph_color_base = Colors.RED,      # Only used if color = "kemper". See MORPH_DISPLAY
                 morph_color_morphed = Colors.BLUE   # Only used if color = "kemper". See MORPH_DISPLAY
    ):
    return PushButtonAction({
        "callback": KemperMorphCallback(
            mapping = MAPPING_MORPH_BUTTON(midi_channel - 1),
            text = text,
            comparison_mode = BinaryParameterCallback.NO_STATE_CHANGE,
            led_brightness_off = "on",
            display_dim_factor_off = "on",
            color = color,
            color_base = morph_color_base,
            color_morph = morph_color_morphed
        ),
        "mode": PushButtonAction.MOMENTARY,
        "useSwitchLeds": use_leds,
        "display": display,
        "id": id,
        "enableCallback": enable_callback
    })

# Morph state (display/LEDs only)
def MORPH_DISPLAY(display = None, 
                  midi_channel = 1,                     # MIDI Channel in range [1..16]
                  text = "Morph", 
                  id = False, 
                  use_leds = True, 
                  enable_callback = None,
                  morph_color_base = Colors.RED,        # Color used for the unmorphed state
                  morph_color_morphed = Colors.BLUE     # Color used for the morphed state
    ):
    return PushButtonAction({
        "callback": KemperMorphCallback(
            mapping = MAPPING_MORPH_PEDAL(midi_channel - 1),
            text = text,
            comparison_mode = BinaryParameterCallback.NO_STATE_CHANGE,
            led_brightness_off = "on",
            display_dim_factor_off = "on",
            suppress_send = True,
            color_base = morph_color_base,
            color_morph = morph_color_morphed
        ),
        "useSwitchLeds": use_leds,
        "display": display,
        "id": id,
        "enableCallback": enable_callback
    })


###################################################################################################

def _get_color(action, value):
    if action.callback.appl and "morphStateOverride" in action.callback.appl.shared:
        value = action.callback.appl.shared["morphStateOverride"]
        
    if value == None:
        return Colors.WHITE

    cb = action.callback
    if cb.fix_color:
        return cb.fix_color

    v = value / 16383
    
    return (
        cb.color_base[0] + int(cb.r_diff * v),
        cb.color_base[1] + int(cb.g_diff * v),
        cb.color_base[2] + int(cb.b_diff * v),
    )

###################################################################################################

# Callback for morph pedal mapping, with colors reflecting the morph state
class KemperMorphCallback(BinaryParameterCallback):

    def __init__(self, 
                 mapping,
                 set_internal_state = True,    # If this is set, a global, internal morph state is used instead of the values coming from the Kemper.
                 color = "kemper",             # Can be "kemper" or a fixed color
                 text = "Morph", 
                 value_enable = 1, 
                 value_disable = 0, 
                 reference_value = 8191, 
                 comparison_mode = BinaryParameterCallback.GREATER_EQUAL, 
                 display_dim_factor_on = None,
                 display_dim_factor_off = None,
                 led_brightness_on = None,
                 led_brightness_off = None,
                 suppress_send = False,
                 color_base = Colors.RED,      # Only used if color = "kemper"
                 color_morph = Colors.BLUE     # Only used if color = "kemper"

        ):
        super().__init__(
            mapping = mapping, 
            color_callback = _get_color,
            text = text, 
            value_enable = value_enable, 
            value_disable = value_disable, 
            reference_value = reference_value, 
            comparison_mode = comparison_mode, 
            display_dim_factor_on = display_dim_factor_on, 
            display_dim_factor_off = display_dim_factor_off, 
            led_brightness_on = led_brightness_on, 
            led_brightness_off = led_brightness_off
        )

        self.__set_internal_state = set_internal_state
        self.__suppress_send = suppress_send
        self.fix_color = color if color != "kemper" else None

        self.r_diff = color_morph[0] - color_base[0]
        self.g_diff = color_morph[1] - color_base[1]
        self.b_diff = color_morph[2] - color_base[2]
        
        self.color_base = color_base
        self.color_morph = color_morph

        self.__last_value = None
        self.appl = None

        self.ignore_next_value = False


    def init(self, appl, listener = None):
        super().init(appl, listener)

        if self.__set_internal_state:
            self.appl = appl
            appl.shared["morphStateOverride"] = 0


    def state_changed_by_user(self):
        if self.__suppress_send:
            return
        
        super().state_changed_by_user()

        if self.__set_internal_state and self.action.state:
            self.appl.shared["morphStateOverride"] = 0 if (self.appl.shared["morphStateOverride"] > 0) else 16383

    
    def evaluate_value(self, value):
        if self.__set_internal_state and value != None and value != self.__last_value:
            self.__last_value = value

            if not self.ignore_next_value:
                # Morph value has changed from the outside
                self.appl.shared["morphStateOverride"] = value
            else:
                self.ignore_next_value = False

        super().evaluate_value(value)