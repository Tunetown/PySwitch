from micropython import const

from ...misc import get_option, PeriodCounter
from ...colors import Colors, dim_color
from ...controller.callbacks import Callback
from ...controller.client import ClientParameterMapping

# Fractal Audio Axe-Fx II client (Axe-Fx II Mark I/II, XL, XL+), experimental. Protocol: "Fractal MIDI Spec Public"
# (Fractal Audio, 2014) and community hardware evidence, see claude/001 Fractal Support/spec/axe_fx_ii/protocol.md in
# the PySwitch repository. Values are polled; answers pushed by the device (preset, scene) are received while a request
# is pending, tuner and beat data whenever they arrive (I/O > MIDI > SEND REALTIME SYSEX on the device).

####################################################################################################################

# Device models (model byte of all SysEx messages). Set the model with the "fractalIIModel" option in config.py.
MODEL_AXE_FX_II = const(0x03)           # Axe-Fx II Mark I/II (384 presets)
MODEL_AXE_FX_II_XL = const(0x06)        # Axe-Fx II XL (768 presets)
MODEL_AXE_FX_II_XL_PLUS = const(0x07)   # Axe-Fx II XL+ (768 presets)

NUM_SCENES = const(8)

# Category colors of the footswitch functions (same as the Fractal client)
COLOR_BANK = Colors.ORANGE
COLOR_PRESET = Colors.GREEN
COLOR_SCENE = Colors.RED
COLOR_EFFECT = Colors.CYAN
COLOR_UTILITY = Colors.BLUE

####################################################################################################################

# Label options. Which ones are available depends on the action (same values as for the Fractal client).
class FractalIILabel:
    NAME = 0                   # Name of the target preset
    NUMBER = 1                 # Number of the target preset/scene/bank
    P_NUM = 2                  # Position of the target preset in the bank ("P1")
    BOTH_NUM = 3               # Toggle: both numbers, the current one in brackets
    BOTH_P_NUM = 4             # Toggle in bank: both positions, the current one in brackets
    DESTINATION_NAME = 5       # Name of the preset that will be loaded
    DESTINATION_NUM = 6        # Number of the preset/scene/bank that will be loaded
    CURRENT_NAME = 7           # Name of the current preset
    CURRENT_NUM = 8            # Number of the current preset/scene/bank
    ACTION = 9                 # Action and step size ("Preset +1")

    LONG_NAME = 20             # Block name and instance ("Drive 1")
    SHORT_NAME = 21            # Block abbreviation and instance ("DRV1")
    SHORT_NAME_CHANNEL = 22    # Abbreviation, instance and channel ("DRV1 Y")
    LONG_NAME_CHANNEL = 23     # Name, instance and channel ("Drive 1 Y")
    BOTH_CHANNELS = 24         # Channel toggle: both channels, the current one in brackets ("DRV1 [X]Y")
    DESTINATION_CHANNEL = 25   # Abbreviation, instance and the channel that will be selected
    CURRENT_CHANNEL = 26       # Abbreviation, instance and the current channel

    FUNCTION = 30              # Function name ("Tap Tempo")
    BPM = 31                   # Current tempo


# Preset Load option of the bank functions
class FractalIIPresetLoad:
    NONE = 0                   # Only select the bank, no preset is loaded
    FIRST = 1                  # Load the first preset of the new bank
    CURRENT = 2                # Load the preset at the same position in the new bank


# 2nd Press option of EFFECT_CHANNEL_SELECT
class FractalIISecondPress:
    SMART_BYPASS = 1           # Pressing the active channel engages/bypasses the block
    PREVIOUS_CHANNEL = 2       # Pressing the active channel selects the other channel


# Block channels (X/Y)
class FractalIIChannel:
    X = 0
    Y = 1

    NAMES = ("X", "Y")


####################################################################################################################


# Blocks (effect IDs of the Axe-Fx II)
class FractalIIBlock:
    COMPRESSOR_1 = 100
    COMPRESSOR_2 = 101
    GRAPHIC_EQ_1 = 102
    GRAPHIC_EQ_2 = 103
    PARAMETRIC_EQ_1 = 104
    PARAMETRIC_EQ_2 = 105
    AMP_1 = 106
    AMP_2 = 107
    CAB_1 = 108
    CAB_2 = 109
    REVERB_1 = 110
    REVERB_2 = 111
    DELAY_1 = 112
    DELAY_2 = 113
    MULTI_DELAY_1 = 114
    MULTI_DELAY_2 = 115
    CHORUS_1 = 116
    CHORUS_2 = 117
    FLANGER_1 = 118
    FLANGER_2 = 119
    ROTARY_1 = 120
    ROTARY_2 = 121
    PHASER_1 = 122
    PHASER_2 = 123
    WAH_1 = 124
    WAH_2 = 125
    FORMANT_1 = 126
    VOLUME_1 = 127
    TREMOLO_1 = 128
    TREMOLO_2 = 129
    PITCH_1 = 130
    FILTER_1 = 131
    FILTER_2 = 132
    DRIVE_1 = 133
    DRIVE_2 = 134
    ENHANCER_1 = 135
    FX_LOOP_1 = 136
    MIXER_1 = 137
    MIXER_2 = 138
    SYNTH_1 = 144
    SYNTH_2 = 145
    VOCODER_1 = 146
    MEGATAP_1 = 147
    CROSSOVER_1 = 148
    CROSSOVER_2 = 149
    GATE_1 = 150
    GATE_2 = 151
    RING_MOD_1 = 152
    PITCH_2 = 153
    MULTIBAND_COMP_1 = 154
    MULTIBAND_COMP_2 = 155
    QUAD_CHORUS_1 = 156
    QUAD_CHORUS_2 = 157
    RESONATOR_1 = 158
    RESONATOR_2 = 159
    GRAPHIC_EQ_3 = 160
    GRAPHIC_EQ_4 = 161
    PARAMETRIC_EQ_3 = 162
    PARAMETRIC_EQ_4 = 163
    FILTER_3 = 164
    FILTER_4 = 165
    VOLUME_2 = 166
    VOLUME_3 = 167
    VOLUME_4 = 168
    LOOPER_1 = 169
    TONE_MATCH_1 = 170

    # Returns the name of a block ("Drive 1", short: "DRV1"), or None for IDs which are no blocks listed above
    @staticmethod
    def name(block, short = False):
        if not isinstance(block, int) or block < 100 or block > 170:
            return None

        type = _BLOCK_TYPES[block - 100]
        if type == None:
            return None

        return f"{ _TYPE_SHORT[type] }{ _BLOCK_INSTANCES[block - 100] }" if short else f"{ _TYPE_LONG[type] } { _BLOCK_INSTANCES[block - 100] }"


# Block type and instance per effect ID (index: ID - 100). None: no switchable block (input, output, controllers, feedback send/return).
_BLOCK_TYPES = (
    0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,                 # 100..119
    10, 10, 11, 11, 12, 12, 13, 14, 15, 15, 16, 17, 17, 18, 18, 19, 20, 21, 21, # 120..138
    None, None, None, None, None,                                               # 139..143
    22, 22, 23, 24, 25, 25, 26, 26, 27, 16, 28, 28, 29, 29, 30, 30,             # 144..159
    1, 1, 2, 2, 17, 17, 14, 14, 14, 31, 32                                      # 160..170
)
_BLOCK_INSTANCES = (
    1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
    1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2,
    0, 0, 0, 0, 0,
    1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
    3, 4, 3, 4, 3, 4, 2, 3, 4, 1, 1
)

# Names and abbreviations of the block types (indexed by the types above)
_TYPE_LONG = (
    "Compressor", "Graphic EQ", "Param EQ", "Amp", "Cab", "Reverb", "Delay", "MultiDly", "Chorus", "Flanger",
    "Rotary", "Phaser", "Wah", "Formant", "Volume", "TremPan", "Pitch", "Filter", "Drive", "Enhancer",
    "FX Loop", "Mixer", "Synth", "Vocoder", "Megatap", "Crossover", "Gate", "Ring Mod", "MultiComp", "QuadChorus",
    "Resonator", "Looper", "Tone Match"
)
_TYPE_SHORT = (
    "CPR", "GEQ", "PEQ", "AMP", "CAB", "REV", "DLY", "MTD", "CHO", "FLG",
    "ROT", "PHA", "WAH", "FRM", "VOL", "TRM", "PIT", "FIL", "DRV", "ENH",
    "FXL", "MIX", "SYN", "VOC", "MGT", "XVR", "GTE", "RNG", "MBC", "QCH",
    "RES", "LPR", "TMA"
)


####################################################################################################################


# Client settings from config.py and state shared by all Axe-Fx II actions and callbacks.
# There is only one instance: FRACTAL_II.
class FractalIIState:

    def __init__(self):
        self.model = MODEL_AXE_FX_II_XL_PLUS
        self.bank_size = 5
        self.display_offset = 1

        self.selected_bank = None    # Bank selected by a bank function with preset load NONE (None: the bank of the current preset)

        self.__initialized = False
        self.__last_preset = None

    # Reads the settings from config.py (once). Mappings created before with another model byte are patched.
    def init(self, config):
        if self.__initialized:
            return

        self.__initialized = True

        self.bank_size = get_option(config, "fractalIIBankSize", 5)
        self.display_offset = get_option(config, "fractalIIPresetDisplayOffset", 1)

        model = get_option(config, "fractalIIModel", MODEL_AXE_FX_II_XL_PLUS)
        if model != self.model:
            self.model = model

            for m in ClientParameterMapping._mappings:
                if isinstance(m, FractalIIMapping):
                    m.set_model(model)

    # Number of presets of the model
    @property
    def num_presets(self):
        return 384 if self.model == MODEL_AXE_FX_II else 768

    # Number of banks (the last bank can be partial)
    @property
    def num_banks(self):
        return int((self.num_presets + self.bank_size - 1) / self.bank_size)

    # Returns the bank shown by the bank and preset functions (selected bank, or the one of the current preset)
    def current_bank(self, preset):
        if self.selected_bank != None:
            return self.selected_bank
        if preset == None:
            return None
        return int(preset / self.bank_size)

    # Must be called by callbacks with the current preset number. Resets preset dependent state on change.
    def track_preset(self, preset):
        if preset == self.__last_preset or preset == None:
            return

        self.__last_preset = preset
        self.selected_bank = None

    # Formats a preset number for display (3 digits, regarding the display offset)
    def preset_text(self, preset):
        ret = str(preset + self.display_offset)
        while len(ret) < 3:
            ret = "0" + ret
        return ret


FRACTAL_II = FractalIIState()


####################################################################################################################


# XOR checksum of the first "end" bytes of a message
def _checksum(msg, end):
    cs = 0
    for i in range(end):
        cs ^= msg[i]
    return cs & 0x7f

# Creates a SysEx message with checksum for the current model
def _sysex(function, data = ()):
    msg = [0xf0, 0x00, 0x01, 0x74, FRACTAL_II.model, function]
    msg.extend(data)
    msg.append(_checksum(msg, len(msg)))
    msg.append(0xf7)
    return msg

# Creates a response template (message start up to the value; the model byte is checked separately)
def _response(function, data = ()):
    msg = [0xf0, 0x00, 0x01, 0x74, 0x00, function]
    msg.extend(data)
    return msg

# Decodes a name (max. 32 characters) starting at index, cut at the first NUL and trimmed
def _decode_name(midi_message, index):
    end = min(index + 32, len(midi_message) - 2)
    ret = ""
    for i in range(index, end):
        c = midi_message[i]
        if c == 0:
            break
        ret += chr(c)
    return ret.strip()

# Decodes the block states answer: bytes with effect ID and state flags of each block (pairs). The answer has no
# checksum and 5 septets per block (32-bit word, LS first: effect ID << 24 | X/Y CC << 16 | bypass CC << 8 | flags).
def _decode_blocks(midi_message):
    num = int((len(midi_message) - 7) / 5)
    ret = bytearray(2 * num)

    for i in range(num):
        index = 6 + 5 * i
        ret[2 * i] = ((midi_message[index + 3] >> 3) & 0x0f) | ((midi_message[index + 4] & 0x0f) << 4)
        ret[2 * i + 1] = midi_message[index] & 0x03

    return bytes(ret)


####################################################################################################################


# Mapping for Axe-Fx II SysEx messages. Answers must have the model byte of the configured model; the response
# template is compared from the function byte on.
class FractalIIMapping(ClientParameterMapping):

    # Value types
    VALUE_7BIT = 0           # One byte after the template
    VALUE_PRESET = 1         # Preset number after the template (two bytes, MS first)
    VALUE_14BIT = 2          # 14-bit value after the template (two bytes, LS first)
    VALUE_STRING = 3         # Name at value_index
    VALUE_BLOCKS = 4         # Block states (see _decode_blocks)
    VALUE_NOTE = 5           # Tuner note (0 = C)
    VALUE_DEVIANCE = 6       # Tuner deviance (PySwitch scale: 8192 = in tune, +-8192 = +-50 cents)

    # Singleton factory
    @staticmethod
    def get(name,
            set = None,
            request = None,
            response = None,
            value_type = 0,
            value_index = None,     # Index of the value in the answer (default: end of the response template)
            length = 0,             # If set, only messages with exactly this length are parsed (push data without checksum)
            set_index = 0,          # Index of the value in the SysEx set message
            set_bytes = 1,          # 1: 7-bit value, 2: preset number (MS first)
            invert = False          # If set, values in range [0..1] are inverted when set (bypass)
        ):
        for m in ClientParameterMapping._mappings:
            if m.name == name:
                return m

        m = FractalIIMapping(
            name = name,
            create_key = ClientParameterMapping,
            set = set,
            request = request,
            response = response,
            value_type = value_type,
            value_index = value_index,
            length = length,
            set_index = set_index,
            set_bytes = set_bytes,
            invert = invert
        )

        ClientParameterMapping._mappings.append(m)
        return m

    def __init__(self, name, create_key, set = None, request = None, response = None, value_type = 0, value_index = None, length = 0, set_index = 0, set_bytes = 1, invert = False):
        super().__init__(
            name = name,
            create_key = create_key,
            set = set,
            request = request,
            response = response
        )

        self.value_type = value_type
        self._value_index = value_index if value_index != None else (len(response) if response else 0)
        self.__length = length
        self.__set_index = set_index
        self.__set_bytes = set_bytes
        self.__invert = invert
        self._skip = 0

    # Parse a message. If an answer has to be skipped (see feedback()), the value is kept.
    def parse(self, midi_message):
        value = self.parse_against(midi_message, self.response)
        if value == None:
            return False

        if self._skip > 0:
            self._skip -= 1
        else:
            self.value = value

        return True

    # Shows a value locally after it has been set. The next answer is skipped, as it can answer a request
    # sent before the set message.
    def feedback(self, value):
        self.value = value
        self._skip = 1

    def parse_against(self, midi_message, response):
        try:
            if midi_message[0] != 0xf0 or midi_message[4] != FRACTAL_II.model:
                return None

            if self.__length and len(midi_message) != self.__length:
                return None

            end = len(response)
            if bytes(midi_message[5:end]) != bytes(response[5:end]):
                return None

            return self._decode(midi_message)

        except (TypeError, IndexError):
            return None

    # Decodes the value of a matching message
    def _decode(self, midi_message):
        index = self._value_index
        value_type = self.value_type

        if value_type == self.VALUE_7BIT:
            return midi_message[index]

        if value_type == self.VALUE_PRESET:
            return 128 * midi_message[index] + midi_message[index + 1]

        if value_type == self.VALUE_14BIT:
            return midi_message[index] + 128 * midi_message[index + 1]

        if value_type == self.VALUE_STRING:
            return _decode_name(midi_message, index)

        if value_type == self.VALUE_BLOCKS:
            return _decode_blocks(midi_message)

        if value_type == self.VALUE_NOTE:
            # The device counts from A (0 = A, 1 = Bb, ...)
            return (midi_message[index] + 9) % 12

        # Deviance: cents in offset binary (63 = in tune) after note and string
        value = 8192 + int((midi_message[index + 2] - 63) * 8192 / 50)
        return max(0, min(value, 16383))

    # Set the value on the SysEx set message
    def set_value(self, value):
        msg = self.set
        index = self.__set_index

        if self.__invert:
            value = 1 - value

        if self.__set_bytes == 2:
            msg[index] = (value >> 7) & 0x7f
            msg[index + 1] = value & 0x7f
        else:
            msg[index] = value & 0x7f

        msg[-2] = _checksum(msg, len(msg) - 2)

    # Patches the model byte (and checksums) of the request and set messages
    def set_model(self, model):
        if self.request:
            req = bytearray(self.request)
            _patch_model(req, model)
            self.request = req

        if self.set and self.set[0] == 0xf0:
            _patch_model(self.set, model)

# Sets the model byte and recalculates the checksum of a SysEx message with checksum
def _patch_model(msg, model):
    msg[4] = model
    msg[-2] = _checksum(msg, len(msg) - 2)


####################################################################################################################


# Name of the current preset. Only requested after the preset has changed: callbacks using it call refresh()
# in update() instead of registering it.
class _FractalIIPresetNameMapping(FractalIIMapping):

    # Singleton factory
    @staticmethod
    def get(name, request, response, value_type):
        for m in ClientParameterMapping._mappings:
            if m.name == name:
                return m

        m = _FractalIIPresetNameMapping(
            name = name,
            create_key = ClientParameterMapping,
            request = request,
            response = response,
            value_type = value_type
        )

        ClientParameterMapping._mappings.append(m)
        return m

    def __init__(self, name, create_key, request, response, value_type):
        super().__init__(
            name = name,
            create_key = create_key,
            request = request,
            response = response,
            value_type = value_type
        )

        self.__preset = None

    # Requests the name if the preset has changed or the name is unknown. An answer to a request sent before
    # the preset changed is skipped.
    def refresh(self, client, listener, preset):
        pending = client.get_matching_request(self)

        if preset != self.__preset:
            self.__preset = preset
            self.value = None
            self._skip = 1 if pending else 0

        if preset != None and self.value == None and not pending:
            client.request(self, listener)


# Name of a preset chosen by an action (target), e.g. the preset a switch selects. One instance per action (no
# singleton): the target is changed with set_target(), which rewrites the request message in place. The answer
# contains the preset number, so only answers for the target are accepted.
class FractalIIPresetTargetNameMapping(FractalIIMapping):

    _count = 0

    def __init__(self):
        FractalIIPresetTargetNameMapping._count += 1

        super().__init__(
            name = f"Axe-Fx II Preset Target Name { FractalIIPresetTargetNameMapping._count }",
            create_key = ClientParameterMapping,
            request = _sysex(0x15, (0x00, 0x00)),
            response = _response(0x15),
            value_type = FractalIIMapping.VALUE_STRING,
            value_index = 8
        )

        self.request = bytearray(self.request)
        self.target = 0

        # Registered for model patching (see FractalIIState.init)
        ClientParameterMapping._mappings.append(self)

    # Sets the target preset. The name is requested again.
    def set_target(self, preset):
        if preset == self.target:
            return

        self.target = preset
        self.value = None

        req = self.request
        req[6] = (preset >> 7) & 0x7f
        req[7] = preset & 0x7f
        req[8] = _checksum(req, 8)

    def parse_against(self, midi_message, response):
        value = super().parse_against(midi_message, response)
        if value == None or 128 * midi_message[6] + midi_message[7] != self.target:
            return None

        return value


# Tuner state, derived from the tuner data pushed by the device: 1 while data arrives, 0 after a timeout or after
# switching the tuner off (late data is ignored for a short time then). Callbacks using it must call check(client)
# in update().
class _FractalIITunerStateMapping(FractalIIMapping):

    _TIMEOUT_MILLIS = 1500       # Tuner is regarded as off when no data arrives for this time
    _IGNORE_MILLIS = 500         # Data is ignored for this time after switching the tuner off

    # Singleton factory
    @staticmethod
    def get(name, response, length):
        for m in ClientParameterMapping._mappings:
            if m.name == name:
                return m

        m = _FractalIITunerStateMapping(
            name = name,
            create_key = ClientParameterMapping,
            response = response,
            length = length
        )

        ClientParameterMapping._mappings.append(m)
        return m

    def __init__(self, name, create_key, response, length):
        super().__init__(
            name = name,
            create_key = create_key,
            response = response,
            length = length
        )

        self.__period = PeriodCounter(self._TIMEOUT_MILLIS)
        self.__ignore = False

    # Returns True only when the state changes (data comes in continuously)
    def parse(self, midi_message):
        if self.parse_against(midi_message, self.response) == None:
            return False

        if self.__ignore:
            if self.__period.passed < self._IGNORE_MILLIS:
                return False
            self.__ignore = False

        self.__period.reset()

        if self.value == 1:
            return False

        self.value = 1
        return True

    # Switches the state off when no data arrived for the timeout
    def check(self, client):
        if self.value == 1 and self.__period.passed > self._TIMEOUT_MILLIS:
            self.__change(client, 0)

    # Local feedback after switching the tuner on/off
    def switched(self, client, on):
        self.__period.reset()
        self.__ignore = not on
        self.__change(client, 1 if on else 0)

    def __change(self, client, value):
        self.value = value

        req = client.get_matching_request(self)
        if req:
            req.notify_listeners()


####################################################################################################################


# Mappings used by the actions and callbacks
class FractalIIMappings:

    # Current preset number (0-based, also answers pushed by the device). Set: selects a preset (SysEx, independent
    # of the MIDI channel and the program change settings of the device).
    @staticmethod
    def PRESET():
        return FractalIIMapping.get(
            name = "Axe-Fx II Preset",
            request = _sysex(0x14),
            response = _response(0x14),
            value_type = FractalIIMapping.VALUE_PRESET,
            length = 10,
            set = _sysex(0x3c, (0x00, 0x00)),
            set_index = 6,
            set_bytes = 2
        )

    # Name of the current preset (see _FractalIIPresetNameMapping)
    @staticmethod
    def PRESET_NAME():
        return _FractalIIPresetNameMapping.get(
            name = "Axe-Fx II Preset Name",
            request = _sysex(0x0f),
            response = _response(0x0f),
            value_type = FractalIIMapping.VALUE_STRING
        )

    # Current scene (0-7)
    @staticmethod
    def SCENE():
        return FractalIIMapping.get(
            name = "Axe-Fx II Scene",
            request = _sysex(0x29, (0x7f,)),
            response = _response(0x29),
            length = 9,
            set = _sysex(0x29, (0x00,)),
            set_index = 6
        )

    # Block states of the current preset: bytes with effect ID and flags per block (bit 0: engaged, bit 1: X)
    @staticmethod
    def BLOCK_STATES():
        return FractalIIMapping.get(
            name = "Axe-Fx II Block States",
            request = _sysex(0x0e),
            response = _response(0x0e),
            value_type = FractalIIMapping.VALUE_BLOCKS
        )

    # Engage (1) or bypass (0) a block. The value is inverted for the device (0 = engaged).
    @staticmethod
    def BYPASS(block):
        return FractalIIMapping.get(
            name = f"Axe-Fx II Bypass { block }",
            set = _sysex(0x02, (block & 0x7f, (block >> 7) & 0x7f, 0x7f, 0x01, 0x00, 0x00, 0x00, 0x01)),
            set_index = 10,
            invert = True
        )

    # Select the channel of a block (0 = X, 1 = Y)
    @staticmethod
    def CHANNEL(block):
        return FractalIIMapping.get(
            name = f"Axe-Fx II Channel { block }",
            set = _sysex(0x11, (block & 0x7f, (block >> 7) & 0x7f, 0x00, 0x01)),
            set_index = 8
        )

    # Tuner state (1 while tuner data arrives)
    @staticmethod
    def TUNER_STATE():
        return _FractalIITunerStateMapping.get(
            name = "Axe-Fx II Tuner State",
            response = _response(0x0d),
            length = 10
        )

    # Tuner note (0-11, 0 = C)
    @staticmethod
    def TUNER_NOTE():
        return FractalIIMapping.get(
            name = "Axe-Fx II Tuner Note",
            response = _response(0x0d),
            value_type = FractalIIMapping.VALUE_NOTE,
            length = 10
        )

    # Tuner deviance (8192 = in tune)
    @staticmethod
    def TUNER_DEVIANCE():
        return FractalIIMapping.get(
            name = "Axe-Fx II Tuner Deviance",
            response = _response(0x0d),
            value_type = FractalIIMapping.VALUE_DEVIANCE,
            length = 10
        )

    # Tuner on (127) / off (0) via the tuner CC of the device (I/O > CTRL > Tuner, default 15)
    @staticmethod
    def TUNER_ON_OFF(cc, channel):
        return ClientParameterMapping.get(
            name = f"Axe-Fx II Tuner { cc } { channel }",
            set = [0xb0 + channel, cc, 0x00]
        )

    # Tap tempo via the tap tempo CC of the device (I/O > CTRL > Tap Tempo, default 14)
    @staticmethod
    def TAP_TEMPO(cc, channel):
        return ClientParameterMapping.get(
            name = f"Axe-Fx II Tap Tempo { cc } { channel }",
            set = [0xb0 + channel, cc, 0x00]
        )

    # Tempo in BPM
    @staticmethod
    def TEMPO_BPM():
        return FractalIIMapping.get(
            name = "Axe-Fx II Tempo BPM",
            request = _sysex(0x2f),
            response = _response(0x2f),
            value_type = FractalIIMapping.VALUE_14BIT,
            length = 10
        )

    # Tempo beat (data pushed by the device on every beat). The value counts the beats.
    @staticmethod
    def TEMPO_BEAT():
        return _FractalIITempoBeatMapping.get(
            name = "Axe-Fx II Tempo Beat",
            response = _response(0x10),
            length = 7
        )


# Counts the beats (value in range [0..127])
class _FractalIITempoBeatMapping(FractalIIMapping):

    # Singleton factory
    @staticmethod
    def get(name, response, length):
        for m in ClientParameterMapping._mappings:
            if m.name == name:
                return m

        m = _FractalIITempoBeatMapping(
            name = name,
            create_key = ClientParameterMapping,
            response = response,
            length = length
        )

        ClientParameterMapping._mappings.append(m)
        return m

    def _decode(self, midi_message):
        return ((self.value if self.value != None else 0) + 1) & 0x7f


####################################################################################################################


# Steps a value like the FC Inc/Dec functions: step size, wrap, lower and upper limit
def _inc_dec(value, step, wrap, lower, upper):
    value += step

    if value > upper:
        return lower if wrap else upper

    if value < lower:
        return upper if wrap else lower

    return value

# Label text for toggle functions: both entries, the active one in brackets ("[A] B", "A [B]" or "A/B")
def _both(primary, secondary, primary_active, secondary_active):
    if primary_active:
        return f"[{ primary }] { secondary }"
    if secondary_active:
        return f"{ primary } [{ secondary }]"
    return f"{ primary }/{ secondary }"

# Label text for Inc/Dec functions ("Preset +1")
def _action_text(prefix, step):
    return f"{ prefix } +{ step }" if step > 0 else f"{ prefix } { step }"


####################################################################################################################


# Base class for the callbacks of the Axe-Fx II actions: LED states (off/dim/bright) like the FC controllers.
class FractalIICallback(Callback):

    # LED states
    OFF = 0
    DIM = 1
    BRIGHT = 2

    def __init__(self, color, text, mappings = []):
        super().__init__(mappings = mappings)

        self._color = color
        self._text = text

    def init(self, appl, listener = None):
        super().init(appl, listener)

        self._appl = appl
        FRACTAL_II.init(appl.config)

        config = appl.config
        self.__brightness = (
            0,
            get_option(config, "ledBrightnessOff", 0.02),
            get_option(config, "ledBrightnessOn", 0.3)
        )
        self.__dim_off = get_option(config, "displayDimFactorOff", 0.2)
        self.__dim_on = get_option(config, "displayDimFactorOn", 1)

    def reset(self):
        if self.action.enabled:
            self.update_displays()

    def push(self):
        pass

    def release(self):
        pass

    # Shows an LED state, the color and the label text (custom text overrides it)
    def _show(self, led, color, text):
        action = self.action

        action.switch_color = color
        action.switch_brightness = self.__brightness[led]

        if action.label:
            action.label.back_color = dim_color(color, self.__dim_on if led == self.BRIGHT else self.__dim_off)
            action.label.text = self._text if self._text != None else text
