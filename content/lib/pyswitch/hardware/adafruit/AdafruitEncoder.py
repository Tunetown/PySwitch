from rotaryio import IncrementalEncoder as _IncrementalEncoder

# Rotary encoder
class AdafruitEncoder:
    
    def __init__(self, port_1, port_2, divisor = 2):
        self.port_1 = port_1
        self.port_2 = port_2
        self.__divisor = divisor
        self.__encoder = None

    # Initializes the input to the GPIO port
    def init(self):
        self.__encoder = _IncrementalEncoder(self.port_1, self.port_2, divisor = self.__divisor)

    # # Representational string for debug output (optional)
    # def __repr__(self):
    #     return f"{ repr(self.port_1) }|{ repr(self.port_2) }"

    # Returns the position of the rotary encoder
    @property
    def position(self):
        if not self.__encoder:
            return None
        
        return self.__encoder.position