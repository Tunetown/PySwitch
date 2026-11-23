from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.fractal import FractalLabel
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT
from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO as KEMPER_TAP_TEMPO
from pyswitch.clients.fractal.actions.scene import SCENE_TOGGLE
from pyswitch.clients.fractal.actions.tap_tempo import TAP_TEMPO as FRACTAL_TAP_TEMPO

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            RIG_SELECT(
                rig = 1, 
                display = DISPLAY_HEADER_1, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            RIG_SELECT(
                rig = 2, 
                display = DISPLAY_HEADER_2, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            SCENE_TOGGLE(
                primary = 1, 
                secondary = 2, 
                display = DISPLAY_FOOTER_1
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            FRACTAL_TAP_TEMPO(
                label = FractalLabel.BPM, 
                display = DISPLAY_FOOTER_2
            ),
            KEMPER_TAP_TEMPO(),
            
        ],
        
    },
    
]
