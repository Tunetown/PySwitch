from gc import collect
from micropython import const
from displayio import Group
from adafruit_display_text import label, wrap_text_to_pixels
from adafruit_display_shapes.rect import Rect

from .ui import DisplayBounds, DisplayElement

from ..controller.client import BidirectionalClient
from ..misc import Updateable, get_option #, do_print
from ..colors import Colors


# Data class for layouts
class DisplayLabelLayout:

    # layout:
    #  {
    #     "font": Path to the font, example: "/fonts/H20.pcf"
    #     "maxTextWidth": Maximum text width in pixels (default: 220) optional
    #     "lineSpacing": Line spacing (optional), float (default: 1)
    #     "textColor": Text color (default is auto)
    #     "backColor": Background color (default is none) Can be a tuple also to show a rainbow background
    #     "text": Initial text (default is none)
    #     "stroke": Amount of pixels to reduce from the background (fake frame, default: 0)
    # }
    def __init__(self, layout = {}):
        self.font_path = get_option(layout, "font", None)
        self.max_text_width = get_option(layout, "maxTextWidth")
        self.line_spacing = get_option(layout, "lineSpacing", 1)
        self.text = str(get_option(layout, "text", ""))
        self.text_color = get_option(layout, "textColor", None)
        self.back_color = get_option(layout, "backColor", None)
        self.stroke = get_option(layout, "stroke", 0)

    # Check mandatory fields
    def check(self, label_id):
        if not self.font_path:
            raise Exception(f"Font missing: { repr(label_id) }")


######################################################################################################################################


# Controller for a generic rectangular label on the user interface.
class DisplayLabel(DisplayElement):

    # Line feed used for display
    LINE_FEED = "\n"

    def __init__(self, layout = None, bounds = DisplayBounds(), name = "", id = 0, scale = 1, callback = None):
        super().__init__(bounds = bounds, name = name, id = id)

        self.__layout = DisplayLabelLayout(layout if layout else {})
        self.__layout.check(self.id)
        self.__initial_text_color = self.__layout.text_color        

        self.__scale = scale
        self.callback = callback

        self.__ui = None    
        self.__appl = None
        self.__background = None 
        self.__label = None

        self.override_text = None
        
    def update_label(self):
        if self.override_text:
            self.text = self.override_text
        elif self.callback:
            self.callback.update_label(self)

    # Adds the slot to the splash
    def init(self, ui, appl):
        self.__ui = ui
        self.__appl = appl

        self.__update_font()

        if self.callback:
            that = self

            class _CallbackMappingListener:
                def parameter_changed(self, mapping):
                    that.update_label()

                def request_terminated(self, mapping):
                    that.update_label()

            self.callback.init(appl, _CallbackMappingListener())

        # Append background, if any
        if self.__layout.back_color:
            collect()
            self.__background = Rect(
                x = self.bounds.x + self.__layout.stroke, 
                y = self.bounds.y + self.__layout.stroke,
                width = self.bounds.width - self.__layout.stroke * 2, 
                height = self.bounds.height - self.__layout.stroke * 2, 
                fill = self.__layout.back_color
            )
            ui.splash.append(self.__background)

        # Trigger automatic text color determination
        self.text_color = self.__layout.text_color

        # Trigger text wrapping
        self.text = self.__layout.text

        # Append text area
        self.__label = label.Label(
            self.__font,
            anchor_point = (0.5, 0.5), 
            anchored_position = (
                int(self.bounds.width / 2), 
                int(self.bounds.height / 2)
            ),
            text = self.__wrap_text(self.__layout.text),
            color = self.__layout.text_color,
            line_spacing = self.__layout.line_spacing,
            scale = self.__scale
        )
        
        group = Group(
            scale = 1, 
            x = self.bounds.x, 
            y = self.bounds.y
        )
        group.append(self.__label)
        ui.splash.append(group)

        super().init(ui, appl)

    # Update font according to layout
    def __update_font(self):
        self.__font = self.__ui.font_loader.get(self.__layout.font_path)

    @property
    def back_color(self):
        return self.__layout.back_color

    @back_color.setter
    def back_color(self, color):
        if self.__layout.back_color and not color:            
            raise Exception() #"You can not remove a background (set color to black instead)")            

        if not self.__layout.back_color and color:
            raise Exception() #"You can only change the background color if an initial background color has been passed")
        
        if self.__layout.back_color == color:
            return

        self.__layout.back_color = color

        if self.__background:
            self.__background.fill = color

        # Update text color, too (might change when no initial color has been set)
        self.text_color = self.__initial_text_color

    @property
    def text_color(self):
        return self.__layout.text_color

    @text_color.setter
    def text_color(self, color):
        text_color = color        
        if not text_color:
            text_color = self.__determine_text_color()

        if self.__layout.text_color == text_color:
            return
        
        self.__layout.text_color = text_color

        if self.__label:
            self.__label.color = text_color

    @property
    def text(self):
        return self.__layout.text

    @text.setter
    def text(self, text):
        # In case of low memory detected by the controller, we just show this information
        if self.__appl and hasattr(self.__appl, "low_memory_warning") and self.__appl.low_memory_warning:
            text = "Low Memory!"
        
        text_str = str(text)

        if self.__layout.text == text_str:
            return
        
        self.__layout.text = text_str

        if self.__label:
            self.__label.text = self.__wrap_text(text_str)

    # Wrap text if requested
    def __wrap_text(self, text):
        if not text:
            return ""
        
        if self.__layout.max_text_width:
            return DisplayLabel.LINE_FEED.join(
                wrap_text_to_pixels(
                    text, 
                    self.__layout.max_text_width,
                    self.__font
                )
            )
        else:
            return text

    # Determines a matching text color to the current background color.
    # Algorithm adapted from https://nemecek.be/blog/172/how-to-calculate-contrast-color-in-python
    def __determine_text_color(self):
        if not self.back_color:
            return Colors.WHITE
        
        luminance = self.back_color[0] * 0.2126 + self.back_color[1] * 0.7151 + self.back_color[2] * 0.0721

        if luminance < 140:
            return Colors.WHITE
        else:
            return Colors.BLACK        


###########################################################################################################################


class TunerDisplay(DisplayElement):

    # DisplayElement for the deviance bar
    class _TunerDevianceDisplay(DisplayElement):

        def __init__(self, 
                    bounds, 
                    zoom,
                    width, 
                    color_in_tune,
                    color_out_of_tune,
                    color_neutral,
                    calibration_high,
                    calibration_low,
                    id = 0
            ):
            DisplayElement.__init__(self, bounds = bounds, id = id)

            self.width = width
            self.__zoom = zoom

            self.__color_in_tune = color_in_tune
            self.__color_out_of_tune = color_out_of_tune
            self.__color_neutral = color_neutral
            self.__calibration_high = calibration_high
            self.__calibration_low = calibration_low

            self.__current_color = None
            self.in_tune = False

        def init(self, ui, appl):
            DisplayElement.init(self, ui, appl)
            
            collect()

            self.__marker_intune = Rect(
                x = int(self.bounds.x + (self.bounds.width - self.width) * 0.5),
                y = self.bounds.y,
                width = self.width,
                height = self.bounds.height,
                fill = self.__color_neutral
            )

            ui.splash.append(self.__marker_intune)

            self.__marker = Rect(
                x = int(self.bounds.x + (self.bounds.width - self.width) * 0.5),
                y = self.bounds.y,
                width = self.width,
                height = self.bounds.height,
                fill = self.__color_in_tune
            )
            self.__current_color = self.__marker.fill

            ui.splash.append(self.__marker)

        # Sets deviance value in range [0..16383]
        def set(self, value):
            value_scaled = value
            if self.__zoom != 1:
                value_scaled = max(-8192, min(int((value - 8192) * self.__zoom), 8192)) + 8191

            self.__marker.x = int(self.bounds.x + (self.bounds.width - self.width) * value_scaled / 16384)

            if value >= self.__calibration_low and value <= self.__calibration_high:
                self.in_tune = True
                self.set_color(self.__color_in_tune)
            else:
                self.in_tune = False
                self.set_color(self.__color_out_of_tune)

        # Sets the color
        def set_color(self, color):
            if self.__current_color == color:
                return
            
            self.__current_color = color
            self.__marker.fill = color


    ##################################################################################################


    def __init__(self, 
                 mapping_note = None, 
                 mapping_deviance = None, 
                 bounds = DisplayBounds(),                 # Bounds of the overall display
                 layout = {},                              # Layout for the Note label
                 scale = 1,                                # Scaling of the note display label
                 deviance_height = 40,                     # Height of the deviance display (taken from the bottom of overall space)
                 deviance_width = 5,                       # Width of the deviance display pointer line and "in tune" marker
                 deviance_zoom = 2.4,                      # Scaling of values. Set to > 1 to make the tuner display more sensitive.
                 color_in_tune = Colors.LIGHT_GREEN,
                 color_out_of_tune = Colors.ORANGE,
                 color_neutral = Colors.WHITE,
                 calibration_high = 8192 + 350,            # Threshold value above which the note is out of tune
                 calibration_low = 8192 - 350,             # Threshold value above which the note is out of tune
                 note_names = None                         # If set, this must be a tuple or list of 12 note name strings starting at C.
        ):
        DisplayElement.__init__(self, bounds = bounds)

        self.__mapping_note = mapping_note
        self.__mapping_deviance = mapping_deviance

        self.__color_in_tune = color_in_tune
        self.__color_out_of_tune = color_out_of_tune
        self.__color_neutral = color_neutral
        self.__note_names = note_names if note_names else ('C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B')

        if self.__mapping_note:
            self.label_note = DisplayLabel(
                bounds = bounds,
                layout = layout,
                scale = scale
            )
            self.add(self.label_note)
        else:
            self.label_note = None

        if self.__mapping_deviance:
            self.deviance = self._TunerDevianceDisplay(
                bounds = DisplayBounds(
                    bounds.x,
                    bounds.y + bounds.height - int(deviance_height),
                    bounds.width,
                    int(deviance_height)
                ),
                width = deviance_width,
                zoom = deviance_zoom,
                color_in_tune = color_in_tune,
                color_out_of_tune = color_out_of_tune,
                color_neutral = color_neutral,
                calibration_high = calibration_high,
                calibration_low = calibration_low
            )            
            self.add(self.deviance)

        self.__last_note = None
        self.__last_deviance = 8192

    # We need access to the client, so we store appl here
    def init(self, ui, appl):
        DisplayElement.init(self, ui, appl)

        self.__appl = appl
        
        # Register mappings
        if self.__mapping_note:
            self.__appl.client.register(self.__mapping_note, self)

        if self.__mapping_deviance:
            self.__appl.client.register(self.__mapping_deviance, self)

    # Reset the display
    def reset(self):
        self.__last_note = None
        self.__last_deviance = 8192
        
        if self.label_note:
            self.label_note.text = "-"
            self.label_note.text_color = self.__color_neutral

    # Listen to client value returns
    def parameter_changed(self, mapping):
        value = mapping.value

        if mapping == self.__mapping_note and value != self.__last_note:
            self.__last_note = mapping.value

            self.label_note.text = self.__note_names[value % 12]            

        if mapping == self.__mapping_deviance and value != self.__last_deviance:
            self.__last_deviance = value               
            
            self.deviance.set(self.__last_deviance)            

            # Uncomment this for calibration.
            #self._debug_calibration(mapping.value)            

            if self.label_note:
                if self.deviance.in_tune:
                    self.label_note.text_color = self.__color_in_tune
                else:
                    self.label_note.text_color = self.__color_out_of_tune
        
    # Called when the client is offline (requests took too long)
    def request_terminated(self, mapping):
        pass                                       # pragma: no cover

    # For calibration: Shows statistics on the tuner deviance over a period of 4 seconds.
    #def _debug_calibration(self, value):
    #    if not hasattr(self, "_calib_period"):
    #        from ..misc import PeriodCounter
    #        self._calib_period = PeriodCounter(4000)
    #        self._min = 9999999
    #        self._max = -1
    #        self._sum = 0
    #        self._steps = 0
    #    
    #    self._sum += value
    #    self._steps += 1
    #
    #    if value > self._max:
    #        self._max = value
    #    if value < self._min:
    #        self._min = value
    #
    #    if self._calib_period.exceeded:
    #        avg = int(self._sum / self._steps)
    #        do_print("[ " + repr(self._min - avg) + " .. " + repr(self._max - avg) + " ] Avg: " + repr(avg))
    #
    #        self._min = 9999999
    #        self._max = -1
    #        self._sum = 0
    #        self._steps = 0


###########################################################################################################################


# Properties for the indicator dots
_PERFORMANCE_INDICATOR_SIZE = const(4)
_PERFORMANCE_INDICATOR_MARGIN = const(2)


# Shows a small dot indicating the bidirectional protocol state (does not show anything when bidirectional 
# communication is disabled)
class BidirectionalProtocolState(DisplayElement, Updateable):

    def __init__(self, bounds = DisplayBounds(), name = "", id = 0):
        DisplayElement.__init__(
            self, 
            bounds = DisplayBounds(
                x = bounds.x + bounds.width - _PERFORMANCE_INDICATOR_SIZE - _PERFORMANCE_INDICATOR_MARGIN,
                y = bounds.y + _PERFORMANCE_INDICATOR_MARGIN,
                w = int(_PERFORMANCE_INDICATOR_SIZE),
                h = int(_PERFORMANCE_INDICATOR_SIZE)
            ), 
            name = name, 
            id = id
        )

        self.__current_color = None

    def init(self, ui, appl):
        DisplayElement.init(self, ui, appl)
        self.__appl = appl

        if not isinstance(self.__appl.client, BidirectionalClient):
            return

        r = int(self.bounds.width / 2) if self.bounds.width > self.bounds.height else int(self.bounds.height / 2)
        
        collect()
        
        self.__dot = Rect(
            x = self.bounds.x, 
            y = self.bounds.y,
            width = 2 * r,
            height = 2 * r,
            fill = (0, 0, 0)
        )
        ui.splash.append(self.__dot)

    def update(self):
        if not isinstance(self.__appl.client, BidirectionalClient):
            return

        new_color = self.__appl.client.protocol.get_color()

        if self.__current_color == new_color:
            return

        self.__current_color = new_color
        self.__dot.fill = self.__current_color
            
