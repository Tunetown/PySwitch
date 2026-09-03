from ....controller.client import ClientTwoPartParameterMapping

# Selects a rig of the current bank. Rig index must be in range [0..4]
def MAPPING_RIG_SELECT(rig, channel = 0):
    return ClientTwoPartParameterMapping.get(
        f"Select Rig { str(rig + 1) } ({channel})",
        set = (176 + channel, 50 + rig, 1),
        response = [
            (176 + channel, 32, 0),
            (192 + channel, 0)
        ]
    )

# Pre-selects a bank.
def MAPPING_BANK_SELECT(channel = 0):
    return ClientTwoPartParameterMapping.get(
        name = f"Select Bank ({channel})",
        set = (176 + channel, 47, 0),
        response = [
            (176 + channel, 32, 0),
            (192 + channel, 0)
        ]
    )
