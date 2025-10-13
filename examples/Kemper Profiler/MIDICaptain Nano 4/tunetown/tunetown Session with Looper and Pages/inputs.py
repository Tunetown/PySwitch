from pyswitch.clients.kemper.actions.looper import LOOPER_REC_PLAY_OVERDUB
from pyswitch.clients.kemper.actions.looper import LOOPER_STOP
from pyswitch.clients.kemper.actions.looper import LOOPER_ERASE
from pyswitch.clients.kemper.actions.looper import LOOPER_CANCEL
from pyswitch.clients.kemper.actions.looper import LOOPER_REVERSE
from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from pyswitch.clients.kemper.actions.tempo import SHOW_TEMPO
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT_DISPLAY_TARGET_RIG
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_PAGE
from display import DISPLAY_RIG_NAME
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *


_pager = PagerAction(
    pages = [
        {
            "id": 1,
            "color": Colors.BLACK,
            "text": "                                                              Looper",
            
        },
        {
            "id": 2,
            "color": Colors.LIGHT_GREEN,
            "text": "L  O  O  P  E  R",
            
        },
        
    ], 
    display = DISPLAY_PAGE
)


Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            TAP_TEMPO(
                use_leds = False
            ),
            SHOW_TEMPO(
                change_display = DISPLAY_RIG_NAME, 
                text = '{bpm} bpm'
            ),
            
        ],
        "actionsHold": [
            TUNER_MODE(
                display = DISPLAY_HEADER_1, 
                text = "Tap|Tune"
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            LOOPER_REC_PLAY_OVERDUB(
                color = Colors.LIGHT_GREEN, 
                display = DISPLAY_HEADER_2, 
                text = "Rec|Erase", 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_STOP(
                color = Colors.LIGHT_RED, 
                display = DISPLAY_HEADER_2, 
                text = "Stp|Erase", 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            LOOPER_ERASE(
                color = Colors.RED
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            RIG_SELECT(
                rig = 4, 
                rig_off = "auto", 
                auto_exclude_rigs = (4, 5), 
                display = DISPLAY_FOOTER_1, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                color = Colors.PINK, 
                text = "Synth-4", 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_CANCEL(
                color = Colors.LIGHT_GREEN, 
                display = DISPLAY_FOOTER_1, 
                text = "Undo|Rev", 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            LOOPER_REVERSE(
                color = Colors.YELLOW, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            RIG_SELECT(
                rig = 5, 
                rig_off = "auto", 
                auto_exclude_rigs = (4, 5), 
                display = DISPLAY_FOOTER_2, 
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG, 
                color = Colors.RED, 
                text = "Lead-5|Lp", 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            LOOPER_REC_PLAY_OVERDUB(
                color = Colors.LIGHT_GREEN, 
                display = DISPLAY_FOOTER_2, 
                text = "Rec|Exit", 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        "actionsHold": [
            _pager,
            
        ],
        
    },
    
]
