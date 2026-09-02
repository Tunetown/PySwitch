from .. import PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping

# Fixed FX: Transpose on/off
def MAPPING_FIXED_TRANSPOSE():
    return _MAPPING_FIXED("TranspSt", 1)

# Fixed FX: Gate on/off
def MAPPING_FIXED_GATE():
    return _MAPPING_FIXED("FixGateSt", 6)

# Fixed FX: Compressor on/off
def MAPPING_FIXED_COMP():
    return _MAPPING_FIXED("FixCompSt", 11)

# Fixed FX: Boost on/off
def MAPPING_FIXED_BOOST():
    return _MAPPING_FIXED("FixBoost", 16)

# Fixed FX: Wah on/off
def MAPPING_FIXED_WAH():
    return _MAPPING_FIXED("FixWah", 21)

# Fixed FX: Vintage Chorus on/off
def MAPPING_FIXED_CHORUS():
    return _MAPPING_FIXED("FixChor", 26)

# Fixed FX: Air Chorus on/off
def MAPPING_FIXED_AIR():
    return _MAPPING_FIXED("FixAir", 36)

# Fixed FX: Double Tracker on/off
def MAPPING_FIXED_DBL_TRACKER():
    return _MAPPING_FIXED("FixTracker", 41)


################################################################

# Common definition shared by all fixed fx mappings
def _MAPPING_FIXED(name, param):
    return ClientParameterMapping.get(
        name = name,
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x05, param, 0xf7),
        # KemperNRPNMessage(
        #     0x01, 
        #     _NRPN_ADDRESS_PAGE_FIXED,
        #     param
        # ),
        request = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x41, INSTANCE_ID, 0x05, param, 0xf7),
        # KemperNRPNMessage(               
        #     0x41, 
        #     _NRPN_ADDRESS_PAGE_FIXED,
        #     param
        # ),
        response = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x05, param, 0xf7)
        # KemperNRPNMessage(               
        #     0x01, 
        #     _NRPN_ADDRESS_PAGE_FIXED,
        #     param
        # )
    )
