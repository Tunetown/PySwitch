from .. import KemperEffectSlot, PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping

# Freeze for slots
def MAPPING_FREEZE(slot_id):
    return ClientParameterMapping.get(
        name = f"Freeze { KemperEffectSlot.EFFECT_SLOT_NAME[slot_id] }",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id], 0xf7),
        # KemperNRPNMessage(
        #     0x01, 
        #     0x7d,
        #     KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id]
        # ),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x7d, KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id], 0xf7),
        # KemperNRPNMessage(               
        #     0x41, 
        #     0x7d,
        #     KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id]
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id], 0xf7),
        # KemperNRPNMessage(               
        #     0x01, 
        #     0x7d,
        #     KemperEffectSlot.NRPN_FREEZE_SLOT_PARAMETER_ADDRESSES[slot_id]
        # )
    )

# Freeze (global) for all reverb and delay modules (no feedback from kemper!)
def MAPPING_FREEZE_ALL_GLOBAL(channel = 0):
    return ClientParameterMapping.get(
        name = "Freeze",
        set = (176 + channel, 35, 0),
        # ControlChange(
        #     35,
        #     0
        # ),
        response = (176 + channel, 35, 0)  # Does not receive anything but is needed so that the callback shows the "fake state"
        # ControlChange(  # Does not receive anything but is needed so that the callback shows the "fake state"
        #     35,
        #     0
        # )
    )