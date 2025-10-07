from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from common.event_bus import Event


@dataclass
class RuleConfig:
    type: str
    params: Dict[str, float | int | str | List[str] | Dict[str, str]] = field(default_factory=dict)


@dataclass
class UseCase:
    metadata: Dict[str, str]
    rules: List[RuleConfig]


class RuleEngine:
    """Evaluates configured rules on detection events."""

    def __init__(self, configs_dir: Path):
        self.usecases = self._load_usecases(configs_dir)
        self.state: Dict[str, Dict[str, float]] = {}

    def _load_usecases(self, path: Path) -> Dict[str, UseCase]:
        mapping: Dict[str, UseCase] = {}
        for file in path.glob("*.yaml"):
            data = yaml.safe_load(file.read_text(encoding="utf-8"))
            metadata = data.get("metadata", {"id": file.stem})
            rules = [RuleConfig(type=rule.pop("type"), params=rule) for rule in data.get("rules", [])]
            mapping[metadata["id"]] = UseCase(metadata=metadata, rules=rules)
        return mapping

    def evaluate(self, event: Dict[str, any]) -> List[Event]:
        """Evaluate event against all rules and return triggered events."""
        triggered: List[Event] = []
        for usecase in self.usecases.values():
            for rule in usecase.rules:
                handler = getattr(self, f"_handle_{rule.type}", None)
                if handler is None:
                    continue
                result = handler(event, rule.params, usecase)
                if result:
                    triggered.append(result)
        return triggered

    # --- Rule handlers ---
    def _handle_line_crossing(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "track":
            return None
        if event.get("class") not in params.get("classes", []):
            return None
        if event.get("line_id") != params.get("line_id"):
            return None
        return Event(
            type=usecase.metadata["id"],
            payload={
                "confidence": event.get("confidence", 0.0),
                "track_id": event.get("track_id"),
                "camera_id": event.get("camera_id"),
                "attributes": {"direction": event.get("direction")},
            },
        )

    def _handle_static_object_dwell(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "object" or event.get("class") not in params.get("classes", []):
            return None
        key = f"{event.get('camera_id')}::{event.get('track_id')}"
        now = event.get("timestamp", time.time())
        dwell_seconds = params.get("dwell_seconds", 30)
        if "first_seen" in event:
            first_seen = float(event["first_seen"])
            self.state.setdefault("dwell", {})[key] = first_seen
        else:
            first_seen = self.state.setdefault("dwell", {}).setdefault(key, now)
        if now - first_seen >= dwell_seconds:
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "track_id": event.get("track_id"),
                    "dwell_seconds": now - first_seen,
                    "confidence": event.get("confidence", 0.0),
                },
            )
        return None

    def _handle_action_score(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "action":
            return None
        label = params.get("label")
        threshold = float(params.get("threshold", 0.5))
        score = event.get("scores", {}).get(label, 0.0)
        if score >= threshold:
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "track_id": event.get("track_id"),
                    "action": label,
                    "score": score,
                },
            )
        return None

    def _handle_pose_velocity_drop(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "pose":
            return None
        velocity = event.get("velocity_drop", 0.0)
        threshold = float(params.get("min_drop", 1.5))
        if velocity >= threshold:
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "track_id": event.get("track_id"),
                    "velocity_drop": velocity,
                },
            )
        return None

    def _handle_prone_dwell(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "pose":
            return None
        height = event.get("height_px", math.inf)
        max_height = params.get("max_height_px", 200)
        dwell = event.get("dwell_seconds", 0)
        if height <= max_height and dwell >= params.get("min_duration_seconds", 4):
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "track_id": event.get("track_id"),
                    "dwell_seconds": dwell,
                },
            )
        return None

    def _handle_frs_match(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "frs":
            return None
        score = event.get("score", 0.0)
        threshold = float(params.get("threshold", 0.47))
        if score >= threshold:
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "identity": event.get("identity"),
                    "score": score,
                },
            )
        return None

    def _handle_blur_detect(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "tamper":
            return None
        variance = event.get("variance", 0.0)
        threshold = float(params.get("variance_threshold", 100))
        if variance <= threshold:
            return Event(
                type=usecase.metadata["id"],
                payload={"variance": variance, "camera_id": event.get("camera_id")},
            )
        return None


__all__ = ["RuleEngine"]
