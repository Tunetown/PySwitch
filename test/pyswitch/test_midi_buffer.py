import random
import unittest

from lib.pyswitch.midi.buffer_raw import MIDIBuffer, sysex


class MockMIDIIn:
    """Simuliert einen MIDI-Input mit readinto(buf)-Schnittstelle (wie von
    MIDIBuffer tatsächlich aufgerufen)."""

    def __init__(self, initial_data=b""):
        self._queue = bytearray(initial_data)

    def feed(self, data):
        """Weitere Bytes anhängen, als kämen sie neu über die Leitung."""
        self._queue.extend(data)

    def readinto(self, buf):
        if not self._queue:
            return 0
        n = min(len(buf), len(self._queue))
        buf[0:n] = self._queue[0:n]
        del self._queue[0:n]
        return n


class MockMIDIInNoneOnEmpty(MockMIDIIn):
    """Variante, die bei leerer Queue None statt 0 liefert - manche
    Geräte-APIs tun das. Der Code fängt das über `or 0` ab."""

    def readinto(self, buf):
        if not self._queue:
            return None
        return super().readinto(buf)


class MockMIDIOut:
    """Zeichnet alles auf, was geschrieben wird."""

    def __init__(self):
        self.messages = []

    def write(self, data, length):
        self.messages.append(bytes(data[:length]))


def make_buffer(data=b"", chunk_size=50, midi_in_cls=MockMIDIIn):
    midi_in = midi_in_cls(data)
    midi_out = MockMIDIOut()
    buf = MIDIBuffer(midi_in, midi_out, receive_chunk_size=chunk_size)
    return buf, midi_in, midi_out


def drain(buf, max_msgs=1000):
    """Ruft receive() auf, bis nichts mehr kommt (max_msgs als Notbremse)."""
    out = []
    for _ in range(max_msgs):
        msg = buf.receive()
        if msg is None:
            break
        out.append(bytes(msg))
    return out


#####################################################################################################
#####################################################################################################

class TestSend(unittest.TestCase):

    def test_send_writes_bytes_and_returns_true(self):
        buf, _, midi_out = make_buffer()
        ok = buf.send((0xB0, 22, 1))
        self.assertTrue(ok)
        self.assertEqual(midi_out.messages, [bytes([0xB0, 22, 1])])

    def test_send_accepts_list(self):
        buf, _, midi_out = make_buffer()
        buf.send([0x90, 60, 127])
        self.assertEqual(midi_out.messages, [bytes([0x90, 60, 127])])

    def test_send_accepts_bytes(self):
        buf, _, midi_out = make_buffer()
        buf.send(bytes([0xC0, 5]))
        self.assertEqual(midi_out.messages, [bytes([0xC0, 5])])

    def test_send_none_returns_false_and_writes_nothing(self):
        buf, _, midi_out = make_buffer()
        self.assertFalse(buf.send(None))
        self.assertEqual(midi_out.messages, [])

    def test_send_empty_message_returns_false_and_writes_nothing(self):
        buf, _, midi_out = make_buffer()
        self.assertFalse(buf.send([]))
        self.assertFalse(buf.send(()))
        self.assertFalse(buf.send(b""))
        self.assertEqual(midi_out.messages, [])

    def test_send_length_matches_message(self):
        buf, _, midi_out = make_buffer()
        buf.send(sysex([0x7D], [1, 2, 3, 4, 5]))
        self.assertEqual(midi_out.messages[0], bytes([0xf0, 0x7d, 1, 2, 3, 4, 5, 0xf7]))


#####################################################################################################
#####################################################################################################


class TestReceiveSysEx(unittest.TestCase):

    def test_simple_sysex(self):
        data = sysex([0x7D], [1, 2, 3])
        buf, _, _ = make_buffer(bytes(data))
        msg = buf.receive()
        self.assertEqual(msg, bytes(data))

    def test_empty_sysex_f0_f7(self):
        buf, _, _ = make_buffer(bytes([0xF0, 0xF7]))
        msg = buf.receive()
        self.assertEqual(msg, bytes([0xF0, 0xF7]))

    def test_long_sysex(self):
        payload = list(range(0, 100, 3))  # lauter Werte < 0x80
        data = sysex([0x00, 0x20, 0x29], payload)
        buf, _, _ = make_buffer(bytes(data))
        msg = buf.receive()
        self.assertEqual(msg, bytes(data))

    def test_two_sysex_messages_back_to_back(self):
        data1 = sysex([0x7D], [1, 2])
        data2 = sysex([0x7D], [3, 4, 5])
        buf, _, _ = make_buffer(bytes(data1) + bytes(data2))
        self.assertEqual(buf.receive(), bytes(data1))
        self.assertEqual(buf.receive(), bytes(data2))
        self.assertIsNone(buf.receive())

    def test_sysex_followed_by_normal_message_is_unaffected_by_bug(self):
        data = bytes(sysex([0x7D], [1, 2])) + bytes([0x90, 0x40, 0x7F])
        buf, _, _ = make_buffer(data)
        self.assertEqual(buf.receive(), bytes(sysex([0x7D], [1, 2])))
        self.assertEqual(buf.receive(), bytes([0x90, 0x40, 0x7F]))
        self.assertIsNone(buf.receive())

    def test_realtime_byte_embedded_in_sysex_is_silently_dropped(self):
        # Laut MIDI-Spezifikation dürfen Realtime-Bytes (z.B. 0xF8 Clock)
        # jederzeit in einen SysEx-Strom eingestreut werden und sollten von
        # einem vollständig spec-konformen Parser separat behandelt werden.
        # Dieser einfache Parser tut das nicht - er verwirft sie stillschweigend
        # und die SysEx-Nachricht läuft unbeeinflusst weiter. Das ist keine
        # Beschädigung, aber eine bewusste Vereinfachung - hier dokumentiert.
        data = bytes([0xF0, 0x7D, 1, 0xF8, 2, 0xF8, 3, 0xF7])
        buf, _, _ = make_buffer(data)
        msg = buf.receive()
        self.assertEqual(msg, bytes([0xF0, 0x7D, 1, 2, 3, 0xF7]))

    def test_sysex_without_terminator_never_completes(self):
        buf, midi_in, _ = make_buffer(bytes([0xF0, 0x7D, 1, 2, 3]))
        self.assertIsNone(buf.receive())
        # Auch nach mehrfachem Pollen ohne neue Daten bleibt es None, es
        # gibt keinen Crash und keinen Datenverlust - die Teilnachricht
        # bleibt im internen State erhalten.
        self.assertIsNone(buf.receive())
        # Kommt der Terminator später nach, wird die Nachricht komplett:
        midi_in.feed([4, 0xF7])
        msg = buf.receive()
        self.assertEqual(msg, bytes([0xF0, 0x7D, 1, 2, 3, 4, 0xF7]))


#####################################################################################################
#####################################################################################################


class TestReceiveMessageTypes(unittest.TestCase):

    def _assert_single_message_parses_to(self, raw_bytes, expected):
        buf, _, _ = make_buffer(bytes(raw_bytes))
        msg = buf.receive()
        self.assertEqual(msg, bytes(expected))

    def test_note_on(self):
        self._assert_single_message_parses_to([0x91, 60, 100], [0x91, 60, 100])

    def test_note_off(self):
        self._assert_single_message_parses_to([0x82, 60, 0], [0x82, 60, 0])

    def test_poly_pressure(self):
        self._assert_single_message_parses_to([0xA3, 60, 50], [0xA3, 60, 50])

    def test_control_change(self):
        self._assert_single_message_parses_to([0xB0, 7, 100], [0xB0, 7, 100])

    def test_program_change(self):
        self._assert_single_message_parses_to([0xC5, 12], [0xC5, 12])

    def test_channel_pressure(self):
        self._assert_single_message_parses_to([0xD2, 90], [0xD2, 90])

    def test_pitch_bend(self):
        self._assert_single_message_parses_to([0xE0, 0x00, 0x40], [0xE0, 0x00, 0x40])

    def test_mtc_quarter_frame(self):
        self._assert_single_message_parses_to([0xF1, 0x03, 0x44], [0xF1, 0x03, 0x44])

    def test_song_position_pointer(self):
        self._assert_single_message_parses_to([0xF2, 0x10, 0x20], [0xF2, 0x10, 0x20])

    def test_song_select(self):
        self._assert_single_message_parses_to([0xF3, 5], [0xF3, 5])

    def test_tune_request(self):
        self._assert_single_message_parses_to([0xF6], [0xF6])

    def test_timing_clock(self):
        self._assert_single_message_parses_to([0xF8], [0xF8])

    def test_start(self):
        self._assert_single_message_parses_to([0xFA], [0xFA])

    def test_continue(self):
        self._assert_single_message_parses_to([0xFB], [0xFB])

    def test_stop(self):
        self._assert_single_message_parses_to([0xFC], [0xFC])

    def test_active_sensing(self):
        self._assert_single_message_parses_to([0xFE], [0xFE])

    def test_system_reset(self):
        self._assert_single_message_parses_to([0xFF], [0xFF])

    def test_undefined_system_common_bytes_are_treated_as_1_byte_messages(self):
        # 0xF4/0xF5 sind laut Spezifikation "undefined". Der Code faengt sie
        # ueber den generischen "byte & 0x80"-Zweig als 1-Byte-Nachricht ab.
        self._assert_single_message_parses_to([0xF4], [0xF4])
        self._assert_single_message_parses_to([0xF5], [0xF5])

    def test_orphaned_eox_without_preceding_sysex(self):
        # Ein 0xF7 ausserhalb eines SysEx wird ueber den generischen Zweig
        # ebenfalls als eigenstaendige 1-Byte-Nachricht behandelt.
        self._assert_single_message_parses_to([0xF7], [0xF7])

    def test_all_16_channels_are_recognised_for_note_on(self):
        for channel in range(16):
            status = 0x90 | channel
            with self.subTest(channel=channel):
                self._assert_single_message_parses_to(
                    [status, 64, 100], [status, 64, 100]
                )

    def test_multiple_messages(self):
        buf, midiIn, _ = make_buffer(bytes([
            3, 4, 
            177, 23, 44, 
            6, 
            0xe7, 22, 33, 
            8, 
            0xf0, 0, 20, 30, 4, 5, 0xf7, 
            0xf8, 
            6, 
            0xf6,
            0,
            0xf0
        ]))
        self.assertEqual(buf.receive(), bytes([177, 23, 44]))
        self.assertEqual(buf.receive(), bytes([0xe7, 22, 33]))
        self.assertEqual(buf.receive(), bytes([0xf0, 0, 20, 30, 4, 5, 0xf7]))
        self.assertEqual(buf.receive(), bytes([0xf8]))
        self.assertEqual(buf.receive(), bytes([0xf6]))
        self.assertIsNone(buf.receive())

        midiIn.feed(bytes([2, 3, 4, 0xf7, 192, 3, 192, 4, 0, 0, 0xf8, 0xf8, 0xf8, 0xf8, 176, 0, 1, 8, 8]))
        self.assertEqual(buf.receive(), bytes([0xf0, 2, 3, 4, 0xf7]))
        self.assertEqual(buf.receive(), bytes([192, 3]))
        self.assertEqual(buf.receive(), bytes([192, 4]))
        self.assertEqual(buf.receive(), bytes([0xf8]))
        self.assertEqual(buf.receive(), bytes([0xf8]))
        self.assertEqual(buf.receive(), bytes([0xf8]))
        self.assertEqual(buf.receive(), bytes([0xf8]))
        self.assertEqual(buf.receive(), bytes([176, 0, 1]))
        self.assertIsNone(buf.receive())


class TestReceiveRobustness(unittest.TestCase):

    def test_stray_data_bytes_with_no_preceding_status_are_ignored(self):
        stream = bytes([0x10, 0x20, 0x30, 0x40])  # alles reine Datenbytes
        buf, _, _ = make_buffer(stream)
        self.assertIsNone(buf.receive())

    def test_garbage_before_a_valid_message_is_skipped(self):
        stream = bytes([0x05, 0x77, 0x12,
                         0xB0, 10, 20])  
        buf, _, _ = make_buffer(stream)
        msg = buf.receive()
        self.assertEqual(msg, bytes([0xB0, 10, 20]))

    def test_interrupting_status_byte_is_dropped_not_used_to_restart(self):
        # Kommt waehrend einer Fixed-length-Nachricht ein NEUES Statusbyte
        # (z.B. weil ein Kabel/Geraet mittendrin eine andere Nachricht
        # reinschiebt), wird dieses Byte einfach verworfen - es startet
        # KEINE neue Nachricht und resettet auch nicht die alte. Das
        # entspricht nicht dem "Running Status reset"-Verhalten aus der
        # MIDI-Spezifikation, ist hier aber dokumentiertes Ist-Verhalten.
        stream = bytes([0xB0, 10,          # CC, erst 1 Datenbyte
                         0xC3,             # unterbrechendes PC-Statusbyte -> verworfen
                         20])              # 2. "Datenbyte" der CC
        buf, _, _ = make_buffer(stream)
        msg = buf.receive()
        # PC-Statusbyte (0xC3) taucht nirgends auf - es wurde verworfen,
        # nicht als neue Nachricht gestartet:
        self.assertEqual(msg, bytes([0xB0, 10, 20]))

    def test_no_running_status_support(self):
        # Dieser Parser unterstuetzt keinen "Running Status" (bei dem
        # aufeinanderfolgende Nachrichten desselben Typs das Statusbyte
        # weglassen duerfen). Reine Datenbytes ohne neues Statusbyte nach
        # einer abgeschlossenen Nachricht werden ignoriert statt als
        # Fortsetzung interpretiert.
        stream = bytes([0xB0, 10, 20, 11, 22])  # CC komplett 
        buf, _, _ = make_buffer(stream)
        msg = buf.receive()
        self.assertEqual(msg, bytes([0xB0, 10, 20]))
        self.assertIsNone(buf.receive())

    def test_incomplete_message_at_end_of_stream_does_not_crash(self):
        stream = bytes([0x90, 0x40])  
        buf, _, _ = make_buffer(stream)
        self.assertIsNone(buf.receive())
        self.assertIsNone(buf.receive()) 

    def test_fuzzing_random_bytes_never_raises(self):
        rnd = random.Random(1234) 
        stream = bytes(rnd.randrange(0, 256) for _ in range(2000))
        buf, _, _ = make_buffer(stream, chunk_size=16)
        try:
            for _ in range(3000):
                if buf.receive() is None:
                    break
        except Exception as exc:  # pragma: no cover - shall never happen
            self.fail(f"receive() throwed an exception: {exc!r}")

    def test_readinto_returning_none_instead_of_zero_is_handled(self):
        buf, _, _ = make_buffer(bytes([0xF8]), midi_in_cls=MockMIDIInNoneOnEmpty)
        self.assertEqual(buf.receive(), bytes([0xF8]))
        self.assertIsNone(buf.receive())


#####################################################################################################
#####################################################################################################


class TestReceiveChunking(unittest.TestCase):

    def test_sysex_split_across_many_small_reads(self):
        data = sysex([0x00, 0x20, 0x29], list(range(20)))
        buf, midi_in, _ = make_buffer(bytes(data), chunk_size=3)

        msg = None
        for _ in range(50):  
            msg = buf.receive()
            if msg is not None:
                break
        self.assertEqual(msg, bytes(data))

    def test_message_arriving_in_separate_feed_calls(self):
        buf, midi_in, _ = make_buffer(b"", chunk_size=50)
        self.assertIsNone(buf.receive())

        midi_in.feed([0xF0, 0x7D])
        self.assertIsNone(buf.receive())

        midi_in.feed([1, 2, 3])
        self.assertIsNone(buf.receive())

        midi_in.feed([0xF7])
        msg = buf.receive()
        self.assertEqual(msg, bytes([0xF0, 0x7D, 1, 2, 3, 0xF7]))

    def test_receive_chunk_size_of_one_byte(self):
        data = sysex([0x7D], [1, 2, 3])
        buf, _, _ = make_buffer(bytes(data), chunk_size=1)
        msg = None
        for _ in range(50):
            msg = buf.receive()
            if msg is not None:
                break
        self.assertEqual(msg, bytes(data))


#####################################################################################################
#####################################################################################################


class TestReceiveNoData(unittest.TestCase):

    def test_empty_stream_returns_none(self):
        buf, _, _ = make_buffer(b"")
        self.assertIsNone(buf.receive())

    def test_repeated_polling_on_empty_stream_is_stable(self):
        buf, _, _ = make_buffer(b"")
        for _ in range(10):
            self.assertIsNone(buf.receive())

    def test_data_arriving_later_is_picked_up(self):
        buf, midi_in, _ = make_buffer(b"")
        for _ in range(5):
            self.assertIsNone(buf.receive())

        midi_in.feed([0xF1, 0x03, 0x00])
        msg = buf.receive()
        self.assertEqual(msg, bytes([0xF1, 0x03, 0x00]))


#####################################################################################################
#####################################################################################################


class TestSysexHelper(unittest.TestCase):

    def test_single_byte_manufacturer_id(self):
        msg = sysex([0x41], [1, 2, 3])
        self.assertEqual(msg, bytearray([0xF0, 0x41, 1, 2, 3, 0xF7]))

    def test_three_byte_extended_manufacturer_id(self):
        msg = sysex([0x00, 0x20, 0x29], [10, 20])
        self.assertEqual(msg, bytearray([0xF0, 0x00, 0x20, 0x29, 10, 20, 0xF7]))

    def test_empty_data(self):
        msg = sysex([0x7D], [])
        self.assertEqual(msg, bytearray([0xF0, 0x7D, 0xF7]))

    def test_starts_and_ends_with_sysex_markers(self):
        msg = sysex([0x7D], [1, 2, 3])
        self.assertEqual(msg[0], 0xF0)
        self.assertEqual(msg[-1], 0xF7)
