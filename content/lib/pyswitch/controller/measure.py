from ..misc import EventEmitter, Updateable, get_current_millis

# Measurement of runtimes 
class RuntimeMeasurement(EventEmitter, Updateable):  
    
    # type is arbitrary and only used externally
    def __init__(self, interval_millis, name = None):
        EventEmitter.__init__(self) #, RuntimeMeasurementListener)

        self.interval_millis = interval_millis
        self.__last_output = 0
        self.name = name

        self.reset()

    # Average runtime
    @property
    def average(self):
        if self.__time_num == 0:
            return 0
        return int(self.__time_aggr / self.__time_num)
    
    @property 
    def sum(self):
        return self.__time_aggr

    @property 
    def calls(self):
        return self.__time_num

    def update(self):
        current = get_current_millis()
        if self.__last_output + self.interval_millis < current:
            self.__last_output = current

            for l in self.listeners:
                l.measurement_updated(self)

            self.reset()

    # Initialize the instance
    def reset(self):
        self.value = 0       # Maximum runtime
        self.start_time = 0  # Start time
        self.end_time = 0    # End time

        self.__time_aggr = 0  # Times added up
        self.__time_num = 0   # Number of times added up

    # Start the measurement
    def start(self):
        self.start_time = get_current_millis()

    # Adds the current diff to the haystack
    def finish(self):
        start = self.start_time
        if start == 0:
            return
        
        now = get_current_millis()
        self.end_time = now
        
        diff = now - start
        if diff > self.value:
            self.value = diff

        self.__time_aggr = self.__time_aggr + diff
        self.__time_num += 1


################################################################################


# Listener for runtime measurement changes
#class RuntimeMeasurementListener:
#    def measurement_updated(self, measurement):
#        pass

