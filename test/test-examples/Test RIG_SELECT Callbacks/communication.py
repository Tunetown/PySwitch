##############################################################################################################################################
# 
# Definition of communication wrappers. This is where the client specific (i.e. Kemper) implementations are linked to the framework.
#
##############################################################################################################################################

from pyswitch.clients.kemper import KemperBidirectionalProtocol

from pyswitch.controller.MidiController import MidiController, MidiRouting
from pyswitch.hardware.Hardware import Hardware

# MIDI Devices in use (optionally you can specify the in/out channels here, too)
#_DIN_MIDI = Hardware.PA_MIDICAPTAIN_DIN_MIDI(
#    in_channel = None,  # All
#    out_channel = 0
#)
_USB_MIDI = Hardware.PA_MIDICAPTAIN_USB_MIDI(
    in_channel = None,  # All
    out_channel = 0
)

# Communication configuration
Communication = {

    # Optional: Protocol to use. If not specified, the standard Client protocol is used which requests all
    # parameters in each update cycle. Use this to implement bidirectional communication.
    "protocol": KemperBidirectionalProtocol(
        time_lease_seconds = 30               # When the controller is removed, the Profiler will stay in bidirectional
                                              # mode for this amount of seconds. The communication is re-initiated every  
                                              # half of this value. 
    ),

    # MIDI setup. This defines all MIDI routings. You at least have to define routings from and to 
    # the MidiController.PYSWITCH source/target or the application will not be able to communicate!
    "midi": {
        "routings": [
            # MIDI Through from DIN to USB
            #MidiRouting(
            #    source = _DIN_MIDI,
            #    target = _USB_MIDI
            #),
            
            ###################################################

            # Application: Receive MIDI messages from USB
            MidiRouting(
                source = _USB_MIDI,
                target = MidiController.APPLICATION
            ),

            # Application: Send MIDI messages to USB
            MidiRouting(
                source = MidiController.APPLICATION,
                target = _USB_MIDI
            ),
        ]
    }
}
