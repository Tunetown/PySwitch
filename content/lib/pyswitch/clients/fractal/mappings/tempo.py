from .. import FractalParameterMapping, _sysex, _response

# Tap the tempo (the value is ignored)
def MAPPING_TAP_TEMPO():
    return FractalParameterMapping.get(
        name = "Tap Tempo",
        set = _sysex(0x10),
        set_bytes = 0
    )

# Tempo beat push data (DIN only, Send Realtime Sysex = ON). The value counts the beats.
def MAPPING_TEMPO_BEAT():
    return _FractalTempoBeatMapping.get(
        name = "Tempo Beat",
        response = _response(0x10),
        length = 7
    )

# Tempo in BPM
def MAPPING_TEMPO_BPM():
    return FractalParameterMapping.get(
        name = "Tempo BPM",
        set = _sysex(0x14, (0x00, 0x00)),
        request = _sysex(0x14, (0x7f, 0x7f)),
        response = _response(0x14),
        value_type = FractalParameterMapping.VALUE_14BIT,
        set_bytes = 2
    )


# Counts the beats (value in range [0..127])
class _FractalTempoBeatMapping(FractalParameterMapping):
    def _decode(self, midi_message):
        return ((self.value if self.value != None else 0) + 1) & 0x7f
