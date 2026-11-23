from lib.pyswitch.clients.fractal_II import FRACTAL_II, FractalIIMapping, MODEL_AXE_FX_II_XL_PLUS
from lib.pyswitch.controller.client import ClientParameterMapping
from lib.pyswitch.ui.elements import DisplayLabel

from .mocks_appl import MockClient, MockController, MockFootswitch


# Client mock providing get_matching_request(). The requests of the mappings in "pending" are regarded as outstanding;
# notify_listeners() calls on them are recorded in "notified".
class MockFractalIIClient(MockClient):
    class _Request:
        def __init__(self, client, mapping):
            self.__client = client
            self.__mapping = mapping

        def notify_listeners(self):
            self.__client.notified.append(self.__mapping)

    def __init__(self):
        super().__init__()
        self.pending = []
        self.notified = []

    def get_matching_request(self, mapping):
        return self._Request(self, mapping) if mapping in self.pending else None


# Resets the shared Axe-Fx II state and the values of all Axe-Fx II mappings (they are singletons)
def reset_fractal_II():
    if FRACTAL_II.model != MODEL_AXE_FX_II_XL_PLUS:
        for m in ClientParameterMapping._mappings:
            if isinstance(m, FractalIIMapping):
                m.set_model(MODEL_AXE_FX_II_XL_PLUS)

    FRACTAL_II.__init__()

    for m in ClientParameterMapping._mappings:
        if isinstance(m, FractalIIMapping):
            m.value = None
            m._skip = 0
            if hasattr(m, "_FractalIIPresetNameMapping__preset"):
                m._FractalIIPresetNameMapping__preset = None


# Parses a hex string
def hex_message(text):
    return bytearray.fromhex(text.replace(" ", ""))

# XOR checksum
def checksum(msg):
    cs = 0
    for b in msg:
        cs ^= b
    return cs & 0x7f

# Axe-Fx II SysEx message with checksum (default model: XL+)
def sysex(function, data = (), model = 0x07):
    msg = [0xf0, 0x00, 0x01, 0x74, model, function] + list(data)
    msg.append(checksum(msg))
    msg.append(0xf7)
    return bytearray(msg)

# Message without checksum (tuner, beat, block states)
def push_message(function, data = (), model = 0x07):
    return bytearray([0xf0, 0x00, 0x01, 0x74, model, function] + list(data) + [0xf7])

# Name padded to 32 characters
def name32(name, fill = 0x20):
    return [ord(c) for c in name] + [fill] * (32 - len(name))

# Answer to the preset request (0x14)
def preset_answer(preset, model = 0x07):
    return sysex(0x14, [preset >> 7, preset & 0x7f], model)

# Answer to the current preset name request (0x0F)
def name_answer(name):
    return sysex(0x0f, name32(name))

# Answer to a preset name request by number (0x15)
def name_by_number_answer(preset, name):
    return sysex(0x15, [preset >> 7, preset & 0x7f] + name32(name))

# Block state record (5 septets) for an effect ID, engaged and X flags, bypass CC and X/Y CC
def block_record(effect_id, engaged, x = True, bypass_cc = 0, xy_cc = 0):
    word = (effect_id << 24) | (xy_cc << 16) | (bypass_cc << 8) | (1 if engaged else 0) | (2 if x else 0)
    return [(word >> (7 * i)) & 0x7f for i in range(5)]

# Block states answer (0x0E): list of (effect_id, engaged, x)
def block_states_answer(blocks):
    data = []
    for b in blocks:
        data += block_record(*b)
    return push_message(0x0e, data)

# Block states value as decoded by the mapping: list of (effect_id, engaged, x)
def block_states(blocks):
    ret = []
    for b in blocks:
        ret += [b[0], (1 if b[1] else 0) | (2 if b[2] else 0)]
    return bytes(ret)


# Sets up an action with a mock controller, a footswitch with one LED and a display label.
# Returns (appl, switch, label).
def setup_action(action, config = {}):
    appl = MockController(config = config, client = MockFractalIIClient())
    switch = MockFootswitch(pixels = [0], actions = [action])
    label = DisplayLabel(layout = { "font": "foo", "backColor": (0, 0, 0) })

    action.label = label
    action.init(appl, switch)

    return (appl, switch, label)


# Default brightness values (config defaults)
LED_BRIGHT = 0.3
LED_DIM = 0.02
LED_OFF = 0
