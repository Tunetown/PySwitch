##############################################################################################################################################
# 
# Definition of communication wrappers. This is where the client specific (i.e. Kemper) implementations are linked to the framework.
#
##############################################################################################################################################

from lib.pyswitch.controller.midi import MidiRouting
from lib.pyswitch.hardware.devices.pa_midicaptain import PA_MIDICAPTAIN_USB_MIDI
from lib.pyswitch.hardware.devices.pa_midicaptain import PA_MIDICAPTAIN_DIN_MIDI

# MIDI Devices in use (optionally you can specify the in/out channels here, too)
_DIN_MIDI = PA_MIDICAPTAIN_DIN_MIDI(
    in_channel = None,  # All
    out_channel = 15
)
# MIDI Devices in use (optionally you can specify the in/out channels here, too)
_USB_MIDI = PA_MIDICAPTAIN_USB_MIDI(
    in_channel = None,  # All
    out_channel = 15
)

# Communication configuration
Communication = {

    # MIDI setup. This defines all MIDI routings. You at least have to define routings from and to 
    # the MidiController.PYSWITCH source/target or the application will not be able to communicate!
    "midi": {
        "routings": [
            # Application: Receive MIDI messages from USB
            MidiRouting(
                source = _USB_MIDI,
                target = MidiRouting.APPLICATION
            ),

            # Application: Send MIDI messages to USB
            MidiRouting(
                source = MidiRouting.APPLICATION,
                target = _USB_MIDI
            ),
            
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
