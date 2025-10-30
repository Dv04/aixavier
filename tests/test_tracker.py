from __future__ import annotations

from trackers import SimpleTracker


def test_simple_tracker_persists_ids() -> None:
    tracker = SimpleTracker(max_age=5, iou_thresh=0.2)
    frame1 = [{"bbox": [0, 0, 100, 100], "confidence": 0.9}]
    tracked1 = tracker.update(frame1)
    tid = tracked1[0]["track_id"]

    frame2 = [{"bbox": [10, 10, 110, 110], "confidence": 0.85}]
    tracked2 = tracker.update(frame2)
    assert tracked2[0]["track_id"] == tid


def test_simple_tracker_spawns_new_ids() -> None:
    tracker = SimpleTracker(max_age=5, iou_thresh=0.5)
    tracker.update([{"bbox": [0, 0, 50, 50], "confidence": 0.8}])
    ids = {det["track_id"] for det in tracker.update([{ "bbox": [100, 100, 150, 150], "confidence": 0.9 }])}
    assert len(ids) == 1
