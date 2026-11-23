from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from pyswitch.clients.fractal_II.actions.scene import SCENE_SELECT
from pyswitch.clients.fractal_II.actions.tuner import TUNER

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            SCENE_SELECT(
                scene = 1, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            SCENE_SELECT(
                scene = 2, 
                display = DISPLAY_HEADER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            SCENE_SELECT(
                scene = 3, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            SCENE_SELECT(
                scene = 4, 
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        "actionsHold": [
            TUNER(
                use_leds = False
            ),
            
        ],
        
    },
    
]
