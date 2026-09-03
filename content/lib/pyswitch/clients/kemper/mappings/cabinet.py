from .. import KemperMappings, PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping

# Cab name (request only)
def MAPPING_CABINET_NAME(): 
    return ClientParameterMapping.get(
        depends = KemperMappings.RIG_DATE(),
        name = "Cab Name",
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x43, INSTANCE_ID, 0x00, 0x20, 0xf7),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x03, INSTANCE_ID, 0x00, 0x20, 0xf7),
        type = ClientParameterMapping.PARAMETER_TYPE_STRING
    )

# Cab on/off
def MAPPING_CABINET_STATE(): 
    return ClientParameterMapping.get(
        name = "Cab State",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x0c, 0x02, 0x00, 0x00, 0xf7),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x0c, 0x02, 0xf7),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x0c, 0x02, 0x00, 0x00, 0xf7)
    )