from pyswitch.hardware.devices.pa_midicaptain_mini_6 import *
from pyswitch.colors import Colors
from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.clients.fractal import FractalBlock
from pyswitch.clients.fractal.actions.preset import PRESET_SELECT_IN_BANK
from pyswitch.clients.fractal.actions.bank import BANK_INC_DEC
from pyswitch.clients.fractal.actions.scene import SCENE_SELECT
from pyswitch.clients.fractal.actions.scene import SCENE_INC_DEC
from pyswitch.clients.fractal.actions.effect_bypass import EFFECT_BYPASS
from pyswitch.clients.fractal.actions.looper import LOOPER_RECORD
from pyswitch.clients.fractal.actions.looper import LOOPER_PLAY_STOP
from pyswitch.clients.fractal.actions.looper import LOOPER_UNDO
from pyswitch.clients.fractal.actions.looper import LOOPER_ONCE
from pyswitch.clients.fractal.actions.looper import LOOPER_REVERSE
from pyswitch.clients.fractal.actions.tuner import TUNER
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3

# Pages, modelled on the Fractal FC layouts (Presets, Scenes, Effects, Looper)
_pager = PagerAction(
    pages = [
        {
            "id": 1,
            "color": Colors.GREEN,
            "text": "Presets"
        },
        {
            "id": 2,
            "color": Colors.RED,
            "text": "Scenes"
        },
        {
            "id": 3,
            "color": Colors.CYAN,
            "text": "Effects"
        },
        {
            "id": 4,
            "color": Colors.PINK,
            "text": "Looper"
        },
    ],
    display = DISPLAY_FOOTER_3
)

Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1, "actions": [
            PRESET_SELECT_IN_BANK(position = 1, display = DISPLAY_HEADER_1, id = 1, enable_callback = _pager.enable_callback),
            SCENE_SELECT(scene = 1, display = DISPLAY_HEADER_1, id = 2, enable_callback = _pager.enable_callback),
            EFFECT_BYPASS(block = FractalBlock.DRIVE, display = DISPLAY_HEADER_1, id = 3, enable_callback = _pager.enable_callback),
            LOOPER_RECORD(display = DISPLAY_HEADER_1, id = 4, enable_callback = _pager.enable_callback),
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2, "actions": [
            PRESET_SELECT_IN_BANK(position = 2, display = DISPLAY_HEADER_2, id = 1, enable_callback = _pager.enable_callback),
            SCENE_SELECT(scene = 2, display = DISPLAY_HEADER_2, id = 2, enable_callback = _pager.enable_callback),
            EFFECT_BYPASS(block = FractalBlock.DELAY, display = DISPLAY_HEADER_2, id = 3, enable_callback = _pager.enable_callback),
            LOOPER_PLAY_STOP(display = DISPLAY_HEADER_2, id = 4, enable_callback = _pager.enable_callback),
        ]
    },

    # Switch 3
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3, "actions": [
            PRESET_SELECT_IN_BANK(position = 3, display = DISPLAY_HEADER_3, id = 1, enable_callback = _pager.enable_callback),
            SCENE_SELECT(scene = 3, display = DISPLAY_HEADER_3, id = 2, enable_callback = _pager.enable_callback),
            EFFECT_BYPASS(block = FractalBlock.REVERB, display = DISPLAY_HEADER_3, id = 3, enable_callback = _pager.enable_callback),
            LOOPER_UNDO(display = DISPLAY_HEADER_3, id = 4, enable_callback = _pager.enable_callback),
        ]
    },

    ############################################################################

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A, "actions": [
            PRESET_SELECT_IN_BANK(position = 4, display = DISPLAY_FOOTER_1, id = 1, enable_callback = _pager.enable_callback),
            SCENE_SELECT(scene = 4, display = DISPLAY_FOOTER_1, id = 2, enable_callback = _pager.enable_callback),
            EFFECT_BYPASS(block = FractalBlock.CHORUS, display = DISPLAY_FOOTER_1, id = 3, enable_callback = _pager.enable_callback),
            LOOPER_ONCE(display = DISPLAY_FOOTER_1, id = 4, enable_callback = _pager.enable_callback),
        ], "actionsHold": [
            BANK_INC_DEC(step = -1, enable_callback = _pager.enable_callback, id = 1, use_leds = False),
        ]
    },

    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B, "actions": [
            PRESET_SELECT_IN_BANK(position = 5, display = DISPLAY_FOOTER_2, id = 1, enable_callback = _pager.enable_callback),
            SCENE_INC_DEC(step = 1, display = DISPLAY_FOOTER_2, id = 2, enable_callback = _pager.enable_callback),
            EFFECT_BYPASS(block = FractalBlock.COMPRESSOR, display = DISPLAY_FOOTER_2, id = 3, enable_callback = _pager.enable_callback),
            LOOPER_REVERSE(display = DISPLAY_FOOTER_2, id = 4, enable_callback = _pager.enable_callback),
        ], "actionsHold": [
            BANK_INC_DEC(step = 1, enable_callback = _pager.enable_callback, id = 1, use_leds = False),
        ]
    },

    # Switch C: Pages, hold for the tuner
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C, "actions": [
            _pager,
        ], "actionsHold": [
            TUNER(use_leds = False),
        ]
    }
]
