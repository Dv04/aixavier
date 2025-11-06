from __future__ import annotations

import json

from src.common.event_bus import Event, FileEventBus


def test_file_event_bus_persists_to_disk(tmp_path):
    bus = FileEventBus(tmp_path, filename="events.log")
    event = Event(type="pose", payload={"camera_id": "CAM01", "value": 1})
    bus.publish(event)
    stored = (tmp_path / "events.log").read_text(encoding="utf-8").strip()
    assert json.loads(stored) == {"type": "pose", "camera_id": "CAM01", "value": 1}


def test_file_event_bus_consume(tmp_path):
    bus = FileEventBus(tmp_path)
    evt = Event(type="object", payload={"camera_id": "CAM01"})
    bus.publish(evt)
    consumer = bus.consume()
    received = next(consumer)
    assert received.type == "object"
    assert received.payload["camera_id"] == "CAM01"
