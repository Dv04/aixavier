from __future__ import annotations

import time
from pathlib import Path

import yaml

from rules.engine import RuleEngine
from common.event_bus import Event


def test_rule_engine_triggers(tmp_path: Path, monkeypatch):
    # Create minimal usecase config
    cfg_dir = tmp_path / "usecases"
    cfg_dir.mkdir()
    cfg_dir.joinpath("camera_tampering.yaml").write_text(
        yaml.dump(
            {
                "metadata": {"id": "camera_tampering"},
                "rules": [
                    {"type": "blur_detect", "variance_threshold": 100},
                ],
            }
        )
    )
    engine = RuleEngine(cfg_dir)
    event = {
        "type": "tamper",
        "camera_id": "CAM01",
        "variance": 50,
    }
    triggered = engine.evaluate(event)
    assert triggered and isinstance(triggered[0], Event)


def test_unattended_baggage(tmp_path: Path):
    cfg_dir = tmp_path / "usecases"
    cfg_dir.mkdir()
    cfg_dir.joinpath("unattended_baggage.yaml").write_text(
        yaml.dump(
            {
                "metadata": {"id": "unattended_baggage"},
                "rules": [
                    {"type": "static_object_dwell", "classes": ["bag"], "dwell_seconds": 1},
                ],
            }
        )
    )
    engine = RuleEngine(cfg_dir)
    now = time.time()
    event = {
        "type": "object",
        "camera_id": "CAM01",
        "track_id": 1,
        "class": "bag",
        "timestamp": now - 2,
        "confidence": 0.9,
    }
    triggered = engine.evaluate(event)
    assert triggered and triggered[0].type == "unattended_baggage"


def test_frs_match(tmp_path: Path):
    cfg_dir = tmp_path / "usecases"
    cfg_dir.mkdir()
    cfg_dir.joinpath("face_recognition.yaml").write_text(
        yaml.dump(
            {
                "metadata": {"id": "face_recognition"},
                "rules": [
                    {"type": "frs_match", "threshold": 0.5},
                ],
            }
        )
    )
    engine = RuleEngine(cfg_dir)
    event = {
        "type": "frs",
        "camera_id": "CAM01",
        "identity": "Test",
        "score": 0.8,
    }
    triggered = engine.evaluate(event)
    assert triggered and triggered[0].payload["score"] == 0.8
