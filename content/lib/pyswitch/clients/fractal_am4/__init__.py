from micropython import const
from struct import pack

from ...misc import get_option
from ...colors import Colors, dim_color
from ...controller.callbacks import Callback
from ...controller.client import ClientParameterMapping

# Fractal Audio AM4 client (experimental). The AM4 does not support the 3rd-party protocol of the other Fractal
# devices; this client uses the protocol of AM4-Edit as documented by the community (only messages confirmed on
# hardware). Protocol: claude/001 Fractal Support/spec/am4/protocol.md in the PySwitch repository. Message formats
# credit: mcp-midi-control (https://github.com/TheAndrewStaker/mcp-midi-control, Apache License 2.0).
# The AM4 sends nothing by itself: all values are polled.

####################################################################################################################

NUM_PRESETS = const(104)            # Locations A01..Z04
PRESETS_PER_BANK = const(4)
NUM_BANKS = const(26)               # Banks A..Z
NUM_SCENES = const(4)
NUM_SLOTS = const(4)

# LED and label colors (same as the Fractal client)
COLOR_BANK = Colors.ORANGE
COLOR_PRESET = Colors.GREEN
COLOR_SCENE = Colors.RED
COLOR_EFFECT = Colors.CYAN
COLOR_UTILITY = Colors.BLUE


####################################################################################################################


# Label options for the actions
class FractalAM4Label:
    NAME = const(0)                 # Name (preset or scene)
    NUMBER = const(1)               # Number ("A01", "Scene 2")
    ACTION = const(2)               # Function ("Preset +1")
    DESTINATION_NAME = const(3)     # Inc/Dec: name of the target
    LONG_NAME = const(4)            # Effects: block name ("Drive")
    SHORT_NAME = const(5)           # Effects: block abbreviation ("DRV")


# Preset load options for the bank functions
class FractalAM4PresetLoad:
    FIRST = const(0)                # Load the first preset of the target bank
    SAME = const(1)                 # Load the preset at the same position in the target bank


# Footswitch modes of the AM4 (argument of the mode select message)
class FractalAM4Mode:
    PRESETS = const(0x48)
    SCENES = const(0x49)
    EFFECTS = const(0x4a)
    AMP = const(0x58)
    TUNER = const(0x18)             # Tuner / tap tempo

    # Returns the display name of a mode
    @staticmethod
    def name(mode):
        return _MODE_NAMES[_MODES.index(mode)]

_MODES = (0x48, 0x49, 0x4a, 0x58, 0x18)
_MODE_NAMES = ("Presets", "Scenes", "Effects", "Amp", "Tuner")


# Block types (IDs as used by the AM4, also the values of the slot registers)
class FractalAM4Block:
    COMPRESSOR = const(0x2e)
    GRAPHIC_EQ = const(0x32)
    PARAMETRIC_EQ = const(0x36)
    AMP = const(0x3a)
    REVERB = const(0x42)
    DELAY = const(0x46)
    CHORUS = const(0x4e)
    FLANGER = const(0x52)
    ROTARY = const(0x56)
    PHASER = const(0x5a)
    WAH = const(0x5e)
    VOLUME_PAN = const(0x66)
    TREMOLO = const(0x6a)
    FILTER = const(0x72)
    DRIVE = const(0x76)
    ENHANCER = const(0x7a)
    GATE = const(0x92)

    # Returns the name of a block ID (long or short), or None for unknown IDs
    @staticmethod
    def name(block, short = False):
        if block not in _BLOCK_IDS:
            return None
        index = _BLOCK_IDS.index(block)
        return _BLOCK_SHORT[index] if short else _BLOCK_LONG[index]

# Parallel tuples, indexed like _BLOCK_IDS (order must match)
_BLOCK_IDS = (0x2e, 0x32, 0x36, 0x3a, 0x42, 0x46, 0x4e, 0x52, 0x56, 0x5a, 0x5e, 0x66, 0x6a, 0x72, 0x76, 0x7a, 0x92)
_BLOCK_LONG = (
    "Compressor", "Graphic EQ", "Param EQ", "Amp", "Reverb", "Delay", "Chorus", "Flanger", "Rotary", "Phaser",
    "Wah", "Volume", "Tremolo", "Filter", "Drive", "Enhancer", "Gate"
)
_BLOCK_SHORT = ("CMP", "GEQ", "PEQ", "AMP", "REV", "DLY", "CHO", "FLG", "ROT", "PHA", "WAH", "VOL", "TRM", "FIL", "DRV", "ENH", "GTE")


####################################################################################################################


# Location text like on the AM4 ("A01".."Z04")
def location_text(location):
    return chr(65 + location // PRESETS_PER_BANK) + "0" + str(location % PRESETS_PER_BANK + 1)


# State shared by the actions and callbacks: invalidates the cached preset names when the current preset changes
# (names of other locations are only read after a preset change, to see renames). There is only one instance.
class FractalAM4State:

    def __init__(self):
        self.preset_names = []      # All preset name mappings (other locations)
        self.stale_names = []       # Preset name mappings to be read again (the names may have been changed on the device)
        self.pending_name = None    # Preset name mapping with an outstanding request (the answer does not contain the location)
        self.__last_preset = None

    # Must be called with the current preset (location). On change, the known names are read again (they are still
    # shown until the new answer arrives).
    def track_preset(self, preset):
        if preset == self.__last_preset or preset == None:
            return

        self.__last_preset = preset
        self.stale_names = [m for m in self.preset_names if m.value != None]

    # Returns if a preset name has to be requested
    def needs_name(self, mapping):
        return mapping.value == None or mapping in self.stale_names

    # Requests a preset name. Only one name request may be outstanding, as all name answers look the same.
    def request_name(self, client, mapping, listener):
        pending = self.pending_name
        if pending and pending != mapping and client.get_matching_request(pending):
            return

        self.pending_name = mapping
        if mapping in self.stale_names:
            self.stale_names.remove(mapping)

        client.request(mapping, listener)


FRACTAL_AM4 = FractalAM4State()


####################################################################################################################


# XOR checksum of the first "end" bytes of a message
def _checksum(msg, end):
    cs = 0
    for i in range(end):
        cs ^= msg[i]
    return cs & 0x7f

# Creates an AM4 SysEx message with checksum
def _sysex(function, data = ()):
    msg = [0xf0, 0x00, 0x01, 0x74, 0x15, function]
    msg.extend(data)
    msg.append(_checksum(msg, len(msg)))
    msg.append(0xf7)
    return msg

# Two septets of a 14-bit value (LS first)
def _f14(value):
    return (value & 0x7f, (value >> 7) & 0x7f)

# Packs raw bytes into septets (8-to-7 sliding window, restarting every 7 bytes)
def _pack(raw):
    ret = []
    for start in range(0, len(raw), 7):
        carry = 0
        chunk = raw[start:start + 7]
        for i in range(len(chunk)):
            k = i + 1
            ret.append(((chunk[i] >> k) & 0x7f) | carry)
            carry = ((~(0x7f << k) & chunk[i]) << (7 - k)) & 0x7f
        ret.append(carry)
    return ret

# Unpacks num raw bytes from septets packed by _pack(), starting at index
def _unpack(msg, index, num):
    ret = bytearray(num)
    pos = 0
    while pos < num:
        n = min(7, num - pos)
        for i in range(n):
            k = i + 1
            ret[pos + i] = (((msg[index + i] & ((1 << (8 - k)) - 1)) << k) | (msg[index + i + 1] >> (7 - k))) & 0xff
        index += n + 1
        pos += n
    return ret

# Parameter message (function 0x01): pid_low, pid_high, action and optional raw payload
def _param(pid_low, pid_high, action, raw = None):
    data = list(_f14(pid_low) + _f14(pid_high) + _f14(action) + (0, 0) + _f14(len(raw) if raw else 0))
    if raw:
        data.extend(_pack(raw))
    return _sysex(0x01, data)

# Raw bytes of a float32 (little endian)
def _float(value):
    return pack("<f", value)

# Raw bytes of an uint32 (little endian)
def _uint(value):
    return pack("<I", value)

# Decodes a 32 byte name (cut at the first NUL, trimmed)
def _decode_name(raw, index):
    ret = ""
    for i in range(index, index + 32):
        c = raw[i]
        if c == 0:
            break
        ret += chr(c)
    return ret.strip()


####################################################################################################################


# Mapping for AM4 SysEx messages. The response template is compared from the function byte on.
class FractalAM4Mapping(ClientParameterMapping):

    # Value types
    VALUE_PRESET = const(0)         # 14-bit value after the template (current preset)
    VALUE_NAME_TABLE = const(1)     # Name table (see _decode_name_table)
    VALUE_BYPASS = const(2)         # Bypass flag of a long read answer (1 = bypassed)
    VALUE_NAME = const(3)           # Preset name answer (32 characters)

    # Singleton factory
    @classmethod
    def get(cls, name, set = None, request = None, response = None, value_type = 0, length = 0, set_function = None):
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
            length = length,
            set_function = set_function
        )

        ClientParameterMapping._mappings.append(m)
        return m

    def __init__(self, name, create_key, set = None, request = None, response = None, value_type = 0, length = 0, set_function = None):
        super().__init__(
            name = name,
            create_key = create_key,
            set = set,
            request = request,
            response = response
        )

        self.value_type = value_type
        self.__length = length                  # If set, only messages with exactly this length are parsed
        self.__set_function = set_function      # Creates the set message for a value
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

            value_type = self.value_type

            if value_type == self.VALUE_PRESET:
                return midi_message[end] + 128 * midi_message[end + 1]

            if value_type == self.VALUE_NAME_TABLE:
                return _decode_name_table(midi_message)

            if value_type == self.VALUE_BYPASS:
                return 1 if midi_message[22] else 0

            # Preset name: only accepted by the mapping of the outstanding request
            if FRACTAL_AM4.pending_name != self:
                return None

            FRACTAL_AM4.pending_name = None
            return _decode_name(_unpack(midi_message, 16, 32), 0)

        except (TypeError, IndexError):
            return None

    # Creates the set message for a value
    def set_value(self, value):
        self.set = self.__set_function(value)


# Decodes the name table answer: (active scene, preset name, scene names (tuple), slot blocks (tuple)).
# The 192 raw bytes are a continuous MSB-first bitstream in the septets from index 16.
def _decode_name_table(midi_message):
    raw = bytearray(192)
    acc = 0
    bits = 0
    pos = 0
    index = 16

    while pos < 192:
        acc = ((acc << 7) | midi_message[index]) & 0x7fff
        index += 1
        bits += 7

        if bits >= 8:
            bits -= 8
            raw[pos] = (acc >> bits) & 0xff
            pos += 1

    def uint(offset):
        return raw[offset] | (raw[offset + 1] << 8) | (raw[offset + 2] << 16) | (raw[offset + 3] << 24)

    return (
        uint(0x08),
        _decode_name(raw, 0x10),
        tuple(_decode_name(raw, 0x30 + 0x20 * i) for i in range(NUM_SCENES)),
        tuple(uint(0xb0 + 4 * i) for i in range(NUM_SLOTS))
    )


####################################################################################################################


# Mappings used by the actions and callbacks
class FractalAM4Mappings:

    # Current preset (location 0..103)
    @staticmethod
    def PRESET():
        return FractalAM4Mapping.get(
            name = "AM4 Preset",
            request = _sysex(0x14),
            response = [0xf0, 0x00, 0x01, 0x74, 0x15, 0x14],
            value_type = FractalAM4Mapping.VALUE_PRESET
        )

    # Loads a preset (location 0..103)
    @staticmethod
    def PRESET_SELECT():
        return FractalAM4Mapping.get(
            name = "AM4 Preset Select",
            set = _param(0xce, 0x0a, 0x01, _float(0)),
            set_function = lambda value: _param(0xce, 0x0a, 0x01, _float(value))
        )

    # Name table: (active scene 0..3, preset name, scene names (tuple of 4), blocks of the 4 slots (tuple, 0 = empty))
    @staticmethod
    def NAME_TABLE():
        return FractalAM4Mapping.get(
            name = "AM4 Name Table",
            request = _param(0xce, 0x00, 0x1f),
            response = [0xf0, 0x00, 0x01, 0x74, 0x15, 0x01, 0x4e, 0x01, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00, 0x40, 0x01],
            value_type = FractalAM4Mapping.VALUE_NAME_TABLE,
            length = 238
        )

    # Selects a scene (0..3)
    @staticmethod
    def SCENE_SELECT():
        return FractalAM4Mapping.get(
            name = "AM4 Scene Select",
            set = _param(0xce, 0x0d, 0x01, _uint(0)),
            set_function = lambda value: _param(0xce, 0x0d, 0x01, _uint(value))
        )

    # Bypass state of a block (1 = bypassed, 0 = engaged; for the active scene)
    @staticmethod
    def BYPASS(block):
        return FractalAM4Mapping.get(
            name = f"AM4 Bypass { block }",
            request = _param(block, 0x03, 0x0d),
            response = [0xf0, 0x00, 0x01, 0x74, 0x15, 0x01] + list(_f14(block)) + [0x03, 0x00, 0x0d, 0x00, 0x00, 0x00, 0x28, 0x00],
            value_type = FractalAM4Mapping.VALUE_BYPASS,
            length = 64,
            set = _param(block, 0x03, 0x01, _float(0)),
            set_function = lambda value: _param(block, 0x03, 0x01, _float(value))
        )

    # Name of any preset (location 0..103)
    @staticmethod
    def PRESET_NAME(location):
        name = f"AM4 Preset Name { location }"
        for m in FRACTAL_AM4.preset_names:
            if m.name == name:
                return m

        request = _param(0xce, 0x0b, 0x12, _uint(location))

        m = FractalAM4Mapping.get(
            name = name,
            request = request,
            response = request[:14] + [0x20, 0x00],
            value_type = FractalAM4Mapping.VALUE_NAME
        )

        FRACTAL_AM4.preset_names.append(m)
        return m

    # Selects a footswitch mode of the AM4 (see FractalAM4Mode)
    @staticmethod
    def MODE():
        return FractalAM4Mapping.get(
            name = "AM4 Mode",
            set = _sysex(0x12, (FractalAM4Mode.PRESETS,)),
            set_function = lambda value: _sysex(0x12, (value,))
        )


####################################################################################################################


# Steps a value: step size, wrap, lower and upper limit
def _inc_dec(value, step, wrap, lower, upper):
    value += step

    if value > upper:
        return lower if wrap else upper

    if value < lower:
        return upper if wrap else lower

    return value

# Label text for Inc/Dec functions ("Preset +1")
def _action_text(prefix, step):
    return f"{ prefix } +{ step }" if step > 0 else f"{ prefix } { step }"


####################################################################################################################


# Base class for the callbacks of the AM4 actions: LED states (off/dim/bright) like the Fractal client.
class FractalAM4Callback(Callback):

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
