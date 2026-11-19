#################################################################################################################################
# 
# Addressing definitions for some known devices. This helps addressing the different hardware I/O. Only change this when either
# one of the supported devices has been updated or new devices are added.
#
#################################################################################################################################
 
import board as _board

from ..adafruit.AdafruitSwitch import AdafruitSwitch as _AdafruitSwitch

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
PA_MIDICAPTAIN_NANO_SWITCH_1 = { "model": _AdafruitSwitch(_board.GP1),  "pixels": (0, 1, 2), "name": "1", "strobeOrder": 0 }
PA_MIDICAPTAIN_NANO_SWITCH_2 = { "model": _AdafruitSwitch(_board.GP25), "pixels": (3, 4, 5), "name": "2", "strobeOrder": 1 }
PA_MIDICAPTAIN_NANO_SWITCH_A = { "model": _AdafruitSwitch(_board.GP9),  "pixels": (6, 8, 7), "name": "A", "strobeOrder": 3 }
PA_MIDICAPTAIN_NANO_SWITCH_B = { "model": _AdafruitSwitch(_board.GP10), "pixels": (9, 11, 10), "name": "B", "strobeOrder": 2 }