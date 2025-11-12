"""
Circular video buffer stub for event-driven recording.
"""

from collections import deque
from typing import Any, Deque, Optional


class CircularBuffer:
    def __init__(self, max_frames: int = 300):
        self.max_frames = max_frames
        self.buffer: Deque[Any] = deque(maxlen=max_frames)

    def add_frame(self, frame: Any) -> None:
        self.buffer.append(frame)

    def get_clip(self, pre: int = 30, post: int = 60) -> list[Any]:
        # Return last `pre` frames and next `post` frames (stub: just returns all)
        return list(self.buffer)

    def clear(self) -> None:
        self.buffer.clear()

    def __len__(self) -> int:
        return len(self.buffer)
