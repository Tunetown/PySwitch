# PySwitch MIDI Controller Firmware

This project provides an open source firmware for CircuitPython Microcontroller based MIDI controllers. It can control devices via MIDI based on a generic configuration script. 

The project has been developed for controling Kemper Profilers, but the framework itself is generic, so it can be adapted for other devices easily. Until now, the following devices are supported out of the box:

- Kemper Profilers (Head, Rack, Stage, Player etc.)
- Boomerang III Phrase Sampler

Features are:

- Program (Foot)switches and expression pedals to send MIDI messages. Each switch or pedal can do any amount of actions. Programming is done by setup scripts or graphically using a MIDI enabled, web based configuration tool, with lots of examples.

- Establishes a bidirectional communication to reflect the states correctly when changed on the Kemper.

- Free MIDI routing capatbilities for MIDI over USB and/or DIN

![Overview Image](https://github.com/user-attachments/assets/c48903b2-a5f7-4d78-b7eb-9fca98dbfbe0)

## Installation

1. Connect you device to your computer via USB and power it up. For PaintAudio MIDICaptain controllers, press and hold switch 1 while powering up to tell the controller to mount the USB drive.
2. On your computer, you should now see the USB drive of the device (named MIDICAPTAIN for Paintaudio controllers, CIRCUITPY for generic boards)
3. Delete the whole content of the USB drive. For PaintAudio devices, dont forget to save the contents on your hard drive (especially the license folder) if you perhaps want to restore the original manufacturer firmware later.
4. Copy everything inside the "content" folder of the project to the root folder on your device drive (named MIDICAPTAIN or CIRCUITPY).
5. Unmount the USB drive (important: wait until the drive really is unmounted, or it will sometimes forget everything again).
6. Reboot the device. 
7. Per default, PySwitch is configured for the PaintAudio MIDICaptain STD. Launch the [PySwitch Emulator](https://pyswitch.tunetown.de) in your Web Browser AFTER the device has been booted completely. It will automatically connect to the controller, you can then choose an example as a starting point (see the load button on the top left) and save it to your controller via the Save button -> Connected Controllers.
8. Connect the controller to your Kemper (or other client).

**NOTE**: If the Save button does not show any connected controllers, your browser might not support Web MIDI (currently, for example Safari does not support this). In this case, you have to:
- After creating your config in the Emulator, download it (see Save -> Download (ZIP)).
- Mount your controller as USB drive (see Installation process), and put the files downloaded in the root folder of it (overwrite existing files).

**NOTE**: If you want to run PySwitch in parallel with the original PaintAudio firmware, see below chapter "Multi-Boot"

## Configuration

If you do not want to program your configuration yourself in Python (as described later) which offers any needed degree of freedom, you can also use the new [**PySwitch Emulator**](https://pyswitch.tunetown.de) to graphically create and test your patch easily:

![image](https://github.com/user-attachments/assets/55270c26-ead9-4d66-a782-ff293bfe2abf)

You can even control your actual Kemper from the browser to pre-test everything before flashing it to a connected device :) for more details see [this README](web/README.md).

## Motivation

The firmware has been developed to interface the PaintAudio MIDI Captain series of MIDI controller pedals to the Kemper Profiler Player, which can be controlled very deeply via MIDI. It is based on the great explorational work of @gstrotmann who did a good part of hardware reverse engineering (https://github.com/gstrotmann/MidiCaptain4Kemper). 

On the Kemper forums, the following thread is dedicated to the project:

https://forum.kemper-amps.com/forum/thread/65206-pyswitch-an-alternative-customizable-firmware-for-paintaudio-midi-captain-contro/

The manufacturer PaintAudio also provides a Kemper Player related firmware (<a href="https://cdn.shopify.com/s/files/1/0656/8312/8548/files/FW_MINI6_KPP_V3.51.zip?v=1711205983" target="_blank">PaintAudio firmware 3.5</a>) but this is hard wired all along and missing features. However, the open architecture of the controller also makes it possible to be more flexible.

This project is developed generically, so it can basically be run on any board which runs CircuitPy, using the Adafruit libraries to run a TFT display and LEDs, to control basically any device which is controlled in a similar way as the Kemper devices and address any parameter or other information the controlled device provides. You just have to provide the apropriate adapter classes and mappings! 

It would particularly be nice to add support for Line6 and FRactal devices, if anybody owning the one of them wants to be part of the project, we could implement that easily. Just reach me on the Kemper forum (see thread above).

## Startup Options

When the controller device is powered up with the pyswitch firmware installed, you have the following options:
- Press and hold switch 1 to mount the USB drive.

## Configuration Files

Most of the time you will configure PySwitch using the [Emulator](https://pyswitch.tunetown.de). Under the hood, the actual configuration is done in some files in the root directory (of the device drive). These are all python scripts and follow the corresponding syntax rules. 

- **inputs.py**: Defines which action(s) are triggered when a switch is pushed or an expression pedal is moved.
- **display.py**: Defines the layout of the TFT display and which data to show
- **config.py**: Global configuration (MIDI channel, processing control, debug switches). This is not edited by the emulator.
- **communication.py**: Defines the communication with the client, as well as generic MIDI routing between available MIDI ports. This is not edited by the emulator.

These files can make use of the objects contained in the **lib/pyswitch/clients/kemper** module which provide lots of mappings for the Kemper devices. This is currently only tested with the Profiler Player, but the MIDI specification is the same for most parts. Additional functionality for the Toaster/Stage versions can be added in kemper.py later if needed. Note that for using other devices than the Player you have to adjust the NRPN_PRODUCT_TYPE value accordingly (which should be the only necessary change). Contributors welcome!

*Technical note: The pyswitch module does not import any of the files in the root folder directly. The code.py script (which is the CircuitPy entry point) loads all configuration by importing pyswitch/process.py*

## Using an external IDE

Using the "Open Directory..." option in the Load menu at the top left, the configuration files in the folder (inputs.py and display.py) are synced automatically when changed from external editors. This way, you can integrate your favorite IDE: The Emulator automatically refreshes when changes have been made. From the emulator, CTRL-S directly saves the files to the opened folder.

Of course you have to grant the website to edit the opened folder when asked.

### Global configuration

The file **config.py** contains the global device configuration, and only defines one dictionary named "Config", which is empty by default. Please refer to the comments in the delivered config.py file for all available options and their defaults.

### Switch Assignment

The file **inputs.py** must provide an "Inputs" list holding all switch assignments. A switch definitions consists of a dict with the following entries:
	
- **"assignment"**: Assignment to the hardware switch and corresponding LED pixels. Must be a dict. You can specify this manually, however it is recommended to use the predefined assignments in lib/pyswitch/hardware/hardware.py. Must contain the following entries:

    - **"model"**: Instance capable of reporting a switch state (reading a board GPIO). Use AdafruitSwitch from lib/pyswitch/hardware/adafruit.py
    
    - **"pixels"**: Tuple of pixel indices assigned to the switch, for example (0, 1, 2) for the first three LEDs. NeoPixels are controlled by index, and for example the PaintAudio MIDICaptain devices feature three LEDs per switch which can be addressed separately.
    
    - **"name"**: Optional name for debugging output

- **"actions"**: List of actions to be triggered by the switch, see below.

- **"actionsHold"**: List of actions to be triggered by the switch on holding, see below.

#### Switch Actions

Example for assigning switch 1 of a MIDICaptain Nano 4 to switching the Kemper effect slot A on or off:

```python
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE

Inputs = [
	{
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A
            ),

            # ... Define further actions for switch 1 here
        ]
    },

    # ... Define further switches here
]
```

##### Actions on Long Press (Hold)

You can assign different actions to long pressing of switches. This is done by providing the "holdActions" parameter of the switch definitions:

```python
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE

Inputs = [
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A
            )
        ],
        "actionsHold": BANK_UP(
            #use_leds = False
        )
    },

    #... Define further switches here
]
```

*NOTE: The LEDs of the switch will be shared among the actions participated. If you want just one action to use all LEDs of a switch, you can switch the usage off for an action using the use_leds parameter, for example with the hold action, so only the normal action will use the LEDs.*

*NOTE: Do not assign the same display label to the actions, this does not make sense and will result in erratic output.*


##### Pushbutton Modes

Most actions feature a "mode" parameter. This parameter controls the behaviour of the switch as defined here:

- **PushButtonAction.ENABLE**: Switch the functionality on (always, no switching off again!)
- **PushButtonAction.DISABLE**: Switch the functionality off (always, no switching on again)
- **PushButtonAction.LATCH**: Toggle state on every button push
- **PushButtonAction.MOMENTARY**: Enable on push, disable on release
- **PushButtonAction.HOLD_MOMENTARY**: Combination of latch, momentary and momentary inverse: If pushed shortly, latch mode is used. If pushed longer than specified in the "holdTimeMillis" parameter, momentary mode is used (inverse or not: This depends on the current state of the functionality. When it is on, it will momentarily be switched off and vice versa). This is the default for most of the actions.
- **PushButtonAction.ONE_SHOT**: Fire the SET command on every push (show as disabled)
- **PushButtonAction.NO_STATE_CHANGE**: The action is not connected to the switch at all. Use this for example to drive displays showing rig ID or effect state without a dedicated switch. (all actions need to be assigned to a switch, so this is the workaround here)

Each switch can be assigned to any number of actions, which are implementing the functionality for the switch. Actions are instances based on the lib/pyswitch/controller/actions/Action base class. Normally you would use predefined actions as provided by lib/pyswitch/clients/kemper/actions, however you could also directly use the classes defined in lib/pyswitch/controller/actions.py and provide all the MIDI mapping manually.

##### Action Colors

Most actions provide a color option: If set, this defines the color for switch LEDs and an eventual display label. For example, the following example creates a rig select action shown in purple:

```python
from pyswitch.clients.kemper.actions.rig_select import RIG_SELECT

Inputs = [
	{
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            RIG_SELECT(
                rig = 1,
                display_mode = RIG_SELECT_DISPLAY_TARGET_RIG,
                color = (180, 0, 120)    # (R, G, B)
            )
        ]
    }
]
```

### Continuous Inputs

Continuous controllers like expression pedals and rotary encoders can also be added to the "Inputs" list in **inputs.py**, using the appropriate models from lib/pyswitch/hardware/hardware.py. However, the actions are different than with switches.

#### Expression Pedals (Analog In)

For anything using the analog inputs of the board (like expression pedals), you have to use a AnalogAction instance like in this example:

```python
from pyswitch.controller.actions.AnalogAction import AnalogAction
from pyswitch.clients.kemper.mappings.rig import MAPPING_RIG_VOLUME

Inputs = [
    # Pedal 1
    {
        "assignment": Hardware.PA_MIDICAPTAIN_10_EXP_PEDAL_1,
        "actions": [
            AnalogAction(
                mapping = MAPPING_RIG_VOLUME(),
                auto_calibrate = True
            )
        ]
    },

    # Switch 1
    {
        # ...
    },

    # ...
]
```

This definition would control the rig volume by expression pedal 1 of the PaintAudio MIDI Captain (10 switch version only).

There are several options to AnalogAction:
- **auto_calibrate**: If this is True (which is the default), the pedal controller will permanently do auto-calibration. Before the pedal is moved the first time, nothing is changed. When you rock the pedal up and down once, the switch remembers the min/max positions and adjusts output values to fill the whole range. This is similar to the Kemper auto-calibration. To reset, reboot the controller.
- **cal_min_window**: If aut-calibration is enabled, this defines how big the window between min/max values has to be before any MIDI messages are being sent. Per default, this is set to 25% of the full range of values.
- **max_frame_rate**: To not overload the MIDI traffic, the controller only sends values to the device at a certain frame rate. This defines this rate in frames per second (default: 24)
- **max_value**: Most NRPN parameters have a value range of 0..16383, which is the default here. If you want to use mappings using a ControlChange message, you have to set this to 127.
- **num_steps**: The full range of values to be sent via MIDI is divided into steps, to reduce MIDI traffic further. The analog IO pins always fluctuate by a very small amount even if the pedal is not moved, this option prevents all of these redundant values to be sent. A good value is 128 which is the default, and splits the range into 128 steps which is enough for most pedal applications.
- **enable_callback**: See the switch actions, this can be used the same way with the same callbacks (e.g. for paging)
- **transfer_function**: Here you can pass a transfer function which is used to transform the incoming raw values in range [0..65535] to the output range needed. This overrides the max_value and num_steps parameters. Note that even if max_value is not needed for calculation, it defines the maximum out value nevertheless, so you have to set it.


#### Rotary Encoders (Wheels)

For rotary encoders like the wheel on the PaintAudio MIDI Captain (10 switch version), use EncoderAction:

```python
from pyswitch.controller.actions.EncoderAction import EncoderAction
from pyswitch.clients.kemper.mappings.amp import MAPPING_AMP_GAIN

Inputs = [
    # Wheel
    {
        "assignment": Hardware.PA_MIDICAPTAIN_10_WHEEL_ENCODER,
        "actions": [
            EncoderAction(
                mapping = MAPPING_AMP_GAIN()
            )
        ]
    },

    # Switch 1
    {
        # ...
    },

    # ...
]
```

This will let you control the gain with the wheel, relative to the current value.

There are some options to EncoderAction:
- **max_value**: Most NRPN parameters have a value range of 0..16383, which is the default here. If you want to use mappings using a ControlChange message, you have to set this to 127.
- **step_width**: Increment/Decrement for one encoder step. 128 (which is the default) results in 16384 / 128 = 128 steps for NRPN parameters. Set to this to 1 for ControlChange parameters.
- **enable_callback**: See the switch actions, this can be used the same way with the same callbacks (e.g. for paging)

##### Enable/Disable Actions by Callback

All Actions (switch and continuous) can also be defined depending on a parameter or other stuff: For example the switch could be assigned to tapping tempo if the rig name contains the token "TAP", and control effect slot A if not. This is accomplished by defining a custom callback class to enable/disable actions:

```python
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from pyswitch.clients.kemper.actions.tempo import TAP_TEMPO

# Custom callback function
class _RigNameCallback(Callback):
    def __init__(self):
        Callback.__init__(self)

        # You have to define the attribute .mappings as a list of mappings on
        # which your callback depends. This is optional, if you do not need further
        # mappings, just leave that out. If specified, the callback is updated 
        # automatically whenever the parameter of the mapping changes.
        self.mappings = [KemperMappings.RIG_NAME()]

        self._mapping = self.mappings[0]  # Just for internal reference

    # For Action enable/disable callbacks, there must be a enabled(action) method. This has to
    # return True or False for the action passed. For finding your actions, the id is used,
    # as set below.
    def enabled(self, action):  
        rig_name = self._mapping.value

        if action.id == 10:
            # Show Tap when TAP is contained
            return "TAP" in rig_name
        elif action.id == 20:
            # Show Effect Enable for slot A when TAP is not contained
            return "TAP" not in rig_name
        
# Create an instance of the callback here and use it for all actions involved. 
# It is also possible to use multiple instances but this saves some memory.
_enable_callback = _EnableCallback()

# Both actions now get the same callback which switches their states.
Inputs = [
	{
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            TAP_TEMPO(
                id = 10,
                callback = _enable_callback
            ),
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A,
                id = 20,
                callback = _enable_callback
            )
        ]
    },

    # ... Define further switches here
]
```

##### Display Labels for Actions

The last example only uses the switch LEDs to indicate the effect status (brightness) and type (color). You can also connect a display area (defined in **display.py**) to the action, so the effect type (color and name) and state (brightness) are also visualized on screen. This works by importing labels defined in **display.py** and pass them to the display attribute of the action(s):

```python
from pyswitch.clients.kemper.actions.effect_state import EFFECT_STATE
from display import DISPLAY_LABEL_X

Inputs = [
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            EFFECT_STATE(
                slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A,
                display = DISPLAY_LABEL_X,
            )
        ]
    },

    #... Define further switches here
]
```

See below how the labels are defined.

### Custom Callbacks for Actions

Besides the general pushbutton or hold mechanisms, all functionality of the actions is implemented in callbacks. This works similar to the Enable callbacks described above (the mapping definition is the same), but these callbacks have to provide different member functions. The basis of this is the PushButtonAction:

```python
from pyswitch.controller.callbacks import Callback

class CustomCallback(Callback):
    def __init__(self):
        Callback.__init__(self)

        self.mappings = [] # DAdd your needed mappings here or remove line
        
    # This is called then the state changed (on/off, according to the pushbutton and
    # eventually hold modes involved around the action).
    def state_changed_by_user(self, action):
        if action.state == True:
            # ... do something
        else:
            # ... do something

    # This is called to update the visual feedback (display and LEDs)
    # whenever state changed or a mapping has been updated with a new value
    def update_displays(self, action):
        # You can set the display label's properties.
        # Beware that the label can be None if no display
        # has been passed to the action!
        if action.label:
            action.label.back_color = Colors.RED
            action.label.text = "foo"

        # The LED segments can be set with special 
        # properties of the Action base class, which 
        # only control the segments assigned to the 
        # action (see above). 
        #
        # Note that setting the color will not change 
        # anything. You have to set the brightness after
        # for the changes to take effect (even if the 
        # brightness is already set).        
        action.switch_color = (255, 255, 255) # (r, g, b), [0..255]
        action.switch_brightness = 0.8        # [0..1]


Inputs = [
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            PushButtonAction({
                "callback": CustomCallback(),
                "display": # ...
            })                        
        ]
    }
```

### Binary Parameter Actions

To simply switch a parameter in an on/off fashion with values for on and off etc., the BinaryParameterAction is provided (which itself is a callback like in the last chapter). This is used by most of the predefined Kemper action definitions internally. Here an example which switches the rotary speed fast/slow:

```python
Inputs = [
    {
        "assignment": Hardware.PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            PushButtonAction({
                "callback": BinaryParameterCallback(
                    mapping = KemperMappings.ROTARY_SPEED(
                        slot_id = KemperEffectSlot.EFFECT_SLOT_ID_A
                    ),
                    text = "Fast",
                    color = Colors.BLUE
                ),
                "useSwitchLeds": True,   # Must be set to enable the LEDs!
                "display": #....
            })
        ]
    }
]
```

### Custom MIDI Messages

If you want to send your own custom MIDI messages, you can also define your mappings. This example is similar to the "Rig Volume Boost" action:

```python
from pyswitch.controller.callbacks import BinaryParameterCallback
from pyswitch.controller.actions import PushButtonAction
from pyswitch.controller.client import ClientParameterMapping
from adafruit_midi.system_exclusive import SystemExclusive

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            PushButtonAction(
                {
                    "callback": BinaryParameterCallback(
                        mapping = ClientParameterMapping.get(
                            name = "My Boost",   # This name MUST be unique! Use your own custom prefix for example.
                            set = SystemExclusive(
                                manufacturer_id = [0x00, 0x20, 0x33], 
                                data = [0x02, 0x7f, 0x01, 0x00, 0x04, 0x01] # Two value bytes will be added by PySwitch
                            ), 
                            request = SystemExclusive(
                                manufacturer_id = [0x00, 0x20, 0x33], 
                                data = [0x02, 0x7f, 0x41, 0x00, 0x04, 0x01]
                            ), 
                            response = SystemExclusive(
                                manufacturer_id = [0x00, 0x20, 0x33], 
                                data = [0x02, 0x7f, 0x01, 0x00, 0x04, 0x01] # Two value bytes will be evaluated by PySwitch
                            )
                        ), 
                        color = (255, 100, 0), 
                        text = "Rig Vol", 
                        value_enable = 12000,    # Value set on enable state
                        value_disable = "auto",    # Value set on disable state
                        reference_value = 12000, # Value to compare incoming messages, to determine the state of the switch (on or off)
                        comparison_mode = BinaryParameterCallback.GREATER_EQUAL
                    ),
                    "display": DISPLAY_HEADER_1,
                    "useSwitchLeds": True,
                    "mode": PushButtonAction.HOLD_MOMENTARY,  # Pushbutton mode                    
                }
            )            
        ]       
    }
]
```

If you want only to send but not receive, you have to set the internal state enabled like in this example, which does not listen to the client at all but just sends messages:

```python
from pyswitch.controller.callbacks import BinaryParameterCallback
from pyswitch.controller.actions import PushButtonAction
from pyswitch.controller.client import ClientParameterMapping
from adafruit_midi.system_exclusive import SystemExclusive

Inputs = [
    {
        "assignment": PA_MIDICAPTAIN_NANO_SWITCH_1,
        "actions": [
            PushButtonAction(
                {
                    "callback": BinaryParameterCallback(
                        mapping = ClientParameterMapping.get(
                            name = "My Boost",   # This name MUST be unique! Use your own custom prefix for example.
                            set = SystemExclusive(
                                manufacturer_id = [0x00, 0x20, 0x33], 
                                data = [0x02, 0x7f, 0x01, 0x00, 0x04, 0x01] # Two value bytes will be added by PySwitch
                            )
                        ), 
                        color = (255, 100, 0), 
                        text = "Rig Vol", 
                        value_enable = 12000,    # Value set on enable state
                        value_disable = 8192,    # Value set on disable state
                        use_internal_state = True
                    ),
                    "display": DISPLAY_HEADER_1,
                    "useSwitchLeds": True,
                    "mode": PushButtonAction.HOLD_MOMENTARY,  # Pushbutton mode                    
                }
            )            
        ]       
    }
]
```

For a complete list of options, see these two classes:

- pyswitch/controller/actions/PushbuttonAction
- pyswitch/controller/callbacks/BinaryParameterCallback

The name of the mapping MUST be unique. Please choose a name not occurring anywhere else, or use the Python uuid module to generate an unique ID.

### TFT Display Layout Definition

The file **display.py** must provide a callback instance which returns the screen content to show, possibly depending on mappings or other criteria. The callback must provide a get_root() method which must return the DisplayElement to show:

```python
# Layout used for the action labels (only used here locally)
_ACTION_LABEL_LAYOUT = {
    "font": "/fonts/H20.pcf",
    "backColor": DEFAULT_LABEL_COLOR,
    "stroke": 1
}

# Labels to be used by **inputs.py**: Header
DISPLAY_HEADER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, 0, 120, 40)
)
DISPLAY_HEADER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(120, 0, 120, 40)
)

# Footer
DISPLAY_FOOTER_1 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(0, 200, 120, 40)
)
DISPLAY_FOOTER_2 = DisplayLabel(
    layout = _ACTION_LABEL_LAYOUT,
    bounds = DisplayBounds(120, 200, 120, 40)
)

class _SplashCallback(Callback):
    def get_root(self):
        return DisplayElement(
            bounds = DisplayBounds(0, 0, 240, 240),
            children = [        
                # Header area
                DISPLAY_HEADER_1,
                DISPLAY_HEADER_2,

                # Footer area
                DISPLAY_FOOTER_1,
                DISPLAY_FOOTER_2,

                # Rig name
                DisplayLabel(
                    bounds = DisplayBounds(0, 40, 160, 40)  # x, y, width, height
                    layout = {
                        "font": "/fonts/PTSans-NarrowBold-40.pcf",
                        "lineSpacing": 0.8,
                        "maxTextWidth": 220,
                    },
                    callback = KemperRigNameCallback()    
                ),

                # ... Define further elements here
            ]
        )

Splashes = _SplashCallback()
```

The areas are stacked in the defined order, elements defined down the list will overlap the upper ones. 

This example defines three display areas:

- A header and a footer consisting of two labels each

- A rig name display

All available area types are defined in lib/pyswitch/ui/elements/elements.py, see there for more details on parameters for the available types:

- **DisplayLabel**: Just a label showing text over a background. 
- **BidirectionalProtocolState**: A small black dot showing the state of the bidirectional communication protocol (green/red)

Display of values (like rig name) is done via callbacks, see below chapters about DisplayLabel.

##### Tuner Display

For the most popular case of showing a tuner display when the device goes into tuner mode, there is a ready made callback:

```python
Splashes = TunerDisplayCallback(
    strobe = True,
    splash_default = DisplayElement(
        bounds = ...,
        children = [
            # ... Display elements for normal display go here
        ]
    )
)
```

This shows a tuner display when tuner mode is enabled:

![image](https://github.com/user-attachments/assets/f4ba454f-b8a2-403c-b6b0-962a80dc9137)

###### Strobe Tuner

The strobe parameter (which defaults to True) will use all available LEDs of the device as strobe tuner. There are several parameters to TunerDisplayCallback controlling the strobe tuner:

- **"strobe_color":** Color to be used for the LEDs
- **"strobe_dim":** Dim factor for the strobe LEDs in range [0..1]. Default is 0.1
- **"strobe_speed":** Determines the speed. Higher values make the strobe tuner go slower. 1000 is the recommended speed to start from. 
- **"strobe_max_fps":** Maximum cumulative frame rate for update of strobe tuner LEDs. Reduce this to save processing power. The number will be divided by the amount of available switches to get the real max. frame rate (that's why it is called cumulative).
- **"strobe_reverse":** Determines the rotation direction. If False, the strobe is rotating clockwise when too high / ccw when too low. If True, the other way round (which is the default). 

*NOTE: If you encounter memory problems, disable strobe as this will save you some kilobytes.*

### Mappings

The MIDI messages to set/request parameters from the device are bundled in Mappings. A mapping (see class ClientParameterMapping) can contain the following (each can be one instance or a list of instances):
- **set**: MIDI message(s) to be used to set the parameter (value will be overridden with the real value before sending)
- **request**: MIDI message(s) to request the parameter from the device. Only used for non-bidirectional mappings.
- **response**: MIDI message(s) template to be used to compare incoming MIDI messages to. Defines how the device receives the parameter value.

See the ClientParameterMapping class for deeper details.

#### Kemper Mappings

The file **lib/pyswitch/clients/kemper.py** contains predefined mappings to be used in the switches and displays configurations. These include the most usual parameters already, if you need more than that you can either define them manually or add new mappings to kemper.py (recommended).

#### DisplayLabel Layout Definition

Layouts for DisplayLabel and related types are defined as dict. Here is an example showing all possible options:

```python
example_layout = {
    # Path to the font in PCF format (mandatory). A lot of fonts are
    # available at https://github.com/adafruit/circuitpython-fonts
    "font": "/fonts/H20.pcf",   
                                
    # Maximum text width in pixels (optional) for wrapping text
    "maxTextWidth": 220,        

    # Line spacing (optional, default is 1)
    "lineSpacing": 1,           

    # Text color (default is None, which will derive a contrasting
    # color automatically)
    "textColor": (255, 120, 0),                               

    # Background color (default is None) Can be a tuple also to 
    # show a rainbow background with multiple colors, 
    # for example (Colors.GREEN, Colors.YELLOW, Colors.RED)
    "backColor": (30, 30, 30), 
                                
    # Ouline stroke (optional, default is 0). Width of the 
    # optional outline. The outline is only "faked" for sake of memory 
    # usage (just the background is reduced in size)
    "stroke": 1,
                                
    # Initial text (default is None).
    "text": "Initial Text"      
}
```

#### Display Label Callbacks

For example if you want to show some custom text or a parameter value in a display label independent of an action or switch, this can be used by passing a callback to DisplayLabel. See example "Freeze and Tap Tempo" for the PaintAudio MIDICaptain NANO 4 which includes a custom callback for showing the current amp name.

### MIDI Communication Setup

The **communication.py** file defines the handling of MIDI data. This includes the MIDI routing. It must contain a "Communication" dictionary like follows:

```python
_USB_MIDI = MidiDevices.PA_MIDICAPTAIN_USB_MIDI(
    in_channel = None,  # All channels will be received
    out_channel = 0     # Send on channel 1
)

Communication = {

    # MIDI setup. This defines all MIDI routings. You at least have to define routings from and to 
    # the MidiController.PYSWITCH source/target or the application will not be able to communicate!
    "midi": {
        "routings": [
            # Application: Receive MIDI messages from USB
            MidiRouting(
                source = _USB_MIDI,
                target = MidiController.APPLICATION
            ),

            # Application: Send MIDI messages to USB
            MidiRouting(
                source = MidiController.APPLICATION,
                target = _USB_MIDI
            )
        ]
    }
}
```

"routings": Must define the routes which MIDI data can take in your scenario. The example above defines the minimal necessary routings to run the application. If you do not provide any routings, the application will not be able to communicate to the outer world. Every route must be a MisiRouting instance, and represents the route only in one direction.

You can for example route MIDI data from/to DIN and/or USB ports to realize MIDI through. There is a separate folder with examples for routings, which can be used in combination with any of the other examples.

##### MIDI Routings

A routing has a source and a target, both of which must be instances being able to send and receive MIDI messages. You can use:
- Adafruit's own MIDI handler (adafruit_midi.MIDI)
- The wrappers AdfruitUsbMidiDevice (for USB MIDI) and AdfruitDinMidiDevice (for DIN MIDI) (recommended) which are also used in the example above (wrapped again by MidiDevices, see the source code there)
- The constant MidiController.APPLICATION. This represents the application itself.

This example will, in addition to normal operation as in the last example, also pass all data from DIN Input to USB output (MIDI Through):

```python

# Pre-define all needed MIDI devices here in advance 
# (multiple creation would waste memory)
_DIN_MIDI = MidiDevices.PA_MIDICAPTAIN_DIN_MIDI(
    in_channel = None,  # All channels will be received
    out_channel = 0     # Send on channel 1
)

_USB_MIDI = MidiDevices.PA_MIDICAPTAIN_USB_MIDI(
    in_channel = None,  # All channels will be received
    out_channel = 0     # Send on channel 1
)

Communication = {

    # MIDI setup. This defines all MIDI routings. You at least have to define routings from and to 
    # the MidiController.PYSWITCH source/target or the application will not be able to communicate!
    "midi": {
        "routings": [
            # MIDI Through from DIN to USB
            MidiRouting(
                source = _DIN_MIDI,
                target = _USB_MIDI
            ),

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
```

It is also possible to either route multiple sources to one target or vice verse, to distribute or merge messages. 
The examples also contains samples for setting up MIDICaptain USB and DIN communication as well as MIDI through, or connecting the application to DIN and/or USB MIDI.

**NOTE**: Not all message types are forwarded by default to save memory, only the message types needed for the Kemper devices are enabled:
- ControlChange
- ProgramChange
- SystemExclusive

There are several other types defined in the <a href="https://docs.circuitpython.org/projects/midi/en/latest/" target="_blank">adafruit_midi library</a>. If you need them to be processed, see file lib/pyswitch/hardware/adafruit.py and add the message types you need in the import section at the top (importing the types is sufficient, no further code changes needed). For types not listed (like MIDI Clock) these can be defined manually, see comments.

#### Bidirectional Communication

Some clients like the Kemper devices support a bidirectional communication mode. This wording is a bit misleading because the PySwitch application can react to changes of the client also if this mode is not enabled. However, bidirectional mode will greatly reduce MIDI traffic and improve reaction delays, and for example the Tuner note and deviation infos necessary for the tuner display (see below) are just sent in bidirectional mode, so this is the preferred mode of operation and enabled by default in all examples.

See this chart for some differences between the operation modes:

|                                             | **Non-Bidirectional** | **Bidirectional**    |
|---------------------------------------------|-----------------------|----------------------|
| Reflect changes on the client               | Yes                   | Yes                  |
| Parameter values are requested periodically | Yes                   | No (\*)              |
| Tuner information available                 | No                    | Yes (Note and dev.)  |
| Tempo Messages (for synced blinking LEDs)   | No                    | Yes                  |


*(\*) Bidirectional mode is not available for all parameters. However, you do not need to specify this, the **lib/pyswitch/clients/kemper.py** file contains the definitions looked up by the application.*

To enable bidirectional communication, you have to provide a suitable protocol implementation (instance of BidirectionalProtocol) to the Communication object like follows, using the Kemper specific implementation from **lib/pyswitch/clients/kemper.py**:

```python
Communication = {

    # Optional: Protocol to use. If not specified, the standard Client protocol is used which requests all
    # parameters in each update cycle. Use this to implement bidirectional communication.
    "protocol": KemperBidirectionalProtocol(
        time_lease_seconds = 30               # When the controller is removed, the Profiler will stay in bidirectional
                                              # mode for this amount of seconds. The communication is re-initiated every  
                                              # half of this value. 
    ),

    # ...
}
```

## Development

The sources are all contained in the lib/pyswitch module, which has the following basic structure:

```
/lib/pyswitch/
    clients/
    controller/
    hardware/
    ui/
```

- **controller** contains the main application logic
- **hardware** provides access to the adafruit hardware
- **ui** contains the uiser interface shown on the TFT display
- **clients** provides code specific to clients (like the Kemper devices). This code is not used in the library itself, but in your config files in the drive root. Further client implementations (for Helix or Quad Cortex devices maybe) can be added here. If you want to contribute an implementation, just create it in the drive root, make it work from there, then share it to others by either putting it into the clients folder and creating a pull request, or just send the file over to me and i will integrate it.

The Controller class in the **controller** folder represents the main application controller class which initiates the processing loop. It is used in the process.py file as follows (irrelevant things omitted for clarity):

```python
from pyswitch.hardware.adafruit import AdafruitST7789DisplayDriver, AdafruitNeoPixelDriver, AdafruitFontLoader
from pyswitch.controller import Controller
from pyswitch.controller.midi import MidiController
from pyswitch.ui.UiController import UiController

# Initialize Display first to get console output on setup/config errors (for users who do not connect to the serial console)
display_driver = AdafruitST7789DisplayDriver()
display_driver.init()

# Load global config
from config import Config

# NeoPixel driver 
led_driver = AdafruitNeoPixelDriver()

# Buffered font loader
font_loader = AdafruitFontLoader()

# Load configuration files (this is where the clients specific code is used)
from display import Splashes
from inputs import Inputs
from communication import Communication

# Controller instance (runs the processing loop and keeps everything together)
appl = Controller(
    led_driver = led_driver, 
    communication = Communication, 
    midi = MidiController(
        routings = Communication["midi"]["routings"]
    ),
    config = Config, 
    inputs = Inputs, 
    ui = UiController(
        display_driver = display_driver,
        font_loader = font_loader,
        splash_callback = Splashes
    )
)

appl.process()
```

For each switch definition, an instance of FootSwitchController is created, which manages the actions provided by the Swiches list.

### Processing Loop

The main processing loop runs as follows (only rough overview, there is more to it in Controller.process(), see source):

```python
while True:
    # Update all actions and display areas in periodic intervals
    if self.period.exceeded:
        self.update(round_robin = False)

    # Receive MIDI messages.
    cnt = 0
    while True:
        # Detect switch state changes
        self._process_switches()

        # Reveive the next available MIDI message from the 
        # MIDI input buffer
        midimsg = self._midi.receive()

        # Process the midi message (see Client class)
        self.client.receive(midimsg)

        # Only a certain amount of messages is 
        # processed at once to prevent lags.
        cnt = cnt + 1
        if not midimsg or cnt > self._max_consecutive_midi_msgs:
            break  
```

All things which need to be updated regularily like Actions (to get current states from the Kemper for parameters not in bidirectional mode) or display elements listening to parameters (ParameterDisplayLabel) are registered to the controller instance using add_updateable(), so in the update() method of Controller, all registered Updateables are updated.

### Actions

All actions inherit from the Action base class. This class provides functionality used by all actions:

- Setting color and brightness of the switch LED(s): If a switch contains multiple actions which want to use the LEDs of the switch (self._use_switch_leds is set to True), the LEDs are assigned to each action. The rules are:
    - If only one action wants to set the LED(s), all three LEDs are used for that action.
	- If two actions use the LEDs, one will get LED 1+2 and the other will get LED 3.
	- If three actions use the LEDs, each action gets one LED.
	- If more than three actions exist, only the first three can use LEDs, the others will not show any LED status.

	*NOTE: This describes the behaviour for three LEDs per Switch, however also other amounts can be addressed. This depends on the "pixels" definitions in the port assignments.*

#### PushButtonAction

For most things, we need the push/release states of the hardware switches to be interpreted as latch/momentary etc., so for those we have the PushButtonAction base class which can be run in several modes (usable in all actions derived from it).

This class implements the push and release methods and provides a **state** property. After changing this property, update_displays is called, so you can react to state changes there.

### Parameter Request Handling

The Client class executes all MIDI calls. The BidirectionalClient class adds bidirectional communication on top of this.

#### Register Parameter Mapping

When you want to use a mapping somewhere (as the actions do for example), you have to register all used mappings in advance. This is done by calling register():

```python
def register(self, mapping, listener):
```

This is only relevant for bidirectional mappings, however it is important because you do not know in advance which parameters will become bidirectional at some times (for example when the parameter set is changed), so all mappings should be registered before the bidirectional protocol is initialized.

#### Set Parameter Value

To set a value via MIDI, use the set() method:

```python
def set(self, mapping, value):
```

It expects a mapping instance and the value to be sent.

#### Request Parameter Value

Requesting via NRPN MIDI messages is done like follows:

1. Send a message telling the device that a parameter value should be sent
2. Wait for the answer message and parse it when it arrives

The request method is used for this:

```python
def request(self, mapping, listener):
```

This requests the parameter (sends the REQUEST message of the passed mapping). The passed listener is called when the answer message has arrived. It has to implement these methods:

```python
# Called by the Client class when a parameter request has been answered.
# The value received is already set on the mapping.
def parameter_changed(self, mapping):
    # IMPORTANT: Use mapping.value even if you have your 
    # copy of the mapping referenced somewhere! The clients may
    # have altered it in the process.
    print("Value received: " + repr(mapping.value))

# Called when the client is offline (requests took too long)
def request_terminated(self, mapping):
    pass
```

Bidirectional mappings do not request values but must be able to receive them. Best practice is to implement everything for both modes (call register(), and request values). The request message (even when request() is called) will only be sent if the mapping is not bidirectional.

Internally, for each parameter a ClientRequest instance is created and added to a list of open requests. This differs between the operation modes: 
- In bidirectional mode, requests for bidirectional parameters will be created on register() already and never die. 
- For non-bidirection mappings, the requests will be created when request() is called, and die when the value has been received.

Every incoming MIDI message will be parsed by all open requests. This is the lifetime of a request:

1. Created (either by calling client.request() for non-bidirectional mappings, or at time of calling register() for bidirectional ones)
   When a request for the same mapping comes in at this time, the listener is just added to the existing request.
2. When a value comes in (MIDI message):
    - Tell all listeners that the value has changed by calling parameter_changed() on each listener.
3. When the mapping is not bidirectional, the request will be set to finished, which will trigger the client to clean it up. When the mapping is bidirectional, the request will never be finished and stay forever to receive further values.

### Multi-Boot with Other Firmwares

If you want to (for example) switch to the original PaintAudio firmware's different versions on boot by holding switches, this is possible. You have to do the following steps:

1. Put all files of both PySwitch's content folder (as described in the Installation above) and the original Firmware you want to use on the MIDICAPTAIN drive. All files of both must exist at their correct places. Some files exist in both, in this case it doesnt matter which you take. You have to do this in deep folder by folder, if your computer does not support merging folders.

2. Replace PySwitch's code.py file with one of the examples in the /examples/multiboot folder (or your own). There are several versions: one which features remembering the used firmware from the last boot (takes around 1.5kB of RAM), and some others. Generally, the simpler, the less extra RAM is needed. See the code.py files themselves for comments about which switch does what.

## Explore Mode: Discover unknown IO Ports

The firmware is capable of running on several controllers, even if it has been developed on the PaintAudio MIDICaptain Nano 4. The definitions in hardware.py provide the hardware mappings for known devices (the MC Mini mapping comes from the original script from @gstrotmann):

```python
class Hardware:

    # PaintAudio MIDI Captain Nano (4 Switches)
    PA_MIDICAPTAIN_NANO_SWITCH_1 = { "model": AdafruitSwitch(board.GP1),  "pixels": (0, 1, 2), "name": "1", "strobeOrder": 0 }
    PA_MIDICAPTAIN_NANO_SWITCH_2 = { "model": AdafruitSwitch(board.GP25), "pixels": (3, 4, 5), "name": "2", "strobeOrder": 1 }
    PA_MIDICAPTAIN_NANO_SWITCH_A = { "model": AdafruitSwitch(board.GP9),  "pixels": (6, 7, 8), "name": "A", "strobeOrder": 3 }
    PA_MIDICAPTAIN_NANO_SWITCH_B = { "model": AdafruitSwitch(board.GP10), "pixels": (9, 10, 11), "name": "B", "strobeOrder": 2 }

    # PaintAudio MIDI Captain Mini (6 Switches)
    PA_MIDICAPTAIN_MINI_SWITCH_1 = { "model": AdafruitSwitch(board.GP1),  "pixels": (0, 1, 2), "name": "1", "strobeOrder": 0 }
    PA_MIDICAPTAIN_MINI_SWITCH_2 = { "model": AdafruitSwitch(board.GP25), "pixels": (3, 4, 5), "name": "2", "strobeOrder": 1 }
    PA_MIDICAPTAIN_MINI_SWITCH_3 = { "model": AdafruitSwitch(board.GP24), "pixels": (6, 7, 8), "name": "3", "strobeOrder": 2 }
    PA_MIDICAPTAIN_MINI_SWITCH_A = { "model": AdafruitSwitch(board.GP9),  "pixels": (9, 10, 11), "name": "A", "strobeOrder": 5 }
    PA_MIDICAPTAIN_MINI_SWITCH_B = { "model": AdafruitSwitch(board.GP10), "pixels": (12, 13, 14), "name": "B", "strobeOrder": 4 }
    PA_MIDICAPTAIN_MINI_SWITCH_C = { "model": AdafruitSwitch(board.GP11), "pixels": (15, 16, 17), "name": "C", "strobeOrder": 3 }
```

The "strobeOrder" attribute controls how the strobe tuner uses the switch LEDs to get a rotary movement.

To discover the GPIO wiring of unknown devices (like the other MIDICaptains for example), a separate mode is provided. This can be enabled in config.py:

```python
Config = {    
    # Set this to True to boot into explore mode. This mode listens to all GPIO pins available
    # and outputs the ID of the last pushed one, and also rotates through all available NeoPixels. 
    # Use this to detect the switch assignments on unknown devices. Optional.
    "exploreMode": True
}
```

This can be used to detect which switch is wired to which IO port, and also determine the LED indexing. 

![image](https://github.com/user-attachments/assets/fb213844-b7e8-41fc-8e4d-5dcb97717822)

### Detect IO Port Wiring

All available IO ports (as defined in the board module) the display shows a separate label. When any port is used (switch is pushed) the corresponding label will be highlighted, so the display always shows the IO assignment of the last pressed switch.

### Detect LED Indexing

This works the following way: The program highlights one triplet of LEDs at a time. The triplet highlighted can be increased/decreased with the switches:
	- Every odd switch (green) will decrease the highlighted indices
	- Every even switch (orange) will increase the highlighted indices

The currently highlighted LEDs (white) will be shown in the display below the GPIO labels, so you can read them out to create your own switch definitions. Please, if you do so, share your results! Just send me a message or create an issue, i will add all definitions to the hardware.py file.

NOTE: This mode is currently hard wired for three LEDs per footswitch. However, it also can deliver the needed information for other constellations with some interpretation.

### Debug RAM Issues

The MIDICaptain Nano 4 only has about 200kB of available RAM. This is not much, especially because the display elements take much space. When creating more advanced display layouts, you might run into an error telling that no more memory can be allocated. 

The program provides some rudimentary memory monitoring. Enable this by uncommenting some lines in process.py:

```python
...

from pyswitch.misc import Tools, Memory   # <-- Uncomment this line
Memory.start()                            # <-- Uncomment this line

...
```

The program will report the allocations of memory on console like this:

```
code.py output:
............................................................ Starting with 187.1 KiB of 203.1 KiB                           XXXXXXXXXXXXXX.
Controller: Showing UI ..................................... Allocated 95.6 KiB     <<<<<<<|....... -> 91.6 KiB        45%  XXXXXXX........
Controller: Starting loop .................................. Allocated 37.9 KiB     <<<<<<<|....... -> 53.7 KiB        26%  XXXX...........
```

Every time memory is allocated or released, another message will be generated.

### Debug Performance Issues

If you notify the device does not react immediately sometimes when a switch is pressed, it might be that some action is taking much CPU. You can monitor the processing loop tick time by enabling the "debugStats" option in **config.py**.

### Unit Testing

All code in the content/lib/pyswitch folder is unit tested to a coverage of > 90%, which is important because this is a tool used in live performances, so stability is a must. The test code is organized in the test folder of the project:

```
/content
/test
    /pyswitch         # Test code (test cases and mocks etc.)
    compose.yaml      # Config for docker compose to provide the test environment
    docker-run        # Runner script which starts the docker container and ssh into it
    Dockerfile        # Docker image (based on the official python image, but adds support for coverage.py)
    run               # Shell script to run tests (to be called in the docker terminal created by docker-run)
```

For running the tests, first run the container. From the project folder, run these commands in a shell:

```console
cd test
./docker-run
```

The docker image is built, the container is started and you get a prompt from a bash session inside the container. There, run the tests:

```console
/project/test/run
```

This should give you a result like this:

```console
a8545571c033:/# /project/test/run 
..................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 194 tests in 0.159s

OK
Wrote HTML report to /project/test/report/index.html
```

You should find a coverage report in the test/report folder like this:

![image](https://github.com/user-attachments/assets/c539aaad-704a-44b5-9408-2f19c8d4da67)

## License

(C) Thomas Weber 2025 tom-vibrant@gmx.de

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Trademarks

Kemper, Kemper Profiler, Kemper Profiler Player are trademarks of Kemper GmbH (www.kemper-amps.com)
Midi Captain, Midi Captain Nano 4, Midi Captain Mini 6 are trademarks of PaintAudio (www.paintaudio.com)

## Donate

If you use and like the application, please consider donating to support open source development: <a href="https://www.paypal.com/webapps/mpp/page-not-found?cmd=_s-xclick&hosted_button_id=6WHW7WRXSGQXY" target="_blank">Donate</a> Thanks a lot for appreciating the big efforts to create a fully tested framework free of charge. If you want me to create custom configurations, you can also pm me at the <a href="https://forum.kemper-amps.com/forum/" target="_blank">Kemper forum</a>, my ID is @tunetown
