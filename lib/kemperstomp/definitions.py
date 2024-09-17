#################################################################################################################################
# 
# Ports configuration for kemperstomp. This helps addressing the different devices. Only change this when either
# one of the supported devices has been updated or new devices are added.
#
#################################################################################################################################
 
import board

#################################################################################################################################


# This defines the available actions. 
class Actions:

    # Switches an effect on/off, if the slot is assigned.
    # Available options:
    # {
    #     "type": Actions.EFFECT_ON_OFF
    #     "slot": SLot ID: Use one of the constants defined in Slots, for example Slots.EFFECT_SLOT_A
    # }
    EFFECT_ON_OFF = 100

    #### Internal and development actions #######################################################################################

    # Soft-Reboot the device. Useful for development.
    REBOOT = 1001

    # Terminate the script. Useful for development.
    TERMINATE = 1002

    # Used internally in expore mode to show the pressed IO port. DO NOT USE IN YOUR CONFIGURATION, OR THE CODE WILL CRASH!
    EXPLORE_IO = 2000

    # Used internally in expore mode to increase/decrease the enlightened foot switch. DO NOT USE IN YOUR CONFIGURATION, OR THE CODE WILL CRASH!
    # Available options:
    # {
    #     "step": Increment step for selecting the next enlightened switch
    # }
    EXPLORE_PIXELS = 2001,

    # Simple action that prints a fixed text on the console. Used internally.
    # Available options:
    # {
    #     "text": Text string to show
    # }
    PRINT = 9000


#################################################################################################################################


# Switch events
class ActionEvents:
    SWITCH_DOWN = 0   # At pushing the switch down
    SWITCH_UP = 1     # At releasing the switch


#################################################################################################################################

# This provides known device definitions, ready to use in the config file.
class Ports:
    # PaintAudio MIDI Captain Nano (4 Switches)
    # Board Infos
    # Raspberry Pi Pico (RP2040)
    #
    # GP1  - FootSwitch 1
    # GP4  bat_chg_led
    # GP6  charging
    # GP7  NeoPixel
    # GP8  asyncio PWMOut frequency
    # GP9  - FootSwitch A
    # GP10 - FootSwitch B
    # GP12 tft_dc   (SPI1 RX)
    # GP13 tft_cs   (Chip Select)
    # GP14 spi_clk  (SPI1SCK)
    # GP15 spi_mosi (SPI1 TX)
    # GP16 Midi GP16GP17 baudrate
    # GP17 Midi GP16GP17 baudrate
    # GP25 - FootSwitch 2
    PA_MIDICAPTAIN_NANO_SWITCH_1 = { "port": board.GP1,  "pixels": (0, 1, 2), "name": "1" }
    PA_MIDICAPTAIN_NANO_SWITCH_2 = { "port": board.GP25, "pixels": (3, 4, 5), "name": "2"  }
    PA_MIDICAPTAIN_NANO_SWITCH_A = { "port": board.GP9,  "pixels": (6, 7, 8), "name": "A"  }
    PA_MIDICAPTAIN_NANO_SWITCH_B = { "port": board.GP10, "pixels": (9, 10, 11), "name": "B"  }

    # PaintAudio MIDI Captain Mini (6 Switches)
    # Board Infos
    # Raspberry Pi Pico (RP2040)
    #
    # GP1  - FootSwitch 1
    # GP4  bat_chg_led
    # GP6  charging
    # GP7  NeoPixel
    # GP8  asyncio PWMOut frequency
    # GP9  - FootSwitch A
    # GP10 - FootSwitch B
    # GP11 - FootSwitch C
    # GP12 tft_dc   (SPI1 RX)
    # GP13 tft_cs   (Chip Select)
    # GP14 spi_clk  (SPI1SCK)
    # GP15 spi_mosi (SPI1 TX)
    # GP16 Midi GP16GP17 baudrate
    # GP17 Midi GP16GP17 baudrate
    # GP24 - FootSwitch 3
    # GP25 - FootSwitch 2
    PA_MIDICAPTAIN_MINI_SWITCH_1 = { "port": board.GP1,  "pixels": (0, 1, 2), "name": "1"  }
    PA_MIDICAPTAIN_MINI_SWITCH_2 = { "port": board.GP25, "pixels": (3, 4, 5), "name": "2"  }
    PA_MIDICAPTAIN_MINI_SWITCH_3 = { "port": board.GP24, "pixels": (6, 7, 8), "name": "3"  }
    PA_MIDICAPTAIN_MINI_SWITCH_A = { "port": board.GP9,  "pixels": (9, 10, 11), "name": "A"  }
    PA_MIDICAPTAIN_MINI_SWITCH_B = { "port": board.GP10, "pixels": (12, 13, 14), "name": "B"  }
    PA_MIDICAPTAIN_MINI_SWITCH_C = { "port": board.GP11, "pixels": (15, 16, 17), "name": "C"  }


#################################################################################################################################


# Color definitions
class Colors:
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    RED = (255, 0, 0)
    PURPLE = (30, 0, 20)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)
    TURQUOISE = (64, 242, 208)
    BLUE = (0, 0, 255)
    GRAY = (190, 190, 190)
    DARK_GRAY = (50, 50, 50)
    BLACK = (0, 0, 0)

    # Text colors for automatic color detection by maximum contrast to the back color of the display label
    TEXT_COLOR_BRIGHT = (255, 255, 0)
    TEXT_COLOR_DARK = (0, 0, 0)

    # Default background color for display slots
    DEFAULT_SLOT_COLOR = (50, 50, 50)             


#################################################################################################################################


# Just used locally here!
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240
SLOT_HEIGHT = 40           # Slot height on the display


# Display area IDs for the (optional) switch displays
class DisplayAreas:
    HEADER = 0
    FOOTER = 10


# Display area definitions
DisplayAreaDefinitions = [
    # Header area
    {
        "area": DisplayAreas.HEADER,
        "name": "Header",

        "x": 0,
        "y": 0,
        "width": DISPLAY_WIDTH,
        "height": SLOT_HEIGHT,
        
        "layout": {
            "font": "/fonts/H20.pcf",
            "backColor": Colors.DEFAULT_SLOT_COLOR
        }
    },

    # Footer area
    {
        "area": DisplayAreas.FOOTER,
        "name": "Footer",

        "x": 0,
        "y": DISPLAY_HEIGHT - SLOT_HEIGHT,
        "width": DISPLAY_WIDTH,
        "height": SLOT_HEIGHT,

        "layout": {
            "font": "/fonts/H20.pcf",
            "backColor": Colors.DEFAULT_SLOT_COLOR
        }        
    }
]


#################################################################################################################################


# Kemper specific definitions
class KemperDefinitions:
    # Effect type color assignment
    EFFECT_COLOR_NONE = Colors.DEFAULT_SLOT_COLOR
    EFFECT_COLOR_WAH = Colors.ORANGE
    EFFECT_COLOR_DISTORTION = Colors.RED
    EFFECT_COLOR_COMPRESSOR = Colors.BLUE
    EFFECT_COLOR_NOISE_GATE = Colors.BLUE
    EFFECT_COLOR_SPACE = Colors.GREEN
    EFFECT_COLOR_CHORUS = Colors.BLUE
    EFFECT_COLOR_PHASER_FLANGER = Colors.PURPLE
    EFFECT_COLOR_EQUALIZER = Colors.YELLOW
    EFFECT_COLOR_BOOSTER = Colors.RED
    EFFECT_COLOR_LOOPER = Colors.PURPLE
    EFFECT_COLOR_PITCH = Colors.WHITE
    EFFECT_COLOR_DUAL = Colors.GREEN
    EFFECT_COLOR_DELAY = Colors.GREEN
    EFFECT_COLOR_REVERB = Colors.GREEN

    # Effect type display names
    EFFECT_NAME_NONE = "-"
    EFFECT_NAME_WAH = "Wah Wah"
    EFFECT_NAME_DISTORTION = "Distortion"
    EFFECT_NAME_COMPRESSOR = "Compressor"
    EFFECT_NAME_NOISE_GATE = "Noise Gate"
    EFFECT_NAME_SPACE = "Space"
    EFFECT_NAME_CHORUS = "Chorus"
    EFFECT_NAME_PHASER_FLANGER = "Phaser"
    EFFECT_NAME_EQUALIZER = "Equalizer"
    EFFECT_NAME_BOOSTER = "Boost"
    EFFECT_NAME_LOOPER = "Looper"
    EFFECT_NAME_PITCH = "Transpose"
    EFFECT_NAME_DUAL = "Dual"
    EFFECT_NAME_DELAY = "Delay"
    EFFECT_NAME_REVERB = "Reverb"

    # Some internal addressing (acc. to Kemper MIDI specification, should not be needed to change)
    PARAMETER_ADDRESS_EFFECT_TYPE = 0x00   
    PARAMETER_ADDRESS_EFFECT_STATUS = 0x03

    RESPONSE_ID_GLOBAL_PARAMETER = -1
    RESPONSE_ID_EFFECT_TYPE = 0x00
    RESPONSE_ID_EFFECT_STATUS = 0x03

    RESPONSE_ANSWER_STATUS_ON = 0x01
    RESPONSE_ANSWER_STATUS_OFF = 0x00

    RESPONSE_PREFIX_RIG_NAME = [0x00, 0x00, 0x03, 0x00, 0x00, 0x01]
    RESPONSE_PREFIX_RIG_DATE = [0x00, 0x00, 0x03, 0x00, 0x00, 0x03]


#################################################################################################################################


# IDs for the available effect slots
class Slots:
    EFFECT_SLOT_ID_A = 0
    EFFECT_SLOT_ID_B = 1
    EFFECT_SLOT_ID_DLY = 2
    EFFECT_SLOT_ID_REV = 3

    # Slot enable/disable. Order has to match the one defined above!
    CC_EFFECT_SLOT_ENABLE = (
        17,    # Slot A
        18,    # Slot B
        27,    # Slot DLY (with Spillover)
        28     # Slot REV (with Spillover)
    )
    
    # Slot address pages. Order has to match the one defined above!
    SLOT_ADDRESS_PAGE = (
        0x32,   # Slot A
        0x33,   # Slot B
        0x3c,   # Slot DLY
        0x3d    # Slot REV
    )

