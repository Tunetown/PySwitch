from micropython import const
from ....controller.actions import PushButtonAction
from ....controller.callbacks.effect_enable import EffectEnableCallback
from ...kemper import KemperMappings, KemperEffectSlot
from ....colors import Colors, DEFAULT_LABEL_COLOR

# Switch an effect slot on / off
def EFFECT_STATE(slot_id,
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
            show_slot_names = show_slot_names
        ),
        "mode": mode,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback,
    })


# Used for effect enable/disable ParameterAction
class KemperEffectEnableCallback(EffectEnableCallback):

    # Effect category enums (used internally, also for indexing colors/names,
    # so these MUST always be a consecutive sequence from 0 to n)
    #
    # Colors match the official Kemper Profiler Main Manual LED color scheme:
    #   Wah=Orange, Distortion/Booster/Shaper=Red, Compressor/Gate=Cyan,
    #   Chorus/Vibrato/Rotary/Tremolo/Slicer=Blue, Phaser/Flanger=Purple,
    #   EQ=Yellow, Pitch=White, Pitch Shifter Delay (Dual)=Light Green,
    #   Delay/Reverb/Space=Green, Looper=Pink
    CATEGORY_WAH            = const(1)
    CATEGORY_DISTORTION     = const(2)   # Distortion + Booster + Shaper all = Red
    CATEGORY_COMPRESSOR     = const(3)
    CATEGORY_NOISE_GATE     = const(4)
    CATEGORY_SPACE          = const(5)
    CATEGORY_CHORUS         = const(6)
    CATEGORY_PHASER_FLANGER = const(7)
    CATEGORY_EQUALIZER      = const(8)
    CATEGORY_BOOSTER        = const(9)
    CATEGORY_LOOPER         = const(10)
    CATEGORY_PITCH          = const(11)
    CATEGORY_DUAL           = const(12)  # Pitch Shifter Delays = Light Green
    CATEGORY_DELAY          = const(13)
    CATEGORY_REVERB         = const(14)
    CATEGORY_TREMOLO        = const(15)  # Tube Bias/Photocell/Harmonic Tremolo — Blue (same as Chorus)
    CATEGORY_ROTARY         = const(16)  # Rotary Speaker — Blue (same as Chorus)
    CATEGORY_VIBRATO        = const(17)  # Vibrato — Blue (same as Chorus)
    CATEGORY_SLICER         = const(18)  # Pulse/Saw Slicer, Autopanner — Blue (same as Chorus)

    # Effect colors. The order MUST match the category enums defined above (index 0 = CATEGORY_NONE).
    # Source: KEMPER PROFILER Main Manual (official LED color designations per effect category)
    CATEGORY_COLORS = (
        DEFAULT_LABEL_COLOR,    # 0  None/Empty
        Colors.ORANGE,          # 1  Wah               — Orange
        Colors.RED,             # 2  Distortion        — Red
        Colors.CYAN,            # 3  Compressor        — Cyan
        Colors.CYAN,            # 4  Noise Gate        — Cyan
        Colors.GREEN,           # 5  Space             — Green
        Colors.BLUE,            # 6  Chorus            — Blue
        Colors.PURPLE,          # 7  Phaser / Flanger  — Purple
        Colors.YELLOW,          # 8  EQ                — Yellow
        Colors.RED,             # 9  Booster           — Red  (same family as Distortion)
        Colors.PINK,            # 10 Looper            — Pink
        Colors.WHITE,           # 11 Pitch             — White
        Colors.LIGHT_GREEN,     # 12 Dual (Pitch Delay)— Light Green
        Colors.GREEN,           # 13 Delay             — Green
        Colors.GREEN,           # 14 Reverb            — Green
        Colors.BLUE,            # 15 Tremolo           — Blue (Kemper groups with Chorus stomps)
        Colors.BLUE,            # 16 Rotary            — Blue (Kemper groups with Chorus stomps)
        Colors.BLUE,            # 17 Vibrato           — Blue (Kemper groups with Chorus stomps)
        Colors.BLUE,            # 18 Slicer/Autopanner — Blue (Kemper groups with Chorus stomps)
    )

    # Effect type display names. The order MUST match the category enums defined above.
    CATEGORY_NAMES = (
        "-",        # 0  None/Empty
        "Wah",      # 1
        "Dist",     # 2
        "Comp",     # 3
        "Gate",     # 4
        "Space",    # 5
        "Chorus",   # 6
        "Phaser",   # 7
        "EQ",       # 8
        "Boost",    # 9
        "Looper",   # 10
        "Pitch",    # 11
        "Dual",     # 12
        "Delay",    # 13
        "Reverb",   # 14
        "Tremolo",  # 15
        "Rotary",   # 16
        "Vibrato",  # 17
        "Slicer",   # 18
    )

    def __init__(self,
                 slot_id,
                 text = None,
                 color = None,
                 show_slot_names = False,
                 extended_type_names = False
                 ):
        super().__init__(
            mapping_state = KemperMappings.EFFECT_STATE(slot_id),
            mapping_type = KemperMappings.EFFECT_TYPE(slot_id)
        )
        self.__text = text
        self.__color = color
        self.__slot_name = KemperEffectSlot.EFFECT_SLOT_NAME[slot_id] if show_slot_names else None
        self.__extended_type_names = extended_type_names


    # Must return the effect category for a mapping value.
    #
    # Effect type values are decoded from Kemper's 14-bit NRPN representation:
    #   decoded_value = (MSB * 128) + LSB
    #
    # Reference: Kemper MIDI Specification (Appendix B), firmware v12+
    # Types below 128 have MSB=0, types 128+ have MSB=1 (add 128 to LSB).
    #
    # Ranges with no defined effects (gaps in the spec) fall through to
    # CATEGORY_NONE so unexpected firmware values don't get misidentified.
    def get_effect_category(self, kpp_effect_type):

        # --- Empty slot ---
        if kpp_effect_type == 0:
            return self.CATEGORY_NONE

        # --- Wah family (MSB=0): 1-10, 12, 13 ---
        # 1=Wah, 2=Low Pass, 3=High Pass, 4=Vowel Filter, 6=Wah Phaser,
        # 7=Wah Flanger, 8=Rate Reducer, 9=Ring Mod, 10=Freq Shifter,
        # 12=Formant Shift, 13=Pedal Vinyl Stop
        elif (1 <= kpp_effect_type <= 10) or kpp_effect_type in (12, 13):
            return self.CATEGORY_WAH

        # --- Pitch Pedal (MSB=0): 11 ---
        elif kpp_effect_type == 11:
            return self.CATEGORY_PITCH

        # --- Distortion / Shaper (MSB=0): 17-42 ---
        # 17=Bit Shaper, 18=Octa Shaper, 19=Soft Shaper, 20=Hard Shaper,
        # 21=Wave Shaper, 32=Kemper Drive, 33=Green Scream, 34=Plus DS,
        # 35=One DS, 36=Muffin, 37=Mouse, 38=Kemper Fuzz, 39=Metal DS, 42=Full OC
        elif 17 <= kpp_effect_type <= 42:
            return self.CATEGORY_DISTORTION

        # --- Dynamics / Compressor (MSB=0): 49-50 ---
        # 49=Compressor, 50=Auto Swell
        elif 49 <= kpp_effect_type <= 50:
            return self.CATEGORY_COMPRESSOR

        # --- Noise Gate (MSB=0): 57-58 ---
        # 57=Gate 2:1, 58=Gate 4:1
        elif 57 <= kpp_effect_type <= 58:
            return self.CATEGORY_NOISE_GATE

        # --- Space (MSB=0): 64 ---
        # 64=Space
        elif kpp_effect_type == 64:
            return self.CATEGORY_SPACE

        # --- Chorus (MSB=0): 65-67, 71 ---
        # 65=Vintage Chorus, 66=Hyper Chorus, 67=Air Chorus, 71=Micro Pitch
        elif kpp_effect_type in (65, 66, 67, 71):
            return self.CATEGORY_CHORUS

        # --- Vibrato (MSB=0): 68 ---
        # 68=Vibrato
        elif kpp_effect_type == 68:
            return self.CATEGORY_VIBRATO

        # --- Rotary (MSB=0): 69 ---
        # 69=Rotary Speaker
        elif kpp_effect_type == 69:
            return self.CATEGORY_ROTARY

        # --- Tremolo (MSB=0): 70, 75, 76 ---
        # 70=Tube Bias Tremolo, 75=Photocell Tremolo, 76=Harmonic Tremolo
        elif kpp_effect_type in (70, 75, 76):
            return self.CATEGORY_TREMOLO

        # --- Slicer / Autopanner (MSB=0): 77-80 ---
        # 77=Pulse Slicer, 78=Saw Slicer, 79=Pulse Autopanner, 80=Saw Autopanner
        elif 77 <= kpp_effect_type <= 80:
            return self.CATEGORY_SLICER

        # --- Phaser / Flanger (MSB=0): 81-91 ---
        # 81=Phaser, 82=Phaser Vibe, 83=Phaser Oneway, 89=Flanger, 91=Flanger Oneway
        elif 81 <= kpp_effect_type <= 91:
            return self.CATEGORY_PHASER_FLANGER

        # --- EQ / Widener (MSB=0): 97-104 ---
        # 97=Graphic EQ, 98=Studio EQ, 99=Metal EQ, 100=Acoustic Sim,
        # 101=Stereo Widener, 102=Phase Widener, 103=Delay Widener, 104=Double Tracker
        elif 97 <= kpp_effect_type <= 104:
            return self.CATEGORY_EQUALIZER

        # --- Booster (MSB=0): 113-116 ---
        # 113=Treble Booster, 114=Lead Booster, 115=Pure Booster, 116=Wah Pedal Booster
        elif 113 <= kpp_effect_type <= 116:
            return self.CATEGORY_BOOSTER

        # --- Looper (MSB=0): 121-123 ---
        # 121=Loop Mono, 122=Loop Stereo, 123=Loop Distortion
        elif 121 <= kpp_effect_type <= 123:
            return self.CATEGORY_LOOPER

        # --- Pitch / Harmony (MSB=1, decoded 129-132) ---
        # 129=Transpose, 130=Chromatic Pitch, 131=Harmonic Pitch, 132=Analog Octaver
        elif 129 <= kpp_effect_type <= 132:
            return self.CATEGORY_PITCH

        # --- Dual / Pitch+Delay hybrids (MSB=1, decoded 138-140) ---
        # 138=Dual Harmonic, 139=Dual Crystal, 140=Dual Loop Pitch
        elif 138 <= kpp_effect_type <= 140:
            return self.CATEGORY_DUAL

        # --- Delay (MSB=1, decoded 145-166) ---
        # 145=Legacy Delay, 146=Single Delay, 147=Dual Delay, 148=Two Tap Delay,
        # 149=Serial TwoTap, 150=Crystal Delay, 151=Loop Pitch Delay,
        # 152=Freq Shifter Delay, 161=Rhythm Delay, 162=Melody Chromatic,
        # 163=Melody Harmonic, 164=Quad Delay, 165=Quad Chromatic, 166=Quad Harmonic
        elif 145 <= kpp_effect_type <= 166:
            return self.CATEGORY_DELAY

        # --- Reverb (MSB=1, decoded 177-193) ---
        # 177=Legacy Reverb, 178=Natural Reverb, 179=Easy Reverb, 180=Echo Reverb,
        # 181=Cirrus Reverb, 182=Formant Reverb, 183=Ionosphere Reverb, 193=Spring Reverb
        elif 177 <= kpp_effect_type <= 193:
            return self.CATEGORY_REVERB

        # --- Unknown / undefined type number ---
        else:
            return self.CATEGORY_NONE


    # Must return the color for a category
    def get_effect_category_color(self, category, kpp_effect_type):
        if self.__color:
            return self.__color

        return self.CATEGORY_COLORS[category]


    # Must return the text to show for a category
    def get_effect_category_text(self, category, kpp_effect_type):
        if self.__text:
            return self.__text

        if self.__extended_type_names:
            if kpp_effect_type in self.__extended_type_names:
                name = self.__extended_type_names[kpp_effect_type]
            else:
                name = self.CATEGORY_NAMES[category]
        else:
            name = self.CATEGORY_NAMES[category]

        if self.__slot_name:
            return self.__slot_name + " " + name

        return name