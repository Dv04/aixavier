from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from common.event_bus import Event, FileEventBus

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("tracker")


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
    source = Path("artifacts/detections/events.log")
    sink = FileEventBus(Path("artifacts/tracker"))
    for event in stream_events(source):
        e_type = event.get("type")
        payload = event.copy()
        payload.setdefault("track_id", payload.get("track_id", hash(str(payload)) % 1000))
        LOGGER.debug("Forwarding %s", e_type)
        sink.publish(Event(type=e_type, payload=payload))


if __name__ == "__main__":
    main()
