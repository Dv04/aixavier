from src.recorder.circular_buffer import CircularBuffer


def test_circular_buffer_add_and_len():
    buf = CircularBuffer(max_frames=5)
    for i in range(10):
        buf.add_frame(f"frame_{i}")
    assert len(buf) == 5
    assert buf.get_clip() == [f"frame_{i}" for i in range(5, 10)]


def test_circular_buffer_clear():
    buf = CircularBuffer(max_frames=3)
    buf.add_frame("a")
    buf.add_frame("b")
    buf.clear()
    assert len(buf) == 0
