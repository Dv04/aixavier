from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from common.event_bus import Event
from aixavier.core.usecases import UseCaseRegistry, UseCaseDefinition


@dataclass
class RuleConfig:
    type: str
    params: Dict[str, float | int | str | List[str] | Dict[str, str]] = field(default_factory=dict)


@dataclass
class UseCase:
    metadata: Dict[str, str]
    rules: List[RuleConfig]
    definition: Optional[UseCaseDefinition] = None


class RuleEngine:
    """Evaluates configured rules on detection events."""

    def __init__(self, configs_dir: Path, manifest_path: Optional[Path] = None):
        self.configs_dir = Path(configs_dir)
        manifest = manifest_path or Path("assets/usecases/catalog.yaml")
        self.registry = UseCaseRegistry(manifest_path=manifest, configs_dir=self.configs_dir)
        self.usecases = self._load_usecases(self.configs_dir)
        self.state: Dict[str, Dict[str, float]] = {}
        self.last_fire: Dict[str, float] = {}

    def _load_usecases(self, path: Path) -> Dict[str, UseCase]:
        raw_configs: Dict[str, Dict[str, object]] = {}
        for file in path.glob("*.yaml"):
            data = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
            metadata = data.get("metadata", {})
            slug = metadata.get("id", file.stem)
            rules = [RuleConfig(type=rule.pop("type"), params=rule) for rule in data.get("rules", [])]
            raw_configs[slug] = {"metadata": metadata, "rules": rules}

        mapping: Dict[str, UseCase] = {}
        for definition in self.registry.definitions:
            payload = raw_configs.pop(definition.slug, {"metadata": {}, "rules": []})
            metadata = self.registry.enrich_metadata(definition.slug, payload.get("metadata", {}))
            rules = payload.get("rules", [])
            mapping[definition.slug] = UseCase(metadata=metadata, rules=rules, definition=definition)

        for slug, payload in raw_configs.items():
            metadata = self.registry.enrich_metadata(slug, payload.get("metadata", {}))
            mapping[slug] = UseCase(metadata=metadata, rules=payload.get("rules", []), definition=self.registry.get(slug))

        return mapping

    def summary(self) -> Dict[str, Dict[str, object]]:
        report: Dict[str, Dict[str, object]] = {}
        for slug, usecase in self.usecases.items():
            maturity = usecase.metadata.get(
                "maturity",
                usecase.definition.maturity if usecase.definition else "planned",
            )
            report[slug] = {
                "rules": len(usecase.rules),
                "maturity": maturity,
            }
        return report

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
        event_ts = float(event.get("timestamp", time.time()))
        wall_clock = time.time()
        dwell_seconds = float(params.get("dwell_seconds", 30))
        dwell_state = self.state.setdefault("dwell", {})

        if "first_seen" in event:
            dwell_state[key] = float(event["first_seen"])
        elif key not in dwell_state:
            dwell_state[key] = min(event_ts, wall_clock)
        else:
            dwell_state[key] = min(float(dwell_state[key]), event_ts)

        first_seen = float(dwell_state[key])
        elapsed = max(event_ts, wall_clock) - first_seen
        if elapsed >= dwell_seconds:
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "track_id": event.get("track_id"),
                    "dwell_seconds": elapsed,
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

    # --- Pose-derived events (UC8/13/20/22) ---
    def _handle_pose_collapse(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "pose.collapse":
            return None
        score = float(event.get("score", 0.0))
        threshold = float(params.get("min_score", 0.65))
        min_speed = float(params.get("min_speed_kmph", 0.0))
        speed = float(event.get("speed_kmph", 0.0) or 0.0)
        door_open = event.get("door_open")
        # optional additional gates
        a_mag = float(event.get("a_mag", 0.0))
        prone_h = float(event.get("prone_height_px", float("inf")))
        max_prone = float(params.get("max_prone_height_px", 240))
        min_abs_accel = float(params.get("min_abs_accel", 1.2))
        cooldown = float(params.get("cooldown_seconds", 3.0))
        key = f"{usecase.metadata['id']}::{event.get('track_id')}"
        if not self._cooldown_ok(key, cooldown):
            return None
        if speed < min_speed:
            return None
        if params.get("door_required") and door_open is False:
            return None
        if score >= threshold and abs(a_mag) >= min_abs_accel and prone_h <= max_prone:
            self.last_fire[key] = time.time()
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "track_id": event.get("track_id"),
                    "score": score,
                    "speed_kmph": speed,
                    "door_open": door_open,
                    "prone_height_px": prone_h,
                    "a_mag": a_mag,
                },
            )
        return None

    def _handle_pose_gesture(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "pose.gesture":
            return None
        label = event.get("label")
        gestures = params.get("gestures", [])
        min_conf = float(params.get("confidence_min", 0.6))
        cooldown = float(params.get("cooldown_seconds", 2.0))
        key = f"{usecase.metadata['id']}::{event.get('track_id')}::{label}"
        if not self._cooldown_ok(key, cooldown):
            return None
        if label in gestures and float(event.get("score", 0.0)) >= min_conf:
            self.last_fire[key] = time.time()
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "track_id": event.get("track_id"),
                    "label": label,
                    "score": float(event.get("score", 0.0)),
                    "delta_r": event.get("delta_r"),
                    "delta_l": event.get("delta_l"),
                },
            )
        return None

    def _handle_pose_phone_usage(self, event: Dict[str, any], params: Dict[str, any], usecase: UseCase) -> Optional[Event]:
        if event.get("type") != "pose.phone_usage":
            return None
        score = float(event.get("score", 0.0))
        threshold = float(params.get("min_score", 0.6))
        min_speed = float(params.get("min_speed_kmph", 0.0))
        speed = float(event.get("speed_kmph", 0.0) or 0.0)
        min_dwell = int(params.get("min_dwell_frames", 0))
        dwell_frames = int(event.get("dwell_frames", 0))
        cooldown = float(params.get("cooldown_seconds", 5.0))
        key = f"{usecase.metadata['id']}::{event.get('track_id')}"
        if not self._cooldown_ok(key, cooldown):
            return None
        if speed < min_speed:
            return None
        if score >= threshold and dwell_frames >= min_dwell:
            self.last_fire[key] = time.time()
            return Event(
                type=usecase.metadata["id"],
                payload={
                    "camera_id": event.get("camera_id"),
                    "track_id": event.get("track_id"),
                    "score": score,
                    "speed_kmph": speed,
                    "dwell_frames": dwell_frames,
                },
            )
        return None

    # --- helpers ---
    def _cooldown_ok(self, key: str, cooldown_s: float) -> bool:
        last = self.last_fire.get(key, 0.0)
        now = time.time()
        if now - last < cooldown_s:
            return False
        return True

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
