from ....controller.actions import PushButtonAction
from ...kemper import KemperMappings
from .effect_state import KemperEffectEnableCallback


# Switch an effect slot on / off, with per-rig slot override support.
# When the active rig changes, the button automatically controls a different slot
# according to the rig_overrides mapping.
def EFFECT_STATE_PER_RIG(
        slot_id,
        rig_overrides,
        display = None,
        mode = PushButtonAction.HOLD_MOMENTARY,
        show_slot_names = False,
        id = False,
        text = None,
        color = None,
        use_leds = True,
        enable_callback = None
    ):
    # rig_overrides: dict mapping absolute rig IDs to slot IDs.
    #   absolute rig ID = (bank - 1) * 5 + (rig - 1)
    #   where bank is 1-based and rig is 1-5.
    # Example:
    #   rig_overrides = {
    #       2: KemperEffectSlot.EFFECT_SLOT_ID_C,   # Bank 1, Rig 3 -> slot C
    #       5: KemperEffectSlot.EFFECT_SLOT_ID_DLY,  # Bank 2, Rig 1 -> slot DLY
    #   }
    return PushButtonAction({
        "callback": KemperEffectEnablePerRigCallback(
            slot_id = slot_id,
            rig_overrides = rig_overrides,
            text = text,
            color = color,
            show_slot_names = show_slot_names
        ),
        "mode": mode,
        "display": display,
        "id": id,
        "useSwitchLeds": use_leds,
        "enableCallback": enable_callback,
    })


class KemperEffectEnablePerRigCallback(KemperEffectEnableCallback):
    """
    Like KemperEffectEnableCallback but with per-rig slot override support.

    slot_id:       Default effect slot (used when no override exists for the current rig).
    rig_overrides: Dict mapping absolute rig IDs to slot IDs.
                   Absolute rig ID = (bank - 1) * 5 + (rig - 1)
                   where bank is 1-based and rig is 1-5.

    When the Kemper changes rig, the button automatically controls the slot
    specified in rig_overrides for that rig, or falls back to slot_id.
    LED color and display label update automatically to reflect the new slot's effect type.
    """

    def __init__(self, slot_id, rig_overrides, **kwargs):
        super().__init__(slot_id, **kwargs)

        self._default_slot = slot_id
        self._rig_overrides = rig_overrides

        # Pre-create state and type mappings for all override slots that differ from the default.
        # These are registered so the client tracks their state via bidirectional MIDI.
        override_slots = set(rig_overrides.values()) - {slot_id}
        self._override_state_maps = {}
        self._override_type_maps = {}
        for slot in override_slots:
            sm = KemperMappings.EFFECT_STATE(slot)
            tm = KemperMappings.EFFECT_TYPE(slot)
            self._override_state_maps[slot] = sm
            self._override_type_maps[slot] = tm
            self.register_mapping(sm)
            self.register_mapping(tm)

        # Track the current rig via the Kemper RIG_ID mapping.
        self._rig_id_mapping = KemperMappings.RIG_ID()
        self.register_mapping(self._rig_id_mapping)
        self._appl_ref = None

    def init(self, appl, listener=None):
        super().init(appl, listener)
        # Store appl reference separately for use in state_changed_by_user().
        # BinaryParameterCallback stores __appl with name mangling, so we keep our own.
        self._appl_ref = appl

    def _current_slot(self):
        """Return the effective slot ID for the current rig."""
        rig = self._rig_id_mapping.value
        if rig is None:
            return self._default_slot
        return self._rig_overrides.get(rig, self._default_slot)

    def state_changed_by_user(self):
        """Send MIDI CC to toggle the effect on the currently active slot."""
        slot = self._current_slot()
        if slot == self._default_slot:
            super().state_changed_by_user()
        else:
            mapping = self._override_state_maps[slot]
            # Toggle: if the slot is currently on (value=1), turn it off, and vice versa.
            value = 0 if (mapping.value == 1) else 1
            self._appl_ref.client.set(mapping, value)

    def update_displays(self):
        """Update LED and display label for the currently active slot."""
        slot = self._current_slot()
        if slot == self._default_slot:
            super().update_displays()
        else:
            # Reset the internal effect-type cache so EffectEnableCallback re-evaluates
            # the label text and color for the override slot.
            self._EffectEnableCallback__current_kpp_type = None

            # Temporarily redirect self.mapping and self.mapping_fxtype to the override slot
            # so the parent update_displays() reads from the right slot.
            orig_mapping = self.mapping
            orig_fxtype = self.mapping_fxtype
            self.mapping = self._override_state_maps[slot]
            self.mapping_fxtype = self._override_type_maps[slot]
            super().update_displays()
            self.mapping = orig_mapping
            self.mapping_fxtype = orig_fxtype

            # Reset again so that when we switch back to the default slot
            # the label is re-evaluated instead of being skipped by the cache.
            self._EffectEnableCallback__current_kpp_type = None

    def parameter_changed(self, mapping):
        """
        Called when any registered mapping receives a MIDI update.
        Trigger a display refresh on rig change, or when the active override slot changes state.
        """
        if mapping is self._rig_id_mapping:
            # Rig changed: update display to reflect the new slot.
            self.update_displays()
        else:
            active_slot = self._current_slot()
            if active_slot != self._default_slot and (
                mapping is self._override_state_maps.get(active_slot) or
                mapping is self._override_type_maps.get(active_slot)
            ):
                # Active override slot state or type changed: update display.
                self.update_displays()
            else:
                super().parameter_changed(mapping)
