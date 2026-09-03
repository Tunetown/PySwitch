from js import externalRefs

class WrapMidiInput:    
    def __init__(self):
        self._buffer = bytearray()

    def read(self, num_bytes = 0):
        buf = bytearray(num_bytes or 100)
        bytes = self.readinto(buf, num_bytes)
        return buf[:bytes]

    def readinto(self, buffer, num_bytes = 0):
        if not "midiWrapper" in externalRefs.to_py() or not externalRefs.midiWrapper:
            return None

        # Get all data from the message queue into the local linear buffer
        while len(externalRefs.midiWrapper.messageQueue) > 0:
            m = externalRefs.midiWrapper.messageQueue.pop(0)
            self._buffer.extend(bytes(m))

            self._monitor(m)
        
        if num_bytes <= 0:
            num_bytes = len(buffer)

        # Read bytes to the output buffer
        pos = 0
        while len(self._buffer) > 0 and pos < num_bytes:
            buffer[pos] = self._buffer.pop(0)
            pos += 1

        return pos
            
    def _monitor(self, msg):
        if not "midiMonitor" in externalRefs.to_py():
            return

        externalRefs.midiMonitor.monitorInput(msg)


class WrapMidiOutput:
    def write(self, packet, length):
        if not "midiWrapper" in externalRefs.to_py() or not externalRefs.midiWrapper:
            return
        
        self._monitor(packet)
        externalRefs.midiWrapper.send(packet)

    def _monitor(self, msg):
        if not "midiMonitor" in externalRefs.to_py():
            return
         
        externalRefs.midiMonitor.monitorOutput(msg)


