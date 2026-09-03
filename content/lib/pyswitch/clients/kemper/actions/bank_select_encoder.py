from ....controller.actions.EncoderAction import EncoderAction
from ..mappings.select import MAPPING_BANK_SELECT
from ....misc import PeriodCounter
from .. import NUM_BANKS, NUM_RIGS_PER_BANK

# Preselects the bank with a rotary encoder. 
# 
# After this, the bank change will be done after a rig has been selected.
def ENCODER_BANK_SELECT(
    midi_channel = 1,              # MIDI Channel in range [1..16]
    preview_display = None,        # If assigned, the adjusted value will be displayed in the passed DisplayLabel when the encoder is adjusted. 
                                   # 
                                   # Bank Preselect is always shown in the Rig Name/ID display, regardless of this option. However, the preselect display is not updated too often so it makes total sense to set your rig name display here, too.
    step_width = 0.5,              # Step width. Can be set to any value greater than 0 (including float values).
    enable_callback = None,
    id = None
):
    return _BankSelectEncoderAction(
        preview_display = preview_display,
        step_width = step_width,
        enable_callback = enable_callback,
        id = id,
        channel = midi_channel - 1
    )


class _BankSelectEncoderAction(EncoderAction):

    def __init__(self,
                 channel,
                 preview_display = None,
                 step_width = 0.5,
                 preselect_blink_interval = 400,
                 enable_callback = None,
                 id = None
    ):
        super().__init__(
            mapping = MAPPING_BANK_SELECT(channel),
            preview_display = preview_display,
            step_width = step_width,
            max_value = NUM_BANKS - 1,
            enable_callback = enable_callback,
            id = id,
            convert_value = _convert_value
        )

        self.__preselect_blink_period = PeriodCounter(preselect_blink_interval)
        
    def update(self):
        super().update()

        if "preselectedBank" in self._appl.shared and self._appl.shared["preselectCallback"] == self and self.__preselect_blink_period.exceeded:
            self._appl.shared["preselectBlinkState"] = not self._appl.shared["preselectBlinkState"]

    def accept(self):
        super().accept()

        if self._last_value == -1:
            return

        if not "preselectCallback" in self._appl.shared or not self._appl.shared["preselectCallback"] == self:
            self._appl.shared["preselectCallback"] = self                
            self._appl.shared["preselectBlinkState"] = False

        self._appl.shared["preselectedBank"] = self._last_value

    def _get_value(self):
        return int(self._mapping.value / NUM_RIGS_PER_BANK)

    def _set_value(self, value):
        self._mapping.value = value * NUM_RIGS_PER_BANK


def _convert_value(value):
    return f"Bank { value + 1 }"