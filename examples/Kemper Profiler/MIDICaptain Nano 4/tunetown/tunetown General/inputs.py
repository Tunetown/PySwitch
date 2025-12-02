from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.clients.local.actions.param_change import PARAMETER_UP_DOWN
from pyswitch.clients.local.actions.binary_switch import BINARY_SWITCH
from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from pyswitch.clients.kemper import KemperEffectSlot
from pyswitch.clients.kemper.mappings.effects import MAPPING_DLY_REV_MIX
from pyswitch.clients.kemper.mappings.amp import MAPPING_AMP_GAIN
from pyswitch.clients.kemper.mappings.rig import MAPPING_RIG_VOLUME
from pyswitch.clients.kemper.mappings.cabinet import MAPPING_CABINET_STATE
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_RIG_NAME
from pyswitch.clients.kemper.callbacks.convert_volume import convert_volume
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *

# The rig volume goes to +12, so we need to wrap the default volume conversion function.
def _convert_volume(value):
    return convert_volume(value, 12)

_pager = PagerAction(
    pages = [
        {
            "id": 1,
            "color": Colors.PURPLE,
            "text": 'Volume',
            
        },
        {
            "id": 2,
            "color": Colors.LIGHT_GREEN,
            "text": 'Slot DLY',
            
        },
        {
            "id": 3,
            "color": Colors.GREEN,
            "text": 'Slot REV',
            
        },
        {
            "id": 4,
            "color": Colors.RED,
            "text": 'Gain',
            
        },
        
    ], 
    display = DISPLAY_HEADER_2
)

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            TUNER_MODE(
                color = Colors.WHITE, 
                text = 'Tuner'
            ),
            
        ],
        "actionsHold": [
            BINARY_SWITCH(
                mapping = MAPPING_CABINET_STATE(), 
                display = DISPLAY_HEADER_1, 
                led_brightness_on = 0.02, 
                led_brightness_off = 0, 
                text = 'Cab|Tuner'
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            _pager,
            
        ],
        "actionsHold": [],
        
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
                led_brightness = 0.15, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            PARAMETER_UP_DOWN(
                mapping = MAPPING_DLY_REV_MIX(
                    KemperEffectSlot.EFFECT_SLOT_ID_DLY
                ), 
                offset = -1024, 
                repeat_interval_millis = 40, 
                display = DISPLAY_FOOTER_1, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Less', 
                color = Colors.LIGHT_GREEN, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            PARAMETER_UP_DOWN(
                mapping = MAPPING_DLY_REV_MIX(
                    KemperEffectSlot.EFFECT_SLOT_ID_REV
                ), 
                offset = -1024, 
                repeat_interval_millis = 40, 
                display = DISPLAY_FOOTER_1, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Less', 
                color = Colors.GREEN, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            PARAMETER_UP_DOWN(
                mapping = MAPPING_AMP_GAIN(), 
                offset = -1024, 
                repeat_interval_millis = 40, 
                display = DISPLAY_FOOTER_1, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Cooler', 
                color = Colors.RED, 
                id = 4, 
                enable_callback = _pager.enable_callback
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
                led_brightness = 0.15, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            PARAMETER_UP_DOWN(
                mapping = MAPPING_DLY_REV_MIX(
                    KemperEffectSlot.EFFECT_SLOT_ID_DLY
                ), 
                offset = 1024, 
                repeat_interval_millis = 40, 
                display = DISPLAY_FOOTER_2, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'More', 
                color = Colors.LIGHT_GREEN, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            PARAMETER_UP_DOWN(
                mapping = MAPPING_DLY_REV_MIX(
                    KemperEffectSlot.EFFECT_SLOT_ID_REV
                ), 
                offset = 1024, 
                repeat_interval_millis = 40, 
                display = DISPLAY_FOOTER_2, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'More', 
                color = Colors.GREEN, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            PARAMETER_UP_DOWN(
                mapping = MAPPING_AMP_GAIN(), 
                offset = 1024, 
                repeat_interval_millis = 40, 
                display = DISPLAY_FOOTER_2, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Hotter', 
                color = Colors.RED, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    
]
