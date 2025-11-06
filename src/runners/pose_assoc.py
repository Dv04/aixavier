from __future__ import annotations

from typing import Iterable, List, Sequence


def _bbox_iou(a: Sequence[float], b: Sequence[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_w = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    inter_h = max(0.0, min(ay2, by2) - max(ay1, by1))
    inter = inter_w * inter_h
    if inter <= 0:
        return 0.0
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    return inter / (area_a + area_b - inter + 1e-6)


def associate_pose_tracks(
    persons: Iterable[dict],
    poses: List[dict],
    min_iou: float = 0.1,
) -> List[dict]:
    person_list = list(persons)
    if not person_list:
        return poses
    for pose in poses:
        best_iou, best_person = 0.0, None
        for person in person_list:
            bbox = person.get("bbox")
            if not bbox or not pose.get("bbox"):
                continue
            score = _bbox_iou(bbox, pose["bbox"])
            if score > best_iou:
                best_iou = score
                best_person = person
        if best_person and best_iou >= min_iou:
            pose["track_id"] = best_person.get("track_id")
            if best_person.get("first_seen") is not None:
                pose["first_seen"] = best_person["first_seen"]
    return poses


__all__ = ["associate_pose_tracks"]
