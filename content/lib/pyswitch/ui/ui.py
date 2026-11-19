from displayio import Group


# Represents a screen area with dimensions.
class DisplayBounds:
    def __init__(self, x = 0, y = 0, w = 0, h = 0):
        self.x = int(x)
        self.y = int(y)
        self.width = int(w)
        self.height = int(h)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    def clone(self):
        return DisplayBounds(
            self.x,
            self.y,
            self.width,
            self.height
        )
    


########################################################################################################


# Base class for all display elements
class DisplayElement:

    def __init__(self, bounds = DisplayBounds(), name = "", id = 0, children = None):
        self.bounds = DisplayBounds(
            x = bounds.x,
            y = bounds.y,
            w = bounds.width,
            h = bounds.height
        )
        self.name = name
        self.id = id
        self.splash = None

        self.__initialized = False

        self.children = children

    # Adds the element to the splash
    def init(self, ui, appl):
        self.__initialized = True

        if self.children:
            for child in self.children:
                if child == None:
                    continue
                
                if child.initialized():
                    continue

                child.init(ui, appl)
        
    # Makes this element the splash holder which is passed as ui to init() later
    def make_splash(self, font_loader):
        if self.splash:
            return      
        
        self.font_loader = font_loader
        self.splash = Group()

    def initialized(self):
        if self.children:
            for child in self.children:
                if child == None:
                    continue
                
                if not child.initialized():
                    return False

        return self.__initialized

    # Adds a child to the element. 
    def add(self, child):
        if not self.children:
            self.children = []
        
        self.children.append(child)

    # Returns a list of all contained DisplayElements.
    def contents_flat(self):
        ret = [self]

        if self.children:
            for child in self.children:
                if not child:
                    continue

                ret += child.contents_flat()

        return ret
    