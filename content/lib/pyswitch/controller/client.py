from micropython import const
from math import floor
from ..misc import EventEmitter, PeriodCounter, Updateable, get_option, do_print

# Midi mapping for a client command. Contains commands to set or request a parameter
class ClientParameterMapping:
   
    _mappings = []

    # Singleton factory
    @staticmethod
    def get(name, set = None, request = None, response = None, value = None, type = 0, depends = None):
        if not name:
            raise Exception() # You must provide an unique name!
        
        for m in ClientParameterMapping._mappings:
            if m.name == name:
                return m
            
        m = ClientParameterMapping(
            name = name,
            create_key = ClientParameterMapping,
            set = set,
            request = request,
            response = response,
            value = value,
            type = type,
            depends = depends
        )

        ClientParameterMapping._mappings.append(m)
        return m

    ##########################################################################################################################

    # Parameter types (used internally in mappings)
    PARAMETER_TYPE_NUMERIC = const(0)   # Default, also used for on/off
    PARAMETER_TYPE_STRING = const(1)    # String parameter

    # Takes MIDI messages as argument (ControlChange or SystemExclusive)
    def __init__(self, name, create_key, set = None, request = None, response = None, value = None, type = 0, depends = None):
        if create_key != ClientParameterMapping:
            # Use the get method exclusively to create mappings!
            raise Exception()   
        
        self.name = name          # Mapping name (used for debug output only)
        self.value = value        # Value of the parameter (buffer). After receiving an answer, the value 
                                  # is buffered here.
        self.type = type          # Numeric or string
        self.depends = depends    # If another mapping is set here, this mapping will only be requested when the dependency has changed value
                                  # NOTE: In 2.4.1, this is prepared but not realized already

        def eval_msg(msg, type_def):
            return (tuple([type_def(x) for x in msg if x]) if ClientTwoPartParameterMapping.is_list(msg) else type_def(msg)) if msg else None

        self.set = eval_msg(set, bytearray)          # MIDI Message to set the parameter
        self.request = eval_msg(request, bytes)      # MIDI Message to request the value
        self.response = eval_msg(response, bytes)    # Response template MIDI message for parsing the received answer

    # Parse the incoming MIDI message and set its value on the mapping.
    # If the response template does not match, returns False, and
    # vice versa. Returns True to notify the listeners of a value change.
    def parse(self, midi_message):
        result = self.parse_against(midi_message, self.response)
        if result != None:
            self.value = result
            return True
        
        return False

    # Parse a message against a response message
    def parse_against(self, midi_message, response):
        try:
            if midi_message[0] != response[0]:
                return None
            
            # SysEx (NRPN) Messages
            if midi_message[0] == 0xf0: 
                # NOTE: We ignore the manufacturer ID for performance reasons (there are two places which
                # have to be ignored, so we would need two comparisons instead of one)
                
                # if bytes(midi_message[1:4]) != bytes(response[1:4]):
                #     return None
                
                if bytes(midi_message[6:10]) != bytes(response[6:10]):
                    return None
                
                # The values starting from index 6 are the value of the response.
                if self.type == self.PARAMETER_TYPE_STRING:
                    # Take as string
                    return ''.join(chr(int(c)) for c in tuple(midi_message[10:-2]))
                else:
                    # Decode 14-bit value to int
                    return midi_message[-3] * 128 + midi_message[-2]

            # CC Messages
            elif midi_message[0] & 0xf0 == 0xb0:
                if midi_message[1] == response[1]:
                    return midi_message[2]

            # PC Messages
            elif midi_message[0] & 0xf0 == 0xc0:
                return midi_message[1]

        except TypeError:
            return  None
        
        return None
    
    # Set the passed value(s) on the SET message(s) of the mapping.
    def set_value(self, value):
        # if isinstance(self.set, list):
        if ClientTwoPartParameterMapping.is_list(self.set):
            for i in range(len(self.set)):
                self.__set_value(self.set[i], value[i])
        else:
            self.__set_value(self.set, value)

    def __set_value(self, midi_message, value):
        if self.type == self.PARAMETER_TYPE_STRING:
            raise Exception() # Setting strings is not implemented yet

        if midi_message[0] & 0xf0 == 0xb0:
            # CC: Set value directly
            midi_message[2] = value

        elif midi_message[0] == 0xf0: 
            # Sysex 14 bit number
            midi_message[-3] = int(floor(value / 128))
            midi_message[-2] = int(value % 128)

        elif midi_message[0] & 0xf0 == 0xc0:
            # PC: Set patch
            midi_message[1] = value

    # Returns if the mapping has finished receiving a result. Per default,
    # this returns True which is valid for mappings with one response.
    def result_finished(self):
        return True


# Parser for two-part messages: The result value will be 128 * value1 + value2, 
# notified when the second message arrives.
class ClientTwoPartParameterMapping(ClientParameterMapping):

    # Singleton factory
    @staticmethod
    def get(name, set = None, request = None, response = None, value = None, type = 0, depends = None):
        for m in ClientParameterMapping._mappings:
            if m.name == name:
                return m
            
        m = ClientTwoPartParameterMapping(
            name = name,
            create_key = ClientParameterMapping,
            set = set,
            request = request,
            response = response,
            value = value,
            type = type,
            depends = depends
        )

        ClientParameterMapping._mappings.append(m)
        return m

    # Returns if the passed value is a list of messages instead of a single message
    @staticmethod
    def is_list(value):
        if not value:
            return False
        
        return not isinstance(value[0], int)


    ##########################################################################################################################

    def __init__(self, name, create_key, set = None, request = None, response = None, value = None, type = 0, depends = None):
        super().__init__(
            name = name, 
            create_key = create_key,
            set = set,
            request = request,
            response = response,
            value = value, 
            type = type, 
            depends = depends
        )

        self.__value_1 = None
    
    def parse(self, midi_message): 
        value_1 = self.parse_against(midi_message, self.response[0])
        if value_1 != None:
            self.__value_1 = value_1
            return True
        
        value_2 = self.parse_against(midi_message, self.response[1])

        if value_2 != None and self.__value_1 != None:
            self.value = 128 * self.__value_1 + value_2
            self.__value_1 = None
            return True
        
        return False
            
    def result_finished(self):
        return (self.__value_1 == None)


############################################################################################################


# Implements all MIDI communication to and from the client device
class Client: #(ClientRequestListener):

    # Listener for dependency mappings
    class _DependencyListener:
        def __init__(self, client, orig_mapping, listener = None):
            self.__client = client
            self.__orig_mapping = orig_mapping
            self.__last_value = None
            self.__listener = listener

        def parameter_changed(self, mapping):
            if mapping.value != self.__last_value:
                self.__last_value = mapping.value

                self.__client._register_mapping(self.__orig_mapping, self.__listener, True)           
        
        def request_terminated(self, mapping):
            pass

    ##########################################################################################################

    def __init__(self, midi, config):
        self.midi = midi
        
        self.debug_unparsed_messages = get_option(config, "debugUnparsedMessages", False)
        self.__debug_sent_messages = get_option(config, "debugSentMessages", False)
        self.debug_exclude_types = get_option(config, "excludeMessageTypes", None)
        self.debug_mapping = get_option(config, "debugMapping", None)
        
        self.__debug_stats = get_option(config, "debugClientStats", False)
        if self.__debug_stats:   # pragma: no cover 
            self.__stats_period = PeriodCounter(get_option(config, "debugStatsInterval", 2000))

        # List of ClientRequest objects    
        self.__requests = []

        # Dict of dependency listeners
        self.__dependencies = {}

        self.__max_request_lifetime = get_option(config, "maxRequestLifetimeMillis", 2000)

        # Helper to only clean up hanging requests from time to time as this is not urgent at all
        self.__cleanup_terminated_period = PeriodCounter(self.__max_request_lifetime / 2)    

    @property
    def requests(self):
        return self.__requests

    # Register the mapping and listener in advance (only plays a role for bidirectional parameters,
    # here this is redundant)
    def register(self, mapping, listener = None):
        if not mapping.request and mapping.response:
            self._register_mapping(mapping, listener, False)

    # Sends the SET message of a mapping. Value has to be a list if the mapping's set field is a list, too!
    def set(self, mapping, value):
        if not mapping.set:
            return
        
        mapping.set_value(value)
                
        # if isinstance(mapping.set, list):
        if ClientTwoPartParameterMapping.is_list(mapping.set):
            for m in mapping.set:
                if not m:
                    continue

                if self.__debug_sent_messages:   # pragma: no cover
                    self.print_message(m)

                self.midi.send(m)
        else:
            if self.__debug_sent_messages:       # pragma: no cover
                self.print_message(mapping.set)
                
            self.midi.send(mapping.set)

    # Send the request message of a mapping. Calls the passed listener when the answer has arrived.
    #@RuntimeStatistics.measure
    def request(self, mapping, listener = None):
        if not mapping.request or not mapping.response:
            return
        
        if mapping.depends:
            if not mapping in self.__dependencies:
                self.__dependencies[mapping] = self._DependencyListener(self, mapping, listener)

            # Register the dependency rather than the mapping itself
            self._register_mapping(mapping.depends, self.__dependencies[mapping], True)
        else:
            self._register_mapping(mapping, listener, True)
        
    # Registers a mapping request or adds the listener to an existing one. Optionally sends the
    # request message. Internal use only.
    def _register_mapping(self, mapping, listener, send):
        # Add request to the list
        req = self.get_matching_request(mapping)
        if not req:
            # New request
            req = self.__create_request(mapping)
            
            if listener:
                req.add_listener(listener)

            # Add to list
            self.__requests.append(req)
            
            # Send 
            if send:           
                req.send()

        else:
            # Existing request: Add listener
            if listener:
                req.add_listener(listener)

    # Create a new request
    def __create_request(self, mapping):
        return ClientRequest(              
            self,
            mapping,
            self.__max_request_lifetime if mapping.request else 0
        )

    # Receive MIDI messages
    #@RuntimeStatistics.measure
    def receive(self, midi_message):
        if self.__cleanup_terminated_period.exceeded:
            self.__cleanup_hanging_requests()

        if self.__debug_stats and self.__stats_period.exceeded:  # pragma: no cover 
            do_print(f"    { len(self.__requests) } requests pending:")
            for r in self.__requests:
                do_print(f"{ r.mapping.name }: { repr([l.__class__.__name__ for l in r.listeners]) }")

        if not midi_message:
            return False
        
        # See if one of the waiting requests matches
        do_cleanup = False

        parsed = False
        for request in self.__requests:
            if request.parse(midi_message):
                parsed = True

            if request.finished:
                do_cleanup = True

        # Check for finished requests
        if do_cleanup:
            self.__cleanup_requests()

        # Debug unparsed messages
        if not parsed and self.debug_unparsed_messages:           # pragma: no cover
            self.print_message(midi_message)

        return parsed
            
    # Returns a matching request from the list if any, or None if no matching
    # request has been found.
    #@RuntimeStatistics.measure
    def get_matching_request(self, mapping):
        for request in self.__requests:
            if request.mapping == mapping:
                return request
            
        return None

    # Remove all finished requests, and terminate the ones which took too long already
    def __cleanup_requests(self):
        self.__requests = [i for i in self.__requests if not i.finished]
            
    # Terminate any requests which took too long from time to time
    def __cleanup_hanging_requests(self):
        # Terminate requests if they waited too long
        for request in self.__requests:
            if request.lifetime and request.lifetime.exceeded:
                request.terminate()

        self.__cleanup_requests()

    # Print info about the passed message
    def print_message(self, midi_message):  # pragma: no cover
        print(list(midi_message))


#######################################################################################################################


# Model for a request for a value
class ClientRequest(EventEmitter):

    def __init__(self, client, mapping, max_request_lifetime = 0):
        super().__init__() #ClientRequestListener)
        
        self.client = client
        self.mapping = mapping
        
        self.lifetime = self.__init_lifetime(max_request_lifetime)

    # Sets up the lifetime for mappings not belonging to a bidirectional protocol
    def __init_lifetime(self, max_request_lifetime):
        if not max_request_lifetime > 0:            
            return None
            
        lifetime = PeriodCounter(max_request_lifetime)
        lifetime.reset()

        return lifetime

    # Sends the request
    def send(self):
        if not self.mapping.request:
            return

        # if isinstance(self.mapping.request, list):
        if ClientTwoPartParameterMapping.is_list(self.mapping.request):
            for m in self.mapping.request:
                if not m:
                    continue
                self.client.midi.send(m)    
        else:
            self.client.midi.send(self.mapping.request)

    # Returns if the request is finished
    @property
    def finished(self):
        return self.listeners == None

    # Send the terminate signal to all listeners and finished it, so it will be
    # cleared up next time.
    def terminate(self):
        if self.finished:
            return
        
        # Call the listeners
        self.notify_terminated()

        # Clear listeners
        self.listeners = None

    # Parses an incoming MIDI message. If the message belongs to the mapping's request,
    # calls the listener with the received value. Returns if the message has been used.
    def parse(self, midi_message):
        mapping = self.mapping

        if not mapping.response:
            return False
        
        if self.finished:
            return False
        
        if not mapping.parse(midi_message):
            return False

        if not mapping.result_finished():
            return

        if self.client.debug_mapping == mapping:    # pragma: no cover
            print(f"{ mapping.name }: Received value '{ repr(mapping.value) }' from { list(midi_message) }")

        # Call the listeners (the mapping has the values set already). Do not use notify_listeners() to keep the stack short.
        for listener in self.listeners:
            listener.parameter_changed(self.mapping)

        # Clear listeners (only if the request has a restricted life time)
        if self.lifetime:
            self.listeners = None

        return True

    def notify_listeners(self):
        for listener in self.listeners:
            listener.parameter_changed(self.mapping)

    def notify_terminated(self):
        for listener in self.listeners:
            listener.request_terminated(self.mapping)


####################################################################################################################


class BidirectionalClient(Client, Updateable):

    def __init__(self, midi, config, protocol):
        Client.__init__(self, midi, config)

        self.protocol = protocol
        self.protocol.debug = get_option(config, "debugBidirectionalProtocol")
        self.protocol.init(midi, self)

    # Register the mapping and listener in advance (only plays a role for bidirectional parameters)
    def register(self, mapping, listener = None):
        if self.protocol.is_bidirectional(mapping):
            mapping.request = None
            mapping.depends = None
    
        Client.register(self, mapping, listener)
        
    # Receive messages (also passes messages to the protocol)
    #@RuntimeStatistics.measure
    def receive(self, midi_message):
        # Dirty hack to disable the debugging of unparsed messages in the Client implementation
        tmp = self.debug_unparsed_messages
        self.debug_unparsed_messages = False
        parsed_by_client =  Client.receive(self, midi_message)
        self.debug_unparsed_messages = tmp

        if parsed_by_client:
            return False

        if not midi_message:
            return False

        parsed = self.protocol.receive(midi_message)

        # Debug unparsed messages
        if not parsed and self.debug_unparsed_messages:           # pragma: no cover
            self.print_message(midi_message)

        return parsed

    # In case of bidirectional parammeters, "simulate" a parameter change directly after the MIDI message
    def set(self, mapping, value):
        Client.set(self, mapping, value)

        # Notify listeners of the mapping with the set value (we do not use echoing, so the actions
        # will not reflect the state change if we just do nothing)
        if self.protocol.feedback_value(mapping):
            req = self.get_matching_request(mapping)
            if not req:
                raise Exception() #"No request for mapping: " + repr(mapping))
            
            req.mapping.value = value
            req.notify_listeners()

    # Update the protocol state
    def update(self):
        self.protocol.update()

    # Calls request_terminated() on all listeners of requests with bidirectional mappings
    def notify_connection_lost(self):
        for r in self.requests:
            if self.protocol.is_bidirectional(r.mapping):
                r.notify_terminated()
        

####################################################################################################################


# Base class for listeners to client parameter changes
#class ClientRequestListener:
#
#    # Called by the Client class when a parameter request has been answered.
#    # The value received is already set on the mapping.
#    def parameter_changed(self, mapping):
#        pass
#
#    # Called when the client is offline (requests took too long)
#    def request_terminated(self, mapping):
#        pass


####################################################################################################################
####################################################################################################################


# Base class for bidirectional protocols
#class BidirectionalProtocol:
#
#    # Called before usage, with a midi handler.
#    def init(self, midi, client):
#        pass
#
#    # Must return (boolean) if the passed mapping is handled in the bidirectional protocol
#    def is_bidirectional(self, mapping):
#        return False
#   
#    # Must return (boolean) if the passed mapping should feed back the set value immediately
#    # without waiting for a midi message.
#    def feedback_value(self, mapping):
#        return False
#
#    # Initialize the communication etc.
#    def update(self):
#        pass
#   
#    # Receive midi messages (for example for state sensing)
#    def receive(self, midi_message):
#        pass
#
#    # Must return a color representation for the current state
#    def get_color(self):
#        return (0, 0, 0)

