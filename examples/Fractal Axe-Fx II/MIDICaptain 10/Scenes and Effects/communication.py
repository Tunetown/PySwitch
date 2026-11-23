##############################################################################################################################################
#
# Definition of communication wrappers. This is where the client specific (i.e. Kemper) implementations are linked to the framework.
#
##############################################################################################################################################

from pyswitch.controller.midi import MidiRouting
from pyswitch.hardware.devices.pa_midicaptain import PA_MIDICAPTAIN_DIN_MIDI

# MIDI Devices. The Axe-Fx II is connected via DIN MIDI (its USB port is a USB device, like the one of the MIDI Captain).
_DIN_MIDI = PA_MIDICAPTAIN_DIN_MIDI()

# Communication configuration. No protocol is set: the Axe-Fx II is polled in every update interval.
Communication = {

    # MIDI setup. This defines all MIDI routings. You at least have to define routings from and to
    # the MidiController.PYSWITCH source/target or the application will not be able to communicate!
    "midi": {
        "routings": [
            # Application: Receive MIDI messages from DIN
            MidiRouting(
                source = _DIN_MIDI,
                target = MidiRouting.APPLICATION
            ),

            # Application: Send MIDI messages to DIN
            MidiRouting(
                source = MidiRouting.APPLICATION,
                target = _DIN_MIDI
            ),
        ]
    }
}
