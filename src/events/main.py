from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from common.event_bus import Event, FileEventBus

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("events")


def stream_events(path: Path):
    offset = 0
    while True:
        if not path.exists():
            time.sleep(1)
            continue
        with path.open("r", encoding="utf-8") as fh:
            fh.seek(offset)
            for line in fh:
                offset = fh.tell()
                if not line.strip():
                    continue
                yield json.loads(line)
        time.sleep(0.2)


def main() -> None:
    source = Path("artifacts/events/events.log")
    sink = FileEventBus(Path("artifacts/normalized"))
    for event in stream_events(source):
        normalized = Event(
            type=event.get("type", "unknown"),
            payload={
                "camera_id": event.get("camera_id"),
                "ts": event.get("timestamp", time.time()),
                "attributes": event,
            },
        )
        LOGGER.info("Normalized event %s", normalized.type)
        sink.publish(normalized)


if __name__ == "__main__":
    main()
