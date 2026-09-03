from ....controller.actions import PushButtonAction
from .effect_state import KemperEffectEnableCallback

# Switch an effect slot on / off. This variant has distinct names for each effect type. 
# 
# <b>Use with care:</b> This takes quite some RAM memory, so if you run a large configuration you might run into memory allocation failures. In this case, just use the normal Effect State action instead.
def EFFECT_STATE_EXT(slot_id, 
                     midi_channel = 1,                               # MIDI Channel in range [1..16]
                     display = None, 
                     mode = PushButtonAction.HOLD_MOMENTARY,
                     show_slot_names = False,
                     id = False,
                     text = None,
                     color = None,
                     use_leds = True, 
                     enable_callback = None
    ):
    return PushButtonAction({
        "callback": KemperEffectEnableCallback(
            slot_id = slot_id,
            text = text,
            color = color,
            show_slot_names = show_slot_names,
            extended_type_names = _EFFECT_TYPE_NAMES,
            channel = midi_channel - 1
        ),
        "mode": mode,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback,
    })


_EFFECT_TYPE_NAMES = {
    0: "Empty",
    1: "Wah",
    2: "LP",
    3: "HP",
    4: "Vowel",
    6: "Wah Ph",  
    7: "Wah Fl",
    8: "Wah RR",
    9: "Ring",
    10: "FShift",
    11: "Pitch",
    12: "Wah Form",
    13: "VinylStp",
    
    17: "Bit Shp",
    18: "Octa Shp",
    19: "Soft Shp",
    20: "Hard Shp",
    21: "Wave Shp",
    32: "KDrive",
    33: "Green",
    34: "Plus DS",
    35: "One DS",
    36: "Muff",
    37: "Mouse",
    38: "KFuzz",
    39: "Metal DS",
    42: "Full OC",

    49: "Comp",
    50: "Swell",
    57: "Gate 2:1",
    58: "Gate 4:1",
    64: "Space",
    
    65: "VChorus",
    66: "HChorus",
    67: "Air Ch.",
    68: "Vibrato",
    69: "Rotary",
    70: "Tremolo",
    71: "MPitch",

    81: "Phaser",
    82: "Vibe",
    83: "Ph 1way",
    89: "Flanger",
    90: "Fl 1way",
 
    97: "Graphic",
    98: "StudioEQ",
    99: "MetalEQ",
    100: "Acoustic",
    101: "Wide",
    102: "WidePh",
    103: "WideDLY",
    104: "Double",

    113: "Treble",
    114: "Lead",
    115: "Boost",
    116: "WahBoost",

    121: "Loop",  # Mono
    122: "Loop",  # Stereo
    123: "LoopDist",

    129: "Transp",
    130: "ChromPtch",
    131: "HarmPtch",
    132: "Octave",

    137: "DualChrom",
    138: "DualHarm",
    139: "DualCryst",
    140: "DualLoop",

    145: "LDelay",    # Legacy Delay
    146: "SDelay",    # Single
    147: "DualDly",
    148: "2TpDelay",
    149: "S2TDelay",
    150: "Crystal",
    151: "LoopPitch",
    152: "FShiftDly",
    161: "RhDelay",
    162: "MeloChr",
    163: "MeloHarm",
    164: "QuadDly",
    165: "QuadChrm",
    166: "QuadHarm",
    
    177: "LReverb",
    178: "NatRev",
    179: "EasyRev",
    180: "Echo",
    181: "Cirrus",
    182: "FormRev",
    183: "Sphere",
    193: "Spring",

    # Undocumented:
    75: "Tremolo",
    76: "HarmTrem",
    77: "Pulse",
    78: "Saw",
    79: "PulsePan",
    80: "SawPan"
}
