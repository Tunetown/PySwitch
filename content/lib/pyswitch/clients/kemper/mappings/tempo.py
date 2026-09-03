from .. import PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping

# Switch tuner mode on/off (no receive possible!)
def MAPPING_TAP_TEMPO(channel = 0): 
    return ClientParameterMapping.get(
        name = f"Tap Tempo ({channel})",
        set = (176 + channel, 30, 0)
    )

def MAPPING_TEMPO_DISPLAY():
    return ClientParameterMapping.get(
        name = "Tempo Pulse",
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7c, 0x00, 0xf7)
    )
