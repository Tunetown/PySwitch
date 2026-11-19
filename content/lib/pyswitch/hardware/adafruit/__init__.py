import board as _board

# Display driver
from busio import SPI as _SPI
from displayio import release_displays as _release_displays
from adafruit_misc.adafruit_st7789 import ST7789 as _ST7789
from adafruit_misc.neopixel import NeoPixel as _NeoPixel

try:
    from fourwire import FourWire as _FourWire
except ImportError:
    from displayio import FourWire as _FourWire

# Font loader
from adafruit_bitmap_font import bitmap_font as _bitmap_font

# TFT driver class
class AdafruitST7789DisplayDriver:

    def __init__(self, 
                width = 240, 
                height = 240,
                tft_cs = _board.GP13,
                tft_dc = _board.GP12,
                spi_mosi = _board.GP15,
                spi_clk = _board.GP14,
                row_start = 80,
                rotation = 180,
                baudrate = 24000000         # 24MHz
        ):
        self.width = width
        self.height = height

        self.__tft_cs = tft_cs
        self.__tft_dc = tft_dc
        self.__spi_mosi = spi_mosi
        self.__spi_clk = spi_clk

        self.__row_start = row_start
        self.__rotation = rotation
        self.__baudrate = baudrate

    # Initialize the display
    def init(self):        
        _release_displays()
        
        spi = _SPI(
            self.__spi_clk, 
            MOSI = self.__spi_mosi
        )
        while not spi.try_lock():
            pass
        
        spi.configure(
            baudrate = self.__baudrate
        )
        spi.unlock()

        display_bus = _FourWire(
            spi, 
            command = self.__tft_dc, 
            chip_select = self.__tft_cs, 
            reset = None
        )

        self.tft = _ST7789(
            display_bus,
            width = self.width, 
            height = self.height,
            rowstart = self.__row_start,
            rotation = self.__rotation
        )


##################################################################################################


# Buffered font loader
class AdafruitFontLoader:
    __fonts = {}

    # Returns a font (buffered)
    def get(self, path):
        if path in self.__fonts:
            return self.__fonts[path]
        
        font = _bitmap_font.load_font(path)
        self.__fonts[path] = font

        return font


##################################################################################################


# Implements communication with an array of NeoPixels
class AdafruitNeoPixelDriver:

    def __init__(self, port = _board.GP7):
        self.__port = port
        self.leds = None
        
    # Initialize NeoPixel array. Neopixel documentation:
    # https://docs.circuitpython.org/projects/neopixel/en/latest/
    # https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython
    def init(self, num_leds):
        self.leds = _NeoPixel(self.__port, num_leds)


