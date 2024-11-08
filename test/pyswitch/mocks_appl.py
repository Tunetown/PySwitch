from lib.pyswitch.controller.actions.Action import Action
from lib.pyswitch.controller.actions.actions import PushButtonAction
from lib.pyswitch.controller.Controller import Controller
from lib.pyswitch.controller.ConditionTree import Condition

from .mocks_lib import *


# Used to build szenarios
class SceneStep:
    def __init__(self, num_pass_ticks = 0, prepare = None, evaluate = None, next = None):
        self.num_pass_ticks = num_pass_ticks
        self.prepare = prepare
        self.evaluate = evaluate
        self.next = next


##################################################################################################################################


class MockController(Controller):
    def __init__(self, led_driver, communication, midi, config = {}, switches = [],  ui = None, period_counter = None):
        super().__init__(
            led_driver = led_driver, 
            communication = communication, 
            midi = midi, 
            config = config, 
            switches = switches, 
            ui = ui, 
            period_counter = period_counter
        )

        self._next_step = None
        self._cnt = 0

    def tick(self):
        if not self._next_step: 
            return super().tick()
        
        if self._cnt < self._next_step.num_pass_ticks:
            self._cnt += 1
            return super().tick()
        
        self._cnt = 0
        if callable(self._next_step.prepare):
            self._next_step.prepare()

        res = super().tick()
        if not res:  
            raise Exception("tick() does not return True")
        
        if not callable(self._next_step.evaluate):
            return False
        
        ret = self._next_step.evaluate()

        self._next_step = self._next_step.next

        return ret        
    
    @property
    def next_step(self):  
        return self._next_step
    
    @next_step.setter
    def next_step(self, step):
        if not isinstance(step, SceneStep): 
            raise Exception("Invalid test step")
        
        self._next_step = step


##################################################################################################################################


class MockMidiController:
    def __init__(self):
        self.messages_sent = []
        self.next_receive_messages = []

    def receive(self):
        if self.next_receive_messages:
            return self.next_receive_messages.pop(0)
        
        return None
    
    def send(self, midi_message):
        self.messages_sent.append(midi_message)


##################################################################################################################################


class MockPeriodCounter():
    def __init__(self):
        self.exceed_next_time = False
        self.num_reset_calls = 0

    def reset(self):
        self.num_reset_calls += 1

    @property
    def exceeded(self):
        if self.exceed_next_time:
            self.exceed_next_time = False
            return True
        return False


##################################################################################################################################


class MockNeoPixelDriver:
    def __init__(self):
        self.leds = None
        
    def init(self, num_leds):
        self.leds = [None for i in range(num_leds)]


##################################################################################################################################


class MockSwitch:
    def __init__(self, port = None):
        self.port = port
        self.shall_be_pushed = False
        self.raise_on_init = None

    def init(self):
        if self.raise_on_init:
            raise self.raise_on_init

    @property
    def pushed(self):
        return self.shall_be_pushed


##################################################################################################################################


class MockValueProvider:
    def __init__(self):
        self.outputs_parse = []
        self.parse_calls = []

        self.set_value_calls = []

    def parse(self, mapping, midi_message):        
        for o in self.outputs_parse:
            if not "mapping" in o or o["mapping"] != mapping:
                continue

            if "value" in o:                   
                mapping.value = o["value"]

            ret = o["result"] if "result" in o else False

            self.parse_calls.append({
                "mapping": mapping,
                "message": midi_message,
                "return": ret
            })

            return ret
        
        return False
    
    def set_value(self, mapping, value):
        self.set_value_calls.append({
            "mapping": mapping,
            "value": value
        })


##################################################################################################################################


class MockPushButtonAction(PushButtonAction):
    def __init__(self, config = {}, period_counter = None):
        super().__init__(config = config, period_counter = period_counter)

        self.num_set_calls = 0

    def set(self, state):
        self.num_set_calls += 1
    

##################################################################################################################################


class MockAction(Action):

    def __init__(self, config = {}):
        super().__init__(config = config)

        self.num_update_calls_overall = 0
        self.num_update_calls_enabled = 0
        self.num_reset_calls = 0
        self.num_push_calls = 0
        self.num_release_calls = 0
        self.num_update_displays_calls = 0
        self.num_force_update_calls = 0
        self.num_reset_display_calls = 0
        
        self.state = False

    def push(self):
        self.num_push_calls += 1

    def release(self):
        self.num_release_calls += 1

    def update(self):
        self.num_update_calls_overall += 1
        
        if self.enabled:
            self.num_update_calls_enabled += 1

    def reset(self):
        self.num_reset_calls += 1

    def update_displays(self):
        self.num_update_displays_calls += 1

    def force_update(self): 
        self.num_force_update_calls += 1

    def reset_display(self): 
        self.num_reset_display_calls += 1


##################################################################################################################################


class MockCondition(Condition):
    def __init__(self, yes = None, no = None):
        super().__init__(yes = yes, no = no)

        self.bool_value = True
        self.num_update_calls = 0

    def update(self):
        self.num_update_calls += 1

        if self.true == self.bool_value:
            return

        self.true = self.bool_value

        for listener in self.listeners:
            listener.condition_changed(self)   


##################################################################################################################################


class MockConditionReplacer:
    def replace(self, entry):
        return entry + " (replaced)"
    

##################################################################################################################################


class MockMeasurement:
    def __init__(self):
        self.output_value = 0
        self.output_message = ""
        self.num_update_calls = 0

    def get_message(self):
        return self.output_message   
    
    def value(self):
        return self.output_value     

    def update(self):
        self.num_update_calls += 1   


##################################################################################################################################


class MockClient:
    def __init__(self):
        self.register_calls = []

    def register(self, mapping, listener):
        self.register_calls.append({
            "mapping": mapping,
            "listener": listener
        })


##################################################################################################################################


class MockClientRequestListener:
    def __init__(self):
        self.parameter_changed_calls = []
        self.request_terminated_calls = []

    def parameter_changed(self, mapping):
        self.parameter_changed_calls.append(mapping)

    # Called when the client is offline (requests took too long)
    def request_terminated(self, mapping):
        self.request_terminated_calls.append(mapping)


##################################################################################################################################


class MockBidirectionalProtocol:
    def __init__(self):
        self.outputs_is_bidirectional = []
        self.outputs_feedback_value = []
        self.output_color = (0, 0, 0)

        self.num_update_calls = 0

        self.init_calls = []
        self.receive_calls = []

    def init(self, midi, client):
        self.init_calls.append({
            "midi": midi,
            "client": client
        })

    # Must return (boolean) if the passed mapping is handled in the bidirectional protocol
    def is_bidirectional(self, mapping):
        for o in self.outputs_is_bidirectional:
            if o["mapping"] == mapping:
                return o["result"]
            
        return False
   
    # Must return (boolean) if the passed mapping should feed back the set value immediately
    # without waiting for a midi message.
    def feedback_value(self, mapping):
        for o in self.outputs_feedback_value:
            if o["mapping"] == mapping:
                return o["result"]
            
        return False

    # Initialize the communication etc.
    def update(self):
        self.num_update_calls += 1
   
    # Receive midi messages (for example for state sensing)
    def receive(self, midi_message):
        self.receive_calls.append(midi_message)

    # Must return a color representation for the current state
    def get_color(self):
        return self.output_color


##################################################################################################################################


class MockCategoryProvider:
    def get_effect_category(self, value):
        return value * 10
    
    # Must return the effect color for a mapping value
    def get_effect_category_color(self, value):
        return (value, value + 2, value * 4)
    
    # Must return the effect name for a mapping value
    def get_effect_category_name(self, value):
        return "name" + repr(value)
    
    # Must return the value interpreted as "not assigned"
    def get_category_not_assigned(self):
        return 0


##################################################################################################################################


class MockSlotInfoProvider:
    def __init__(self):
        self.output = "noname"

    def get_name(self):
        return self.output

