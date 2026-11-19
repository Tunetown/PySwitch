from pyswitch.hardware.devices.pa_midicaptain_mini_6 import *
from pyswitch.clients.boomerang.actions.boomerang import BOOMERANG_PLAY_STOP_ALL
from pyswitch.clients.boomerang.actions.boomerang import BOOMERANG_SYNC_SERIAL
from pyswitch.clients.boomerang.actions.boomerang import BOOMERANG_MUTE_THRU
from pyswitch.clients.boomerang.actions.boomerang import BOOMERANG_PANIC
from pyswitch.clients.boomerang.actions.boomerang import BOOMERANG_ERASE_ALL
from pyswitch.clients.boomerang.actions.boomerang import BOOMERANG_STACK
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1,
        "actions": [
            BOOMERANG_SYNC_SERIAL(
              display = DISPLAY_HEADER_1,
              num_leds = 3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2,
        "actions": [
            BOOMERANG_MUTE_THRU(
              display = DISPLAY_HEADER_2,
              num_leds = 3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3,
        "actions": [
            BOOMERANG_PANIC(
              display = DISPLAY_HEADER_3,
              num_leds = 3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A,
        "actions": [
            BOOMERANG_PLAY_STOP_ALL(
              display = DISPLAY_FOOTER_1, 
              num_leds = 3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B,
        "actions": [
            BOOMERANG_ERASE_ALL(
              display = DISPLAY_FOOTER_2,
              num_leds = 3
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C,
        "actions": [
            BOOMERANG_STACK(
              display = DISPLAY_FOOTER_3,
              num_leds = 3
            ),
            
        ],
        
    },
    
]
