# Communication Analysis: Fractal vs. Kemper

Question: is there a bidirectional protocol that must be initiated, or does Fractal only support requesting values at intervals?
Protocol details referenced here: [FRACTAL.md](FRACTAL.md).


## 1. Answer

**There is no bidirectional protocol.** Fractal's 3rd-party MIDI is purely request/response:
- no session, no handshake, no keep-alive, no sensing messages,
- the device never pushes state changes (preset, scene, bypass, channel, looper),
- the only push data is tempo beat and tuner, and only if the user has enabled *Send Realtime Sysex* (DIN only, FRACTAL.md 3.3).

So the controller has to ask for every value it wants to show, again and again. In PySwitch terms: **no protocol class**, plain `Client`, and everything is done by mappings (SPEC section 5.1).


## 2. Comparison

| Aspect                       | Kemper (bidirectional mode)                       | Fractal                                             |
|------------------------------|---------------------------------------------------|-----------------------------------------------------|
| Session setup                | Beacon SysEx (fn 0x7E) with flags and time lease  | none                                                |
| Keep-alive                   | Beacon re-sent after half the lease time          | none                                                |
| Connection detection         | Sensing message from the Kemper every ~500 ms     | none; only missing answers                          |
| Changes made on the device   | Pushed by the Kemper                              | never pushed, must be polled                        |
| Reading values               | Request per parameter                             | Request per value; status dump for all blocks       |
| Setting values               | CC / PC / SysEx                                   | CC / PC / SysEx with checksum                       |
| 14-bit value encoding        | MSB first, no checksum                            | LSB first, XOR checksum                             |
| Device type in messages      | Product type byte                                 | Model byte (not queryable)                          |
| Tuner data                   | Pushed in bidirectional mode                      | Pushed, DIN only, needs Send Realtime Sysex         |
| Tempo beat                   | Pushed in bidirectional mode                      | Pushed, DIN only, needs Send Realtime Sysex         |
| Rig / preset name            | Rig name (request or push)                        | Preset name + number (`0D`, request)                |
| Scene name                   | – (no scenes)                                     | `0E`, request                                       |
| Effect slots                 | Fixed slots (A–D, X, MOD, DLY, REV), type queried | Blocks addressed by ID, presence via status dump    |
| PySwitch implementation      | `KemperBidirectionalProtocol` + `BidirectionalClient` | plain `Client`, no protocol                     |


## 3. Do changes made on the device arrive in PySwitch?

**Yes, with a delay of at most one update interval** (plus a few ms transfer time):
- Every callback calls `client.request(mapping)` for all its mappings in each `update()`, i.e. every `updateInterval` (config.py; code default 200 ms).
- The `Client` sends a request only if no request for that mapping is pending, so mappings shared by several callbacks (e.g. the status dump) are requested once per interval.
- The answer is parsed by the mapping, and the listeners are notified. So a scene change or bypass change made on the device shows up at the next interval.
- Requests without an answer expire after `maxRequestLifetimeMillis` (default 2000 ms). The value is then reset to `None` (= device not connected).


## 4. Consequences for PySwitch

- **Traffic per interval** (example MIDI Captain 10 with 8 effect switches, preset + scene name display): status dump (~8 + 3 × blocks in preset, about 60 bytes) + preset name (10 + 42) + scene (9 + 9) + scene name (9 + 42) ≈ 180 bytes. At 200 ms that is ~900 B/s = ~30 % of DIN (3125 B/s); at 400 ms ~15 %.
- **One status dump instead of one request per block**: all effect callbacks share one status dump mapping (SPEC 5.1), so the traffic does not grow with the number of effect switches.
- **No immediate feedback after a set**: the plain `Client` has no `feedback_value()`. Callbacks therefore show the new state locally right after sending; the next poll confirms or corrects it.
- **No connection status LED** (that is a protocol feature). A missing device shows up as reset values after the request lifetime.
- **Tuner and tempo beat** work only via DIN and with *Send Realtime Sysex* = ON. The tuner state (on/off) is derived from the push data.
