from .. import KemperMappings, PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping


# Rig comment (request only)
def MAPPING_RIG_COMMENT(): 
    return ClientParameterMapping.get(
        depends = KemperMappings.RIG_DATE(),
        name = "Rig Comment",
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x43, INSTANCE_ID, 0x00, 0x04, 0xf7),
        # KemperNRPNMessage(               
        #     0x43,
        #     0x00,
        #     0x04
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x03, INSTANCE_ID, 0x00, 0x04, 0xf7),
        # KemperNRPNMessage(
        #     0x03, 
        #     0x00,
        #     0x04
        # ),
        type = ClientParameterMapping.PARAMETER_TYPE_STRING
    )

# Rig volume
def MAPPING_RIG_VOLUME(): 
    return ClientParameterMapping.get(
        name = "RigVol",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x04, 0x01, 0xf7),
        # KemperNRPNMessage(
        #     0x01, 
        #     0x04,
        #     0x01
        # ),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x04, 0x01, 0xf7),
        # KemperNRPNMessage(
        #     0x41,
        #     0x04,
        #     0x01
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x04, 0x01, 0xf7)
        # KemperNRPNMessage(
        #     0x01,
        #     0x04,
        #     0x01
        # )
    )

# Rig transpose
def MAPPING_RIG_TRANSPOSE(): 
    return ClientParameterMapping.get(
        name = "RigTrans",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x04, 0x04, 0xf7),
        # KemperNRPNMessage(
        #     0x01, 
        #     0x04,
        #     0x04
        # ),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x04, 0x04, 0xf7),
        # KemperNRPNMessage(
        #     0x41,
        #     0x04,
        #     0x04
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x04, 0x04, 0xf7)
        # KemperNRPNMessage(
        #     0x01,
        #     0x04,
        #     0x04
        # )
    )
