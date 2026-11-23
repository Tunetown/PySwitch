from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT, RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO as KEMPER_TAP_TEMPO
from pyswitch.clients.fractal.actions.scene import SCENE_SELECT
from pyswitch.clients.fractal.actions.tap_tempo import TAP_TEMPO as FRACTAL_TAP_TEMPO
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2

Inputs = [

    # Switch 1: Kemper rig 1, hold: Kemper Tap Tempo
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1, "actions": [
            RIG_SELECT(rig = 1, display = DISPLAY_HEADER_1, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG),
        ], "actionsHold": [
            KEMPER_TAP_TEMPO(),
        ]
    },

    # Switch 2: Kemper rig 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2, "actions": [
            RIG_SELECT(rig = 2, display = DISPLAY_HEADER_2, display_mode = RIG_SELECT_DISPLAY_TARGET_RIG),
        ]
    },

    ############################################################################

    # Switch A: Fractal scene 1, hold: Fractal Tap Tempo
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A, "actions": [
            SCENE_SELECT(scene = 1, display = DISPLAY_FOOTER_1),
        ], "actionsHold": [
            FRACTAL_TAP_TEMPO(use_leds = False),
        ]
    },

    # Switch B: Fractal scene 2
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B, "actions": [
            SCENE_SELECT(scene = 2, display = DISPLAY_FOOTER_2),
        ]
    }
]
