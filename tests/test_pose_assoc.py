from __future__ import annotations

from runners.pose_assoc import associate_pose_tracks


def test_associate_pose_tracks_inherits_track_id():
    persons = [
        {
            "class": "person",
            "bbox": [0, 0, 100, 100],
            "track_id": 99,
            "first_seen": 12.5,
        }
    ]
    poses = [{"bbox": [10, 10, 60, 60], "confidence": 0.5}]
    updated = associate_pose_tracks(persons, poses)
    assert updated[0]["track_id"] == 99
    assert updated[0]["first_seen"] == 12.5


def test_associate_pose_tracks_handles_missing_persons():
    updated = associate_pose_tracks([], [{"bbox": [0, 0, 5, 5]}])
    assert updated[0].get("track_id") is None
