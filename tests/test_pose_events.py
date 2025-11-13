from __future__ import annotations

import numpy as np

from src.models.phone import PhoneUsage
from src.runners.pose_events import PoseUseCaseMonitor


class _StubCollapse:
    def score(self, _window):
        return 0.9


def _keypoints_with_conf() -> list[list[float]]:
    kps = np.zeros((17, 3), dtype=float)
    kps[:, 2] = 0.9
    return kps.tolist()


def test_pose_monitor_records_collapse_event() -> None:
    monitor = PoseUseCaseMonitor(fps_hint=15.0, collapse_model=_StubCollapse())
    detection = {"track_id": 1, "keypoints": _keypoints_with_conf()}
    monitor.process("CAM01", [detection], fps_hint=15.0)
    assert monitor.event_counts["collapse"] == 1
    assert detection["pose_events"][0]["type"] == "pose.collapse"
    labels = monitor.track_labels()
    assert 1 in labels and labels[1].startswith("COLLAPSE")


def test_pose_monitor_gesture_event() -> None:
    monitor = PoseUseCaseMonitor(fps_hint=15.0)
    kps = np.zeros((17, 3), dtype=float)
    kps[:, 2] = 0.9
    # right wrist higher than shoulder triggers "halt"
    kps[10] = [100, 40, 0.9]
    kps[6] = [100, 120, 0.9]
    detection = {"track_id": 7, "keypoints": kps.tolist()}
    monitor.process("CAM01", [detection], fps_hint=15.0)
    assert monitor.event_counts["gesture"] == 1
    events = detection["pose_events"]
    assert any(evt["type"] == "pose.gesture" for evt in events)


def test_pose_monitor_phone_usage_requires_speed() -> None:
    phone_model = PhoneUsage(hand_to_ear_px=200.0, dwell_s=0.05, fps=15)
    monitor = PoseUseCaseMonitor(fps_hint=15.0, phone_model=phone_model)
    kps = np.zeros((17, 3), dtype=float)
    kps[:, 2] = 0.9
    kps[10] = [10, 10, 0.9]  # right wrist near ear
    kps[4] = [15, 10, 0.9]
    detection = {"track_id": 10, "keypoints": kps.tolist()}
    monitor.update_telemetry({"speed_kmph": 6})
    for _ in range(5):
        monitor.process("CAM01", [detection], fps_hint=15.0)
    assert monitor.event_counts["phone"] == 1
