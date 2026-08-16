## Example Description

This demonstrates `EFFECT_STATE_PER_RIG`: assigning a different Kemper effect slot to the same
switch depending on which rig is currently active, so a button keeps controlling "the delay" or
"the modulation effect" even when different rigs put those effects in different slots.

Rigs are identified by their absolute rig ID (`(bank - 1) * 5 + (rig - 1)`). This example uses
bank 1 with five rigs: 0 = acoustic, 1 = clean, 2 = crunch, 3 = heavy, 4 = lead. `rig_overrides`
maps a rig ID to one slot ID, a list of slot IDs (combined with AND — the button turns the LED
on only if all of them are engaged), or is simply left out for a rig to fall back to `slot_id`
(here `None`, so the button is off and the display is cleared on any rig without an override).

Switches A-E also demonstrate `BANK_UP`/`BANK_DOWN` on long press, which keep the currently
selected rig slot when moving to the next/previous bank instead of resetting it.

| Switch     | Short Press | Long Press |
|------------|-------------|------------|
| Switch 1   | (not used)  |            |
| Switch 2   | (not used)  |            |
| Switch 3   | FX per rig: flanger (X) on clean/crunch/lead |  |
| Switch 4   | FX per rig: mod+comp (MOD+C) on acoustic, X on heavy |  |
| Switch up  | FX per rig: delay (DLY) on acoustic, delay+reverb (DLY+REV) on clean/crunch/heavy |  |
| Switch A   | Select rig 1 of curr. bank | Bank down (keeps rig slot) |
| Switch B   | Select rig 2 of curr. bank |  |
| Switch C   | Select rig 3 of curr. bank |  |
| Switch D   | Select rig 4 of curr. bank |  |
| Switch dn  | Select rig 5 of curr. bank | Bank up (keeps rig slot) |
