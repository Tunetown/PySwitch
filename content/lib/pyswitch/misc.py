from time import monotonic

# PySwitch version
PYSWITCH_VERSION = "2.4.9"

# Read a value from an option dictionary with an optional default value
def get_option(config, name, default = False):
    if not config:
        return default
    if name not in config:
        return default        
    return config[name]

# Print (for debugging only!)
def do_print(msg):  # pragma: no cover
    print(msg)

# Returns a current timestmap in integer milliseconds
def get_current_millis():
    return int(monotonic() * 1000)
    
# # Returns a readable string with the current timestamp (local time)
# def formatted_timestamp():
#     ts = localtime()
#     return f"{ str(ts.tm_year) }-{ "{:02d}".format(ts.tm_mon) }-{ "{:02d}".format(ts.tm_mday) } { "{:02d}".format(ts.tm_hour) }:{ "{:02d}".format(ts.tm_min) }:{ "{:02d}".format(ts.tm_sec) }"

# Size (bytes) output formatting 
# Taken from https://stackoverflow.com/questions/1094841/get-a-human-readable-version-of-a-file-size 
def format_size(num, fill_up_to_num = 0, suffix = "B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return fill_up_to(f"{num:3.1f} {unit}{suffix}", fill_up_to_num)
        num /= 1024.0
    return fill_up_to(f"{num:.1f}Yi{suffix}", fill_up_to_num)

# Fill up string with spaces. Needed here because CircuitPython does not seem to support the ljust() function of strings.
def fill_up_to(str, num_spaces_at_right, fill_char = " "):   
    if num_spaces_at_right <= 0:
        return str
    ret = str
    while len(ret) < num_spaces_at_right:
        ret += fill_char
    return ret


#####################################################################################################################################


# Base class for everything that needs to be updated regularily
class Updateable:
    def update(self):
        pass   # pragma: no cover

    def reset(self):
        pass   # pragma: no cover


#####################################################################################################################################


# Base class for handling updateables
class Updater:
    def __init__(self):
        self.updateables = []

    # Add a new Updateable
    def add_updateable(self, u):
        if not isinstance(u, Updateable):
            return
        
        if u in self.updateables:
            return
        
        self.updateables.append(u)

    # Update all updateables. 
    def update(self):
        for u in self.updateables:            
            u.update()

    # Reset all updateables
    def reset(self):
        for u in self.updateables:
            u.reset()


#####################################################################################################################################


# Base class for event distributors (who call listeners)
class EventEmitter:
    def __init__(self): 
        self.listeners = []

     # Adds a listener, and returns True if added, False if already existed.
    def add_listener(self, listener):
        if listener in self.listeners:
            return False
        
        self.listeners.append(listener)
        return True
    

###############################################################################################################


# Periodic update helper    
class PeriodCounter:
    def __init__(self, interval_millis):
        self.interval = int(interval_millis)

        self.__last_reset = 0

    # Resets the period counter to the current time
    def reset(self):
        self.__last_reset = get_current_millis()

    # Returns the amount of milliseconds passed since the last reset
    @property
    def passed(self):
        return get_current_millis() - self.__last_reset

    # Returns if the period has been exceeded. If yes, it lso resets
    # the period to the current time.
    @property
    def exceeded(self):
        current_time = get_current_millis()
        if self.__last_reset + self.interval < current_time:
            self.__last_reset = current_time
            return True
        return False
            
