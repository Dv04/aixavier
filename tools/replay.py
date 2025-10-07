#!/usr/bin/env python3
"""Replay recorded events for diagnostics."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from common.event_bus import Event, FileEventBus


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", default="artifacts/recordings", nargs="?")
    parser.add_argument("--speed", type=float, default=1.0)
    args = parser.parse_args()

    source = Path(args.source)
    bus = FileEventBus(Path("artifacts/replay"))
    files = sorted(source.glob("*.json"))
    for path in files:
        event = json.loads(path.read_text(encoding="utf-8"))
        bus.publish(Event(type=event.get("type", "unknown"), payload=event))
        time.sleep(1.0 / args.speed)


if __name__ == "__main__":
    main()
