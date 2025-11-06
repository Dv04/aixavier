from __future__ import annotations

from src.trackers import ByteTrack, SimpleTracker


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


def test_byte_track_assigns_consistent_ids() -> None:
    tracker = ByteTrack(high_thresh=0.1, low_thresh=0.05, match_iou=0.1, max_age=3)
    dets1 = tracker.update([{"bbox": [0, 0, 100, 100], "confidence": 0.9}])
    tid = dets1[0]["track_id"]
    dets2 = tracker.update([{"bbox": [5, 5, 105, 105], "confidence": 0.85}])
    assert dets2[0]["track_id"] == tid


def test_byte_track_creates_new_ids_for_far_objects() -> None:
    tracker = ByteTrack(high_thresh=0.1, low_thresh=0.05, match_iou=0.2, max_age=3)
    tracker.update([{"bbox": [0, 0, 50, 50], "confidence": 0.9}])
    first_id = tracker.get_active_tracks()[0]["track_id"]
    dets = tracker.update([{"bbox": [200, 200, 250, 250], "confidence": 0.95}])
    assert dets[0]["track_id"] != first_id
