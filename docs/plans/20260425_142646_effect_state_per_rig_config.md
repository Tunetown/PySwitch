# Piano: Configurazione EFFECT_STATE_PER_RIG per 5 switch

**Data**: 2026-04-25  
**Branch**: feature/effect-state-per-rig  
**Dispositivo**: MIDICaptain 10

## Obiettivo

Riconfigurare `content/inputs.py` e `content/display.py` da zero per gestire
5 switch con `EFFECT_STATE_PER_RIG`:

- Switch 1 e 2: sempre disabilitati (nessuna azione)
- Switch 3, 4, 5: disabilitati di default (`slot_id=None`), attivi solo per
  i rig specificati

## Mapping switch → display

| Switch HW              | Label utente | Display slot       |
|------------------------|--------------|--------------------|
| PA_MIDICAPTAIN_10_SWITCH_1 | Switch 1 | nessuno (disabilitato) |
| PA_MIDICAPTAIN_10_SWITCH_2 | Switch 2 | nessuno (disabilitato) |
| PA_MIDICAPTAIN_10_SWITCH_3 | Switch 3 | DISPLAY_FOOTER_1   |
| PA_MIDICAPTAIN_10_SWITCH_4 | Switch 4 | DISPLAY_FOOTER_2   |
| PA_MIDICAPTAIN_10_SWITCH_UP | Switch 5 | nessuno           |

## Mapping rig → slot per switch

Rig ID assoluto = (bank-1)*5 + (rig-1), banco 1 rig 1-5 → ID 0-4.

| Rig | Nome  | Switch 3          | Switch 4              | Switch 5              |
|-----|-------|-------------------|-----------------------|-----------------------|
| 0   | acou  | disabilitato      | [MOD + C] insieme     | DLY                   |
| 1   | clen  | X                 | disabilitato          | [DLY + REV] insieme   |
| 2   | crnc  | X                 | disabilitato          | [DLY + REV] insieme   |
| 3   | heavy | disabilitato      | X                     | [DLY + REV] insieme   |
| 4   | lead  | X                 | disabilitato          | disabilitato          |

## Slot Kemper

- `EFFECT_SLOT_ID_X`   = 4  (X)
- `EFFECT_SLOT_ID_MOD` = 5  (MOD)
- `EFFECT_SLOT_ID_C`   = 2  (C)
- `EFFECT_SLOT_ID_DLY` = 6  (DLY)
- `EFFECT_SLOT_ID_REV` = 7  (REV)

## File da creare / modificare

1. `content/inputs.py` — configurazione switch (da zero)
2. `content/display.py` — layout display semplificato (da zero)
3. `test/pyswitch/test_kemper_action_effect_state_per_rig.py` — test unitari

## Stato

- [x] display.py
- [x] inputs.py
- [x] test file (26 test)
- [x] test verdi (363/363 OK)
