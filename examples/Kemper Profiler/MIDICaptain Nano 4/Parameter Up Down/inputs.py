from lib.pyswitch.clients.local.actions.param_change import PARAMETER_UP_DOWN
from lib.pyswitch.colors import Colors
from lib.pyswitch.clients.kemper import KemperEffectSlot
from lib.pyswitch.clients.kemper.mappings.effects import MAPPING_DLY_REV_MIX
from lib.pyswitch.clients.kemper.mappings.amp import MAPPING_AMP_GAIN
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_RIG_NAME
from lib.pyswitch.hardware.devices.pa_midicaptain_nano_4 import *

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            PARAMETER_UP_DOWN(
                mapping = MAPPING_DLY_REV_MIX(
                    KemperEffectSlot.EFFECT_SLOT_ID_REV
                ), 
                offset = 512, 
                display = DISPLAY_HEADER_1, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Rev Up'
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            PARAMETER_UP_DOWN(
                mapping = MAPPING_AMP_GAIN(), 
                offset = 512, 
                display = DISPLAY_HEADER_2, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Gain Up', 
                color = Colors.RED
            ),
            
        ],
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            PARAMETER_UP_DOWN(
                mapping = MAPPING_DLY_REV_MIX(
                    KemperEffectSlot.EFFECT_SLOT_ID_REV
                ), 
                offset = -512, 
                display = DISPLAY_FOOTER_1, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Rev Down'
            ),
            
        ],
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            PARAMETER_UP_DOWN(
                mapping = MAPPING_AMP_GAIN(), 
                offset = -511, 
                display = DISPLAY_FOOTER_2, 
                change_display = DISPLAY_RIG_NAME, 
                text = 'Gain Down', 
                color = Colors.RED
            ),
            
        ],
        
    },
    
]
