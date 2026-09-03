from ....controller.client import ClientParameterMapping

# Send a simple PC message
def MAPPING_SEND_PROGRAM_CHANGE(channel = 0): 
    return ClientParameterMapping.get(
        name = f"PC ({channel})",
        set = (192 + channel, 0)
    )