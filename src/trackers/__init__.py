"""Tracking utilities (ByteTrack + manager helpers)."""

from __future__ import annotations

import os
from typing import Dict, List

from .bytetrack import ByteTrack, SimpleTracker, TrackState


class TrackerManager:
    """Manages per-camera trackers (ByteTrack by default)."""

    def __init__(
        self,
        algorithm: str = "bytetrack",
        high_thresh: float = 0.6,
        low_thresh: float = 0.1,
        match_iou: float = 0.3,
        max_age: int = 30,
    ) -> None:
        self.algorithm = algorithm.lower()
        self.trackers: Dict[str, object] = {}
        self.high_thresh = high_thresh
        self.low_thresh = low_thresh
        self.match_iou = match_iou
        self.max_age = max_age
        self._cache: Dict[str, List[Dict[str, object]]] = {}

    def _build_tracker(self) -> object:
        if self.algorithm == "simple":
            return SimpleTracker(max_age=self.max_age, iou_thresh=self.match_iou)
        return ByteTrack(
            high_thresh=self.high_thresh,
            low_thresh=self.low_thresh,
            match_iou=self.match_iou,
            max_age=self.max_age,
        )

    def for_camera(self, camera_id: str) -> object:
        if camera_id not in self.trackers:
            self.trackers[camera_id] = self._build_tracker()
        return self.trackers[camera_id]

    def update(self, camera_id: str, detections: List[Dict[str, object]]) -> List[Dict[str, object]]:
        tracker = self.for_camera(camera_id)
        updated = tracker.update(detections)
        self._cache[camera_id] = updated
        return updated

    def get_tracks(self, camera_id: str) -> List[Dict[str, object]]:
        tracker = self.trackers.get(camera_id)
        if tracker is None:
            return []
        return tracker.get_active_tracks()

    def latest_detections(self, camera_id: str) -> List[Dict[str, object]]:
        return self._cache.get(camera_id, [])


__all__ = ["ByteTrack", "SimpleTracker", "TrackerManager", "TrackState"]
