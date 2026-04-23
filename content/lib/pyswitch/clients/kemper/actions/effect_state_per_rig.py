from ....controller.actions import PushButtonAction
from ...kemper import KemperMappings
from .effect_state import KemperEffectEnableCallback


# Switch an effect slot on / off, with per-rig slot override support.
# When the active rig changes, the button automatically controls a different slot
# according to the rig_overrides mapping.
#
# rig_overrides: dict mapping absolute rig IDs to slot ID(s).
#   Values can be:
#     - A single slot_id     → button controls that slot for this rig
#     - A list of slot_ids   → button controls all slots simultaneously;
#                              LED shows ON only when ALL slots are ON (AND logic);
#                              color/label derived from the first slot in the list
#     - None                 → button is disabled for this rig
#   Absolute rig ID = (bank - 1) * 5 + (rig - 1), bank 1-based, rig 1–5.
#
# Example:
#   rig_overrides = {
#       0: [KemperEffectSlot.EFFECT_SLOT_ID_MOD,
#           KemperEffectSlot.EFFECT_SLOT_ID_C],   # Rig 1 → controls MOD + C together
#       4: None,                                    # Rig 5 → button disabled
#   }
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
    rig_overrides: Dict mapping absolute rig IDs to slot ID(s) or None.
                   See EFFECT_STATE_PER_RIG docstring for details.
    """

    def __init__(self, slot_id, rig_overrides, **kwargs):
        super().__init__(slot_id, **kwargs)

        self._default_slot = slot_id

        # Normalize rig_overrides: store None as-is, scalars as [slot], lists as-is.
        self._rig_overrides = {}
        for rig, slots in rig_overrides.items():
            if slots is None:
                self._rig_overrides[rig] = None
            elif isinstance(slots, list):
                self._rig_overrides[rig] = slots
            else:
                self._rig_overrides[rig] = [slots]

        # Register state/type mappings for all override slots that differ from the default.
        override_slots = set()
        for slots in self._rig_overrides.values():
            if slots is None:
                continue
            for s in slots:
                if s != slot_id:
                    override_slots.add(s)

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

    def init(self, appl, listener = None):
        super().init(appl, listener)
        # Store appl reference separately for use in state_changed_by_user().
        # BinaryParameterCallback stores __appl with name mangling, so we keep our own.
        self._appl_ref = appl

    def _current_slots(self):
        """
        Return the effective list of slot IDs for the current rig.
        Returns None if the button is disabled for this rig.
        Returns [self._default_slot] when no override is configured for the rig.
        """
        rig = self._rig_id_mapping.value
        if rig is None or rig not in self._rig_overrides:
            return [self._default_slot]
        return self._rig_overrides[rig]  # None or list

    def _state_map(self, slot):
        """Return the state mapping for the given slot."""
        if slot == self._default_slot:
            return self.mapping
        return self._override_state_maps[slot]

    def _type_map(self, slot):
        """Return the type mapping for the given slot."""
        if slot == self._default_slot:
            return self.mapping_fxtype
        return self._override_type_maps[slot]

    def state_changed_by_user(self):
        """Send MIDI CC to toggle the effect on the currently active slot(s)."""
        slots = self._current_slots()
        if slots is None:
            return  # Button disabled for this rig

        if slots == [self._default_slot]:
            super().state_changed_by_user()
            return

        # Override slot(s): AND logic — all ON → turn all OFF, else → turn all ON.
        all_on = all(self._state_map(s).value == 1 for s in slots)
        new_value = 0 if all_on else 1
        for s in slots:
            self._appl_ref.client.set(self._state_map(s), new_value)
        self.update()

    def update_displays(self):
        """Update LED and display label for the currently active slot(s)."""
        slots = self._current_slots()

        if slots is None:
            # Disabled for this rig: turn off LED and clear label.
            # Reset cached display state so the next real slot switch forces a redraw.
            self.reset()
            self.action.switch_brightness = 0
            if self.action.label:
                self.action.label.text = ""
            return

        if slots == [self._default_slot]:
            super().update_displays()
            return

        # Override slot(s): derive color/label from the first slot, AND logic for state.
        first_slot = slots[0]

        # Reset all display caches so the parent re-evaluates state, color and label
        # for the override slot. This is necessary because:
        #   1. The AND correction below may set action.state to False after the parent
        #      has already recorded state=True in its _current_display_state cache.
        #      Without a reset, subsequent calls where the first-slot value/color is
        #      unchanged will skip the display update entirely and the LED will be stuck.
        #   2. When switching between override slots the color/value caches from the
        #      previous slot must not suppress the redraw for the new slot.
        self.reset()

        # Temporarily redirect self.mapping and self.mapping_fxtype to the first override slot
        # so the parent update_displays() reads from the right slot.
        orig_mapping = self.mapping
        orig_fxtype = self.mapping_fxtype
        self.mapping = self._state_map(first_slot)
        self.mapping_fxtype = self._type_map(first_slot)

        super().update_displays()  # Sets color/label from first slot; state from first slot.

        # AND correction: if controlling multiple slots, override state with AND of all.
        if len(slots) > 1 and self.action.state:
            all_on = all(self._state_map(s).value == 1 for s in slots)
            if not all_on:
                self.action.feedback_state(False)
                type_val = self.mapping_fxtype.value
                cat = self.get_effect_category(type_val) if type_val is not None else self.CATEGORY_NONE
                color = self.get_effect_category_color(cat, type_val)
                self.set_switch_color(color)
                self.set_label_color(color)

        self.mapping = orig_mapping
        self.mapping_fxtype = orig_fxtype

        # Reset caches again so the next call always re-evaluates from scratch.
        # This ensures that a change in any secondary slot (which is not the "first
        # slot" used for color/label) triggers a correct AND re-check instead of
        # being silently skipped by the BinaryParameterCallback value cache.
        self.reset()

    def parameter_changed(self, mapping):
        """
        Called when any registered mapping receives a MIDI update.
        Trigger a display refresh on rig change, or when the active slot(s) change state.
        """
        if mapping is self._rig_id_mapping:
            # Rig changed: update display to reflect the new slot(s).
            self.update_displays()
            return

        active_slots = self._current_slots()
        if active_slots is None or active_slots == [self._default_slot]:
            super().parameter_changed(mapping)
            return

        # Check if the changed mapping belongs to any active override slot.
        for s in active_slots:
            if mapping is self._state_map(s) or mapping is self._type_map(s):
                self.update_displays()
                return

        super().parameter_changed(mapping)
