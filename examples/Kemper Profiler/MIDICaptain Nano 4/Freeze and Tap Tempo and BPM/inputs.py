from lib.pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from lib.pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from lib.pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from lib.pyswitch.colors import Colors
from lib.pyswitch.controller.callbacks import BinaryParameterCallback
from lib.pyswitch.controller.actions import PushButtonAction
from lib.pyswitch.clients.kemper import KemperEffectSlot
from lib.pyswitch.clients.kemper.mappings.freeze import MAPPING_FREEZE
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
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B, 
                display = DISPLAY_HEADER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            PushButtonAction(
                {
                    "callback": BinaryParameterCallback(
                        mapping = MAPPING_FREEZE(
                            KemperEffectSlot.EFFECT_SLOT_ID_REV
                        ), 
                        text = "RvFreeze", 
                        color = Colors.DARK_GREEN
                    ),
                    "mode": PushButtonAction.MOMENTARY,
                    "display": DISPLAY_FOOTER_1,
                    "useSwitchLeds": True,
                    
                }
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            TAP_TEMPO(
                color = Colors.LIGHT_GREEN
            ),
            SHOW_TEMPO(
                display = DISPLAY_FOOTER_2, 
                change_display = DISPLAY_RIG_NAME, 
                text = '{bpm} bpm'
            ),
            
        ],
        
    },
    
]
