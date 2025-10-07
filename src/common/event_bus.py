from __future__ import annotations

import json
import queue
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator

from .config import ensure_dir


@dataclass
class Event:
    type: str
    payload: Dict[str, Any]


class FileEventBus:
    """Minimal local event bus backed by newline-delimited JSON.

    Not for production but keeps services loosely coupled in demo profile.
    """

    def __init__(self, path: Path, filename: str = "events.log") -> None:
        directory = ensure_dir(path)
        self.path = directory.joinpath(filename)
        self._lock = threading.Lock()
        self._queue: "queue.Queue[Event]" = queue.Queue()

    def publish(self, event: Event) -> None:
        self._queue.put(event)
        with self._lock:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"type": event.type, **event.payload}) + "\n")

    def consume(self) -> Iterator[Event]:
        while True:
            event = self._queue.get()
            yield event


__all__ = ["Event", "FileEventBus"]
