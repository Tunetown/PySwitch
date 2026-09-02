from ....controller.client import ClientTwoPartParameterMapping

# Selects a rig of the current bank. Rig index must be in range [0..4]
def MAPPING_RIG_SELECT(rig, channel = 0):
    return ClientTwoPartParameterMapping.get(
        f"Select Rig { str(rig + 1) }",
        set = (176 + channel, 50 + rig, 1),
        # ControlChange(
        #     50 + rig,
        #     1    # Dummy value, will be overridden
        # ),

        response = [
            (176 + channel, 32, 0),
            (192 + channel, 0)
            # ControlChange(
            #     32,
            #     0    # Dummy value, will be ignored
            # ),
            # ProgramChange(
            #     0    # Dummy value, will be ignored
            # )
        ]
    )

# Pre-selects a bank.
def MAPPING_BANK_SELECT(channel = 0):
    return ClientTwoPartParameterMapping.get(
        name = "Select Bank",
        set = (176 + channel, 47, 0),
        # ControlChange(
        #     47,
        #     0    # Dummy value, will be overridden
        # ),

        response = [
            (176 + channel, 32, 0),
            (192 + channel, 0)
            # ControlChange(
            #     32,
            #     0    # Dummy value, will be ignored
            # ),
            # ProgramChange(
            #     0    # Dummy value, will be ignored
            # )
        ]
    )
