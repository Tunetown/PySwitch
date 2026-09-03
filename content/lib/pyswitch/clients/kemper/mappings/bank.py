from ....controller.client import ClientTwoPartParameterMapping


def MAPPING_NEXT_BANK(channel = 0): 
    return ClientTwoPartParameterMapping.get(
        name = f"Next Bank ({channel})",
        set = (176 + channel, 48, 0),
        response = [
            (176 + channel, 32, 0),
            (192 + channel, 0)
        ]
    )

def MAPPING_PREVIOUS_BANK(channel = 0):
    return ClientTwoPartParameterMapping.get(
        name = f"Prev Bank ({channel})",
        set = (176 + channel, 49, 0),
        response = [
            (176 + channel, 32, 0),
            (192 + channel, 0)
        ]
    )