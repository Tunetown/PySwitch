from lib.pyswitch.clients.fractal import FRACTAL, FractalParameterMapping, MODEL_FM3
from lib.pyswitch.controller.client import ClientParameterMapping
from lib.pyswitch.ui.elements import DisplayLabel

from .mocks_appl import MockClient, MockController, MockFootswitch


# Client mock which also provides get_matching_request() (used by the tuner state mapping)
class MockFractalClient(MockClient):
    class _Request:
        def __init__(self, client, mapping):
            self.__client = client
            self.__mapping = mapping

        def notify_listeners(self):
            self.__client.notified.append(self.__mapping)

    def __init__(self):
        super().__init__()
        self.notified = []

    def get_matching_request(self, mapping):
        return self._Request(self, mapping)


# Resets the shared Fractal state and the values of all Fractal mappings (they are singletons)
def reset_fractal():
    if FRACTAL.model != MODEL_FM3:
        for m in ClientParameterMapping._mappings:
            if isinstance(m, FractalParameterMapping):
                m.set_model(MODEL_FM3)

    FRACTAL.__init__()

    for m in ClientParameterMapping._mappings:
        if isinstance(m, FractalParameterMapping):
            m.value = None
            m._FractalParameterMapping__skip = 0


# XOR checksum
def checksum(msg):
    cs = 0
    for b in msg:
        cs ^= b
    return cs & 0x7f

# Fractal SysEx message with checksum
def sysex(function, data = (), model = 0x11):
    msg = [0xf0, 0x00, 0x01, 0x74, model, function] + list(data)
    msg.append(checksum(msg))
    msg.append(0xf7)
    return bytearray(msg)

# Push message without checksum
def push_message(function, data = (), model = 0x11):
    return bytearray([0xf0, 0x00, 0x01, 0x74, model, function] + list(data) + [0xf7])

# Name padded to 32 characters
def name32(name, fill = 0x20):
    return [ord(c) for c in name] + [fill] * (32 - len(name))

# Preset answer (0D) with number and name
def preset_answer(preset, name):
    return sysex(0x0d, [preset & 0x7f, preset >> 7] + name32(name))

# Status dump payload: list of (effect_id, bypassed, channel, num_channels)
def dump(blocks):
    ret = []
    for b in blocks:
        ret += [b[0] & 0x7f, b[0] >> 7, (1 if b[1] else 0) | (b[2] << 1) | (b[3] << 4)]
    return bytes(ret)


# Sets up an action with a mock controller, a footswitch with one LED and a display label.
# Returns (appl, switch, label).
def setup_action(action, config = {}):
    appl = MockController(config = config, client = MockFractalClient())
    switch = MockFootswitch(pixels = [0], actions = [action])
    label = DisplayLabel(layout = { "font": "foo", "backColor": (0, 0, 0) })

    action.label = label
    action.init(appl, switch)

    return (appl, switch, label)


# Default brightness values (config defaults)
LED_BRIGHT = 0.3
LED_DIM = 0.02
LED_OFF = 0
