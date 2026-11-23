from pyswitch.colors import Colors
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from pyswitch.clients.fractal_am4.actions.scene import SCENE_SELECT
from pyswitch.clients.fractal_am4.actions.effect_bypass import EFFECT_BYPASS
from pyswitch.clients.local.actions.rotate import ROTATING_MESSAGES

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
            EFFECT_BYPASS(
                slot = 1, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            EFFECT_BYPASS(
                slot = 2, 
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        "actionsHold": [
            ROTATING_MESSAGES(
                messages = [
                    [0xb0, 15, 127],
                    [0xb0, 15, 0],
                    
                ], 
                texts = ["Tuner", "Tuner"], 
                led_colors = [Colors.WHITE, Colors.WHITE], 
                use_leds = False
            ),
            
        ],
        
    },
    
]
