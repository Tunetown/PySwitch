from .. import FractalParameterMapping, FRACTAL, _sysex, _response, _checksum, _decode_name
from ....controller.client import ClientParameterMapping


# Name of a preset chosen by an action (target), e.g. the preset a switch selects. One instance per action
# (no singleton): the target is changed with set_target(), which rewrites the request message in place.
# Answers look like answers to the current preset query, so pending queries are tracked in FRACTAL.
class FractalPresetTargetNameMapping(FractalParameterMapping):

    _count = 0

    def __init__(self):
        FractalPresetTargetNameMapping._count += 1

        super().__init__(
            name = f"Preset Target Name { FractalPresetTargetNameMapping._count }",
            create_key = ClientParameterMapping,
            request = _sysex(0x0d, (0x00, 0x00)),
            response = _response(0x0d),
            value_type = FractalParameterMapping.VALUE_STRING,
            value_index = 8
        )

        self.request = bytearray(self.request)
        self.target = 0
        self.__previous = None

        # Registered for model patching (see FractalState.init)
        ClientParameterMapping._mappings.append(self)

    # Sets the target preset. The name is requested again.
    def set_target(self, preset):
        if preset == self.target:
            return

        self.__previous = self.target
        self.target = preset
        self.value = None

        req = self.request
        req[6] = preset & 0x7f
        req[7] = (preset >> 7) & 0x7f
        req[8] = _checksum(req, 8)

    # Requests the name (use this instead of client.request())
    def send_request(self, client, listener):
        if self.target not in FRACTAL.pending_names:
            FRACTAL.pending_names.append(self.target)

        client.request(self, listener)

    # Must be called when the request has been terminated
    def discard(self):
        if self.target in FRACTAL.pending_names:
            FRACTAL.pending_names.remove(self.target)

    # Accepts answers for the target. An answer for the previous target completes a request
    # sent before the target changed (the value stays None so the name is requested again).
    def parse(self, midi_message):
        if self.parse_against(midi_message, self.response) == None:
            return False

        preset = midi_message[6] + 128 * midi_message[7]

        if preset == self.target:
            FRACTAL.is_target_answer(midi_message, preset)
            self.value = _decode_name(midi_message, 8)
            return True

        if preset == self.__previous:
            FRACTAL.is_target_answer(midi_message, preset)
            self.__previous = None
            return True

        return False
