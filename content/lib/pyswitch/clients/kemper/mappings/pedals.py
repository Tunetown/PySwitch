from ....controller.client import ClientParameterMapping

def MAPPING_WAH_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"Wah ({channel})",
        set = (176 + channel, 1, 0)
    )

def MAPPING_VOLUME_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"Vol ({channel})",
        set = (176 + channel, 7, 0)
    )

def MAPPING_PITCH_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"Pitch ({channel})",
        set = (176 + channel, 4, 0)
    )

def MAPPING_DELAY_MIX_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"DlMix ({channel})",
        set = (176 + channel, 68, 0)
    )

def MAPPING_DELAY_FEEDBACK_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"Feed ({channel})",
        set = (176 + channel, 69, 0)
    )

def MAPPING_REVERB_MIX_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"RvMix ({channel})",
        set = (176 + channel, 70, 0)
    )

def MAPPING_REVERB_TIME_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"RvTime ({channel})",
        set = (176 + channel, 71, 0)
    )

def MAPPING_VOLUME_OUTPUT_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = f"OutVol ({channel})",
        set = (176 + channel, 73, 0)
    )
