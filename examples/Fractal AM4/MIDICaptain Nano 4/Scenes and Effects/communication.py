##############################################################################################################################################
#
# Definition of communication wrappers. This is where the client specific (i.e. Kemper) implementations are linked to the framework.
#
##############################################################################################################################################

from pyswitch.controller.midi import MidiRouting
from pyswitch.hardware.devices.pa_midicaptain import PA_MIDICAPTAIN_DIN_MIDI

# MIDI Devices. The AM4 is connected via its 3.5 mm TRS MIDI jacks (the USB ports of the MIDI Captain and the AM4 are
# both USB devices).
_DIN_MIDI = PA_MIDICAPTAIN_DIN_MIDI()

# Communication configuration. No protocol is set: the AM4 is polled in every update interval.
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
