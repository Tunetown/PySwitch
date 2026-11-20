from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from pyswitch.colors import Colors
from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.clients.fractal import FractalBlock
from pyswitch.clients.fractal import FractalChannel
from pyswitch.clients.fractal import FractalLabel
from pyswitch.clients.fractal import FractalPresetLoad
from pyswitch.clients.fractal import FractalSecondPress
from pyswitch.clients.fractal.actions.preset import PRESET_INC_DEC
from pyswitch.clients.fractal.actions.bank import BANK_INC_DEC
from pyswitch.clients.fractal.actions.scene import SCENE_SELECT
from pyswitch.clients.fractal.actions.scene import SCENE_INC_DEC
from pyswitch.clients.fractal.actions.effect_bypass import EFFECT_BYPASS
from pyswitch.clients.fractal.actions.effect_channel import EFFECT_CHANNEL_SELECT
from pyswitch.clients.fractal.actions.effect_channel import EFFECT_CHANNEL_TOGGLE
from pyswitch.clients.fractal.actions.effect_channel import EFFECT_CHANNEL_INC_DEC
from pyswitch.clients.fractal.actions.tap_tempo import TAP_TEMPO
from pyswitch.clients.fractal.actions.tuner import TUNER
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2

# Pages, modelled on the views of the FM3 factory layouts (three switches each)
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
            "color": Colors.LIGHT_BLUE,
            "text": "Channels"
        },
    ],
    display = DISPLAY_FOOTER_2
)

Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1, "actions": [
            PRESET_INC_DEC(step = -1, label = FractalLabel.DESTINATION_NAME, display = DISPLAY_HEADER_1, id = 1, enable_callback = _pager.enable_callback),
            SCENE_SELECT(scene = 1, display = DISPLAY_HEADER_1, id = 2, enable_callback = _pager.enable_callback),
            EFFECT_BYPASS(block = FractalBlock.DRIVE, display = DISPLAY_HEADER_1, id = 3, enable_callback = _pager.enable_callback),
            EFFECT_CHANNEL_TOGGLE(block = FractalBlock.AMP, primary = FractalChannel.A, secondary = FractalChannel.B, display = DISPLAY_HEADER_1, id = 4, enable_callback = _pager.enable_callback),
        ], "actionsHold": [
            BANK_INC_DEC(step = -1, preset_load = FractalPresetLoad.FIRST, enable_callback = _pager.enable_callback, id = 1, use_leds = False),
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2, "actions": [
            PRESET_INC_DEC(step = 1, label = FractalLabel.DESTINATION_NAME, display = DISPLAY_HEADER_2, id = 1, enable_callback = _pager.enable_callback),
            SCENE_SELECT(scene = 2, display = DISPLAY_HEADER_2, id = 2, enable_callback = _pager.enable_callback),
            EFFECT_BYPASS(block = FractalBlock.DELAY, display = DISPLAY_HEADER_2, id = 3, enable_callback = _pager.enable_callback),
            EFFECT_CHANNEL_INC_DEC(block = FractalBlock.DRIVE, label = FractalLabel.CURRENT_CHANNEL, display = DISPLAY_HEADER_2, id = 4, enable_callback = _pager.enable_callback),
        ], "actionsHold": [
            BANK_INC_DEC(step = 1, preset_load = FractalPresetLoad.FIRST, enable_callback = _pager.enable_callback, id = 1, use_leds = False),
        ]
    },

    ############################################################################

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A, "actions": [
            TAP_TEMPO(label = FractalLabel.BPM, display = DISPLAY_FOOTER_1, id = 1, enable_callback = _pager.enable_callback),
            SCENE_INC_DEC(step = 1, label = FractalLabel.DESTINATION_NAME, display = DISPLAY_FOOTER_1, id = 2, enable_callback = _pager.enable_callback),
            EFFECT_BYPASS(block = FractalBlock.REVERB, display = DISPLAY_FOOTER_1, id = 3, enable_callback = _pager.enable_callback),
            EFFECT_CHANNEL_SELECT(block = FractalBlock.DELAY, channel = FractalChannel.B, second_press = FractalSecondPress.SMART_BYPASS, display = DISPLAY_FOOTER_1, id = 4, enable_callback = _pager.enable_callback),
        ]
    },

    # Switch B: Pages, hold for the tuner
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B, "actions": [
            _pager,
        ], "actionsHold": [
            TUNER(use_leds = False),
        ]
    }
]
