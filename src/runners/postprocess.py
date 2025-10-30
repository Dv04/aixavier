from __future__ import annotations

import os
from typing import List, Sequence

if os.environ.get("AIXAVIER_DISABLE_NUMPY") == "1":  # test fallback path
    np = None
else:  # pragma: no cover - actual runtime path
    try:
        import numpy as np
    except Exception:  # pragma: no cover - runtime without numpy
        np = None


class SimpleArray:
    def __init__(self, data: Sequence[Sequence[float]]) -> None:
        self.data = data
        self.shape = self._compute_shape(data)
        self.ndim = len(self.shape)

    @staticmethod
    def _compute_shape(data: Sequence) -> tuple:
        shape = []
        ref = data
        while isinstance(ref, (list, tuple)):
            shape.append(len(ref))
            if len(ref) == 0:
                break
            ref = ref[0]
        return tuple(shape)

    def __getitem__(self, item):  # pragma: no cover - debugging helper
        result = self.data[item]
        return SimpleArray(result) if isinstance(result, (list, tuple)) else result


def _transpose_021(data: Sequence[Sequence[Sequence[float]]]) -> List[List[List[float]]]:
    dim0 = len(data)
    dim1 = len(data[0]) if dim0 else 0
    dim2 = len(data[0][0]) if dim1 else 0
    result: List[List[List[float]]] = []
    for i in range(dim0):
        anchors: List[List[float]] = []
        for k in range(dim2):
            row = [data[i][j][k] for j in range(dim1)]
            anchors.append(row)
        result.append(anchors)
    return result


def xywh_to_xyxy(box: "np.ndarray") -> "np.ndarray":  # type: ignore[valid-type]
    if np is None:
        raise RuntimeError("numpy is required for detector execution")
    x, y, w, h = box.T
    return np.stack((x - w / 2, y - h / 2, x + w / 2, y + h / 2), axis=1)


def nms(boxes: "np.ndarray", scores: "np.ndarray", iou_thres: float) -> List[int]:  # type: ignore[valid-type]
    if np is None:
        raise RuntimeError("numpy is required for detector execution")
    if boxes.size == 0:
        return []
    x1, y1, x2, y2 = boxes.T
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    keep: List[int] = []
    while order.size > 0:
        i = order[0]
        keep.append(int(i))
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)
        inds = np.where(ovr <= iou_thres)[0]
        order = order[inds + 1]
    return keep


def normalise_object_output(out):
    if np is not None:
        arr = np.asarray(out)
        if arr.ndim == 3:
            if arr.shape[1] < arr.shape[2]:
                arr = np.transpose(arr, (0, 2, 1))
            arr = arr[0]
        elif arr.ndim != 2:
            raise RuntimeError(f"Unexpected detector output shape: {arr.shape}")
        if arr.shape[1] < 6:
            raise RuntimeError(f"Detector output has insufficient features: {arr.shape}")
        return arr

    data = out
    if isinstance(data, SimpleArray):
        arr = data
    else:
        arr = SimpleArray(data)
    if arr.ndim == 3:
        nested = arr.data
        if arr.shape[1] < arr.shape[2]:
            nested = _transpose_021(nested)
        nested = nested[0]
        arr = SimpleArray(nested)
    elif arr.ndim != 2:
        raise RuntimeError(f"Unexpected detector output structure: {arr.shape}")
    if arr.shape[1] < 6:
        raise RuntimeError(f"Detector output has insufficient features: {arr.shape}")
    return arr


def normalise_pose_output(out):
    if np is not None:
        arr = np.asarray(out)
        if arr.ndim == 3:
            if arr.shape[1] < arr.shape[2]:
                arr = np.transpose(arr, (0, 2, 1))
            arr = arr[0]
        elif arr.ndim != 2:
            raise RuntimeError(f"Unexpected pose output shape: {arr.shape}")
        if arr.shape[1] < 6:
            raise RuntimeError(f"Pose output has insufficient features: {arr.shape}")
        return arr

    data = out
    if isinstance(data, SimpleArray):
        arr = data
    else:
        arr = SimpleArray(data)
    if arr.ndim == 3:
        nested = arr.data
        if arr.shape[1] < arr.shape[2]:
            nested = _transpose_021(nested)
        nested = nested[0]
        arr = SimpleArray(nested)
    elif arr.ndim != 2:
        raise RuntimeError(f"Unexpected pose output structure: {arr.shape}")
    if arr.shape[1] < 6:
        raise RuntimeError(f"Pose output has insufficient features: {arr.shape}")
    return arr


__all__ = [
    "xywh_to_xyxy",
    "nms",
    "normalise_object_output",
    "normalise_pose_output",
]
