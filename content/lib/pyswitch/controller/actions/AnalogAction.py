from ...misc import PeriodCounter, Updateable

from adafruit_midi.system_exclusive import SystemExclusive

class AnalogAction(Updateable):
    
    # Use this action for all analog inputs like expression pedals.
    def __init__(self, 
                 mapping,                           # Parameter mapping to be controlled
                 max_frame_rate = 24,               # Maximum frame rate for sending MIDI values (fps)
                 max_value = None,                  # Maximum value of the mapping (16383 for NRPN, 127 for CC) Set this to None to auto-detect these ranges.
                 num_steps = 128,                   # Number of steps to be regarded as different (saves MIDI traffic at the cost of precision).
                 enable_callback = None,            # Callback to set enabled state (optional). Must contain an enabled(action) function.
                 id = None,
                 auto_calibrate = False,            # Auto-calibrate (similar to Kemper devices)
                 cal_min_window = 0.25,             # Minimum calibration range in percent [0..1]. A value of 0.25 means that the pedal has to cover at least 25% of the full range to be regarded.
                 transfer_function = None,          # Transfer function. Input is the raw encoder value in range [0..65535]. Must return the value to be sent for 
                                                    # the mapping, in its range. If used, this disables the num_steps and max_value parameters.
                                                    # 
                                                    # NOTE: When designing your transfer function, take care that the output values do not change too often as this 
                                                    # imposes performance issues!
                 change_display = None,             # If assigned, the adjusted value will be displayed in the passed DisplayLabel when the pedal is adjusted. 
                 change_timeout_millis = 1500,      # This is the amount of time (milliseconds) after which the preview display will return to its normal state.
                 convert_value = None,              # Optional conversion routine for displaying values: (value) => string
                 min_raw_value = 1024               # Optional minimum raw value threshold for stable zero
        ):
        if isinstance(mapping.set, SystemExclusive):
            if max_value == None:
                max_value = 16383
        else:
            if max_value == None:
                max_value = 127
        
        self.id = id
        self.__mapping = mapping
        self.__factor = 65536 / (max_value + 1)
        self.__max_value = max_value
        self.__period = PeriodCounter(1000 / max_frame_rate)
        
        self.__enable_callback = enable_callback
        if self.__enable_callback:
            self.__enable_callback.action = self

        self.__step_width = int(65536 / num_steps)
        self.__last_value = -1
        self.__transfer_function = transfer_function
        self.__convert_value = convert_value
        
        self.__calibrate = auto_calibrate
        self.__cal_min = None
        self.__cal_max = None
        self.__cal_min_window = int(65536 * cal_min_window)

        self.__min_raw_value = min_raw_value   # store the custom min raw value

        if change_display:
            from ..preview import ValuePreview
            self.__preview = ValuePreview.get(change_display)
            self.__change_timeout_millis = change_timeout_millis
        else:
            self.__preview = None

    @property
    def enabled(self):
        return self.__enable_callback.enabled(self) if self.__enable_callback else True

    def update(self):
        if self.__preview:
            self.__preview.update()

    # is_pot tells whether the input is a potentiometer (True) or a rotary encoder (False)
    def init(self, appl):
        self.__appl = appl

    def reset(self):
        pass
    
    # Process a value in range [0..65535]
    def process(self, value):
        if self.__period.exceeded:
            # Initial value: Start calibration
            if self.__calibrate:
                if self.__cal_min == None:
                    # Set the window of values to zero at first
                    self.__cal_min = value
                    self.__cal_max = value
                else:
                    # Widen up the window 
                    if value < self.__cal_min:
                        self.__cal_min = value
                        self.__cal_factor = 65536 / (self.__cal_max - self.__cal_min)

                    if value > self.__cal_max:
                        self.__cal_max = value
                        self.__cal_factor = 65536 / (self.__cal_max - self.__cal_min)

                # If the calibration window is too small, we dont send anything
                if (self.__cal_max - self.__cal_min) < self.__cal_min_window:
                    return
                
                # Scale the input value up
                value = int((value - self.__cal_min) * self.__cal_factor)

            # Determine the output value to be sent from the (possibly calibrated) input
            # value in range [0..65535]
            if self.__transfer_function:
                # Use an external transfer function
                v = self.__transfer_function(value)
            else:
                # Apply custom minimum raw value threshold for stable zero
                if self.__min_raw_value is not None and value < self.__min_raw_value:
                    v = 0  # force zero MIDI when under threshold
                else:
                    # Scale and quantize
                    v = round(value / self.__step_width) * self.__step_width 
                    v = int(v / self.__factor)

                    if v < 0:
                        v = 0
                    if v > self.__max_value:
                        v = self.__max_value

            # Send MIDI message for new value if the output value has changed
            if self.__last_value != v:
                # Update value on client
                self.__last_value = v
                self.__appl.client.set(self.__mapping, v)

                if self.__preview:
                    if not self.__convert_value:
                        self.__preview.preview_mapping(
                            mapping = self.__mapping,
                            value = v,
                            max_value = self.__max_value,
                            timeout_millis = self.__change_timeout_millis
                        )
                    else:
                        self.__preview.preview(
                            text = self.__convert_value(v),
                            timeout_millis = self.__change_timeout_millis
                        )
