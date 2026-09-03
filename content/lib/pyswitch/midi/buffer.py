##################################################################################################
# A raw MIDI buffer implementation which does not work with object oriented overhead
# and does not distinguish between message types and MIDI channels etc. 
# Expects midi in and out objects providing read/write interfaces. 
# 
# Also, no input buffer size is needed because this buffer can receive arbitrarily 
# sized messages (if the in/out interfaces can handle it) while staying very memory
# efficient nevertheless.
# 
# The messages are provided/processed as raw list of bytes.
#
# Dependencies: None!
##################################################################################################

class MIDIBuffer:
    def __init__(
        self,
        midi_in,                  # MIDI in handler, providing a readinto(buffer, num_bytes) -> int method
        midi_out,                 # MIDI out handler providing a write(bytearray, num_bytes) method.
        receive_chunk_size = 50   # Receiving buffer size. This does NOT affect the maximum 
                                  # length of input messages, just adjusts between RAM usage / CPU time.
                                  # Larger values read more bytes at once which takes more RAM but is 
                                  # slightly faster for large SYSEX transfers.
    ):
        self._midi_in = midi_in
        self._midi_out = midi_out

        # Receive buffer
        self._receive_buffer = bytearray(receive_chunk_size)
        self._receive_buffer_pos = 0           # Current parsing position in the buffer
        self._receive_buffer_size = 0          # Amount of bytes currently filled in the buffer (the rest is meaningless)

        # Parser: Next message
        self._next_msg = None
        self._next_msg_pos = 0                 # Parsing position in the currently parsed message (0 = status)
        self._next_msg_num_bytes = -1          # Number of bytes for the currently parsed type. -1 means 
                                               # SysEx terminated by 0xf7.

    # Returns the next available message or None if the buffer is empty. Allows any length of 
    # sysex messages to be received.
    def receive(self):
        # Start a message.
        def start_msg(status_byte, num_bytes):
            self._next_msg = bytearray([status_byte])
            self._next_msg_pos = 0
            self._next_msg_num_bytes = num_bytes

        # Terminates the parsing of the current message and returns it.
        def end_msg():
            msg = self._next_msg
            self._next_msg = None
            return msg

        # Start parsing a new message if a valid status byte has been passed.
        #
        # NOTE: The order of checks regards the fact that on smaller devices no live playing
        #       or real audio synthesis takes place, so CC/PC/Sysex will be the 
        #       most used messages, so these are checked first for slightly better 
        #       performance.
        def parse_status(byte):
            # CC/PC/Sysex
            if byte & 0xF0 == 0xB0: start_msg(byte, num_bytes = 3)          # CC
            elif byte & 0xF0 == 0xC0: start_msg(byte, num_bytes = 2)        # PC
            elif byte == 0xF0: start_msg(byte, num_bytes = -1)              # SysEx

            # Common "live playing" messages with channel
            elif byte & 0xF0 == 0x90: start_msg(byte, num_bytes = 3)        # Note On
            elif byte & 0xF0 == 0x80: start_msg(byte, num_bytes = 3)        # Note Off
            elif byte & 0xF0 == 0xE0: start_msg(byte, num_bytes = 3)        # Pitch bend
            elif byte & 0xF0 == 0xD0: start_msg(byte, num_bytes = 2)        # Channel pressure
            elif byte & 0xF0 == 0xA0: start_msg(byte, num_bytes = 3)        # Poly pressure
            
            # Other system messages with data bytes
            elif byte == 0xf1: start_msg(byte, num_bytes = 3)               # MIDI Quarter Frame
            elif byte == 0xf2: start_msg(byte, num_bytes = 3)               # Song Position Pointer
            elif byte == 0xf3: start_msg(byte, num_bytes = 2)               # Song Select

            # Other system messages without arguments: These have the status byte as type and no data.
            elif byte & 0x80: start_msg(byte, num_bytes = 1)

        # Parse the stream. The instance walks through the bytes and remembers the current
        # parsing state in the _next_msg field, which will finally be returned if 
        # fully parsed. The parsing of one message therefore can also span multiple
        # read blocks as the message is held in memory, which allows any length of message.
        # The RAM usage ultimately depends on the message length.
        def parse():
            while True:
                # Check if there is a completed message
                if self._next_msg and self._next_msg_pos == self._next_msg_num_bytes - 1:
                    return end_msg()

                # Are there any bytes left in the receive buffer?
                if self._receive_buffer_pos >= self._receive_buffer_size:
                    # No more bytes
                    return None

                # Get next byte from buffer
                byte = self._receive_buffer[self._receive_buffer_pos]
                self._receive_buffer_pos += 1

                # Evaluate the byte
                if self._next_msg:
                    # We are currently parsing a message which needs at least one byte of data
                    if self._next_msg_num_bytes != -1:
                        # Fixed length: Append byte to message data.
                        if byte < 0x80:
                            self._next_msg.append(byte)
                            self._next_msg_pos += 1
                    else:
                        # SysEx: Check for termination (EOX)
                        if byte < 0x80:
                            self._next_msg.append(byte)
                        elif byte == 0xf7:
                            self._next_msg.append(byte)
                            return end_msg()

                else:
                    # Currently no message is parsed: Check for start bytes (Status),
                    # and start parsing a new message if we have a valid status byte.
                    parse_status(byte)

        ##################################################################################################

        # If there are bytes left in the last chunk, we continue parsing there first.
        ret = parse()

        # Message found: Return it
        if ret:
            # print(f"Parsed {list(ret)}")
            return ret
        
        # Buffer empty or no message found: Read next bytes into the receive buffer
        # and try again
        self._receive_buffer_size = self._midi_in.readinto(self._receive_buffer) or 0
        # if self._receive_buffer_size != 0:
        #     print(f"Received {list(self._receive_buffer[:self._receive_buffer_size])}")
        self._receive_buffer_pos = 0

        ret = parse()
        if ret:
            # print(f"Parsed {list(ret)}")
            return ret

    # Sends a message. The format is described in the class comments. Returns if sending was processed. 
    def send(self, message):
        if not message:
            return False
        
        self._midi_out.write(bytes(message), len(message))        
        return True

## Helpers for programs using this buffer ##############################################################

# Creates a sysex message
def sysex(manufacturer_id, data):
    return bytearray((240,) + tuple(manufacturer_id) + tuple(data) + (247,))
