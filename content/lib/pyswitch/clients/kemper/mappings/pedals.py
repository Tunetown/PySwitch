from ....controller.client import ClientParameterMapping

def MAPPING_WAH_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = "Wah",
        set = (176 + channel, 1, 0)
        # ControlChange(
        #     1, 
        #     0
        # )
    )

def MAPPING_VOLUME_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = "Vol",
        set = (176 + channel, 7, 0)
        # ControlChange(
        #     7, 
        #     0
        # )
    )

def MAPPING_PITCH_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = "Pitch",
        set = (176 + channel, 4, 0)
        # ControlChange(
        #     4, 
        #     0
        # )
    )

def MAPPING_DELAY_MIX_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = "DlMix",
        set = (176 + channel, 68, 0)
        # ControlChange(
        #     68, 
        #     0
        # )
    )

def MAPPING_DELAY_FEEDBACK_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = "Feed",
        set = (176 + channel, 69, 0)
        # ControlChange(
        #     69, 
        #     0
        # )
    )

def MAPPING_REVERB_MIX_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = "RvMix",
        set = (176 + channel, 70, 0)
        # ControlChange(
        #     70, 
        #     0
        # )
    )

def MAPPING_REVERB_TIME_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = "RvTime",
        set = (176 + channel, 71, 0)
        # ControlChange(
        #     71, 
        #     0
        # )
    )

def MAPPING_VOLUME_OUTPUT_PEDAL(channel = 0): 
    return ClientParameterMapping.get(
        name = "OutVol",
        set = (176 + channel, 73, 0)
        # ControlChange(
        #     73, 
        #     0
        # )
    )
