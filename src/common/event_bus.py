from __future__ import annotations

import json
import queue
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Union

from .config import ensure_dir


@dataclass
class Event:
    type: str
    payload: Dict[str, Any]


class FileEventBus:
    """Minimal local event bus backed by newline-delimited JSON.

    Not for production but keeps services loosely coupled in demo profile.
    """

    def __init__(
        self,
        path: Union[Path, str],
        filename: str = "events.log",
        *,
        write_last: bool = True,
    ) -> None:
        directory = ensure_dir(Path(path))
        self.path = directory.joinpath(filename)
        self.last_event_path = directory.joinpath("last.json") if write_last else None
        self._lock = threading.Lock()
        self._queue: "queue.Queue[Event]" = queue.Queue()

    def publish(self, event: Event) -> None:
        self._queue.put(event)
        with self._lock:
            record = {"type": event.type, **event.payload}
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")
            if self.last_event_path is not None:
                with self.last_event_path.open("w", encoding="utf-8") as fh:
                    json.dump(record, fh, indent=2)

    def consume(self) -> Iterator[Event]:
        while True:
            event = self._queue.get()
            yield event


__all__ = ["Event", "FileEventBus"]
