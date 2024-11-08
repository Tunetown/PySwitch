from adafruit_midi.system_exclusive import SystemExclusive

from ..misc import Tools, EventEmitter, PeriodCounter, Updateable


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


######################################################################################################################


# Must implement preparation of MIDI messages for sending as well as parsing the received ones.
#class ClientValueProvider:
#    # Must parse the incoming MIDI message and set it on the passed mapping.
#    # If the response template does not match, must return False.
#    # Must return True to notify the listeners of a value change.
#    def parse(self, mapping, midi_message):
#        return False
#
#    # Must set the passed value on the SET message of the mapping.
#    def set_value(self, mapping, value):
#        pass


######################################################################################################################


# Implements all MIDI communication to and from the client device
class Client: #(ClientRequestListener):

    def __init__(self, midi, config, value_provider):
        self.midi = midi
        self._config = config

        self.debug = Tools.get_option(self._config, "debugClient")
        self.debug_mapping = Tools.get_option(self._config, "clientDebugMapping", None)
        self.debug_raw_midi = Tools.get_option(self._config, "debugClientRawMidi")
        
        self.value_provider = value_provider

        # List of ClientRequest objects    
        self._requests = []

        self._max_request_lifetime = Tools.get_option(self._config, "maxRequestLifetimeMillis", 2000)

        # Helper to only clean up hanging requests from time to time as this is not urgent at all
        self._cleanup_terminated_period = PeriodCounter(self._max_request_lifetime / 2)    

    @property
    def requests(self):
        return self._requests

    # Register the mapping and listener in advance (only plays a role for bidirectional parameters,
    # here this is redundant)
    def register(self, mapping, listener):
        pass

    # Sends the SET message of a mapping
    def set(self, mapping, value):
        if not mapping.set:
            raise Exception("No SET message prepared for this MIDI mapping")
        
        self.value_provider.set_value(mapping, value)
                
        if self.debug:  # pragma: no cover
            self._print("Send SET message (" + mapping.name + "): " + Tools.stringify_midi_message(mapping.set), mapping)

        self.midi.send(mapping.set)

    # Send the request message of a mapping. Calls the passed listener when the answer has arrived.
    def request(self, mapping, listener):
        self.register_mapping(mapping, listener, True)
        
    # Registers a mapping request or adds the listener to an existing one. Optionally sends the
    # request message. Internal use only.
    def register_mapping(self, mapping, listener, send):
        # Add request to the list
        req = self.get_matching_request(mapping)
        if not req:
            # New request
            req = self.create_request(mapping)
            
            req.add_listener(listener)

            # Add to list
            self._requests.append(req)
            
            if self.debug:  # pragma: no cover
                self._print("Added new request for " + mapping.name + ". Open requests: " + str(len(self._requests)), mapping)

            # Send 
            if send:           
                req.send()            

        else:
            # Existing request: Add listener
            req.add_listener(listener)

            if self.debug:  # pragma: no cover
                self._print("Added new listener to existing request for " + mapping.name + ". Open requests: " + str(len(self._requests)) + ", Listeners: " + str(len(req.listeners)), mapping)

    # Create a new request
    def create_request(self, mapping):
        return ClientRequest(              
            self,
            mapping,
            self._max_request_lifetime
        )

    # Receive MIDI messages
    def receive(self, midi_message):
        if self._cleanup_terminated_period.exceeded:
            self._cleanup_hanging_requests()

        if not midi_message:
            return
        
        # See if one of the waiting requests matches
        do_cleanup = False

        for request in self._requests:
            request.parse(midi_message)
            
            if request.finished:
                do_cleanup = True

        # Check for finished requests
        if do_cleanup:
            self._cleanup_requests()

    # Returns a matching request from the list if any, or None if no matching
    # request has been found.
    def get_matching_request(self, mapping):
        if not isinstance(mapping.response, SystemExclusive):
            return None
        
        for request in self._requests:
            if request.mapping == mapping:
                return request
            
        return None

    # Remove all finished requests, and terminate the ones which took too long already
    def _cleanup_requests(self):
        self._requests = [i for i in self._requests if not i.finished]
            
    # Terminate any requests which took too long from time to time
    def _cleanup_hanging_requests(self):
        # Terminate requests if they waited too long
        for request in self._requests:
            if request.lifetime and request.lifetime.exceeded:
                request.terminate()

                if self.debug:  # pragma: no cover
                    self._print("Terminated request for " + request.mapping.name + ", took too long")

        self._cleanup_requests()

    # Debug console output
    def _print(self, msg, mapping = None): # pragma: no cover
        if self.debug_mapping != None and mapping != None and self.debug_mapping != mapping:
            return
        
        Tools.print("Client: " + msg)


#######################################################################################################################


# Midi mapping for a client command. Contains commands to set or request a parameter
class ClientParameterMapping:
    # Takes MIDI messages as argument (ControlChange or SystemExclusive)
    def __init__(self, name = "", set = None, request = None, response = None, type = None, value = None):
        self.name = name          # Mapping name (used for debug output only)
        self.set = set            # MIDI Message to set the parameter
        self.request = request    # MIDI Message to request the value
        self.response = response  # Response template MIDI message for parsing the received answer        
        self.type = type          # Type of mapping
        self.value = value        # Value of the parameter (buffer). After receiving an answer, the value 
                                  # is buffered here.                                  

    def __eq__(self, other):
        if not other:
            return False
        
        if self.response != None:
            if other.response != None:
                return Tools.compare_midi_messages(self.response, other.response)
            else:
                return False
            
        elif self.set != None:
            if other.set != None:
                return Tools.compare_midi_messages(self.set, other.set)
            else:
                return False
            
        elif self.request != None:
            if other.request != None:
                return Tools.compare_midi_messages(self.request, other.request)
            else:
                return False
            
        return False

    @property
    def can_set(self):
        return self.set != None

    @property
    def can_request(self):
        return self.request != None
    
    @property
    def can_receive(self):
        return self.response != None

    # Returns a (shallow) copy of the mapping with no request/response and value. Use this
    # if you have performance issues with too much requests.
    @property
    def set_only(self):
        return ClientParameterMapping(
            name = self.name,
            set = self.set,
            type = self.type
        )
    
    # Returns a (shallow) copy of the mapping with no request/response and value. Use this
    # if you have performance issues with too much requests.
    @property
    def set_and_receive_only(self):
        return ClientParameterMapping(
            name = self.name,
            set = self.set,
            response = self.response,
            type = self.type
        )


############################################################################################################


# Model for a request for a value
class ClientRequest(EventEmitter):

    def __init__(self, client, mapping, max_request_lifetime = 0):
        super().__init__() #ClientRequestListener)
        
        self.client = client
        self.mapping = mapping
        self.debug = self.client.debug     
        
        if self.mapping.request and not isinstance(self.mapping.request, SystemExclusive):
            raise Exception("Parameter requests do not work with ControlChange or other types. Use SystemExclusive instead. (" + self.mapping.name + ")")

        if not self.mapping.response:
            raise Exception("No response template message prepared for this MIDI mapping (" + self.mapping.name + ")")
        
        if not isinstance(self.mapping.response, SystemExclusive):
            raise Exception("Parameter requests do not work with ControlChange or other types. Use SystemExclusive instead. (" + self.mapping.name + ")")
        
        self.lifetime = self._init_lifetime(max_request_lifetime)

    # Sets up the lifetime for mappings not belonging to a bidirectional protocol
    def _init_lifetime(self, max_request_lifetime):
        if not max_request_lifetime > 0:            
            return None
            
        lifetime = PeriodCounter(max_request_lifetime)
        lifetime.reset()
        return lifetime

    # Sends the request
    def send(self):
        if not self.mapping.can_request:
            return

        if self.debug:   # pragma: no cover
            self._print(" -> Send REQUEST message for " + self.mapping.name + ": " + Tools.stringify_midi_message(self.mapping.request))

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
    # calls the listener with the received value.
    def parse(self, midi_message):
        if not self.mapping.can_receive:
            return 
        
        if self.finished:
            return
        
        if not isinstance(midi_message, SystemExclusive):
            return

        if self.client.debug_raw_midi:  # pragma: no cover
            self._print("RAW Receive : " + Tools.stringify_midi_message(midi_message))
            self._print("RAW Template: " + Tools.stringify_midi_message(self.mapping.response))

        if not self.client.value_provider.parse(self.mapping, midi_message):
            return
        
        if self.debug:   # pragma: no cover
            self._print("   -> Received value " + repr(self.mapping.value) + " for " + self.mapping.name + ": " + Tools.stringify_midi_message(midi_message))

        # Call the listeners (the mapping has the values set already)
        self.notify_listeners()

        # Clear listeners (only if the request has a restricted life time)
        if self.lifetime:
            self.listeners = None

    def notify_listeners(self):
        for listener in self.listeners:
            listener.parameter_changed(self.mapping)

    def notify_terminated(self):
        for listener in self.listeners:
            listener.request_terminated(self.mapping)

    # Debug console output
    def _print(self, msg):  # pragma: no cover
        if self.client.debug_mapping != None and self.client.debug_mapping != self.mapping:
            return

        Tools.print("ClientRequest: " + msg)


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


####################################################################################################################


class BidirectionalClient(Client, Updateable):

    def __init__(self, midi, config, value_provider, protocol):
        Client.__init__(self, midi, config, value_provider)

        self.protocol = protocol
        self.protocol.debug = Tools.get_option(config, "debugBidirectionalProtocol")
        self.protocol.init(midi, self)

    # Register the mapping and listener in advance (only plays a role for bidirectional parameters)
    def register(self, mapping, listener):
        if not self.protocol.is_bidirectional(mapping):
            return

        self.register_mapping(mapping.set_and_receive_only, listener, False)

    # Filter the request messages from the mappings which are part of a bidirectional parameter set
    # (those cannot be requested anymore but get updates from the client automatically).
    def request(self, mapping, listener):        
        if self.protocol.is_bidirectional(mapping):
            super().request(mapping.set_and_receive_only, listener)
        
        super().request(mapping, listener)

    # Receive messages (also passes messages to the protocol)
    def receive(self, midi_message):
        Client.receive(self, midi_message)

        if not midi_message:
            return

        self.protocol.receive(midi_message)

    # In case of bidirectional parammeters, "simulate" a parameter change directly after the MIDI message
    def set(self, mapping, value):
        Client.set(self, mapping, value)

        # Notify listeners of the mapping with the set value (we do not use echoing, so the actions
        # will not reflect the state change if we just do nothing)
        if self.protocol.feedback_value(mapping):
            req = self.get_matching_request(mapping)
            if not req:
                raise Exception("No request for mapping: " + repr(mapping))
            
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

    # Create a new request
    def create_request(self, mapping):
        # For bidirectional parameters, do not set a request lifetime so the requests never get cleaned up
        if self.protocol.is_bidirectional(mapping):  
            return ClientRequest(              
                self,
                mapping
            )
        else:
            return super().create_request(mapping)
        