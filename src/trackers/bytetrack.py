from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


def _iou(box_a: Sequence[float], box_b: Sequence[float]) -> float:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    inter_w = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    inter_h = max(0.0, min(ay2, by2) - max(ay1, by1))
    inter = inter_w * inter_h
    if inter <= 0:
        return 0.0
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    return inter / (area_a + area_b - inter + 1e-6)


@dataclass
class TrackState:
    track_id: int
    bbox: List[float]
    score: float
    age: int = 0
    hits: int = 1
    active: bool = True


class ByteTrack:
    """Minimal ByteTrack-style tracker (greedy IoU matching with high/low thresholds)."""

    def __init__(
        self,
        high_thresh: float = 0.6,
        low_thresh: float = 0.1,
        match_iou: float = 0.3,
        max_age: int = 30,
    ) -> None:
        self.high_thresh = high_thresh
        self.low_thresh = low_thresh
        self.match_iou = match_iou
        self.max_age = max_age
        self._tracks: Dict[int, TrackState] = {}
        self._next_id = 1

    def _spawn_track(self, det: Dict[str, object]) -> TrackState:
        tid = self._next_id
        self._next_id += 1
        track = TrackState(track_id=tid, bbox=list(det["bbox"]), score=float(det.get("confidence", 0.0)))
        self._tracks[tid] = track
        det["track_id"] = tid
        det["first_seen"] = det.get("timestamp")
        return track

    def _match(self, tracks: Iterable[TrackState], detections: List[Dict[str, object]]) -> None:
        unmatched_tracks: Dict[int, TrackState] = {t.track_id: t for t in tracks}
        for det in detections:
            best_iou, best_id = 0.0, None
            for tid, state in list(unmatched_tracks.items()):
                iou = _iou(state.bbox, det["bbox"])
                if iou > best_iou:
                    best_iou = iou
                    best_id = tid
            if best_iou >= self.match_iou and best_id is not None:
                state = self._tracks[best_id]
                state.bbox = list(det["bbox"])
                state.score = float(det.get("confidence", state.score))
                state.age = 0
                state.hits += 1
                det["track_id"] = best_id
                unmatched_tracks.pop(best_id, None)
            else:
                det["track_id"] = None

    def update(self, detections: List[Dict[str, object]]) -> List[Dict[str, object]]:
        # Age tracks and drop stale ones
        for tid in list(self._tracks):
            state = self._tracks[tid]
            state.age += 1
            if state.age > self.max_age:
                del self._tracks[tid]

        high_conf = [det for det in detections if float(det.get("confidence", 0.0)) >= self.high_thresh]
        low_conf = [
            det
            for det in detections
            if self.low_thresh <= float(det.get("confidence", 0.0)) < self.high_thresh
        ]

        self._match(self._tracks.values(), high_conf)

        # Spawn tracks for unmatched high-confidence detections
        for det in high_conf:
            if not det.get("track_id"):
                self._spawn_track(det)

        # Try to salvage low-confidence detections (keeps tracks alive)
        self._match(
            (state for state in self._tracks.values() if state.track_id not in [det.get("track_id") for det in high_conf]),
            low_conf,
        )

        for det in low_conf:
            if not det.get("track_id"):
                continue
            state = self._tracks[det["track_id"]]
            state.bbox = list(det["bbox"])
            state.score = float(det.get("confidence", state.score))
            state.age = 0

        # Assign IDs back into detections if not already filled
        for det in detections:
            if det.get("track_id"):
                continue
            det["track_id"] = None
        return detections

    def get_active_tracks(self) -> List[Dict[str, object]]:
        return [
            {
                "track_id": state.track_id,
                "bbox": state.bbox,
                "confidence": state.score,
                "age": state.age,
                "hits": state.hits,
            }
            for state in self._tracks.values()
        ]


class SimpleTracker:
    """Kept for backwards compatibility / low-resource deployments."""

    def __init__(self, max_age: int = 30, iou_thresh: float = 0.3) -> None:
        self.max_age = max_age
        self.iou_thresh = iou_thresh
        self._tracks: Dict[int, TrackState] = {}
        self._next_id = 1

    def update(self, detections: List[Dict[str, object]]) -> List[Dict[str, object]]:
        for tid in list(self._tracks):
            self._tracks[tid].age += 1
            if self._tracks[tid].age > self.max_age:
                del self._tracks[tid]

        for det in detections:
            if det.get("track_id"):
                tid = int(det["track_id"])
                self._tracks[tid] = TrackState(track_id=tid, bbox=list(det["bbox"]), score=float(det.get("confidence", 0.0)))

        for det in detections:
            if det.get("track_id"):
                continue
            best_iou, best_id = 0.0, None
            for tid, state in self._tracks.items():
                iou = _iou(state.bbox, det["bbox"])
                if iou > best_iou:
                    best_iou = iou
                    best_id = tid
            if best_iou >= self.iou_thresh and best_id is not None:
                state = self._tracks[best_id]
                state.bbox = list(det["bbox"])
                state.score = float(det.get("confidence", state.score))
                state.age = 0
                det["track_id"] = best_id
            else:
                tid = self._next_id
                self._next_id += 1
                self._tracks[tid] = TrackState(track_id=tid, bbox=list(det["bbox"]), score=float(det.get("confidence", 0.0)))
                det["track_id"] = tid
        return detections

    def get_active_tracks(self) -> List[Dict[str, object]]:
        return [
            {
                "track_id": state.track_id,
                "bbox": state.bbox,
                "confidence": state.score,
                "age": state.age,
                "hits": state.hits,
            }
            for state in self._tracks.values()
        ]


__all__ = ["ByteTrack", "SimpleTracker", "TrackState"]
