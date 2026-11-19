# Describes a routing from source to target, which must be MidiDevices definitions.
class MidiRouting:

    # Used as source/target for routings to/from the application itself
    APPLICATION = 1

    def __init__(self, source, target):
        # Source MIDI device (can be either a AdafruitXXXMidiDevice or 
        # MidiController.PYSWITCH for the application itself)
        self.source = source    

        # Target MIDI device (can be either a AdafruitXXXMidiDevice or 
        # MidiController.PYSWITCH for the application itself)
        self.target = target    
        

##################################################################################################


# MIDI Communication wrapper. Can distribute/merge from/to application and external MIDI
# controllers, as defined ba routings. Remember that you have to define routes from and to
# the application manually!
class MidiController:

    # routings must be a list of MidiRouting instances
    def __init__(self, routings):
        self.__routings_from_appl = [x for x in routings if x.source == MidiRouting.APPLICATION]
        self.__routings_to_appl = [x for x in routings if x.target == MidiRouting.APPLICATION]
        self.__routings_external = [x for x in routings if x.source != MidiRouting.APPLICATION and x.target != MidiRouting.APPLICATION]

    def send(self, midi_message):
        # Send to all routings which have APPLICATION as source
        for r in self.__routings_from_appl:    
            r.target.send(midi_message)

    def receive(self):
        # Process routings without APPLICATION involved 
        self.__process_external_routings()

        # Process routings targeting APPLICATION
        for r in self.__routings_to_appl:
            msg = r.source.receive()

            if msg:
                # Return first message for APPLICATION in the queue (next ticks will deliver the next messages)
                return msg                
    
    # Process all routings where APPLICATION is not involved (this processes one message of each source every time)
    def __process_external_routings(self):
        routings = self.__routings_external
        if not routings:
            return
        
        # Get all sources messages
        sources = []
        results = []

        for r in routings:
            if r.source in sources:
                continue

            sources.append(r.source)
            results.append(r.source.receive())
            
        # Distribute messages
        for r in routings:
            for i in range(len(sources)):
                if sources[i] != r.source:
                    continue

                msg = results[i]
        
                if not msg:
                    continue
                
                r.target.send(msg)

                break
