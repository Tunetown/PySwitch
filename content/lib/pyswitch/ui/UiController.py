from .ui import DisplayBounds
from ..misc import Updateable, Updater


class UiController(Updater, Updateable):

    # splash_callback must contain a get_root() function
    def __init__(self, display_driver, font_loader, splash_callback = None):     
        Updater.__init__(self)

        self.__font_loader = font_loader
        self.__display_driver = display_driver
        self.__splash_callback = splash_callback

        self.__current_splash_element = None

    def set_callback(self, splash_callback):
        self.__splash_callback = splash_callback

    @property
    def bounds(self):
        return DisplayBounds(0, 0, self.__display_driver.width, self.__display_driver.height)

    # Initialize the GUI. Mus be called before usage.
    def init(self, appl):
        self.__appl = appl

        self.__splash_callback.init(appl, self)

    def parameter_changed(self, mapping):
        self.show()

    def request_terminated(self, mapping):
        pass

    #@RuntimeStatistics.measure
    def update(self):
        Updater.update(self)

    # Shows the current splash
    def show(self):
        # Get DisplayElement from callback
        splash_element = self.__splash_callback.get_root()

        if splash_element == self.__current_splash_element:
            return

        # Make it a splash (creates the Group if not yet done)
        splash_element.make_splash(self.__font_loader)

        if not splash_element.initialized():
            splash_element.init(splash_element, self.__appl)

        # Add elements which are Updateables to the update queue
        self.updateables = [i for i in splash_element.contents_flat() if isinstance(i, Updateable)]
        
        # Show splash
        self.__current_splash_element = splash_element
        self.__display_driver.tft.show(splash_element.splash)
