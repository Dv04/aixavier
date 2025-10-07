from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from common.event_bus import Event, FileEventBus

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("runners")


def stream_frames(path: Path):
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
    frames_log = Path("artifacts/ingest/frames.log")
    bus = FileEventBus(Path("artifacts/detections"))
    bag_first_seen = None
    for frame in stream_frames(frames_log):
        idx = frame.get("frame_index", 0)
        camera_id = frame.get("camera_id", "CAM01")
        timestamp = frame.get("timestamp", time.time())

        # Camera tamper (frame 10)
        if idx % 200 == 10:
            bus.publish(
                Event(
                    type="tamper",
                    payload={
                        "camera_id": camera_id,
                        "variance": 50.0,
                    },
                )
            )

        # Unattended baggage dwell simulation
        if bag_first_seen is None:
            bag_first_seen = timestamp - 60
        bus.publish(
            Event(
                type="object",
                payload={
                    "camera_id": camera_id,
                    "track_id": 101,
                    "class": "bag",
                    "timestamp": timestamp,
                    "first_seen": bag_first_seen,
                    "confidence": 0.9,
                },
            )
        )

        # Violence action event (frame multiple of 120)
        if idx % 120 == 30:
            bus.publish(
                Event(
                    type="action",
                    payload={
                        "camera_id": camera_id,
                        "track_id": 22,
                        "scores": {"violence": 0.8},
                    },
                )
            )

        # Medical collapse (pose)
        if idx % 150 == 40:
            bus.publish(
                Event(
                    type="pose",
                    payload={
                        "camera_id": camera_id,
                        "track_id": 501,
                        "velocity_drop": 2.0,
                        "height_px": 150,
                        "dwell_seconds": 6,
                    },
                )
            )

        # Trespass line crossing
        if idx % 180 == 50:
            bus.publish(
                Event(
                    type="track",
                    payload={
                        "camera_id": camera_id,
                        "track_id": 77,
                        "class": "person",
                        "line_id": "danger_line",
                        "direction": "both",
                        "confidence": 0.85,
                    },
                )
            )

        # FRS match event
        if idx % 210 == 60:
            bus.publish(
                Event(
                    type="embedding",
                    payload={
                        "camera_id": camera_id,
                        "embedding": "{{FRS_WHITELIST_EMBEDDING_01}}",
                    },
                )
            )

        time.sleep(0.05)


if __name__ == "__main__":
    main()
