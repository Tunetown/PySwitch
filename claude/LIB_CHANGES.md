# Changes to existing files (compared to `dev_midi` @ `955fdd0`)

Every change to a file that already exists on `dev_midi` is logged here. New files are not listed.

Format, one block per file:

```
### <path>
- <Class.method or function> – <description>
```

---

### content/lib/pyswitch/hardware/devices/pa_midicaptain.py
- `PA_MIDICAPTAIN_DIN_MIDI()` – signature changed to `(receive_chunk_size = 50)`, passed through to `AdafruitDinMidiDevice`. The old parameters `in_channel`, `out_channel`, `in_buf_size` are no longer accepted by `AdafruitDinMidiDevice.__init__()` (since `993406c`) and caused a `TypeError` on construction. All existing callers use no arguments.
