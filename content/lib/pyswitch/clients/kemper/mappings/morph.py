from .. import PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping


def MAPPING_MORPH_BUTTON(channel = 0): 
    return ClientParameterMapping.get(
        name = f"Morph Button ({channel})",
        set = (176 + channel, 80, 0),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x00, 0x0b, 0xf7),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x00, 0x0b, 0x00, 0x00, 0xf7)
    )

def MAPPING_MORPH_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"Morph ({channel})",
        set = (176 + channel, 11, 0),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x00, 0x0b, 0xf7),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x00, 0x0b, 0x00, 0x00, 0xf7)
    )