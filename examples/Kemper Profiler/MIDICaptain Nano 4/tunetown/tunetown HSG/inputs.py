from pyswitch.clients.kemper.actions.rig_volume_boost import RIG_VOLUME_BOOST
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_EFFECT_STATE
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.colors import Colors
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_BOOST
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *


Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            TUNER_MODE(
                display = DISPLAY_HEADER_1, 
                use_leds = False
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            FIXED_EFFECT_STATE(
                slot = FIXED_SLOT_ID_BOOST, 
                display = DISPLAY_HEADER_2, 
                color = Colors.PINK
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            RIG_SELECT(
                rig = 4, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                display = DISPLAY_FOOTER_1, 
                rig_off = 1, 
                color = Colors.RED, 
                text = 'JCM800'
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            RIG_VOLUME_BOOST(
                boost_volume = 0.75, 
                display = DISPLAY_FOOTER_2, 
                color = Colors.TURQUOISE, 
                text = 'RigBoost'
            ),
            
        ],
        
    },
    
]
