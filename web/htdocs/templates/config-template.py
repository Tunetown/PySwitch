##############################################################################################################################################
# 
# Firmware processing configuration. Most options are optional.
#
##############################################################################################################################################

Config = {
    
    # Max. number of MIDI messages being parsed before the next switch state evaluation
    # is triggered. If set to 0, only one message is parsed per tick, which leads to 
    # flickering states sometimes. If set too high, switch states will not be read for too long.
    # A good value is the maximum amount of switches. Default is 10.
    %maxConsecutiveMidiMessages%,

    # Clear MIDI buffer before starting processing. Default is True.
    %clearBuffers%,

    # Max. milliseconds until a request is being terminated and it is
    # assumed that the Kemper device is offline. Optional, default is 2 seconds.
    %maxRequestLifetimeMillis%,

    # Update interval, for updating the rig date (which triggers all other data to update when changed) (milliseconds)
    # and other displays if assigned. 200 is the default.
    %updateInterval%,

    # Amount of bytes that must at least be free at the time processing starts (normally the program requires anther about
    # 10kB for character loading etc., default threshold for the warning is 15kB).
    %memoryWarnLimitBytes%,

    # Enables file transfer via MIDI from and to the device using PyMidiBridge (https://github.com/Tunetown/PyMidiBridge).
    # This costs about 11kB of RAM, so if you run into memory issues, disable this.
    "enableMidiBridge": True,

    # Globally used dim factors for the DisplayLabels. 
    %displayDimFactorOn%,
    %displayDimFactorOff%,

    # Globally used brightness values for the LEDs. 
    # Note that not all action definitions in kemper.py or other client implementations have to regard this! See the
    # parameters of the action definitions in question.
    %ledBrightnessOn%,
    %ledBrightnessOff%,

    ## Fractal Audio Client ##################################################################################################################

    # Model of the Fractal Audio device (model byte of all SysEx messages): 16 (0x10) = Axe-Fx III, 17 (0x11) = FM3, 18 (0x12) = FM9. 
    # Default is 17 (FM3).
    %fractalModel%,

    # Number of presets per bank for the Fractal bank functions (like the Bank Size of the Fractal FC controllers). Default is 5.
    %fractalBankSize%,

    # Fractal preset numbers are shown starting at 000 (0, default) or 001 (1), like the Display Offset setting of the device.
    %fractalPresetDisplayOffset%,

    ## Development Options ###################################################################################################################

    # Debug output is printed to serial console via USB. 
    # See https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-mac-and-linux 

    %debugStats%,                              # Show info about runtime and memory usage periodically every update interval
    %debugStatsInterval%,                      # Update interval for runtime statistics (also affects the performance dot, default is 
                                                      # the "updateInterval" option)
    %debugBidirectionalProtocol%,              # Debug the bidirectional protocol, if any
    %debugUnparsedMessages%,                   # Shows all incoming MIDI messages which have not been parsed by the application.
    %debugSentMessages%,                       # Shows all sent messages
    #"excludeMessageTypes": [ "SystemExclusive" ],    # Types to excude from "debugUnparsedMessage"
    %debugClientStats%,                        # Periodically shows client information (pending requests etc.). "debugStatsInterval" is used as period.

    # When a ClientParameterMapping instance is set here, incoming messages for this mapping will be shown.
    #"debugMapping": MAPPING_MORPH_PEDAL(),

    # Explore Mode: Set this to True to boot into explore mode. This mode listens to all GPIO pins available
    # and outputs the ID of the last pushed one, and also rotates through all available NeoPixels. 
    # Use this to detect the switch assignments on unknown devices. Optional.
    %exploreMode%
}
