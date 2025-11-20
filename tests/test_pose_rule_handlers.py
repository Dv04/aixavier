from __future__ import annotations

from src.rules.engine import RuleEngine, RuleConfig, UseCase


def _uc(slug: str) -> UseCase:
    return UseCase(metadata={"id": slug}, rules=[])


def test_pose_collapse_rule_triggers():
    engine = RuleEngine(configs_dir=__import__("pathlib").Path("configs/usecases"))
    event = {
        "type": "pose.collapse",
        "score": 0.8,
        "camera_id": "CAM01",
        "track_id": 1,
        "speed_kmph": 6,
        "a_mag": -2.0,
        "prone_height_px": 150,
    }
    rule = RuleConfig(type="pose_collapse", params={"min_score": 0.6, "min_speed_kmph": 5, "max_prone_height_px": 220, "min_abs_accel": 1.5})
    res = engine._handle_pose_collapse(event, rule.params, _uc("passenger_falling_from_door"))
    assert res is not None


def test_pose_gesture_rule_triggers():
    engine = RuleEngine(configs_dir=__import__("pathlib").Path("configs/usecases"))
    event = {"type": "pose.gesture", "label": "halt", "score": 0.9, "camera_id": "CAM01", "track_id": 7}
    rule = RuleConfig(type="pose_gesture", params={"gestures": ["halt"], "confidence_min": 0.6})
    res = engine._handle_pose_gesture(event, rule.params, _uc("hand_gesture_signal_identification"))
    assert res is not None


def test_pose_phone_rule_gated_by_speed():
    engine = RuleEngine(configs_dir=__import__("pathlib").Path("configs/usecases"))
    event = {"type": "pose.phone_usage", "score": 0.7, "camera_id": "CAM01", "track_id": 3, "speed_kmph": 0, "dwell_frames": 2}
    rule = RuleConfig(type="pose_phone_usage", params={"min_score": 0.6, "min_speed_kmph": 1, "min_dwell_frames": 3})
    res = engine._handle_pose_phone_usage(event, rule.params, _uc("mobile_phone_usage_detection"))
    assert res is None
    event["speed_kmph"] = 5
    event["dwell_frames"] = 4
    res = engine._handle_pose_phone_usage(event, rule.params, _uc("mobile_phone_usage_detection"))
    assert res is not None
