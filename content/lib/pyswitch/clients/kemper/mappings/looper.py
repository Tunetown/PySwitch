from .. import PRODUCT_TYPE, DEVICE_ID_OMNI, INSTANCE_ID
from ....controller.client import ClientParameterMapping

def MAPPING_LOOPER_REC_PLAY_OVERDUB():
    return ClientParameterMapping.get(
        name = "LoopRec",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, 88, 0x00, 0x00, 0xf7),
    )

def MAPPING_LOOPER_STOP():
    return ClientParameterMapping.get(
        name = "LoopStop",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, 89, 0x00, 0x00, 0xf7),
    )

def MAPPING_LOOPER_TRIGGER():
    return ClientParameterMapping.get(
        name = "LoopTrig",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, 90, 0x00, 0x00, 0xf7),
    )

def MAPPING_LOOPER_REVERSE():
    return ClientParameterMapping.get(
        name = "LoopRev",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, 91, 0x00, 0x00, 0xf7),
    )

def MAPPING_LOOPER_HALF_SPEED():
    return ClientParameterMapping.get(
        name = "Loop1/2",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, 92, 0x00, 0x00, 0xf7),
    )

def MAPPING_LOOPER_CANCEL():
    return ClientParameterMapping.get(
        name = "LoopCanc",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, 93, 0x00, 0x00, 0xf7),
    )

def MAPPING_LOOPER_ERASE():
    return ClientParameterMapping.get(
        name = "LoopErase",
        set = (0xf0, 0x00, 0x20, 0x33, PRODUCT_TYPE, DEVICE_ID_OMNI, 0x01, INSTANCE_ID, 0x7d, 94, 0x00, 0x00, 0xf7),
    )