from micropython import const
from .. import KemperParameterMapping, KemperNRPNMessage, KemperEffectSlot
from .. import NRPN_FUNCTION_SET_SINGLE_PARAMETER, NRPN_FUNCTION_REQUEST_SINGLE_PARAMETER, NRPN_FUNCTION_RESPONSE_SINGLE_PARAMETER

from adafruit_midi.control_change import ControlChange

_CC_FREEZE_DELAYS_GLOBAL = const(34)
_CC_FREEZE_ALL_GLOBAL = const(35)

_NRPN_ADDRESS_PAGE_FREEZE = const(0x7d)

# Freeze for slots
def MAPPING_FREEZE(slot_id):
    return KemperParameterMapping(
        name = f"Freeze { str(slot_id) }",
        set = KemperNRPNMessage(
            NRPN_FUNCTION_SET_SINGLE_PARAMETER, 
            _NRPN_ADDRESS_PAGE_FREEZE,
            KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id]
        ),
        request = KemperNRPNMessage(               
            NRPN_FUNCTION_REQUEST_SINGLE_PARAMETER, 
            _NRPN_ADDRESS_PAGE_FREEZE,
            KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id]
        ),
        response = KemperNRPNMessage(               
            NRPN_FUNCTION_RESPONSE_SINGLE_PARAMETER, 
            _NRPN_ADDRESS_PAGE_FREEZE,
            KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id]
        )
    )

# Freeze (global) for all reverb and delay modules (no feedback from kemper!)
def MAPPING_FREEZE_ALL_GLOBAL():
    return KemperParameterMapping(
        name = "Freeze",
        set = ControlChange(
            _CC_FREEZE_ALL_GLOBAL,
            0
        ),
        response = ControlChange(  # Does not receive anything but is needed so that the callback shows the "fake state"
            _CC_FREEZE_ALL_GLOBAL,
            0
        )
    )