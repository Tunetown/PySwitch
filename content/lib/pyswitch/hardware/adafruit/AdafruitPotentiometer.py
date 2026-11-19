from analogio import AnalogIn as _AnalogIn

# Analog GPIO (Potentiometer)
class AdafruitPotentiometer:
    
    # port: The board GPIO pin definition to be used for this pot (for example board.GP1)
    def __init__(self, port):
        self.port = port
        self.__input = None

    # Initializes the input to the GPIO port
    def init(self):
        self.__input = _AnalogIn(self.port)

    # # Representational string for debug output (optional)
    # def __repr__(self):
    #     return repr(self.port)

    # Returns the value of the pot (integer in range [0..65535])
    @property
    def value(self):
        if not self.__input:
            return None
        
        return self.__input.value