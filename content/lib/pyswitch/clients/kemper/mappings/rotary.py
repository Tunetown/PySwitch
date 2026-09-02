from .. import KemperEffectSlot, PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping

# Rotary speed (fast/slow)
def MAPPING_ROTARY_SPEED(slot_id):
    return ClientParameterMapping.get(
        name = f"Rot. Speed { KemperEffectSlot.EFFECT_SLOT_NAME[slot_id] }",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id], 0x1e, 0xf7),
        # KemperNRPNMessage(
        #     0x01, 
        #     KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id],
        #     0x1e
        # ),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id], 0x1e, 0xf7),
        # KemperNRPNMessage(               
        #     0x41, 
        #     KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id],
        #     0x1e
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id], 0x1e, 0xf7),
        # KemperNRPNMessage(
        #     0x01,
        #     KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id],
        #     0x1e
        # )
    )

