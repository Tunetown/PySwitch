from .. import KemperMappings, PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping

# Amp name (request only)
def MAPPING_AMP_NAME(): 
    return ClientParameterMapping.get(
        depends = KemperMappings.RIG_DATE(),
        name = "Amp Name",
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x43, INSTANCE_ID, 0x00, 0x10, 0xf7),
        #   KemperNRPNMessage(               
        #     0x43, 
        #     0x00,
        #     0x10
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x03, INSTANCE_ID, 0x00, 0x10, 0xf7),
        # KemperNRPNMessage(
        #     0x03, 
        #     0x00,
        #     0x10
        # ),
        type = ClientParameterMapping.PARAMETER_TYPE_STRING
    )

# Amp on/off
def MAPPING_AMP_STATE(): 
    return ClientParameterMapping.get(
        name = "Amp State",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x0a, 0x02, 0xf7),
        # KemperNRPNMessage(
        #     0x01, 
        #     0x0a,
        #     0x02
        # ),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x0a, 0x02, 0xf7),
        # KemperNRPNMessage(
        #     0x41,
        #     0x0a,
        #     0x02
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x0a, 0x02, 0xf7)
        # KemperNRPNMessage(
        #     0x01,
        #     0x0a,
        #     0x02
        # )
    )

# Amp gain
def MAPPING_AMP_GAIN(): 
    return ClientParameterMapping.get(
        name = "Gain",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x0a, 0x04, 0xf7),
        # KemperNRPNMessage(
        #     0x01, 
        #     0x0a,
        #     0x04
        # ),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x0a, 0x04, 0xf7),
        # KemperNRPNMessage(
        #     0x41,
        #     0x0a,
        #     0x04
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x0a, 0x04, 0xf7)
        # KemperNRPNMessage(
        #     0x01,
        #     0x0a,
        #     0x04
        # )
    )
