import struct

from lib.pyswitch.clients.fractal_am4 import FRACTAL_AM4, FractalAM4Mapping
from lib.pyswitch.controller.client import ClientParameterMapping
from lib.pyswitch.ui.elements import DisplayLabel

from .mocks_appl import MockClient, MockController, MockFootswitch


# Client mock providing get_matching_request() (used for the preset name requests). The requests of the mappings
# in "pending" are regarded as outstanding.
class MockFractalAM4Client(MockClient):
    def __init__(self):
        super().__init__()
        self.pending = []

    def get_matching_request(self, mapping):
        return mapping if mapping in self.pending else None


# Resets the shared AM4 state and the values of all AM4 mappings (they are singletons)
def reset_fractal_am4():
    FRACTAL_AM4.__init__()

    for m in ClientParameterMapping._mappings:
        if isinstance(m, FractalAM4Mapping):
            m.value = None
            m._FractalAM4Mapping__skip = 0


# Parses the hex string of a captured message
def hex_message(text):
    return bytearray.fromhex(text.replace(" ", ""))

# XOR checksum
def checksum(msg):
    cs = 0
    for b in msg:
        cs ^= b
    return cs & 0x7f

# AM4 SysEx message with checksum
def sysex(function, data = ()):
    msg = [0xf0, 0x00, 0x01, 0x74, 0x15, function] + list(data)
    msg.append(checksum(msg))
    msg.append(0xf7)
    return bytearray(msg)

# Answer to the preset request (0x14)
def preset_answer(location):
    return sysex(0x14, [location & 0x7f, location >> 7])

# Encodes raw bytes as a continuous MSB-first bitstream of septets (like the name table answer)
def encode_msb(raw):
    out = []
    acc = 0
    bits = 0
    for b in raw:
        acc = (acc << 8) | b
        bits += 8
        while bits >= 7:
            bits -= 7
            out.append((acc >> bits) & 0x7f)
    if bits:
        out.append((acc << (7 - bits)) & 0x7f)
    return out

# Name table answer (238 bytes)
def name_table_answer(scene, preset_name, scene_names, blocks):
    raw = bytearray(192)
    raw[0x08:0x0c] = struct.pack("<I", scene)
    raw[0x0c:0x10] = struct.pack("<f", 71.5)        # Level meter (ignored)

    def put(offset, text):
        raw[offset:offset + 32] = (text.encode() + b" " * 32)[:32]

    put(0x10, preset_name)
    for i in range(4):
        put(0x30 + 0x20 * i, scene_names[i])
        raw[0xb0 + 4 * i:0xb4 + 4 * i] = struct.pack("<I", blocks[i])

    return sysex(0x01, [0x4e, 0x01, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00, 0x40, 0x01] + encode_msb(raw))

# Answer to a bypass read (64 bytes, byte 22 is the bypass flag)
def bypass_answer(block, bypassed):
    payload = [0x11] * 46
    payload[22 - 16] = 0x01 if bypassed else 0x00
    return sysex(0x01, [block & 0x7f, block >> 7, 0x03, 0x00, 0x0d, 0x00, 0x00, 0x00, 0x28, 0x00] + payload)

# Captured answers to preset name reads (source: mcp-midi-control SYSEX-MAP §6m)
NAME_ANSWER_GIG_RIG = "F0 00 01 74 15 01 4E 01 0B 00 12 00 00 00 20 00 20 53 26 42 02 1D 52 67 10 14 4D 16 39 00 40 20 10 08 04 02 01 00 40 20 10 08 04 02 01 00 40 20 10 08 04 02 01 00 40 20 10 08 04 00 00 40 F7"
NAME_ANSWER_EMPTY = "F0 00 01 74 15 01 4E 01 0B 00 12 00 00 00 20 00 1E 11 29 55 02 51 32 3E 00 08 04 02 01 00 40 20 10 08 04 02 01 00 40 20 10 08 04 02 01 00 40 20 10 08 04 00 00 38 F7"


# Sets up an action with a mock controller, a footswitch with one LED and a display label.
# Returns (appl, switch, label).
def setup_action(action, config = {}):
    appl = MockController(config = config, client = MockFractalAM4Client())
    switch = MockFootswitch(pixels = [0], actions = [action])
    label = DisplayLabel(layout = { "font": "foo", "backColor": (0, 0, 0) })

    action.label = label
    action.init(appl, switch)

    return (appl, switch, label)


# Default brightness values (config defaults)
LED_BRIGHT = 0.3
LED_DIM = 0.02
LED_OFF = 0
