from ....controller.callbacks import Callback
from ....controller.actions import Action

# Simple action to display a message in a display field
def DISPLAY_MESSAGE(text, display=None, color=None, id=None, enable_callback=None):
	return Action({
		"callback": _DisplayMessageCallback(text=text, color=color),
		"display": display,
		"id": id,
		"enableCallback": enable_callback
	})


class _DisplayMessageCallback(Callback):
	def __init__(self, text, color=None):
		super().__init__()
		self._text = text
		self._color = color

	def update_displays(self):
		if self.action and self.action.label:
			self.action.label.text = self._text
			if self._color is not None:
				self.action.label.back_color = self._color
