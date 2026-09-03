from .. import KemperEffectSlot, PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping

# Effect Button I-IIII (set only). num must be a number (1 to 4).
def MAPPING_EFFECT_BUTTON(num, channel = 0): 
    return ClientParameterMapping.get(
        name = f"Effect Button { repr(num) } ({channel})",
        set = (176 + channel, 75 + (num - 1), 0)
    )


def MAPPING_DLY_REV_MIX(slot_id):
    return ClientParameterMapping.get(
        name = f"Mix { KemperEffectSlot.EFFECT_SLOT_NAME[slot_id] }",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id], 0x45, 0x00, 0x00, 0xf7),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id], 0x45, 0xf7),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, KemperEffectSlot.NRPN_SLOT_ADDRESS_PAGE[slot_id], 0x45, 0x00, 0x00, 0xf7)
    )

