from digitalio import DigitalInOut as _DigitalInOut, Direction as _Direction, Pull as _Pull

# GPIO switch
class AdafruitSwitch: #(SwitchDriver):
    
    # port: The board GPIO pin definition to be used for this switch (for example board.GP1)
    def __init__(self, port):
        self.port = port
        self.__switch = None

    # Initializes the switch to the GPIO port
    def init(self):
        self.__switch = _DigitalInOut(self.port)
        
        self.__switch.direction = _Direction.INPUT
        self.__switch.pull = _Pull.UP

    # # Representational string for debug output (optional)
    # def __repr__(self):
    #     return repr(self.port)

    # Return if the switch is currently pushed
    @property
    def pushed(self):
        if not self.__switch:
            return None
        
        return self.__switch.value == False  # Inverse logic!