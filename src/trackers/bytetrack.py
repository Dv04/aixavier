from __future__ import annotations

from typing import Dict, List


class SimpleTracker:
    """Lightweight IoU-based tracker to provide persistent IDs per camera."""

    def __init__(self, max_age: int = 30, iou_thresh: float = 0.3) -> None:
        self.max_age = max_age
        self.iou_thresh = iou_thresh
        self._tracks: Dict[int, Dict[str, object]] = {}
        self._next_id = 1

    @staticmethod
    def _iou(a: List[float], b: List[float]) -> float:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        inter_w = max(0.0, min(ax2, bx2) - max(ax1, bx1))
        inter_h = max(0.0, min(ay2, by2) - max(ay1, by1))
        inter = inter_w * inter_h
        if inter <= 0:
            return 0.0
        area_a = max(0.0, (ax2 - ax1)) * max(0.0, (ay2 - ay1))
        area_b = max(0.0, (bx2 - bx1)) * max(0.0, (by2 - by1))
        denom = area_a + area_b - inter + 1e-6
        return inter / denom

    def _register(self, det: Dict[str, object]) -> int:
        tid = self._next_id
        self._next_id += 1
        self._tracks[tid] = {"bbox": det["bbox"], "age": 0}
        det["track_id"] = tid
        return tid

    def update(self, detections: List[Dict[str, object]]) -> List[Dict[str, object]]:
        # Age all tracks
        for tid in list(self._tracks):
            self._tracks[tid]["age"] = int(self._tracks[tid]["age"]) + 1
            if self._tracks[tid]["age"] > self.max_age:
                del self._tracks[tid]

        # Pre-assigned IDs update directly
        assigned = set()
        for det in detections:
            if det.get("track_id"):
                tid = int(det["track_id"])
                self._tracks[tid] = {"bbox": det["bbox"], "age": 0}
                assigned.add(tid)

        for det in detections:
            if det.get("track_id"):
                continue
            best_iou, best_id = 0.0, None
            for tid, track in self._tracks.items():
                if tid in assigned:
                    continue
                iou = self._iou(track["bbox"], det["bbox"])
                if iou > best_iou:
                    best_iou, best_id = iou, tid
            if best_iou >= self.iou_thresh and best_id is not None:
                det["track_id"] = best_id
                self._tracks[best_id] = {"bbox": det["bbox"], "age": 0}
                assigned.add(best_id)
            else:
                self._register(det)
        return detections


__all__ = ["SimpleTracker"]
