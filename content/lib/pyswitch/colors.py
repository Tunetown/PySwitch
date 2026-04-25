# Color definitions (can be used for LEDs and labels)
class Colors:

    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (130, 130, 0)
    ORANGE = (255, 125, 0)
    RED = (255, 0, 0)
    LIGHT_RED = (255, 100, 100)
    PINK = (255, 125, 70)
    PURPLE = (180, 0, 120)
    DARK_PURPLE = (100, 0, 65)
    LIGHT_GREEN = (100, 255, 100)
    GREEN = (0, 255, 0)
    DARK_GREEN = (73, 110, 41)
    TURQUOISE = (64, 242, 208)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (100, 100, 255)
    DARK_BLUE = (0, 0, 120)
    GRAY = (190, 190, 190)
    DARK_GRAY = (50, 50, 50)
    BLACK = (0, 0, 0)

# Default background color for display slots
DEFAULT_LABEL_COLOR = (50, 50, 50)

# Default color for switches
DEFAULT_SWITCH_COLOR = (255, 255, 255)

##########################################################

# Dims a passed color for display of disabled state
def dim_color(color, factor):
    if isinstance(color[0], tuple):
        # Multi color
        return [(
                int(c[0] * factor),
                int(c[1] * factor),
                int(c[2] * factor)
            ) for c in color]            
    else:
        # Single color
        return (
            int(color[0] * factor),
            int(color[1] * factor),
            int(color[2] * factor)
        )
