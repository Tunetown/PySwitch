from ....controller.callbacks.parameter_display import ParameterDisplayCallback
from .. import FractalIIMappings, FRACTAL_II

# Callback for DisplayLabel to show the tempo (BPM)
class FractalIITempoDisplayCallback(ParameterDisplayCallback):
    def __init__(self):
        def convert_value(value):
            if value == None:
                return None
            return f"{ value } bpm"

        super().__init__(
            mapping = FractalIIMappings.TEMPO_BPM(),
            convert_value = convert_value
        )

    def init(self, appl, listener = None):
        super().init(appl, listener)
        FRACTAL_II.init(appl.config)
