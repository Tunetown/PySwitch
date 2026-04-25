from pyswitch.hardware.devices.pa_midicaptain_10 import *
from pyswitch.clients.kemper import KemperEffectSlot
from pyswitch.clients.kemper.actions.effect_state_per_rig import EFFECT_STATE_PER_RIG
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT, RIG_SELECT_DISPLAY_TARGET_RIG
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from display import DISPLAY_SWITCH_3, DISPLAY_SWITCH_4

# Absolute rig IDs: (bank - 1) * 5 + (rig - 1)
# Bank 1: 0=acou  1=clen  2=crnc  3=heavy  4=lead

Inputs = [

    # Switch 1 — always disabled
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_1,
        "actions": []
    },

    # Switch 2 — always disabled
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_2,
        "actions": []
    },

    # Switch 3 — flanger (X slot) for rigs clen(1), crnc(2), lead(4)
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_3,
        "actions": [
            EFFECT_STATE_PER_RIG(
                slot_id = None,
                rig_overrides = {
                    1: KemperEffectSlot.EFFECT_SLOT_ID_X,   # clen
                    2: KemperEffectSlot.EFFECT_SLOT_ID_X,   # crnc
                    4: KemperEffectSlot.EFFECT_SLOT_ID_X,   # lead
                },
                display = DISPLAY_SWITCH_3
            )
        ]
    },

    # Switch 4 — [MOD+C] for acou(0); X for heavy(3)
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_4,
        "actions": [
            EFFECT_STATE_PER_RIG(
                slot_id = None,
                rig_overrides = {
                    0: [KemperEffectSlot.EFFECT_SLOT_ID_MOD, KemperEffectSlot.EFFECT_SLOT_ID_C],  # acou
                    3: KemperEffectSlot.EFFECT_SLOT_ID_X,                                          # heavy
                },
                display = DISPLAY_SWITCH_4
            )
        ]
    },

    # Switch 5 (UP) — DLY for acou(0); [DLY+REV] for clen(1), crnc(2), heavy(3)
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_UP,
        "actions": [
            EFFECT_STATE_PER_RIG(
                slot_id = None,
                rig_overrides = {
                    0: KemperEffectSlot.EFFECT_SLOT_ID_DLY,                                          # acou
                    1: [KemperEffectSlot.EFFECT_SLOT_ID_DLY, KemperEffectSlot.EFFECT_SLOT_ID_REV],  # clen
                    2: [KemperEffectSlot.EFFECT_SLOT_ID_DLY, KemperEffectSlot.EFFECT_SLOT_ID_REV],  # crnc
                    3: [KemperEffectSlot.EFFECT_SLOT_ID_DLY, KemperEffectSlot.EFFECT_SLOT_ID_REV],  # heavy
                },
                display = None
            )
        ]
    },

    # Switch A — Rig 1, hold: Bank Down
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_A,
        "actions": [
            RIG_SELECT(
                rig = 1,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ],
        "actionsHold": [
            BANK_DOWN(
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                text = "Bank dn"
            )
        ]
    },

    # Switch B — Rig 2
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_B,
        "actions": [
            RIG_SELECT(
                rig = 2,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    },

    # Switch C — Rig 3
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_C,
        "actions": [
            RIG_SELECT(
                rig = 3,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    },

    # Switch D — Rig 4
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_D,
        "actions": [
            RIG_SELECT(
                rig = 4,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ]
    },

    # Switch E (DOWN) — Rig 5, hold: Bank Up
    {
        "assignment": PA_MIDICAPTAIN_10_SWITCH_DOWN,
        "actions": [
            RIG_SELECT(
                rig = 5,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG
            )
        ],
        "actionsHold": [
            BANK_UP(
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                text = "Bank up"
            )
        ]
    },

]
