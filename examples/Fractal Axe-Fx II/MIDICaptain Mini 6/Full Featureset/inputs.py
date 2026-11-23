from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from pyswitch.clients.fractal_II import FractalIILabel
from pyswitch.clients.fractal_II import FractalIIBlock
from pyswitch.clients.fractal_II import FractalIIPresetLoad
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3
from pyswitch.hardware.devices.pa_midicaptain_mini_6 import *
from pyswitch.clients.fractal_II.actions.preset import PRESET_SELECT_IN_BANK
from pyswitch.clients.fractal_II.actions.bank import BANK_INC_DEC
from pyswitch.clients.fractal_II.actions.scene import SCENE_SELECT, SCENE_INC_DEC
from pyswitch.clients.fractal_II.actions.effect_bypass import EFFECT_BYPASS
from pyswitch.clients.fractal_II.actions.effect_channel import EFFECT_CHANNEL_TOGGLE
from pyswitch.clients.fractal_II.actions.tuner import TUNER

_pager = PagerAction(
    pages = [
        {
            "id": 1,
            "color": Colors.GREEN,
            "text": "Presets",
            
        },
        {
            "id": 2,
            "color": Colors.RED,
            "text": "Scenes",
            
        },
        {
            "id": 3,
            "color": Colors.CYAN,
            "text": "Effects",
            
        },
        {
            "id": 4,
            "color": Colors.CYAN,
            "text": "Channels",
            
        },
        
    ], 
    display = DISPLAY_FOOTER_3
)

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1,
        "actions": [
            PRESET_SELECT_IN_BANK(
                position = 1, 
                display = DISPLAY_HEADER_1, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_SELECT(
                scene = 1, 
                display = DISPLAY_HEADER_1, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.DRIVE_1, 
                display = DISPLAY_HEADER_1, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.AMP_1, 
                display = DISPLAY_HEADER_1, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2,
        "actions": [
            PRESET_SELECT_IN_BANK(
                position = 2, 
                display = DISPLAY_HEADER_2, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_SELECT(
                scene = 2, 
                display = DISPLAY_HEADER_2, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.DELAY_1, 
                display = DISPLAY_HEADER_2, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.DRIVE_1, 
                display = DISPLAY_HEADER_2, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3,
        "actions": [
            PRESET_SELECT_IN_BANK(
                position = 3, 
                display = DISPLAY_HEADER_3, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_SELECT(
                scene = 3, 
                display = DISPLAY_HEADER_3, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.REVERB_1, 
                display = DISPLAY_HEADER_3, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.DELAY_1, 
                display = DISPLAY_HEADER_3, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A,
        "actions": [
            BANK_INC_DEC(
                step = -1, 
                label = FractalIILabel.NUMBER, 
                preset_load = FractalIIPresetLoad.FIRST, 
                display = DISPLAY_FOOTER_1, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_INC_DEC(
                step = -1, 
                display = DISPLAY_FOOTER_1, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.CHORUS_1, 
                display = DISPLAY_FOOTER_1, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.REVERB_1, 
                display = DISPLAY_FOOTER_1, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B,
        "actions": [
            BANK_INC_DEC(
                step = 1, 
                label = FractalIILabel.NUMBER, 
                preset_load = FractalIIPresetLoad.FIRST, 
                display = DISPLAY_FOOTER_2, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_INC_DEC(
                step = 1, 
                display = DISPLAY_FOOTER_2, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.COMPRESSOR_1, 
                display = DISPLAY_FOOTER_2, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.CAB_1, 
                display = DISPLAY_FOOTER_2, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C,
        "actions": [
            _pager,
            
        ],
        "actionsHold": [
            TUNER(
                use_leds = False
            ),
            
        ],
        
    },
    
]
