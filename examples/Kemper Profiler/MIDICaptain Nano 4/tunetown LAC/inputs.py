from lib.pyswitch.clients.kemper.actions.rig_volume_boost import RIG_VOLUME_BOOST
from lib.pyswitch.clients.kemper.actions.morph import MORPH_DISPLAY
from lib.pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from lib.pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from lib.pyswitch.colors import Colors
from lib.pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from lib.pyswitch.hardware.devices.pa_midicaptain_nano_4 import *


Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_MOD, 
                display = DISPLAY_HEADER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            TUNER_MODE(
                display = DISPLAY_FOOTER_1, 
                text = 'Tuner'
            ),
            MORPH_DISPLAY(
                text = 'Morph'
            ),
            
        ],
        "actionsHold": [],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            RIG_VOLUME_BOOST(
                boost_volume = 0.625, 
                display = DISPLAY_FOOTER_2, 
                color = Colors.RED, 
                text = '+3dB'
            ),
            
        ],
        
    },
    
]
