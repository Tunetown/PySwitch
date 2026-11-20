from ....controller.callbacks.parameter_display import ParameterDisplayCallback
from ..mappings.tempo import MAPPING_TEMPO_BPM

# Callback for DisplayLabel to show the tempo (BPM)
class FractalTempoDisplayCallback(ParameterDisplayCallback):
    def __init__(self):
        def convert_value(value):
            if value == None:
                return None
            return f"{ value } bpm"

        super().__init__(
            mapping = MAPPING_TEMPO_BPM(),
            convert_value = convert_value
        )
