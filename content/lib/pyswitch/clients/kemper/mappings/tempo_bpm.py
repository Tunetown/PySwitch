from ....controller.client import ClientParameterMapping
from .. import PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID

# Tempo (BPM value)
def MAPPING_TEMPO_BPM():
    return ClientParameterMapping.get(
        name = "BPM",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x04, 0x00, 0x00, 0x00, 0xf7),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x04, 0x00, 0xf7),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x04, 0x00, 0x00, 0x00, 0xf7)
    )

# Output conversion for BPM
def convert_bpm(value):
    return str(round(value / 64))

