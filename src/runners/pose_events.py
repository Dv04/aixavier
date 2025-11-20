from __future__ import annotations

import os
import time
from collections import deque
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional

import numpy as np
import yaml

from src.models.collapse import CollapseModel
from src.models.gesture import GestureModel
from src.models.phone import PhoneUsage
from src.telemetry.ingest import Telemetry


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        data = {}
    return data


class PoseUseCaseMonitor:
    """Collects pose-driven heuristics and exposes HUD-friendly status."""

    def __init__(
        self,
        fps_hint: float = 15.0,
        collapse_model: Optional[CollapseModel] = None,
        gesture_model: Optional[GestureModel] = None,
        phone_model: Optional[PhoneUsage] = None,
    ) -> None:
        self.fps_hint = max(fps_hint, 1.0)
        self.collapse = collapse_model or CollapseModel(os.getenv("UC8_COLLAPSE_ONNX"))
        self.gesture = gesture_model or GestureModel()
        self.phone = phone_model or PhoneUsage(fps=int(round(self.fps_hint)))
        self.telemetry = Telemetry()
        self.track_state: Dict[int, Dict[str, Any]] = {}
        self.event_counts = {"collapse": 0, "gesture": 0, "phone": 0}
        self._active_labels: Deque[Dict[str, Any]] = deque()
        self._track_banners: Dict[int, Dict[str, Any]] = {}
        self.banner_ttl = float(os.getenv("POSE_EVENT_BANNER_TTL", "3"))

        collapse_cfg = _load_yaml(Path("configs/usecases/medical_emergency_collapse.demo.yaml"))
        gesture_cfg = _load_yaml(Path("configs/usecases/hand_gesture_signal_identification.demo.yaml"))
        phone_cfg = _load_yaml(Path("configs/usecases/mobile_phone_usage_detection.demo.yaml"))

        thresholds = collapse_cfg.get("thresholds", {})
        self.collapse_threshold = float(thresholds.get("collapse_score", 0.65))
        self.prone_window = int(thresholds.get("followup_prone_s", 4))

        self.gesture_thresholds: Dict[str, float] = {
            label: float(score) for label, score in (gesture_cfg.get("labels") or {}).items()
        }
        self.default_gesture_threshold = float(os.getenv("POSE_GESTURE_THRESHOLD", "0.6"))

        phone_thresholds = phone_cfg.get("thresholds", {})
        self.phone_usage_threshold = float(phone_thresholds.get("phone_usage_score", 0.6))
        gate = phone_cfg.get("gate", {})
        self.phone_min_speed = float(gate.get("min_speed_kmph", 0.0))

    def update_telemetry(self, payload: Optional[Dict[str, Any]]) -> None:
        if not payload:
            return
        if "speed_kmph" in payload:
            self.telemetry.set_speed(payload["speed_kmph"])
        if "door_open" in payload:
            self.telemetry.set_door(payload["door_open"])
        if "gps" in payload:
            self.telemetry.set_gps(payload["gps"])

    def process(self, camera_id: str, detections: List[Dict[str, Any]], fps_hint: float | None = None) -> None:
        fps = fps_hint or self.fps_hint
        telemetry = self.telemetry.snapshot()
        for det in detections:
            keypoints = det.get("keypoints")
            track_id = det.get("track_id")
            if keypoints is None or track_id is None:
                continue
            kp_array = np.asarray(keypoints, dtype=np.float32)
            features = self._update_track_state(track_id, kp_array, fps)
            events: List[Dict[str, Any]] = []
            latest = features[-1] if features else {}

            if len(features) >= 1:
                collapse_score = self.collapse.score(features[-15:])
                if collapse_score >= self.collapse_threshold:
                    events.append({
                        "type": "pose.collapse",
                        "score": collapse_score,
                        "speed_kmph": telemetry.get("speed_kmph"),
                        "door_open": telemetry.get("door_open"),
                        "v_mag": latest.get("v_mag"),
                        "a_mag": latest.get("a_mag"),
                        "prone_height_px": latest.get("prone_height_px"),
                    })
                    self._record_event("collapse", f"COLLAPSE {collapse_score:.2f}", track_id)

            label, gesture_score = self.gesture.predict(kp_array)
            min_score = self.gesture_thresholds.get(label, self.default_gesture_threshold)
            if label != "unknown" and gesture_score >= min_score:
                delta_r = float(self._y_delta(kp_array, 10, 6))
                delta_l = float(self._y_delta(kp_array, 9, 5))
                events.append({
                    "type": "pose.gesture",
                    "label": label,
                    "score": gesture_score,
                    "speed_kmph": telemetry.get("speed_kmph"),
                    "delta_r": delta_r,
                    "delta_l": delta_l,
                })
                self._record_event("gesture", label.upper(), track_id)

            phone_score, active = self.phone.score(kp_array)
            if active and phone_score >= self.phone_usage_threshold:
                if self._speed_ok():
                    if not self._phone_already_active(track_id):
                        events.append({
                            "type": "pose.phone_usage",
                            "score": phone_score,
                            "speed_kmph": telemetry.get("speed_kmph"),
                            "dwell_frames": self.phone.last_dwell_frames,
                        })
                        self._record_event("phone", "PHONE-USAGE", track_id)
                    self._set_phone_active(track_id, True)
                else:
                    self._set_phone_active(track_id, False)
            elif active is False:
                self._set_phone_active(track_id, False)

            if events:
                det.setdefault("pose_events", []).extend(events)

    def hud_lines(self) -> List[str]:
        counts = (
            f"Pose events: collapse={self.event_counts['collapse']} "
            f"gesture={self.event_counts['gesture']} phone={self.event_counts['phone']}"
        )
        now = time.time()
        self._active_labels = deque(label for label in self._active_labels if label["expires"] > now)
        banner_lines = [item["label"] for item in self._active_labels]
        return [counts] + banner_lines if banner_lines else [counts]

    def track_labels(self) -> Dict[int, str]:
        now = time.time()
        expired = [track_id for track_id, meta in self._track_banners.items() if meta["expires"] <= now]
        for track_id in expired:
            self._track_banners.pop(track_id, None)
        return {track_id: meta["label"] for track_id, meta in self._track_banners.items()}

    def _speed_ok(self) -> bool:
        snapshot = self.telemetry.snapshot()
        return float(snapshot.get("speed_kmph", 0.0)) >= self.phone_min_speed

    def _update_track_state(self, track_id: int, keypoints: np.ndarray, fps: float) -> List[Dict[str, float]]:
        state = self.track_state.setdefault(track_id, {"history": deque(maxlen=120)})
        midhip = self._midhip(keypoints)
        prev_midhip = state.get("midhip")
        prev_velocity = state.get("velocity", 0.0)
        if prev_midhip is None:
            velocity = 0.0
        else:
            velocity = float(np.linalg.norm(midhip - prev_midhip) * fps)
        accel = velocity - prev_velocity
        prone_height = self._prone_height(keypoints)
        feature = {
            "v_mag": velocity,
            "a_mag": accel,
            "prone_height_px": prone_height,
        }
        history: Deque[Dict[str, float]] = state["history"]
        history.append(feature)
        state["midhip"] = midhip
        state["velocity"] = velocity
        return list(history)

    def _phone_already_active(self, track_id: int) -> bool:
        state = self.track_state.setdefault(track_id, {"history": deque(maxlen=120)})
        return bool(state.get("phone_active"))

    def _set_phone_active(self, track_id: int, active: bool) -> None:
        state = self.track_state.setdefault(track_id, {"history": deque(maxlen=120)})
        state["phone_active"] = active

    @staticmethod
    def _midhip(keypoints: np.ndarray) -> np.ndarray:
        try:
            return (keypoints[11][:2] + keypoints[12][:2]) / 2.0
        except Exception:  # pragma: no cover - fallback to zeros
            return np.zeros(2, dtype=np.float32)

    @staticmethod
    def _prone_height(keypoints: np.ndarray) -> float:
        try:
            head_y = float(keypoints[0][1])
            midhip_y = float(((keypoints[11][1] + keypoints[12][1]) / 2.0))
            return abs(head_y - midhip_y) * 2.0
        except Exception:  # pragma: no cover - fallback height
            return 400.0

    @staticmethod
    def _y_delta(keypoints: np.ndarray, idx_a: int, idx_b: int) -> float:
        try:
            return float(keypoints[idx_a][1] - keypoints[idx_b][1])
        except Exception:  # pragma: no cover
            return 0.0

    def _record_event(self, kind: str, label: str, track_id: Optional[int] = None) -> None:
        self.event_counts[kind] += 1
        self._active_labels.append({"label": label, "expires": time.time() + self.banner_ttl})
        if track_id is not None:
            self._track_banners[track_id] = {"label": label, "expires": time.time() + self.banner_ttl}


__all__ = ["PoseUseCaseMonitor"]
