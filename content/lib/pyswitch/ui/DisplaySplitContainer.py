from .ui import DisplayElement, DisplayBounds

# Contains a list of display elements. If template_element is given, this element is
# never used itself but cloned for creating 
class DisplaySplitContainer(DisplayElement):
    
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, direction = 0, bounds = DisplayBounds(), name = "", id = 0, children = None):
        DisplayElement.__init__(self, bounds = bounds, name = name, id = id, children = children)

        self.direction = direction        
    
    # Add a child element
    def add(self, child):
        super().add(child)
        self.update_bounds()
        
    # Update dimensions of all contained elements
    def update_bounds(self):
        if not self.children:
            return
         
        active_children = [x for x in self.children if x != None]

        if len(active_children) == 0:
            return
        
        bounds = self.bounds

        # Horizontal
        if self.direction == DisplaySplitContainer.HORIZONTAL:
            # Horizontal
            slot_width = int(bounds.width / len(active_children))

            for i in range(len(active_children)):
                active_children[i].bounds = DisplayBounds(
                    bounds.x + i * slot_width,
                    bounds.y,
                    slot_width,
                    bounds.height
                )
        else:
            # Vertical
            slot_height = int(bounds.height / len(active_children))

            for i in range(len(active_children)):
                active_children[i].bounds = DisplayBounds(
                    bounds.x,
                    bounds.y + i * slot_height,
                    bounds.width,
                    slot_height
                )

        for c in self.children:
            if c == None:
                continue

            if isinstance(c, DisplaySplitContainer):
                c.update_bounds()

