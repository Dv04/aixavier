"""
Rendering helpers for pose detections (skeleton, bbox, HUD overlays).
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

import cv2
import numpy as np

# Edges for COCO-17 style skeletons.
COCO_EDGES: List[Tuple[int, int]] = [
    (5, 7),
    (7, 9),
    (6, 8),
    (8, 10),
    (5, 6),
    (5, 11),
    (6, 12),
    (11, 12),
    (11, 13),
    (13, 15),
    (12, 14),
    (14, 16),
    (0, 5),
    (0, 6),
]


def draw_pose(
    image: np.ndarray,
    keypoints: np.ndarray,
    bbox: Sequence[float] | None = None,
    threshold: float = 0.25,
) -> np.ndarray:
    """Draws joints, skeleton edges, and (optionally) bounding box."""
    overlay = image
    h, w = overlay.shape[:2]
    kpts = np.asarray(keypoints, dtype=np.float32)
    if kpts.ndim != 2 or kpts.shape[1] < 3:
        return overlay
    for x, y, conf in kpts:
        if conf < threshold:
            continue
        if 0 <= x < w and 0 <= y < h:
            cv2.circle(overlay, (int(x), int(y)), 3, (0, 255, 0), -1, lineType=cv2.LINE_AA)
    for u, v in COCO_EDGES:
        if u >= len(kpts) or v >= len(kpts):
            continue
        x1, y1, c1 = kpts[u]
        x2, y2, c2 = kpts[v]
        if c1 < threshold or c2 < threshold:
            continue
        if not (0 <= x1 < w and 0 <= y1 < h and 0 <= x2 < w and 0 <= y2 < h):
            continue
        cv2.line(
            overlay,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 200, 255),
            2,
            lineType=cv2.LINE_AA,
        )
    if bbox is not None and len(bbox) == 4:
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 100, 0), 2, lineType=cv2.LINE_AA)
    return overlay


def draw_hud(image: np.ndarray, lines: Iterable[str], origin: Tuple[int, int] = (10, 20)) -> np.ndarray:
    """Writes multi-line heads-up display text."""
    x, y = origin
    for line in lines:
        cv2.putText(
            image,
            line,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            lineType=cv2.LINE_AA,
        )
        y += 22
    return image

