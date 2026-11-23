##############################################################################################################################################
#
# Definition of communication wrappers. This is where the client specific (i.e. Kemper) implementations are linked to the framework.
#
##############################################################################################################################################

from pyswitch.clients.kemper import KemperBidirectionalProtocol

from pyswitch.controller.midi import MidiRouting
from pyswitch.hardware.devices.pa_midicaptain import PA_MIDICAPTAIN_DIN_MIDI, PA_MIDICAPTAIN_USB_MIDI

# MIDI Devices: the Kemper is connected via USB, the Fractal device via DIN MIDI (In and Out)
_DIN_MIDI = PA_MIDICAPTAIN_DIN_MIDI()
_USB_MIDI = PA_MIDICAPTAIN_USB_MIDI()

# Communication configuration
Communication = {

    # Protocol of the Kemper (at most one bidirectional protocol per configuration). The Fractal device
    # is polled in every update interval, as usual.
    "protocol": KemperBidirectionalProtocol(
        time_lease_seconds = 30               # When the controller is removed, the Profiler will stay in bidirectional
                                              # mode for this amount of seconds. The communication is re-initiated every
                                              # half of this value.
    ),

    # MIDI setup. All messages are sent to both devices, and the messages of both devices are received.
    "midi": {
        "routings": [
            # Application: Receive MIDI messages from USB (Kemper)
            MidiRouting(
                source = _USB_MIDI,
                target = MidiRouting.APPLICATION
            ),

            # Application: Send MIDI messages to USB (Kemper)
            MidiRouting(
                source = MidiRouting.APPLICATION,
                target = _USB_MIDI
            ),

            # Application: Receive MIDI messages from DIN (Fractal)
            MidiRouting(
                source = _DIN_MIDI,
                target = MidiRouting.APPLICATION
            ),

            # Application: Send MIDI messages to DIN (Fractal)
            MidiRouting(
                source = MidiRouting.APPLICATION,
                target = _DIN_MIDI
            ),
        ]
    }
}
