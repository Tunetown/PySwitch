from lib.pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from lib.pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from lib.pyswitch.clients.kemper.actions.effect_state_extended_names import EFFECT_STATE_EXT
from lib.pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from lib.pyswitch.clients.local.actions.param_change import PARAMETER_UP_DOWN
from lib.pyswitch.colors import Colors
from lib.pyswitch.clients.kemper import KemperEffectSlot
from lib.pyswitch.clients.kemper.mappings.rig import MAPPING_RIG_VOLUME
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_RIG_NAME
from lib.pyswitch.clients.kemper.callbacks.convert_volume import convert_volume
from lib.pyswitch.hardware.devices.pa_midicaptain_nano_4 import *

# The rig volume goes to +12, so we need to wrap the default volume conversion function.
def _convert_volume(value):
    return convert_volume(value, 12)

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_STATE_EXT(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_X, 
                display = DISPLAY_HEADER_1, 
                text = 'Slap'
            ),
            
        ],
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            TAP_TEMPO(),
            SHOW_TEMPO(
                text = '{bpm} bpm'
            ),
            
        ],
        "actionsHold": [
            TUNER_MODE(
                display = DISPLAY_HEADER_2, 
                use_leds = False, 
                text = 'Tap|Tuner'
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            PARAMETER_UP_DOWN(
                mapping = MAPPING_RIG_VOLUME(), 
                offset = -1024, 
                repeat_interval_millis = 40, 
                display = DISPLAY_FOOTER_1, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Leiser', 
                preview_text_callback = _convert_volume, 
                color = Colors.PURPLE, 
                led_brightness = 0.15
            ),
            
        ],
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            PARAMETER_UP_DOWN(
                mapping = MAPPING_RIG_VOLUME(), 
                offset = 1024, 
                repeat_interval_millis = 40, 
                display = DISPLAY_FOOTER_2, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Lauter', 
                preview_text_callback = _convert_volume, 
                color = Colors.PURPLE, 
                led_brightness = 0.15
            ),
            
        ],
        
    },
    
]
