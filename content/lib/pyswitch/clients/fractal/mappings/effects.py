from .. import FractalParameterMapping, _sysex

# Engage (1) or bypass (0) a block. The value is inverted for the device (0 = engaged).
def MAPPING_BLOCK_BYPASS(effect_id):
    return FractalParameterMapping.get(
        name = f"Block Bypass { effect_id }",
        set = _sysex(0x0a, (effect_id & 0x7f, (effect_id >> 7) & 0x7f, 0x00)),
        invert = True
    )

# Select the channel (0-5) of a block
def MAPPING_BLOCK_CHANNEL(effect_id):
    return FractalParameterMapping.get(
        name = f"Block Channel { effect_id }",
        set = _sysex(0x0b, (effect_id & 0x7f, (effect_id >> 7) & 0x7f, 0x00))
    )
