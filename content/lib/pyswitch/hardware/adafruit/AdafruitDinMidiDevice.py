from busio import UART as _UART
from ...midi.buffer_raw import MIDIBuffer as _MIDIBuffer

# DIN MIDI Device
class AdafruitDinMidiDevice:
    def __init__(self, 
                 gpio_in, 
                 gpio_out,
                 baudrate, 
                 timeout,
                 receive_chunk_size = 50
        ):

        midi_uart = _UART(
            gpio_in, 
            gpio_out, 
            baudrate = baudrate, 
            timeout = timeout
        ) 

        self.__midi = _MIDIBuffer(
            midi_out = midi_uart,
            midi_in = midi_uart,
            receive_chunk_size = receive_chunk_size
        )

    def send(self, midi_message):
        self.__midi.send(midi_message)

    def receive(self):
        return self.__midi.receive()