#################################################################################################################################
# 
# Addressing definitions for some known devices. This helps addressing the different hardware I/O. Only change this when either
# one of the supported devices has been updated or new devices are added.
#
#################################################################################################################################
 
import board as _board

from ..adafruit.AdafruitSwitch import AdafruitSwitch as _AdafruitSwitch
from ..adafruit.AdafruitPotentiometer import AdafruitPotentiometer as _AdafruitPotentiometer
from ..adafruit.AdafruitEncoder import AdafruitEncoder as _AdafruitEncoder

# PaintAudio MIDI Captain (10 Switches) EXPERIMENTAL/UNTESTED! 
# Thanks to @Erikcb and @RickMrChaos at the Kemper Forums for providing the GPIO mappings
# Board Infos
# Raspberry Pi Pico (RP2040)
#
# GP0  - Wheel push button
# GP1  - FootSwitch 1
# GP2  - Wheel Rotary Encoder
# GP3  - Wheel Rotary Encoder
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
# GP18 - Footswitch D
# GP19 - Footswitch down
# GP20 - FootSwitch up
# GP23 - FootSwitch 4
# GP24 - FootSwitch 3
# GP25 - FootSwitch 2
# GP27 - Exp. Pedal 1
# GP28 - Exp. Pedal 2
PA_MIDICAPTAIN_10_SWITCH_1      = { "model": _AdafruitSwitch(_board.GP1),  "pixels": (0, 1, 2), "name": "1", "strobeOrder": 0 }
PA_MIDICAPTAIN_10_SWITCH_2      = { "model": _AdafruitSwitch(_board.GP25), "pixels": (3, 4, 5), "name": "2", "strobeOrder": 1 }
PA_MIDICAPTAIN_10_SWITCH_3      = { "model": _AdafruitSwitch(_board.GP24), "pixels": (6, 7, 8), "name": "3", "strobeOrder": 2 }
PA_MIDICAPTAIN_10_SWITCH_4      = { "model": _AdafruitSwitch(_board.GP23), "pixels": (9, 10, 11), "name": "4", "strobeOrder": 3 }
PA_MIDICAPTAIN_10_SWITCH_UP     = { "model": _AdafruitSwitch(_board.GP20), "pixels": (12, 13, 14), "name": "Up", "strobeOrder": 4 }

PA_MIDICAPTAIN_10_SWITCH_A      = { "model": _AdafruitSwitch(_board.GP9),  "pixels": (15, 17, 16), "name": "A", "strobeOrder": 9 }
PA_MIDICAPTAIN_10_SWITCH_B      = { "model": _AdafruitSwitch(_board.GP10), "pixels": (18, 20, 19), "name": "B", "strobeOrder": 8 }
PA_MIDICAPTAIN_10_SWITCH_C      = { "model": _AdafruitSwitch(_board.GP11), "pixels": (21, 23, 22), "name": "C", "strobeOrder": 7 }
PA_MIDICAPTAIN_10_SWITCH_D      = { "model": _AdafruitSwitch(_board.GP18), "pixels": (24, 26, 25), "name": "D", "strobeOrder": 6 }
PA_MIDICAPTAIN_10_SWITCH_DOWN   = { "model": _AdafruitSwitch(_board.GP19), "pixels": (27, 29, 28), "name": "Down", "strobeOrder": 5 }

# Exp Pedals
PA_MIDICAPTAIN_10_EXP_PEDAL_1   = { "model": _AdafruitPotentiometer(_board.GP27), "name": "Exp1" }
PA_MIDICAPTAIN_10_EXP_PEDAL_2   = { "model": _AdafruitPotentiometer(_board.GP28), "name": "Exp2" }

# These are for using the EXP inputs with switches:
PA_MIDICAPTAIN_10_EXP_SWITCH_1   = { "model": _AdafruitSwitch(_board.GP27), "name": "ExpSw1" }
PA_MIDICAPTAIN_10_EXP_SWITCH_2   = { "model": _AdafruitSwitch(_board.GP28), "name": "ExpSw2" }

# Wheel encoder
PA_MIDICAPTAIN_10_WHEEL_ENCODER = { "model": _AdafruitEncoder(_board.GP2, _board.GP3, divisor = 2), "name": "Wheel" }
PA_MIDICAPTAIN_10_WHEEL_BUTTON  = { "model": _AdafruitSwitch(_board.GP0), "name": "Wheel" }

