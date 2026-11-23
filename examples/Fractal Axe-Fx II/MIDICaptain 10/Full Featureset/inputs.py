from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from pyswitch.clients.fractal_II import FractalIILabel
from pyswitch.clients.fractal_II import FractalIIBlock
from pyswitch.clients.fractal_II import FractalIIChannel
from pyswitch.clients.fractal_II import FractalIISecondPress
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_HEADER_4
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3
from display import DISPLAY_FOOTER_4
from display import DISPLAY_PAGE
from pyswitch.hardware.devices.pa_midicaptain_10 import *
from pyswitch.clients.fractal_II.actions.preset import PRESET_SELECT_IN_BANK, PRESET_INC_DEC
from pyswitch.clients.fractal_II.actions.bank import BANK_INC_DEC
from pyswitch.clients.fractal_II.actions.scene import SCENE_SELECT
from pyswitch.clients.fractal_II.actions.effect_bypass import EFFECT_BYPASS
from pyswitch.clients.fractal_II.actions.effect_channel import EFFECT_CHANNEL_SELECT, EFFECT_CHANNEL_TOGGLE
from pyswitch.clients.fractal_II.actions.tap_tempo import TAP_TEMPO
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
    display = DISPLAY_PAGE
)

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
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
                block = FractalIIBlock.COMPRESSOR_1, 
                display = DISPLAY_HEADER_1, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.DRIVE_1, 
                display = DISPLAY_HEADER_1, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
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
                block = FractalIIBlock.WAH_1, 
                display = DISPLAY_HEADER_2, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.AMP_1, 
                display = DISPLAY_HEADER_2, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
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
                block = FractalIIBlock.DRIVE_1, 
                display = DISPLAY_HEADER_3, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.CAB_1, 
                display = DISPLAY_HEADER_3, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            PRESET_SELECT_IN_BANK(
                position = 4, 
                display = DISPLAY_HEADER_4, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_SELECT(
                scene = 4, 
                display = DISPLAY_HEADER_4, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.AMP_1, 
                display = DISPLAY_HEADER_4, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.DELAY_1, 
                display = DISPLAY_HEADER_4, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            PRESET_SELECT_IN_BANK(
                position = 5, 
                display = DISPLAY_FOOTER_1, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_SELECT(
                scene = 5, 
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
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            BANK_INC_DEC(
                step = -1, 
                label = FractalIILabel.NUMBER, 
                display = DISPLAY_FOOTER_2, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_SELECT(
                scene = 6, 
                display = DISPLAY_FOOTER_2, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.DELAY_1, 
                display = DISPLAY_FOOTER_2, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalIIBlock.CHORUS_1, 
                display = DISPLAY_FOOTER_2, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            BANK_INC_DEC(
                step = 1, 
                label = FractalIILabel.NUMBER, 
                display = DISPLAY_FOOTER_3, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_SELECT(
                scene = 7, 
                display = DISPLAY_FOOTER_3, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.REVERB_1, 
                display = DISPLAY_FOOTER_3, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_SELECT(
                block = FractalIIBlock.AMP_2, 
                channel = FractalIIChannel.X, 
                second_press = FractalIISecondPress.SMART_BYPASS, 
                display = DISPLAY_FOOTER_3, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            PRESET_INC_DEC(
                step = 1, 
                label = FractalIILabel.DESTINATION_NAME, 
                display = DISPLAY_FOOTER_4, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            SCENE_SELECT(
                scene = 8, 
                display = DISPLAY_FOOTER_4, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalIIBlock.AMP_2, 
                display = DISPLAY_FOOTER_4, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_SELECT(
                block = FractalIIBlock.AMP_2, 
                channel = FractalIIChannel.Y, 
                second_press = FractalIISecondPress.SMART_BYPASS, 
                display = DISPLAY_FOOTER_4, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            _pager,
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            TAP_TEMPO(
                label = FractalIILabel.BPM
            ),
            
        ],
        "actionsHold": [
            TUNER(
                use_leds = False
            ),
            
        ],
        
    },
    
]
