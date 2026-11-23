from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from pyswitch.clients.fractal import FractalLabel
from pyswitch.clients.fractal import FractalBlock
from pyswitch.clients.fractal import FractalChannel
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
from pyswitch.clients.fractal.actions.preset import PRESET_SELECT_IN_BANK
from pyswitch.clients.fractal.actions.preset import PRESET_INC_DEC
from pyswitch.clients.fractal.actions.bank import BANK_INC_DEC
from pyswitch.clients.fractal.actions.scene import SCENE_SELECT
from pyswitch.clients.fractal.actions.effect_bypass import EFFECT_BYPASS
from pyswitch.clients.fractal.actions.effect_channel import EFFECT_CHANNEL_SELECT
from pyswitch.clients.fractal.actions.effect_channel import EFFECT_CHANNEL_TOGGLE
from pyswitch.clients.fractal.actions.effect_channel import EFFECT_CHANNEL_INC_DEC
from pyswitch.clients.fractal.actions.looper import LOOPER_RECORD
from pyswitch.clients.fractal.actions.looper import LOOPER_PLAY_STOP
from pyswitch.clients.fractal.actions.looper import LOOPER_UNDO
from pyswitch.clients.fractal.actions.looper import LOOPER_ONCE
from pyswitch.clients.fractal.actions.looper import LOOPER_REVERSE
from pyswitch.clients.fractal.actions.looper import LOOPER_HALF_SPEED
from pyswitch.clients.fractal.actions.tuner import TUNER
from pyswitch.clients.fractal.actions.tap_tempo import TAP_TEMPO

# Pages, modelled on the Fractal FC layouts (Presets, Scenes, Effects, Channels, Looper)
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
            "color": Colors.LIGHT_BLUE,
            "text": "Channels",
            
        },
        {
            "id": 5,
            "color": Colors.PINK,
            "text": "Looper",
            
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
                block = FractalBlock.DRIVE, 
                display = DISPLAY_HEADER_1, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_SELECT(
                block = FractalBlock.AMP, 
                channel = FractalChannel.A, 
                display = DISPLAY_HEADER_1, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_RECORD(
                display = DISPLAY_HEADER_1, 
                id = 5, 
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
                block = FractalBlock.DELAY, 
                display = DISPLAY_HEADER_2, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_SELECT(
                block = FractalBlock.AMP, 
                channel = FractalChannel.B, 
                display = DISPLAY_HEADER_2, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_PLAY_STOP(
                display = DISPLAY_HEADER_2, 
                id = 5, 
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
                block = FractalBlock.REVERB, 
                display = DISPLAY_HEADER_3, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_SELECT(
                block = FractalBlock.AMP, 
                channel = FractalChannel.C, 
                display = DISPLAY_HEADER_3, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_UNDO(
                display = DISPLAY_HEADER_3, 
                id = 5, 
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
                block = FractalBlock.CHORUS, 
                display = DISPLAY_HEADER_4, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_SELECT(
                block = FractalBlock.AMP, 
                channel = FractalChannel.D, 
                display = DISPLAY_HEADER_4, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_ONCE(
                display = DISPLAY_HEADER_4, 
                id = 5, 
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
                block = FractalBlock.COMPRESSOR, 
                display = DISPLAY_FOOTER_1, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalBlock.DRIVE, 
                primary = FractalChannel.A, 
                secondary = FractalChannel.B, 
                display = DISPLAY_FOOTER_1, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_REVERSE(
                display = DISPLAY_FOOTER_1, 
                id = 5, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            BANK_INC_DEC(
                step = -1, 
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
                block = FractalBlock.PHASER, 
                display = DISPLAY_FOOTER_2, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_TOGGLE(
                block = FractalBlock.DRIVE, 
                instance = 2, 
                primary = FractalChannel.A, 
                secondary = FractalChannel.B, 
                display = DISPLAY_FOOTER_2, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_HALF_SPEED(
                display = DISPLAY_FOOTER_2, 
                id = 5, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            BANK_INC_DEC(
                step = 1, 
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
                block = FractalBlock.PITCH, 
                display = DISPLAY_FOOTER_3, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_INC_DEC(
                block = FractalBlock.DELAY, 
                label = FractalLabel.CURRENT_CHANNEL, 
                display = DISPLAY_FOOTER_3, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_BYPASS(
                block = FractalBlock.LOOPER, 
                display = DISPLAY_FOOTER_3, 
                id = 5, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            PRESET_INC_DEC(
                step = 1, 
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
                block = FractalBlock.WAH, 
                display = DISPLAY_FOOTER_4, 
                id = 3, 
                enable_callback = _pager.enable_callback
            ),
            EFFECT_CHANNEL_INC_DEC(
                block = FractalBlock.REVERB, 
                label = FractalLabel.CURRENT_CHANNEL, 
                display = DISPLAY_FOOTER_4, 
                id = 4, 
                enable_callback = _pager.enable_callback
            ),
            TAP_TEMPO(
                label = FractalLabel.BPM, 
                display = DISPLAY_FOOTER_4, 
                id = 5, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            TAP_TEMPO(),
            
        ],
        "actionsHold": [
            TUNER(),
            
        ],
        
    },
    
]
