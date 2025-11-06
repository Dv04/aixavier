from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("prometheus_client")

from exporter import main as exporter_main


def test_count_events_returns_pose_counts(tmp_path):
    log = tmp_path / "events.log"
    events = [
        {"type": "pose", "camera_id": "CAM01"},
        {"type": "pose_velocity", "camera_id": "CAM01"},
        {"type": "object", "camera_id": "CAM01"},
    ]
    log.write_text("\n".join(json.dumps(evt) for evt in events), encoding="utf-8")
    result = exporter_main.count_events(log)
    assert result["CAM01"] == 2


def test_count_events_handles_missing_file(tmp_path):
    missing = tmp_path / "missing.log"
    result = exporter_main.count_events(missing)
    assert result == {}
