from ....controller.client import ClientTwoPartParameterMapping


def MAPPING_NEXT_BANK(channel = 0): 
    return ClientTwoPartParameterMapping.get(
        name = "Next Bank",
        set = (176 + channel, 48, 0),
        # ControlChange(
        #     _CC_BANK_INCREASE,
        #     0    # Dummy value, will be overridden
        # ),
        response = [
            (176 + channel, 32, 0),
            (192 + channel, 0)
            # ControlChange(
            #     _CC_RIG_INDEX_PART_1,
            #     0    # Dummy value, will be ignored
            # ),
            # ProgramChange(
            #     0    # Dummy value, will be ignored
            # )
        ]
    )

def MAPPING_PREVIOUS_BANK(channel = 0):
    return ClientTwoPartParameterMapping.get(
        name = "Prev Bank",
        set = (176 + channel, 49, 0),
        # ControlChange(
        #     _CC_BANK_DECREASE,
        #     0    # Dummy value, will be overridden
        # ),
        response = [
            (176 + channel, 32, 0),
            (192 + channel, 0)
            # ControlChange(
            #     _CC_RIG_INDEX_PART_1,
            #     0    # Dummy value, will be ignored
            # ),
            # ProgramChange(
            #     0    # Dummy value, will be ignored
            # )
        ]
    )