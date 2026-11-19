from pyswitch.hardware.devices.pa_midicaptain_mini_6 import *
from pyswitch.colors import Colors
from pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_HEADER_1, DISPLAY_HEADER_2, DISPLAY_HEADER_3, DISPLAY_FOOTER_1, DISPLAY_FOOTER_2, DISPLAY_FOOTER_3, DISPLAY_PAGE
from pyswitch.clients.kemper.actions.rig_volume_boost import RIG_VOLUME_BOOST
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from pyswitch.clients.kemper.actions.rig_up_down import RIG_UP, RIG_DOWN
from pyswitch.clients.kemper.actions.looper import LOOPER_REC_PLAY_OVERDUB, LOOPER_STOP, LOOPER_ERASE, LOOPER_CANCEL, LOOPER_REVERSE, LOOPER_HALF_SPEED
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from pyswitch.clients.local.actions.pager import PagerAction

_pager = PagerAction(
    pages = [
       {
            "id": 1, 
            "color": Colors.RED,
            "text": "E  F  F  E  C  T  S "
        },
        {
            "id": 2, 
            "color": Colors.GREEN,
            "text": "L  O  O  P  E  R"
        },   ],
    display = DISPLAY_PAGE
)


Inputs = [

    # Switch 1
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_1,
        "actions": [
            # Page 1: Effects Slot 1
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A,
                display = DISPLAY_HEADER_1,
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            
            # Page 2: Looper Undo/Reactivate Overdub
            LOOPER_CANCEL(
                color = Colors.LIGHT_GREEN,
                display = DISPLAY_HEADER_1,
                id = 2,
                enable_callback = _pager.enable_callback
            )
        ],
        "actionsHold": [
            # Page 1: Bank Up
            BANK_UP(
                id = 1,
                color = Colors.BLUE,
                enable_callback = _pager.enable_callback
            )
        ]
    },

    # Switch 2
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_2,
        "actions": [
	        # Page 1: Effects Slot 2
            EFFECT_STATE(
		        slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B,
                display = DISPLAY_HEADER_2,
		        id = 1,
                enable_callback = _pager.enable_callback
            ),
            
            # Page 2: Looper Half Speed
            LOOPER_HALF_SPEED(
                color = Colors.LIGHT_GREEN,
                id = 2,
		        display = DISPLAY_HEADER_2,
	            enable_callback = _pager.enable_callback
            )
        ],

        "actionsHold": [
            # Page 1: Rig Up
            RIG_UP(
                id = 1,
	            color = Colors.RED,
	            enable_callback = _pager.enable_callback
	        )
        ]
    },

    # Switch 3
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_3,
        "actions": [
            # Page 1: Effects Slot 3
            EFFECT_STATE(
		        id = 1,
		        slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C,
                display = DISPLAY_HEADER_3,
                enable_callback = _pager.enable_callback
            ),
            
            # Page 2: Looper Reverse
            LOOPER_REVERSE(
                color = Colors.LIGHT_GREEN,
                display = DISPLAY_HEADER_3,
                text = "Rev",
                id = 2,
                enable_callback = _pager.enable_callback
            )
        ]
    },

    #############################################################################

    # Switch A
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_A,
        "actions": [
            # Page 1: Effects Slot 4
            EFFECT_STATE(
		        slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D,
                display = DISPLAY_FOOTER_1,
		        id = 1,
		        enable_callback = _pager.enable_callback
            ),

            # Page 2: Looper Rec/Play/Overdub
            LOOPER_REC_PLAY_OVERDUB(
                color = Colors.LIGHT_GREEN,
                display = DISPLAY_FOOTER_1,
                id = 2,
                enable_callback = _pager.enable_callback
            )
        ],
        "actionsHold": [
             # Page 1: Bank Down
        	BANK_DOWN(
                id = 1,
		        color = Colors.BLUE,
		        enable_callback = _pager.enable_callback
            )
        ]     
    },
    
    # Switch B
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_B,
         "actions": [
            # Page 1: Effects Slot Delay
            EFFECT_STATE(
		        slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY,
                display = DISPLAY_FOOTER_2,
		        id = 1,
		        enable_callback = _pager.enable_callback
            ),
            
            # Page 2: Looper Stop
            LOOPER_STOP(
                color = Colors.LIGHT_GREEN,
                display = DISPLAY_FOOTER_2,
                id = 2,
                enable_callback = _pager.enable_callback
            ) 
        ],
        "actionsHold": [
            # Page 2: Looper Erase
            LOOPER_ERASE(
        		id = 2,
		        enable_callback = _pager.enable_callback
            ),
            
            # Page 1: Rig Down
            RIG_DOWN(
                id = 1,
	            color=Colors.RED,
	            enable_callback=_pager.enable_callback
	        )
        ]
    },

    # Switch C
    {
        "assignment": PA_MIDICAPTAIN_MINI_SWITCH_C,
        "actions": [
            RIG_VOLUME_BOOST(
		        id = 1,
                boost_volume = 0.60,    # Value im [0..1] representing the Rig Volume Knob. Examples: 0.5 = 0dB (no boost), 0.75 = +6dB, 1.0 = +12dB
                text = "Boost",
                display = DISPLAY_FOOTER_3
            )        
        ],
       
        "actionsHold": [        
            _pager
        ]
    }
]