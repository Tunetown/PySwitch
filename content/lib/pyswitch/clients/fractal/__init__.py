from micropython import const

from ...misc import get_option, PeriodCounter
from ...colors import Colors, dim_color
from ...controller.callbacks import Callback
from ...controller.client import ClientParameterMapping
from ...ui.elements import TunerDisplay

# Fractal Audio client (Axe-Fx III, FM9, FM3). Protocol: 3rd-party SysEx, see claude/001 Fractal Support/FRACTAL.md in the
# PySwitch repository. There is no bidirectional protocol: all values are polled.

####################################################################################################################

# Device models (model byte of all SysEx messages). Set the model with the "fractalModel" option in config.py.
MODEL_AXE_FX_III = const(0x10)
MODEL_FM3 = const(0x11)
MODEL_FM9 = const(0x12)

NUM_SCENES = const(8)

# Category colors of the FC footswitch functions
COLOR_BANK = Colors.ORANGE
COLOR_PRESET = Colors.GREEN
COLOR_SCENE = Colors.RED
COLOR_EFFECT = Colors.CYAN
COLOR_UTILITY = Colors.BLUE

# Block ID of the Looper block
LOOPER_BLOCK_ID = const(166)

####################################################################################################################

# Label options (FC "Mini-Display Label"). Which ones are available depends on the action.
class FractalLabel:
    NAME = const(0)                   # Name of the target preset/scene
    NUMBER = const(1)                 # Number of the target preset/scene/bank
    P_NUM = const(2)                  # Position of the target preset in the bank ("P1")
    BOTH_NUM = const(3)               # Toggle: both numbers, the current one in brackets
    BOTH_P_NUM = const(4)             # Toggle in bank: both positions, the current one in brackets
    DESTINATION_NAME = const(5)       # Name of the preset/scene that will be loaded
    DESTINATION_NUM = const(6)        # Number of the preset/scene/bank that will be loaded
    CURRENT_NAME = const(7)           # Name of the current preset/scene
    CURRENT_NUM = const(8)            # Number of the current preset/scene/bank
    ACTION = const(9)                 # Action and step size ("Preset +1")

    LONG_NAME = const(20)             # Block name and instance ("Drive 1")
    SHORT_NAME = const(21)            # Block abbreviation and instance ("DRV1")
    SHORT_NAME_CHANNEL = const(22)    # Abbreviation, instance and channel ("DRV1 B")
    LONG_NAME_CHANNEL = const(23)     # Name, instance and channel ("Drive 1 B")
    BOTH_CHANNELS = const(24)         # Channel toggle: both channels, the current one in brackets ("DRV1 [A]B")
    DESTINATION_CHANNEL = const(25)   # Abbreviation, instance and the channel that will be selected
    CURRENT_CHANNEL = const(26)       # Abbreviation, instance and the current channel

    FUNCTION = const(30)              # Function name ("Tuner", "Tap Tempo")
    BPM = const(31)                   # Current tempo


# Preset Load option of the bank functions
class FractalPresetLoad:
    NONE = const(0)                   # Only select the bank, no preset is loaded
    FIRST = const(1)                  # Load the first preset of the new bank
    CURRENT = const(2)                # Load the preset at the same position in the new bank


# 2nd Press option of EFFECT_CHANNEL_SELECT
class FractalSecondPress:
    SMART_BYPASS = const(1)           # Pressing the active channel engages/bypasses the block
    PREVIOUS_CHANNEL = const(2)       # Pressing the active channel selects the previous channel


# Block channels
class FractalChannel:
    A = const(0)
    B = const(1)
    C = const(2)
    D = const(3)
    E = const(4)                      # Multiplexer only
    F = const(5)                      # Multiplexer only

    NAMES = ("A", "B", "C", "D", "E", "F")


####################################################################################################################


# Block types. Regular blocks are numbered in the order of the effect ID enum (4 IDs per type, starting at 46),
# special blocks follow. Names and abbreviations are indexed by the type.
class FractalBlock:
    COMPRESSOR = const(0)
    GRAPHIC_EQ = const(1)
    PARAMETRIC_EQ = const(2)
    AMP = const(3)
    CAB = const(4)
    REVERB = const(5)
    DELAY = const(6)
    MULTI_DELAY = const(7)
    CHORUS = const(8)
    FLANGER = const(9)
    ROTARY = const(10)
    PHASER = const(11)
    WAH = const(12)
    FORMANT = const(13)
    VOLUME = const(14)
    TREMOLO = const(15)
    PITCH = const(16)
    FILTER = const(17)
    DRIVE = const(18)
    ENHANCER = const(19)
    MIXER = const(20)
    SYNTH = const(21)
    VOCODER = const(22)
    MEGATAP = const(23)
    CROSSOVER = const(24)
    GATE = const(25)
    RING_MOD = const(26)
    MULTIBAND_COMP = const(27)
    TEN_TAP_DELAY = const(28)
    RESONATOR = const(29)
    LOOPER = const(30)
    TONE_MATCH = const(31)
    RTA = const(32)
    PLEX_DELAY = const(33)
    SEND = const(34)
    RETURN = const(35)

    INPUT = const(36)
    OUTPUT = const(37)
    MULTIPLEXER = const(38)
    IR_PLAYER = const(39)

    # Long names (max. 10 characters). Order must match the types above!
    NAMES = (
        "Compressor", "Graphic EQ", "Param EQ", "Amp", "Cab", "Reverb", "Delay", "MultiDly", "Chorus", "Flanger",
        "Rotary", "Phaser", "Wah", "Formant", "Volume", "TremPan", "Pitch", "Filter", "Drive", "Enhancer",
        "Mixer", "Synth", "Vocoder", "Megatap", "Crossover", "Gate", "Ring Mod", "MultiComp", "TenTap", "Resonator",
        "Looper", "Tone Match", "RTA", "Plex Delay", "Send", "Return",
        "Input", "Output", "Mux", "IR Player"
    )

    # 3-letter abbreviations (device grid labels). Order must match the types above!
    ABBREVIATIONS = (
        "CMP", "GEQ", "PEQ", "AMP", "CAB", "REV", "DLY", "MTD", "CHO", "FLG",
        "ROT", "PHA", "WAH", "FRM", "VOL", "TRM", "PIT", "FIL", "DRV", "ENH",
        "MIX", "SYN", "VOC", "MGT", "XVR", "GTE", "RNG", "MBC", "TTD", "RES",
        "LPR", "TMA", "RTA", "PLX", "SND", "RTN",
        "IN", "OUT", "MUX", "IRP"
    )

    # First effect IDs of the special blocks (INPUT, OUTPUT, MULTIPLEXER, IR_PLAYER)
    SPECIAL_IDS = (37, 42, 191, 195)

    # Returns the effect ID for a block type and instance (1-based)
    @staticmethod
    def effect_id(block, instance):
        if block < FractalBlock.INPUT:
            return 46 + 4 * block + instance - 1
        return FractalBlock.SPECIAL_IDS[block - FractalBlock.INPUT] + instance - 1


####################################################################################################################


# Client settings from config.py and state shared by all Fractal actions and callbacks.
# There is only one instance: FRACTAL.
class FractalState:

    def __init__(self):
        self.model = MODEL_FM3
        self.bank_size = 5
        self.display_offset = 0

        self.selected_bank = None    # Bank selected by a bank function with preset load NONE (None: the bank of the current preset)
        self.pending_names = []      # Preset numbers with a pending target name query
        self.target_answer = None    # The last preset answer identified as answer to a target name query
        self.scene_names = []        # All scene name mappings (invalidated on preset change)

        self.__initialized = False
        self.__last_preset = None

    # Reads the settings from config.py (once). Mappings created before with another model byte are patched.
    def init(self, config):
        if self.__initialized:
            return

        self.__initialized = True

        self.bank_size = get_option(config, "fractalBankSize", 5)
        self.display_offset = get_option(config, "fractalPresetDisplayOffset", 0)

        model = get_option(config, "fractalModel", MODEL_FM3)
        if model != self.model:
            self.model = model

            for m in ClientParameterMapping._mappings:
                if isinstance(m, FractalParameterMapping):
                    m.set_model(model)

    # Number of presets of the model
    @property
    def num_presets(self):
        return 1024 if self.model == MODEL_AXE_FX_III else 512

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

        for m in self.scene_names:
            m.value = None

    # Returns if a preset answer (0D) for the passed number answers a target name query. All mappings receiving
    # preset answers call this, so the first one consumes the pending entry and the others recognize the message.
    def is_target_answer(self, midi_message, preset):
        if midi_message is self.target_answer:
            return True

        if preset in self.pending_names:
            self.pending_names.remove(preset)
            self.target_answer = midi_message
            return True

        return False

    # Formats a preset number for display (3 digits, regarding the display offset)
    def preset_text(self, preset):
        ret = str(preset + self.display_offset)
        while len(ret) < 3:
            ret = "0" + ret
        return ret


FRACTAL = FractalState()


####################################################################################################################


# XOR checksum of the first "end" bytes of a message
def _checksum(msg, end):
    cs = 0
    for i in range(end):
        cs ^= msg[i]
    return cs & 0x7f

# Creates a SysEx message with checksum for the current model
def _sysex(function, data = ()):
    msg = [0xf0, 0x00, 0x01, 0x74, FRACTAL.model, function]
    msg.extend(data)
    msg.append(_checksum(msg, len(msg)))
    msg.append(0xf7)
    return msg

# Creates a response template (message start up to the value)
def _response(function, data = ()):
    msg = [0xf0, 0x00, 0x01, 0x74, FRACTAL.model, function]
    msg.extend(data)
    return msg


####################################################################################################################


# Mapping for Fractal SysEx messages. Compares the response template from the function byte on (manufacturer ID
# and model byte are ignored) and decodes the value starting at value_index (default: end of the template).
class FractalParameterMapping(ClientParameterMapping):

    # Value types
    VALUE_7BIT = const(0)
    VALUE_14BIT = const(1)          # Two 7-bit bytes, LS first
    VALUE_STRING = const(2)         # 32 characters, cut at the first NUL and trimmed
    VALUE_RAW = const(3)            # Payload up to the checksum as bytes

    # Singleton factory
    @classmethod
    def get(cls,
            name,
            set = None,
            request = None,
            response = None,
            value_type = 0,
            value_index = None,     # Index of the value in the response (default: end of the response template)
            length = 0,             # If set, only messages with exactly this length are parsed (push data without checksum)
            set_bytes = 1,          # Number of value bytes at the end of a SysEx set message (0 = fixed message)
            invert = False          # If set, values in range [0..1] are inverted when set (bypass)
        ):
        for m in ClientParameterMapping._mappings:
            if m.name == name:
                return m

        m = cls(
            name = name,
            create_key = ClientParameterMapping,
            set = set,
            request = request,
            response = response,
            value_type = value_type,
            value_index = value_index,
            length = length,
            set_bytes = set_bytes,
            invert = invert
        )

        ClientParameterMapping._mappings.append(m)
        return m

    def __init__(self, name, create_key, set = None, request = None, response = None, value_type = 0, value_index = None, length = 0, set_bytes = 1, invert = False):
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
        self.__set_bytes = set_bytes
        self.__invert = invert
        self.__skip = 0

    # Parse a message. If an answer has to be skipped (see feedback()), the value is kept.
    def parse(self, midi_message):
        value = self.parse_against(midi_message, self.response)
        if value == None:
            return False

        if self.__skip > 0:
            self.__skip -= 1
        else:
            self.value = value

        return True

    # Shows a value locally after it has been set. The next answer is skipped, as it can answer a request
    # sent before the set message.
    def feedback(self, value):
        self.value = value
        self.__skip = 1

    def parse_against(self, midi_message, response):
        try:
            if midi_message[0] != 0xf0:
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

        elif value_type == self.VALUE_14BIT:
            return midi_message[index] + 128 * midi_message[index + 1]

        elif value_type == self.VALUE_STRING:
            return _decode_name(midi_message, index)

        return bytes(midi_message[index:-2])

    # Set the value on the set message(s)
    def set_value(self, value):
        msg = self.set

        if not isinstance(msg[0], int):
            # CC0 + PC (preset select): Bank and program
            msg[0][2] = int(value / 128) & 0x7f
            msg[1][1] = value % 128
            return

        if msg[0] != 0xf0:
            super().set_value(value)
            return

        if self.__set_bytes == 0:
            return

        if self.__invert:
            value = 1 - value

        if self.__set_bytes == 2:
            msg[-4] = value & 0x7f
            msg[-3] = (value >> 7) & 0x7f
        else:
            msg[-3] = value & 0x7f

        msg[-2] = _checksum(msg, len(msg) - 2)

    # Patches the model byte (and checksums) of the request and set messages
    def set_model(self, model):
        if self.request:
            req = bytearray(self.request)
            _patch_model(req, model)
            self.request = req

        if self.set and isinstance(self.set[0], int) and self.set[0] == 0xf0:
            _patch_model(self.set, model)

# Sets the model byte and recalculates the checksum of a SysEx message with checksum
def _patch_model(msg, model):
    msg[4] = model
    msg[-2] = _checksum(msg, len(msg) - 2)

# Decodes a name (32 characters) starting at index
def _decode_name(midi_message, index):
    end = min(index + 32, len(midi_message) - 2)
    ret = ""
    for i in range(index, end):
        c = midi_message[i]
        if c == 0:
            break
        ret += chr(c)
    return ret.strip()


####################################################################################################################


# Current preset (request/response): ignores answers to target name queries
class _FractalPresetMapping(FractalParameterMapping):
    def parse_against(self, midi_message, response):
        value = super().parse_against(midi_message, response)
        if value == None:
            return None

        if FRACTAL.is_target_answer(midi_message, midi_message[6] + 128 * midi_message[7]):
            return None

        return value


# Tuner state, derived from the tuner push data: 1 while data arrives, 0 after a timeout or after switching
# the tuner off (late push data is ignored for a short time then). Callbacks using it must call check(client)
# in update().
class _FractalTunerStateMapping(FractalParameterMapping):

    _TIMEOUT_MILLIS = const(1500)       # Tuner is regarded as off when no push data arrives for this time
    _IGNORE_MILLIS = const(500)         # Push data is ignored for this time after switching the tuner off

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__period = PeriodCounter(self._TIMEOUT_MILLIS)
        self.__ignore = False

    # Returns True only when the state changes (push data comes in continuously)
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

    # Switches the state off when no push data arrived for the timeout
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


# Tuner deviance: converts the cents (offset binary, 63 = in tune) to the PySwitch scale (8192 = in tune,
# +-8192 = +-50 cents)
class _FractalTunerDevianceMapping(FractalParameterMapping):
    def _decode(self, midi_message):
        value = 8192 + int((midi_message[8] - 63) * 8192 / 50)
        return max(0, min(value, 16383))


####################################################################################################################


# Mappings used by several actions and callbacks. More specific mappings are in the mappings folder.
class FractalMappings:

    # Current preset number (0-based). The answer also contains the preset name (PRESET_NAME).
    @staticmethod
    def PRESET():
        return _FractalPresetMapping.get(
            name = "Preset",
            request = _sysex(0x0d, (0x7f, 0x7f)),
            response = _response(0x0d),
            value_type = FractalParameterMapping.VALUE_14BIT
        )

    # Name of the current preset (receives the answers to PRESET)
    @staticmethod
    def PRESET_NAME():
        return _FractalPresetMapping.get(
            name = "Preset Name",
            response = _response(0x0d),
            value_type = FractalParameterMapping.VALUE_STRING,
            value_index = 8
        )

    # Selects a preset via CC0 (bank) + PC. Value: preset number (0-based)
    @staticmethod
    def PRESET_SELECT(channel = 0):
        return FractalParameterMapping.get(
            name = f"Preset Select ({ channel })",
            set = [
                (0xb0 + channel, 0x00, 0x00),
                (0xc0 + channel, 0x00)
            ]
        )

    # Current scene (0-7)
    @staticmethod
    def SCENE():
        return FractalParameterMapping.get(
            name = "Scene",
            set = _sysex(0x0c, (0x00,)),
            request = _sysex(0x0c, (0x7f,)),
            response = _response(0x0c)
        )

    # Name of a scene (0-7) of the current preset
    @staticmethod
    def SCENE_NAME(scene):
        name = f"Scene Name { scene }"
        for m in FRACTAL.scene_names:
            if m.name == name:
                return m

        m = FractalParameterMapping.get(
            name = name,
            request = _sysex(0x0e, (scene,)),
            response = _response(0x0e, (scene,)),
            value_type = FractalParameterMapping.VALUE_STRING
        )

        FRACTAL.scene_names.append(m)
        return m

    # Status dump: all blocks of the current preset with bypass state and channel (raw payload)
    @staticmethod
    def STATUS_DUMP():
        return FractalParameterMapping.get(
            name = "Status Dump",
            request = _sysex(0x13),
            response = _response(0x13),
            value_type = FractalParameterMapping.VALUE_RAW
        )

    # Switch the tuner on (1) or off (0)
    @staticmethod
    def TUNER_ON_OFF():
        return FractalParameterMapping.get(
            name = "Tuner On/Off",
            set = _sysex(0x11, (0x00,))
        )

    # Tuner state (1 while tuner push data arrives)
    @staticmethod
    def TUNER_STATE():
        return _FractalTunerStateMapping.get(
            name = "Tuner State",
            response = _response(0x11),
            length = 10
        )

    # Tuner note (0-11, push data)
    @staticmethod
    def TUNER_NOTE():
        return FractalParameterMapping.get(
            name = "Tuner Note",
            response = _response(0x11),
            length = 10
        )

    # Tuner deviance (push data, 8192 = in tune)
    @staticmethod
    def TUNER_DEVIANCE():
        return _FractalTunerDevianceMapping.get(
            name = "Tuner Deviance",
            response = _response(0x11),
            length = 10
        )


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


# Base class for the callbacks of the Fractal actions: LED states (off/dim/bright) like the FC controllers.
class FractalCallback(Callback):

    # LED states
    OFF = const(0)
    DIM = const(1)
    BRIGHT = const(2)

    def __init__(self, color, text, mappings = []):
        super().__init__(mappings = mappings)

        self._color = color
        self._text = text

    def init(self, appl, listener = None):
        super().init(appl, listener)

        self._appl = appl
        FRACTAL.init(appl.config)

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


####################################################################################################################


# Splash callback for the tuner display. Pass your default display root element as default splash, and a
# tuner display will be shown while the tuner is on (requires DIN MIDI and Send Realtime Sysex = ON).
class FractalTunerDisplayCallback(Callback):
    def __init__(self,
                 splash_default,                           # Default DisplayElement (root of default display to be shown when not in tuner mode)
                 splash_tuner = None,                      # DisplayElement to be shown when tuner is engaged
                 color_in_tune = Colors.LIGHT_GREEN,
                 color_out_of_tune = Colors.ORANGE,
                 color_neutral = Colors.WHITE,
                 calibration_high = 8192 + 350,            # Threshold value above which the note is out of tune (8192 + 8192 = 50 cents)
                 calibration_low = 8192 - 350,             # Threshold value below which the note is out of tune
                 note_names = None,                        # If set, this must be a tuple or list of 12 note name strings starting at C.
                 strobe = False,                           # If set, all available switch LEDs will act as a strobe tuner.
                 strobe_color = Colors.WHITE,              # LED color for strobe tuner
                 strobe_dim = 0.1,                         # Dim factor for strobe tuner in range [0..1]
                 strobe_speed = 1000,                      # Higher values make the strobe tuner go slower. 1000 is the recommended speed to start from.
                 strobe_max_fps = 120,                     # Maximum cumulative frame rate for update of strobe tuner LEDs
                 strobe_reverse = True,                    # If False, the strobe is rotating clockwise when too high / ccw when too low. If True, the other way round.
                 process_overridden_actions = False        # If set, when in tuner mode, the underlying actions will also be processed after disabling the tuner.
        ):
        Callback.__init__(self)

        self.__mapping = FractalMappings.TUNER_STATE()
        self.register_mapping(self.__mapping)

        self.__splash_tuner = splash_tuner
        self.__splash_default = splash_default
        self.__process_overridden_actions = process_overridden_actions
        self.__pushed_before = False

        if not self.__splash_tuner:
            self.__splash_tuner = TunerDisplay(
                mapping_note = FractalMappings.TUNER_NOTE(),
                mapping_deviance = FractalMappings.TUNER_DEVIANCE(),
                bounds = self.__splash_default.bounds,
                scale = 3,
                layout = {
                    "font": "/fonts/PTSans-NarrowBold-40.pcf"
                },
                color_in_tune = color_in_tune,
                color_out_of_tune = color_out_of_tune,
                color_neutral = color_neutral,
                calibration_high = calibration_high,
                calibration_low = calibration_low,
                note_names = note_names
            )

        if strobe:
            from ...controller.strobe import StrobeController

            self.__strobe_controller = StrobeController(
                mapping_state = self.__mapping,
                mapping_deviance = FractalMappings.TUNER_DEVIANCE(),
                dim_factor = strobe_dim,
                speed = strobe_speed,
                color = strobe_color,
                max_fps = strobe_max_fps,
                reverse = strobe_reverse
            )
        else:
            self.__strobe_controller = None

    def init(self, appl, listener = None):
        Callback.init(self, appl, listener)
        self.__appl = appl

        FRACTAL.init(appl.config)

        if self.__strobe_controller:
            self.__strobe_controller.init(appl)

    def update(self):
        Callback.update(self)
        self.__mapping.check(self.__appl.client)

    def parameter_changed(self, mapping):
        super().parameter_changed(mapping)

        if mapping != self.__mapping:
            return

        if self.__mapping.value == 1:
            # Tuner on
            for input in self.__appl.inputs:
                if hasattr(input, "pixels"):
                    input.override_action = self

                    if not self.__process_overridden_actions:
                        input.color = Colors.WHITE
                        input.brightness = 0
        else:
            # Tuner off
            for input in self.__appl.inputs:
                if hasattr(input, "pixels"):
                    input.override_action = None

                    for action in input.actions:
                        action.reset()

    def push(self):
        self.__pushed_before = True
        return self.__process_overridden_actions

    def release(self):
        if not self.__pushed_before:
            # This prevents that the tuner button switches off the tuner immediately at releasing
            return

        self.__pushed_before = False

        client = self.__appl.client
        client.set(FractalMappings.TUNER_ON_OFF(), 0)
        self.__mapping.switched(client, False)

        return self.__process_overridden_actions

    def get_root(self):
        if self.__mapping.value != 1:
            return self.__splash_default
        else:
            return self.__splash_tuner
