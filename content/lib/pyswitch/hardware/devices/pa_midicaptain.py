import board as _board
from usb_midi import ports as _ports

# USB Midi in/out for PA MIDICaptain devices. No UART, so ports have to be adafruit MIDI ports from 
# the usb_midi module.
def PA_MIDICAPTAIN_USB_MIDI(receive_chunk_size = 50):
    from ...midi.buffer import MIDIBuffer as _MIDIBuffer
    return _MIDIBuffer(
        midi_in = _ports[0],
        midi_out = _ports[1],
        receive_chunk_size = receive_chunk_size
    )

# DIN Midi in/out for PA MIDICaptain devices. Uses UART mode so the ports must be board GPIO pins.
def PA_MIDICAPTAIN_DIN_MIDI(receive_chunk_size = 50):
    from ..adafruit.AdafruitDinMidiDevice import AdafruitDinMidiDevice
    return AdafruitDinMidiDevice(
        gpio_in = _board.GP16,
        gpio_out = _board.GP17,
        baudrate = 31250,
        timeout = 0.001,
        receive_chunk_size = receive_chunk_size
    )

