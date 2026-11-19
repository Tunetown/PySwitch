from .ui import DisplayBounds

# Functions for modifying DisplayBounds for subtractive layouting

# Returns a copy which is translated
def translated(bounds, x, y):
    cl = bounds.clone()
    translate(cl, int(x), int(y))
    return cl

# Move by
def translate(bounds, x, y):
    bounds.x = bounds.x + int(x)
    bounds.y = bounds.y + int(y)

# Removes a part of the rectangle and returns it.
def remove_from_top(bounds, amount):
    ret = DisplayBounds(
        bounds.x,
        bounds.y,
        bounds.width,
        int(amount)
    )

    bounds.y = bounds.y + int(amount)
    bounds.height = bounds.height - int(amount)
    
    return ret

# Removes a part of the rectangle and returns it.
def remove_from_bottom(bounds, amount):
    ret = DisplayBounds(
        bounds.x,
        bounds.y + bounds.height - int(amount),
        bounds.width,
        int(amount)
    )

    bounds.height = bounds.height - int(amount)
    
    return ret

# Removes a part of the rectangle and returns it.
def remove_from_left(bounds, amount):
    ret = DisplayBounds(
        bounds.x,
        bounds.y,
        int(amount),
        bounds.height
    )

    bounds.x = bounds.x + int(amount)
    bounds.width = bounds.width - int(amount)
    
    return ret

# Removes a part of the rectangle and returns it.
def remove_from_right(bounds, amount):
    ret = DisplayBounds(
        bounds.x + bounds.width - int(amount),
        bounds.y,
        int(amount),
        bounds.height
    )

    bounds.width = bounds.width - int(amount)
    
    return ret

# Returns a part of the rectangle without modifying it
def top(bounds, amount):
    return DisplayBounds(
        bounds.x,
        bounds.y,
        bounds.width,
        int(amount)
    )

# Returns a part of the rectangle without modifying it
def bottom(bounds, amount):
    return DisplayBounds(
        bounds.x,
        bounds.y + bounds.height - int(amount),
        bounds.width,
        int(amount)
    )

# Returns a part of the rectangle without modifying it
def left(bounds, amount):
    return DisplayBounds(
        bounds.x,
        bounds.y,
        int(amount),
        bounds.height
    )

# Returns a part of the rectangle without modifying it    
def right(bounds, amount):
    return DisplayBounds(
        bounds.x + bounds.width - int(amount),
        bounds.y,
        int(amount),
        bounds.height
    )

# Returns a copy of the rectangle at the given position
def with_position(bounds, x, y):
    return DisplayBounds(
        int(x),
        int(y),
        bounds.width,
        bounds.height
    )

