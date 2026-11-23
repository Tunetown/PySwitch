from pyswitch.colors import Colors
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3
from pyswitch.hardware.devices.pa_midicaptain_mini_6 import *
from pyswitch.clients.fractal_am4 import FractalAM4Label
from pyswitch.clients.fractal_am4.actions.preset import PRESET_INC_DEC
from pyswitch.clients.fractal_am4.actions.scene import SCENE_SELECT
from pyswitch.clients.local.actions.rotate import ROTATING_MESSAGES

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1,
        "actions": [
            SCENE_SELECT(
                scene = 1, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2,
        "actions": [
            SCENE_SELECT(
                scene = 2, 
                display = DISPLAY_HEADER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3,
        "actions": [
            SCENE_SELECT(
                scene = 3, 
                display = DISPLAY_HEADER_3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A,
        "actions": [
            PRESET_INC_DEC(
                step = -1, 
                label = FractalAM4Label.DESTINATION_NAME, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B,
        "actions": [
            PRESET_INC_DEC(
                step = 1, 
                label = FractalAM4Label.DESTINATION_NAME, 
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C,
        "actions": [
            SCENE_SELECT(
                scene = 4, 
                display = DISPLAY_FOOTER_3
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
