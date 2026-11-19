from gc import collect, mem_free

from .inputs import SwitchController, ContinuousController
from .client import Client, BidirectionalClient
from ..misc import Updater, PeriodCounter, get_option, do_print, format_size, fill_up_to
from ..stats import Memory #, RuntimeStatistics


# Main application class (controls the processing)    
class Controller(Updater): #ClientRequestListener

    # IDs for all available measurements (for statistics)
    STAT_ID_TICK_TIME = 1             # Time one processing loop takes overall

    # config:   Configuration dictionary. 
    # inputs:  [           list of switch and input definitions
    #                {
    #                     "assignment": {   Selects which switch of your device you want to assign. 
    #                          "model":    Instance of AdafruitSwitch or AdafruitPotentiometer or other hardware models
    #                          "pixels":   Optional, tiple of LED indices to assign to the switch, for example (0, 1, 2) 
    #                          "name":     Optional, name of the switch for output
    #                     },
    #
    #                     # Defines the actions you want to happen on different events of the switch. You can 
    #                     # define as many actions as you want, they will be executed in that order.
    #                     # You can also use the Condition class to have different actions active depending
    #                     # on another parameter.
    #                     "actions": [
    #                           ...See Actions.py and its children
    #                     ]
    #                },
    #                ...
    #           ]
    def __init__(self, led_driver, midi, protocol = None, config = {}, inputs = [], ui = None, period_counter = None):
        Updater.__init__(self)

        # Flag which is used by display elements to show the user there is not enough memory left
        self.low_memory_warning = False

        # MIDI handler
        self.__midi = midi

        # User interface
        self.ui = ui        

        # Global config
        self.config = config
        update_interval = get_option(config, "updateInterval", 200)

        # Max. number of MIDI messages being parsed before the next switch state evaluation
        self.__max_consecutive_midi_msgs = get_option(config, "maxConsecutiveMidiMessages", 10)   

        # Print debug info        
        self.__debug_stats = get_option(config, "debugStats", False)        

        # Statistical measurement for tick time
        if self.__debug_stats:
            from .measure import RuntimeMeasurement

            self.__measurement_process_jitter = RuntimeMeasurement(get_option(config, "debugStatsInterval", update_interval))
            self.__measurement_process_jitter.add_listener(self)
            self.add_updateable(self.__measurement_process_jitter)            

        # Limit of minimum free memory before low_memory_warning is set to True (the check is done before ticks
        # are running so this should be enough to operate all configurations imaginable. Normally you need about 
        # 10-15k from there, so 25k is enough headroom)
        self.__memory_warn_limit = get_option(config, "memoryWarnLimitBytes", 1024 * 15)  # 15kB

        # Clear MIDI buffers on startup
        self.__clear_buffer = get_option(config, "clearBuffers", True)

        # Global shared data (some actions/callbacks use this)
        self.shared = {}

        # NeoPixel driver 
        self.led_driver = led_driver
            
        # Determine how many NeoPixels are needed overall
        def get_num_pixels(switches):
            ret = 0
            for sw_def in switches:
                pixels = get_option(sw_def["assignment"], "pixels", [])
                for p in pixels:
                    pp1 = p + 1
                    if pp1 > ret:
                        ret = pp1
            return ret
        
        self.led_driver.init(get_num_pixels(inputs))
        
        # Periodic update handler (the client is only asked when a certain time has passed)
        self.period = period_counter
        if not self.period:
            self.period = PeriodCounter(update_interval)        

        # Client access. When no protocol is passed, every value will be requested periodically. If a protocol
        # is passed, bidirectional communication is used according to the protocol.
        if protocol:
            self.client = BidirectionalClient(self.__midi, config, protocol)
            self.add_updateable(self.client)
        else:
            self.client = Client(self.__midi, config)

        # Set up inputs
        self.inputs = []
        for sw_def in inputs:
            if hasattr(sw_def["assignment"]["model"], "pushed"):
                # It is a switch
                self.inputs.append(SwitchController(self, sw_def))
            else:
                # It is a continuous input or rotary encoder. 
                self.inputs.append(ContinuousController(self, sw_def))

        # Set up the screen elements
        if self.ui:
            self.ui.init(self)
            self.add_updateable(ui)

    # Prepare to run the processing loop
    def init(self):
        # Show user interface
        if self.ui:            
            Memory.watch("Showing UI")

            self.ui.show()           
        
        Memory.watch("Application loaded")

        # Check memory usage and issue a warning if too high
        collect()
        if mem_free() < self.__memory_warn_limit:
            do_print(f"LOW MEMORY: { format_size(mem_free()) }")
            self.low_memory_warning = True

        # Consume all MIDI messages which might be still in some buffers, 
        # and start when the queue is empty.
        if self.__clear_buffer:
            while True:
                if not self.__midi.receive():
                    break

    # Single tick in the processing loop. Must return True to keep the loop alive. Call this in an endless loop.
    def tick(self):
        # Update all Updateables in periodic intervals, less frequently than every tick.        
        if self.period.exceeded:
            for u in self.updateables:
                # Receive MIDI messages in between updates, too
                self.__receive_midi_messages()

                u.update()

            Memory.watch("Controller: update", only_if_changed = True)

        # Receive all available MIDI messages
        self.__receive_midi_messages()

        return True

    # Resets all actions (which refreshes their buffer memories, triggering re-rendering of LEDs and displays)
    def reset_actions(self):
        for input in self.inputs:
            for action in input.actions:
                action.reset()

    # Receive MIDI messages, and in between check for switch state changes
    def __receive_midi_messages(self):
        cnt = 0
        
        while True:            
            if self.__debug_stats:
                self.__measurement_process_jitter.finish()
            
            # Detect switch state changes
            for input in self.inputs:
                input.process()
            
            if self.__debug_stats:
                self.__measurement_process_jitter.start()

            # Receive MIDI
            midimsg = self.__midi.receive()
            self.client.receive(midimsg)

            # Break after a certain amount of messages to keep the device responsive
            cnt = cnt + 1
            if not midimsg or cnt > self.__max_consecutive_midi_msgs:
                break  

        #self._measurement_midi_jitter.start()

    # Callback called when the measurement wants to show something
    def measurement_updated(self, measurement):
        collect()
        do_print(f"{ fill_up_to(str(measurement.name), 30, '.') }: Max { repr(measurement.value) }ms, Avg { repr(measurement.average) }ms, Calls: { repr(measurement.calls) }, Free: { format_size(mem_free()) }")

