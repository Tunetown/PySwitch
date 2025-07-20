#from pyswitch.clients.kemper.actions.effect_button import EFFECT_BUTTON
# ^^^ Not enough memory to add these
from pyswitch.clients.kemper.actions.looper import LOOPER_REC_PLAY_OVERDUB, LOOPER_CANCEL, LOOPER_STOP
from pyswitch.clients.kemper.actions.morph import MORPH_BUTTON
from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO
from pyswitch.clients.kemper.actions.bank_up_down import BANK_UP, BANK_DOWN
from pyswitch.clients.kemper.actions.rig_up_down import RIG_UP, RIG_DOWN
from pyswitch.clients.kemper.actions.tuner import TUNER_MODE
from pyswitch.clients.local.actions.binary_switch import BINARY_SWITCH
from pyswitch.clients.local.actions.pager import PagerAction
from pyswitch.clients.local.actions.param_change import PARAMETER_UP_DOWN
from pyswitch.colors import Colors
from pyswitch.clients.kemper import KemperEffectSlot
from pyswitch.clients.kemper.mappings.freeze import MAPPING_FREEZE_ALL_GLOBAL
from pyswitch.clients.kemper.mappings.system import MAPPING_SPACE_INTENSITY, MAPPING_LOOPER_VOLUME
from display import HEADER_1, HEADER_2, HEADER_3, HEADER_4, FOOTER_1, FOOTER_2, FOOTER_3, FOOTER_4, DISP_PAGE, RIG_NAME
from pyswitch.controller.actions import PushButtonAction
from pyswitch.controller.callbacks import BinaryParameterCallback
from pyswitch.controller.client import ClientParameterMapping
from pyswitch.hardware.devices.pa_midicaptain_nano_4 import *

## -----------------------------------------
from pyswitch.clients.kemper.actions.effect_state import KemperEffectEnableCallback

# '''
# What it does:
#   - Model: Nano 4 Footswitch
#   - Layout and Footswitch presses
#      - Header:
#        - 4 Slots: Header_1. Header_2, Header_3, Header_4
#        - The outermost ones (Header_1 and Header_4) are controlled by the closest footswitch on a press (1 and 2)*
#        - The innermost ones (Header_2 and Header_3) are controlled by the closest footswitch on a hold (1 and 2)
#      - Rig ID (Bank-Preset) number - Always displayed
#      - Footer:
#        - 4 Slots: Footer_1. Footer_2, Footer_3, Footer_4
#        - The outermost ones (Footer_1 and Footer_4) are controlled by the closest footswitch press (A and B)*
#        - The innermost ones (Footer_2 and Footer_3) are controlled by the closest footswitch hold action (A and B)
#        - Footer_4 and Footswitch B will change to the next page on a Press.  This is indicated by '>>'.
#      * Note: If there is not an action on the innermost slot (e.g., Footer 2), the outermost slot can have a hold action
#   - Pages
#     - Effect
#       - Status of enhanced effect blocks
#       - Footswitches:
#         - See "Layout and Footswitch presses" section above for general approach
#         - Press (or hold) to  toggle state on/off of the corresponding slot
#         - Note:
#           - Press Action on Footswitch B is next page ('>>').  This is standard for all pages.
#           - Footer_4 displays Reverb Effect status and color only.  There is no action to toggle state.
#     - Looper:
#        - Footswitch A:
#          - Press: Start/Record/Overdub
#          - Hold: Stop
#        - Footswitch B: Undo/Redo
#        - Footswitch 1: Loooper Volume decrease
#        - Footswitch 2: Looper Volume increase
#     - Rig:
#        - Footswitch A: Next Rig
#        - Footswitch B:
#          - Press: Next Page ('>>')
#          - Hold: Prev Rig
#        - Footswitch 1: Bank Up
#        - Footswitch 2: Bank Down
#     - Util:
#        - Footswitch A: Freeze
#        - Footswitch B:
#          - Press: Next Page ('>>')
#          - Hold: Tuner
#        - Footswitch 1: Morph
#        - Footswitch 2:
#           - Press: Tap Temp
#           - Hold: Toggle Headphone Space Intensity between 33% and 0%
#     - Effect Buttons: Display and toggle status of FX I through FX IIII
#        NOTE: This is **Disabled** due to limited memory
#        - Footswitch A: FX III on/off
#        - Footswitch B:
#          - Press: Next Page ('>>')
#          - Hold: FX IIII on/off
#        - Footswitch 1: FX I
#        - Footswitch 2: FX II
# '''

# Patch all the names so they fit in a label
_MAX_LENGTH = 5
def _trim_str_vowels_first_rightmost(s: str):
    # Removes characters from the right of a string until it reaches _MAX_LENGTH.
    # Prioritizes removing vowels first, then any other character from the right side.

    if len(s) <= _MAX_LENGTH:
        return s

    vowels = "aeiouAEIOU"
    temp_list = list(s)

    i = len(temp_list) - 1
    while i >= 0 and len(temp_list) > _MAX_LENGTH:
        if temp_list[i] in vowels:
            temp_list.pop(i)
        i -= 1

    while len(temp_list) > _MAX_LENGTH:
        temp_list.pop()

    return "".join(temp_list)

KemperEffectEnableCallback.CATEGORY_NAMES = tuple(map(_trim_str_vowels_first_rightmost, KemperEffectEnableCallback.CATEGORY_NAMES))

# Switch an effect slot on / off. This variant has a few extra category names for effects that are truly a new category.
#
# <b>Use with care:</b> This takes some extra RAM memory, so if you run a large configuration you might run into memory allocation failures. In this case, just use the normal Effect State action instead.
def EFFECT_STATE_ENHANCED(slot_id,
                          display = None,
                          mode = PushButtonAction.HOLD_MOMENTARY,
                          show_slot_names = False,
                          id : int = False,
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
            extended_type_names = _EFFECT_TYPE_NAMES
        ),
        "mode": mode,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback,
    })


_TREMOLO = _trim_str_vowels_first_rightmost("Tremolo")
_WIDE = _trim_str_vowels_first_rightmost("Wide")
_EFFECT_TYPE_NAMES = {
    # 0: "Empty",
    # 1: "Wah",
    # 2: "LP",
    # 3: "HP",
    # 4: "Vowel",
    # 6: "Wah Ph",
    # 7: "Wah Fl",
    # 8: "Wah RR",
    # 9: "Ring",
    # 10: "FShift",
    # 11: "Pitch",
    # 12: "Wah Form",
    # 13: "VinylStp",
    #
    # 17: "Bit Shp",
    # 18: "Octa Shp",
    # 19: "Soft Shp",
    # 20: "Hard Shp",
    # 21: "Wave Shp",
    # 32: "KDrive",
    # 33: "Green",
    # 34: "Plus DS",
    # 35: "One DS",
    # 36: "Muff",
    # 37: "Mouse",
    # 38: "KFuzz",
    # 39: "Metal DS",
    # 42: "Full OC",

    # 49: "Comp",
    50: _trim_str_vowels_first_rightmost("Swell"),
    # 57: "Gate 2:1",
    # 58: "Gate 4:1",
    # 64: "Space",

    # 65: "VChorus",
    # 66: "HChorus",
    # 67: "Air Ch.",
    68: _trim_str_vowels_first_rightmost("Vibrato"),
    69: _trim_str_vowels_first_rightmost("Rotary"),
    70: _TREMOLO,
    #71: "MPitch",

    # 81: "Phaser",
    # 82: "Vibe",
    # 83: "Ph 1way",
    # 89: "Flanger",
    # 90: "Fl 1way",

    # 97: "Graphic",
    # 98: "StudioEQ",
    # 99: "MetalEQ",
    100: _trim_str_vowels_first_rightmost("Acoustic"),
    101: _WIDE,
    102: _WIDE,
    103: _WIDE,
    # 102: "WidePh",
    # 103: "WideDLY",
    104: _trim_str_vowels_first_rightmost("Double"),

    # 113: "Treble",
    # 114: "Lead",
    # 115: "Boost",
    # 116: "WahBoost",

    # 121: "Loop",  # Mono
    # 122: "Loop",  # Stereo
    # 123: "LoopDist",
    #
    # 129: "Transp",
    # 130: "ChromPtch",
    # 131: "HarmPtch",
    # 132: "Octave",
    #
    # 137: "DualChrom",
    # 138: "DualHarm",
    # 139: "DualCryst",
    # 140: "DualLoop",
    #
    # 145: "LDelay",    # Legacy Delay
    # 146: "SDelay",    # Single
    # 147: "DualDly",
    # 148: "2TpDelay",
    # 149: "S2TDelay",
    # 150: "Crystal",
    # 151: "LoopPitch",
    # 152: "FShiftDly",
    # 161: "RhDelay",
    # 162: "MeloChr",
    # 163: "MeloHarm",
    # 164: "QuadDly",
    # 165: "QuadChrm",
    # 166: "QuadHarm",
    #
    # 177: "LReverb",
    # 178: "NatRev",
    # 179: "EasyRev",
    # 180: "Echo",
    # 181: "Cirrus",
    # 182: "FormRev",
    # 183: "Sphere",
    # 193: "Spring",

    # Undocumented:
    75: _TREMOLO,
    76: _TREMOLO,
    # 77: "Pulse",
    # 78: "Saw",
    # 79: "PulsePan",
    # 80: "SawPan"
}

## -----------------------------------------
class _Static_Text_Callback(BinaryParameterCallback):
    def __init__(self, color, text, text_disabled = None):
        super().__init__(
            mapping = ClientParameterMapping.get("stText"),
            comparison_mode = BinaryParameterCallback.NO_STATE_CHANGE,
            text = text,
            text_disabled = text_disabled if text_disabled else text,
            color = color
        )

    def init(self, appl, listener = None):
        super().init(appl, listener)
        self.__appl = appl

def _STATIC_TEXT(display = None,
                 id:int = False,
                 text = " ",
                 text_disabled = None,
                 color = Colors.BLACK,
                 enable_callback = None,
                 ):
    return PushButtonAction({
        "callback": _Static_Text_Callback(text=text, text_disabled=text_disabled, color=color),
        "mode": PushButtonAction.NO_STATE_CHANGE,
        "display": display,
        "id": id,
        "useSwitchLeds": False,
        "enableCallback": enable_callback,
    })

## -----------------------------------------

_pager = PagerAction(
    pages = [
        {
            "id": 1,
            "color": Colors.RED,
            "text": "Effect ",
        },
        {
            "id": 2,
            "color": Colors.GREEN,
            "text": "Looper",
        },
        {
            "id": 3,
            "color": Colors.BLUE,
            "text": "Rig",
        },
        {
            "id": 4,
            "color": Colors.YELLOW,
            "text": 'Util',
        },
        # Not enough memory to run this
        # {
        #     "id": 5,
        #     "color": Colors.ORANGE,
        #     "text": 'FX',
        # }
    ],
    use_leds = False,
    display = DISP_PAGE
)

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_STATE_ENHANCED(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A,
                display = HEADER_1,
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            # LOOPER_STOP(
            #     display = HEADER_1,
            #     use_leds = False,
            #     text = 'Stop',
            #     color = Colors.LIGHT_GREEN,
            #     id = 2,
            #     enable_callback = _pager.enable_callback
            # ),
            PARAMETER_UP_DOWN(
                mapping = MAPPING_LOOPER_VOLUME(),
                offset = -512,
                display = HEADER_1,
                change_display = RIG_NAME,
                text = 'Loop\nVol-',
                use_leds=False,
                id=2,
                enable_callback= _pager.enable_callback
            ),
            BANK_UP(
                display = HEADER_1,
                use_leds = False,
                id = 3,
                text = '^^',
                color = Colors.BLUE,
                enable_callback = _pager.enable_callback
            ),
            MORPH_BUTTON(
                display = HEADER_1,
                text = 'Morph',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            # Not enough memory to run this
            # EFFECT_BUTTON(
            #     display = HEADER_1,
            #     num = 1,
            #     id=5,
            #     enable_callback = _pager.enable_callback
            # )
        ],
        "actionsHold": [
            EFFECT_STATE_ENHANCED(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_B,
                display = HEADER_2,
                use_leds = False,
                id = 1,
                enable_callback = _pager.enable_callback
            ),

            _STATIC_TEXT(
                display=HEADER_2,
                id=2,
                enable_callback = _pager.enable_callback,
            ),
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_2,
        "actions": [
            EFFECT_STATE_ENHANCED(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_D,
                display = HEADER_4,
                use_leds = False,
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            # LOOPER_ERASE(
            #     color = Colors.RED,
            #     id = 2,
            #     display = HEADER_4,
            #     enable_callback = _pager.enable_callback,
            #     use_leds = False
            # ),
            PARAMETER_UP_DOWN(
                mapping = MAPPING_LOOPER_VOLUME(),
                offset = 512,
                display = HEADER_4,
                change_display = RIG_NAME,
                text = 'Loop\nVol+',
                use_leds=False,
                id=2,
                enable_callback= _pager.enable_callback
            ),
            BANK_DOWN(
                id = 3,
                display = HEADER_4,
                color = Colors.BLUE,
                use_leds = False,
                text = 'vv',
                enable_callback = _pager.enable_callback
            ),
            TAP_TEMPO(
                display = HEADER_4,
                use_leds = True,
                color=Colors.TURQUOISE,
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            # Not enough memory to run this
            # EFFECT_BUTTON(
            #     display = HEADER_4,
            #     num = 2,
            #     id=5,
            #     enable_callback = _pager.enable_callback
            # )
        ],
        "actionsHold": [
            EFFECT_STATE_ENHANCED(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_C,
                display = HEADER_3,
                use_leds = False,
                id = 1,
                enable_callback = _pager.enable_callback
            ),

            _STATIC_TEXT(
                display=HEADER_3,
                id=2,
                enable_callback = _pager.enable_callback),

            BINARY_SWITCH(
                mapping = MAPPING_SPACE_INTENSITY(),
                mode = PushButtonAction.LATCH,
                display = HEADER_3,
                use_leds = False,
                text = 'Head\nSpace',
                color = Colors.LIGHT_BLUE,
                id = 4,
                enable_callback = _pager.enable_callback,
                value_on = int(2**14/3 + 0.5),
                value_off = 0,
                reference_value = int(2**14/3 + 0.5)
            ),
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_A,
        "actions": [
            EFFECT_STATE_ENHANCED(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_X,
                display = FOOTER_1,
                use_leds = False,
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            LOOPER_REC_PLAY_OVERDUB(
                display = FOOTER_1,
                text = 'Rec',
                color = Colors.LIGHT_GREEN,
                id = 2,
                enable_callback = _pager.enable_callback
            ),

            # _STATIC_TEXT(text = "\n^", display=FOOTER_1, id=3, enable_callback = _pager.enable_callback),
            RIG_UP(
                display = FOOTER_1,
                #color = Colors.BLUE,
                id = 3,
                enable_callback = _pager.enable_callback,
                keep_bank = False,
                use_leds = False,
                #text_callback= lambda action, bank, rig: "\n^",
                text = "\n^"
            ),
            BINARY_SWITCH(
                mapping = MAPPING_FREEZE_ALL_GLOBAL(),
                display = FOOTER_1,
                text = 'Freeze',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            # Not enough memory to run this
            # EFFECT_BUTTON(
            #     display = FOOTER_1,
            #     num=3,
            #     id=5,
            #     enable_callback = _pager.enable_callback
            # )
        ],
        "actionsHold": [
            EFFECT_STATE_ENHANCED(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_MOD,
                display = FOOTER_2,
                use_leds = False,
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            LOOPER_STOP(
                display = FOOTER_2,
                text = 'Stop',
                color = Colors.RED,
                use_leds= False,
                id = 2,
                enable_callback = _pager.enable_callback
            ),

            _STATIC_TEXT(
                display=FOOTER_2,
                id=3,
                enable_callback = _pager.enable_callback
            ),
        ],
    },
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_B,
        "actions": [
            _pager,
            EFFECT_STATE_ENHANCED(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_REV,
                display = FOOTER_4,
                use_leds = False,
                id = 1,
                text = '>>\nRev',
                enable_callback = _pager.enable_callback,
                mode=PushButtonAction.NO_STATE_CHANGE
            ),
            _STATIC_TEXT(
                text = ">>",
                display=FOOTER_4,
                id=2,
                enable_callback = _pager.enable_callback
            ),
        ],
        "actionsHold": [
            EFFECT_STATE_ENHANCED(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_DLY,
                display = FOOTER_3,
                use_leds = False,
                id = 1,
                enable_callback = _pager.enable_callback
            ),
            _STATIC_TEXT(display=FOOTER_3,
                         id=2,
                         enable_callback = _pager.enable_callback
            ),
            RIG_DOWN(
                display = FOOTER_3,
                keep_bank = False,
                use_leds = False,
                id = 3,
                #color = Colors.TURQUOISE,
                text = 'v',
                #text_callback= lambda action, bank, rig: "v",
                enable_callback = _pager.enable_callback
            ),
            _STATIC_TEXT(
                display=FOOTER_3,
                id=4,
                enable_callback = _pager.enable_callback
            ),

            LOOPER_CANCEL(
                display = FOOTER_3,
                text = 'Undo',
                color = Colors.LIGHT_GREEN,
                id = 2,
                enable_callback = _pager.enable_callback
            ),

            TUNER_MODE(
                display = FOOTER_3,
                text = 'Tuner',
                id = 4,
                enable_callback = _pager.enable_callback
            ),
            # Not enough memory to run this
            # EFFECT_BUTTON(
            #     display = FOOTER_3,
            #     num=4,
            #     text="FX IV",
            #     id=5,
            #     enable_callback = _pager.enable_callback
            # ),
        ],
    },
]
