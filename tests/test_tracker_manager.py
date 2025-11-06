from __future__ import annotations

from trackers import TrackerManager


def test_tracker_manager_assigns_ids_with_bytetrack() -> None:
    manager = TrackerManager(
        algorithm="bytetrack",
        high_thresh=0.1,
        low_thresh=0.05,
        match_iou=0.1,
        max_age=5,
    )
    detections = manager.update("CAM_TEST", [{"bbox": [0, 0, 100, 100], "confidence": 0.9}])
    assert detections[0]["track_id"] is not None
    latest = manager.latest_detections("CAM_TEST")
    assert latest and latest[0]["track_id"] == detections[0]["track_id"]


def test_tracker_manager_simple_mode_persists_tracks() -> None:
    manager = TrackerManager(algorithm="simple", match_iou=0.5, max_age=5)
    first = manager.update("CAM_SIMPLE", [{"bbox": [0, 0, 50, 50], "confidence": 0.8}])
    tid = first[0]["track_id"]
    second = manager.update("CAM_SIMPLE", [{"bbox": [5, 5, 55, 55], "confidence": 0.85}])
    assert second[0]["track_id"] == tid
    assert manager.get_tracks("CAM_SIMPLE")[0]["track_id"] == tid
