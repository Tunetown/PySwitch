from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from pyswitch.clients.fractal_am4 import FractalAM4Label, FractalAM4Mode
from pyswitch.clients.fractal_am4.actions.preset import PRESET_SELECT_IN_BANK, BANK_INC_DEC
from pyswitch.clients.fractal_am4.actions.scene import SCENE_SELECT, SCENE_INC_DEC
from pyswitch.clients.fractal_am4.actions.effect_bypass import EFFECT_BYPASS
from pyswitch.clients.fractal_am4.actions.mode import MODE_SELECT
from pyswitch.clients.local.actions.rotate import ROTATING_MESSAGES

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
            "color": Colors.BLUE,
            "text": "Modes",
            
        },
        
    ], 
    display = DISPLAY_FOOTER_2
)

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
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
                slot = 1, 
                display = DISPLAY_HEADER_1, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            MODE_SELECT(
                mode = FractalAM4Mode.PRESETS, 
                display = DISPLAY_HEADER_1, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            BANK_INC_DEC(
                step = -1, 
                use_leds = False, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
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
                slot = 2, 
                display = DISPLAY_HEADER_2, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            MODE_SELECT(
                mode = FractalAM4Mode.SCENES, 
                display = DISPLAY_HEADER_2, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            BANK_INC_DEC(
                step = 1, 
                use_leds = False, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            PRESET_SELECT_IN_BANK(
                position = 3, 
                display = DISPLAY_FOOTER_1, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_INC_DEC(
                step = 1, 
                label = FractalAM4Label.DESTINATION_NAME, 
                display = DISPLAY_FOOTER_1, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                slot = 3, 
                display = DISPLAY_FOOTER_1, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            MODE_SELECT(
                mode = FractalAM4Mode.EFFECTS, 
                display = DISPLAY_FOOTER_1, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            _pager,
            
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
