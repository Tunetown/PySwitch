from ....controller.callbacks import Callback
from ....controller.actions import Action

# Simple action to display a fixed text in a display field. Ignores any switch pushes.
def DISPLAY_FIXED_TEXT(text,                           # Text to be shown on the label
					   display = None,                 # Display label to show the fixed text on 
					   back_color = None,              # Background color of the label
					   text_color = None,              # Text color (optional, if empty this will be chosen automatically based on the background color)
					   id = None, 
					   enable_callback = None
	):
	return Action({
		"callback": _DisplayMessageCallback(
			text = text, 
			back_color = back_color,
			text_color = text_color
		),
		"display": display,
		"id": id,
		"enableCallback": enable_callback
	})


class _DisplayMessageCallback(Callback):
	def __init__(self, 
			     text, 
				 back_color = None,
				 text_color = None
	):
		super().__init__()
	
		self.__text = text
		self.__back_color = back_color
		self.__text_color = text_color

	def update_displays(self):
		if not self.action or not self.action.label:
			return
		
		self.action.label.text = self.__text
		
		if self.__back_color is not None:
			self.action.label.back_color = self.__back_color
		
		if self.__text_color is not None:
			self.action.label.color = self.__text_color

	def push(self):
		pass

	def release(self):
		pass
