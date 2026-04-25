from js import document
from math import pow
# import colorsys

class WrapNeoPixelDriver:
    class LedList(list):
        def __init__(self, dom_namespace):
            super().__init__()
            self.dom_namespace = dom_namespace

        def __add__(self, *args, **kwargs):
            return WrapNeoPixelDriver.LedList(super().__add__(*args, **kwargs))
        
        def __setitem__(self, key, value):            
            super(WrapNeoPixelDriver.LedList, self).__setitem__(key, value)

            led = document.getElementById(self.dom_namespace + "-led-" + str(key))

            if not led:
                #print("Warning: LED " + str(key) + " not found in DOM")
                return
            
            # Store original value for testing
            led.dataset.color = [v for v in value]

            # When black, show as off (dark)
            if value == (0, 0, 0):
                led.style.backgroundColor = f"rgb(0, 0, 0)"
                return

            # Apply gamma correction
            def trans(x, gamma = 0.28):
                if x <= 0:
                    return 0
                return pow((x/255), gamma) * 255
            
            def clip(x):
                return x if x < 256 else 255
            
            value = [clip(trans(v * 3)) for v in value]

            led.style.backgroundColor = f"rgb({ value[0] }, { value[1] }, { value[2] })"

        def fill(self, color):
            for i in range(len(self)):
                self[i] = color

    def __init__(self, dom_namespace):
        self.leds = None
        self.dom_namespace = dom_namespace
        
    def init(self, num_leds):
        self.leds = self.LedList(self.dom_namespace) 

        while len(self.leds) < num_leds:
            self.leds.append(None)


