from __future__ import annotations

import json
import os
import time
from pathlib import Path

from prometheus_client import Counter, Gauge, start_http_server

INGEST_FPS = Gauge("ingest_fps", "Ingest frames per second", ["camera"])
DETECT_LATENCY = Gauge("detect_latency_ms", "Detector latency", ["usecase"])
EVENT_COUNT = Counter("event_count", "Event count", ["type"])
GPU_UTIL = Gauge("gpu_util", "Simulated GPU utilization")
MEM_USED = Gauge("mem_used_bytes", "Simulated memory usage")
DROP_FRAMES = Counter("drop_frames_total", "Dropped frames total")


def count_events(path: Path) -> None:
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines[-20:]:
        event = json.loads(line)
        EVENT_COUNT.labels(type=event.get("type", "unknown")).inc()


def main() -> None:
    port = int(os.getenv("PROMETHEUS_SCRAPE_PORT", "9100"))
    start_http_server(port)
    while True:
        INGEST_FPS.labels(camera="CAM01").set(25)
        DETECT_LATENCY.labels(usecase="trespassing_on_track").set(8.0)
        GPU_UTIL.set(0.42)
        MEM_USED.set(2_147_483_648)
        count_events(Path("artifacts/events/events.log"))
        time.sleep(5)


if __name__ == "__main__":
    main()
