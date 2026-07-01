# inputs.py — Default Effect State + 3-char ALL-CAPS for categories AND fixed FX (MC10-safe)

# --- Imports -----------------------------------------------------------------
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_EFFECT_STATE
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from pyswitch.clients.kemper.actions.bank_select_encoder import ENCODER_BANK_SELECT
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.colors import Colors
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_TRANSPOSE
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_GATE
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_COMP
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_BOOST
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_WAH
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_CHORUS
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_AIR
from pyswitch.clients.kemper.actions.fixed_fx import FIXED_SLOT_ID_DBL_TRACKER
from pyswitch.clients.kemper import KemperEffectSlot
from display import DISPLAY_HEADER_1
from display import DISPLAY_HEADER_2
from display import DISPLAY_HEADER_3
from display import DISPLAY_HEADER_4
from display import DISPLAY_FOOTER_1
from display import DISPLAY_FOOTER_2
from display import DISPLAY_FOOTER_3
from display import DISPLAY_FOOTER_4
from pyswitch.clients.kemper.actions.effect_state import KemperEffectEnableCallback
from pyswitch.hardware.devices.pa_midicaptain_10 import (
    PA_MIDICAPTAIN_10_EXP_PEDAL_1,
    PA_MIDICAPTAIN_10_EXP_PEDAL_2,
    PA_MIDICAPTAIN_10_WHEEL_ENCODER,
    PA_MIDICAPTAIN_10_WHEEL_BUTTON,
    PA_MIDICAPTAIN_10_SWITCH_1,
    PA_MIDICAPTAIN_10_SWITCH_2,
    PA_MIDICAPTAIN_10_SWITCH_3,
    PA_MIDICAPTAIN_10_SWITCH_4,
    PA_MIDICAPTAIN_10_SWITCH_A,
    PA_MIDICAPTAIN_10_SWITCH_B,
    PA_MIDICAPTAIN_10_SWITCH_C,
    PA_MIDICAPTAIN_10_SWITCH_D,
    PA_MIDICAPTAIN_10_SWITCH_UP,
    PA_MIDICAPTAIN_10_SWITCH_DOWN,
)
# -----------------------------------------------------------------------------


# --- Global category label override (ALL CAPS, 3 chars) ----------------------
# IMPORTANT: Order/length must match Kemper's category enum. Keep '-' at index 0.
KemperEffectEnableCallback.CATEGORY_NAMES = (
    "-",    # 0 (none)
    "WAH",  # 1
    "DIS",  # 2 Distortion/Drive/Fuzz
    "CMP",  # 3 Compressor
    "GAT",  # 4 Gate
    "SPA",  # 5 Space
    "CHO",  # 6 Chorus
    "PHA",  # 7 Phaser
    "EQ",   # 8 EQ
    "BST",  # 9 Boost
    "LOP",  # 10 Loop
    "PIT",  # 11 Pitch
    "DUA",  # 12 Dual
    "DLY",  # 13 Delay
    "REV",  # 14 Reverb
)
# -----------------------------------------------------------------------------


# --- Fixed-FX 3-char ALL-CAPS mapping + safe constructor ---------------------
FIXED_SLOT_LABELS = {
    FIXED_SLOT_ID_TRANSPOSE:   "TRN",
    FIXED_SLOT_ID_GATE:        "GAT",
    FIXED_SLOT_ID_COMP:        "CMP",
    FIXED_SLOT_ID_BOOST:       "BST",
    FIXED_SLOT_ID_WAH:         "WAH",
    FIXED_SLOT_ID_CHORUS:      "CHO",
    FIXED_SLOT_ID_AIR:         "AIR",  # or "SPA" if you prefer to match Space
    FIXED_SLOT_ID_DBL_TRACKER: "DBL",
}

def make_fixed_effect_state(*, slot, display, id, enable_callback):
    """
    Construct FIXED_EFFECT_STATE and ensure its label uses our 3-char code.
    Tries text/label/name kwargs (different builds accept different names).
    Falls back to seeding the display text if needed.
    """
    label = FIXED_SLOT_LABELS.get(slot, "FX")
    for kw in ({"text": label}, {"label": label}, {"name": label}, {}):
        try:
            act = FIXED_EFFECT_STATE(
                slot=slot,
                display=display,
                id=id,
                enable_callback=enable_callback,
                **kw
            )
            if kw:
                return act
            try:
                if hasattr(display, "set_text"):
                    display.set_text(label)
            except Exception:
                pass
            return act
        except TypeError:
            continue
    return FIXED_EFFECT_STATE(slot=slot, display=display, id=id, enable_callback=enable_callback)
# -----------------------------------------------------------------------------


# --- Pager -------------------------------------------------------------------
_pager = PagerAction(
    pages = [
        {
            "id": 1,
            
        },
        {
            "id": 2,
            "color": Colors.PURPLE,
            
        },
        
    ]
)
# -----------------------------------------------------------------------------


# --- Inputs ------------------------------------------------------------------
Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_1,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_EXP_PEDAL_2,
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_ENCODER,
        "actions": [
            ENCODER_BANK_SELECT(),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_WHEEL_BUTTON,
        "actions": [
            RIG_SELECT(
                rig = 1, 
                id = None
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A, 
                display = DISPLAY_HEADER_1, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            make_fixed_effect_state(
                slot = FIXED_SLOT_ID_TRANSPOSE, 
                display = DISPLAY_HEADER_1, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B, 
                display = DISPLAY_HEADER_2, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            make_fixed_effect_state(
                slot = FIXED_SLOT_ID_GATE, 
                display = DISPLAY_HEADER_2, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C, 
                display = DISPLAY_HEADER_3, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            make_fixed_effect_state(
                slot = FIXED_SLOT_ID_COMP, 
                display = DISPLAY_HEADER_3, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D, 
                display = DISPLAY_HEADER_4, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            make_fixed_effect_state(
                slot = FIXED_SLOT_ID_BOOST, 
                display = DISPLAY_HEADER_4, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            TUNER_MODE(
                text = 'Tuner'
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_X, 
                display = DISPLAY_FOOTER_1, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            make_fixed_effect_state(
                slot = FIXED_SLOT_ID_WAH, 
                display = DISPLAY_FOOTER_1, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_MOD, 
                display = DISPLAY_FOOTER_2, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            make_fixed_effect_state(
                slot = FIXED_SLOT_ID_CHORUS, 
                display = DISPLAY_FOOTER_2, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY, 
                display = DISPLAY_FOOTER_3, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            make_fixed_effect_state(
                slot = FIXED_SLOT_ID_AIR, 
                display = DISPLAY_FOOTER_3, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_REV, 
                display = DISPLAY_FOOTER_4, 
                id = 1, 
                enable_callback = _pager.enable_callback
            ),
            make_fixed_effect_state(
                slot = FIXED_SLOT_ID_DBL_TRACKER, 
                display = DISPLAY_FOOTER_4, 
                id = 2, 
                enable_callback = _pager.enable_callback
            ),
            
        ],
        
    },
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            _pager,
            
        ],
        
    },
    
]
# -----------------------------------------------------------------------------
