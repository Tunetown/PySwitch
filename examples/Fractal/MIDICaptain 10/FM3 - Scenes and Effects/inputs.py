from pyswitch.clients.fractal import FractalBlock
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_HEADER_4
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3
from display import DISPLAY_FOOTER_4
from pyswitch.hardware.devices.pa_midicaptain_10 import *
from pyswitch.clients.fractal.actions.scene import SCENE_SELECT
from pyswitch.clients.fractal.actions.effect_bypass import EFFECT_BYPASS
from pyswitch.clients.fractal.actions.preset import PRESET_INC_DEC
from pyswitch.clients.fractal.actions.tuner import TUNER

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            SCENE_SELECT(
                scene = 1, 
                display = DISPLAY_HEADER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            SCENE_SELECT(
                scene = 2, 
                display = DISPLAY_HEADER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            SCENE_SELECT(
                scene = 3, 
                display = DISPLAY_HEADER_3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            SCENE_SELECT(
                scene = 4, 
                display = DISPLAY_HEADER_4
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            EFFECT_BYPASS(
                block = FractalBlock.DRIVE, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            EFFECT_BYPASS(
                block = FractalBlock.DELAY, 
                display = DISPLAY_FOOTER_2
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            EFFECT_BYPASS(
                block = FractalBlock.REVERB, 
                display = DISPLAY_FOOTER_3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            EFFECT_BYPASS(
                block = FractalBlock.CHORUS, 
                display = DISPLAY_FOOTER_4
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            PRESET_INC_DEC(
                step = 1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            PRESET_INC_DEC(
                step = -1
            ),
            
        ],
        "actionsHold": [
            TUNER(
                use_leds = False
            ),
            
        ],
        
    },
    
]
