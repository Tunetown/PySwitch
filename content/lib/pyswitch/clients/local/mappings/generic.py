from ....controller.client import ClientParameterMapping

# Send a simple PC message
def MAPPING_SEND_PROGRAM_CHANGE(channel = 0): 
    return ClientParameterMapping.get(
        name = "ProgChg",
        set = (192 + channel, 0)
        # ProgramChange(
        #     0    # Dummy value, will be overridden
        # )
    )