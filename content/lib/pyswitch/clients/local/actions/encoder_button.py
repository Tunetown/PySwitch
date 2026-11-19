from ....controller.actions import Action
from ....controller.callbacks import Callback

# This simple action is used in conjunction with a rotary encoder: If you assign this to an encoder action using its "accept_action" parameter, the encoder will not send any value until this switch is pushed.
# 
# You can also use this to cancel the preselection, see Encoder Action's parameter "cancel_action".
# 
# It makes the most sense assigned to an encoder wheel's own pushbutton, but technically it can be assigned to any switch.
def ENCODER_BUTTON(id = False, 
                   enable_callback = None
    ):
    return Action({
        "callback": _EncoderButtonCallback(),
        "id": id,
        "enableCallback": enable_callback
    })


class _EncoderButtonCallback(Callback):

    def __init__(self):
        super().__init__()
        
        self.__encoders = []
        self.__cancel_mode = False

    # cancel_mode tells us what to trigger later on, accept() or cancel().
    def register_encoder(self, encoder, cancel_mode):
        self.__encoders.append(encoder)
        self.__cancel_mode = cancel_mode

    def push(self):
        for encoder in self.__encoders:
            if self.__cancel_mode:
                encoder.cancel()
            else:
                encoder.accept()

    def release(self):
        pass

    def update_displays(self):
        pass
