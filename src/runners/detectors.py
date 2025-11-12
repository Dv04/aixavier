from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import cv2
import numpy as np

from .postprocess import (
    normalise_object_output,
    normalise_pose_output,
    nms,
    xywh_to_xyxy,
)

LOGGER = logging.getLogger(__name__)

_ORT = None  # lazy-loaded onnxruntime module


def _sync_session_dims(session: Any, input_w: int, input_h: int) -> Tuple[int, int]:
    """Derive spatial dimensions from ONNX model if available."""
    if session is None:
        return input_w, input_h
    try:
        shape = session.get_inputs()[0].shape
    except (IndexError, AttributeError):
        return input_w, input_h
    if not shape or len(shape) < 4:
        return input_w, input_h
    _, _, h_dim, w_dim = shape[:4]

    def _coerce(value: Any, fallback: int) -> int:
        if isinstance(value, (int, float)) and value > 0:
            return int(value)
        return fallback

    inferred_h = _coerce(h_dim, input_h)
    inferred_w = _coerce(w_dim, input_w)
    return inferred_w, inferred_h


def letterbox(
    image: np.ndarray, new_shape: Tuple[int, int]
) -> Tuple[np.ndarray, float, Tuple[int, int]]:
    """Resize image with unchanged aspect ratio using padding (YOLO-style)."""
    height, width = image.shape[:2]
    new_w, new_h = new_shape
    scale = min(new_w / width, new_h / height)
    resized = cv2.resize(
        image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_LINEAR
    )
    top = int((new_h - resized.shape[0]) / 2)
    left = int((new_w - resized.shape[1]) / 2)
    canvas = np.full((new_h, new_w, 3), 114, dtype=np.uint8)
    canvas[top : top + resized.shape[0], left : left + resized.shape[1]] = resized
    return canvas, scale, (left, top)


def load_onnx_session(model_path: Path) -> Optional[Any]:
    global _ORT
    if _ORT is None:
        try:  # pragma: no cover - optional dependency
            import onnxruntime as ort_mod
        except Exception:
            ort_mod = None
        _ORT = ort_mod

    if _ORT is None:
        LOGGER.warning(
            "onnxruntime not available; falling back to heuristic detections."
        )
        return None
    if not model_path.exists():
        LOGGER.warning(
            "ONNX model %s not found; falling back to heuristic detections.", model_path
        )
        return None
    providers = (
        ["CUDAExecutionProvider", "CPUExecutionProvider"]
        if "CUDAExecutionProvider" in _ORT.get_available_providers()
        else ["CPUExecutionProvider"]
    )
    try:
        return _ORT.InferenceSession(str(model_path), providers=providers)
    except Exception as exc:  # pragma: no cover - runtime specific
        LOGGER.error(
            "Failed to load ONNX model %s (%s); falling back to heuristic detections.",
            model_path,
            exc,
        )
        return None


@dataclass
class Detection:
    bbox: Tuple[float, float, float, float]
    score: float
    class_id: int
    class_name: str


@dataclass
class PoseDetection:
    bbox: Tuple[float, float, float, float]
    score: float
    keypoints: List[Tuple[float, float, float]]  # (x, y, confidence)


class BaseDetector:
    event_type: str = "object"

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def detect(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        raise NotImplementedError


class ObjectDetector(BaseDetector):
    event_type = "object"

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.input_w = int(config.get("input", {}).get("width", 640))
        self.input_h = int(config.get("input", {}).get("height", 640))
        self.conf_thres = float(config.get("confidence_threshold", 0.25))
        self.iou_thres = float(config.get("nms_iou_threshold", 0.5))
        self.max_det = int(config.get("max_detections", 300))
        self.classes = config.get("classes") or []
        onnx_path = config.get("onnx_path")
        self.session = load_onnx_session(Path(onnx_path)) if onnx_path else None
        if self.session:
            self.input_name = self.session.get_inputs()[0].name
        else:
            self.input_name = "images"
        self.input_w, self.input_h = _sync_session_dims(
            self.session, self.input_w, self.input_h
        )
        self.frame_shape: Optional[Tuple[int, int]] = None
        LOGGER.info("Object detector ready; ONNX=%s", bool(self.session))

    def detect(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        self.frame_shape = image.shape[:2]
        if self.session:
            return self._detect_onnx(image)
        return self._detect_heuristic(image)

    def _detect_onnx(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        img, scale, pad = letterbox(image, (self.input_w, self.input_h))
        blob = img.transpose(2, 0, 1).astype(np.float32) / 255.0
        blob = np.expand_dims(blob, 0)
        outputs = self.session.run(None, {self.input_name: blob})[0]
        outputs = normalise_object_output(outputs)
        boxes = outputs[:, :4]
        scores = outputs[:, 4:]
        conf = np.max(scores, axis=1)
        class_ids = np.argmax(scores, axis=1)
        mask = conf >= self.conf_thres
        boxes, conf, class_ids = boxes[mask], conf[mask], class_ids[mask]
        if boxes.size == 0:
            return []
        boxes = xywh_to_xyxy(boxes)
        # Undo letterbox
        boxes -= np.array([pad[0], pad[1], pad[0], pad[1]])
        boxes /= scale
        keep = nms(boxes, conf, self.iou_thres)
        if self.max_det and len(keep) > self.max_det:
            ranked = sorted(keep, key=lambda idx: conf[idx], reverse=True)[
                : self.max_det
            ]
            keep = ranked
        detections: List[Dict[str, Any]] = []
        for idx in keep:
            x1, y1, x2, y2 = boxes[idx]
            class_id = int(class_ids[idx])
            class_name = (
                self.classes[class_id]
                if class_id < len(self.classes)
                else str(class_id)
            )
            detections.append(
                {
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "confidence": float(conf[idx]),
                    "class_id": class_id,
                    "class": class_name,
                }
            )
        return detections

    def _detect_heuristic(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        h, w = image.shape[:2]
        size = min(h, w) * 0.4
        x1 = (w - size) / 2
        y1 = (h - size) / 2
        x2 = x1 + size
        y2 = y1 + size
        class_name = self.classes[0] if self.classes else "object"
        LOGGER.debug("Using heuristic bounding box for %s", class_name)
        return [
            {
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                "confidence": 0.5,
                "class_id": 0,
                "class": class_name,
            }
        ]


class PoseDetector(BaseDetector):
    event_type = "pose"

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.input_w = int(config.get("input", {}).get("width", 640))
        self.input_h = int(config.get("input", {}).get("height", 640))
        self.conf_thres = float(config.get("confidence_threshold", 0.25))
        self.iou_thres = float(config.get("nms_iou_threshold", 0.6))
        self.max_det = int(config.get("max_detections", 200))
        onnx_path = config.get("onnx_path")
        self.session = load_onnx_session(Path(onnx_path)) if onnx_path else None
        if self.session:
            self.input_name = self.session.get_inputs()[0].name
        else:
            self.input_name = "images"
        self.input_w, self.input_h = _sync_session_dims(
            self.session, self.input_w, self.input_h
        )
        LOGGER.info("Pose detector ready; ONNX=%s", bool(self.session))

    def detect(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        if self.session:
            return self._detect_onnx(image)
        return self._detect_heuristic(image)

    def _decode_simcc(
        self, simcc_x: Any, simcc_y: Any
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if np is None:
            raise RuntimeError("numpy is required for pose detection")
        simcc_x = np.asarray(simcc_x)
        simcc_y = np.asarray(simcc_y)

        def _prepare(arr: np.ndarray) -> np.ndarray:
            if arr.ndim == 2:
                arr = arr[None, ...]
            if arr.ndim != 3:
                raise RuntimeError(f"Unexpected SimCC tensor shape: {arr.shape}")
            return arr

        simcc_x = _prepare(simcc_x)
        simcc_y = _prepare(simcc_y)
        if simcc_x.shape[:2] != simcc_y.shape[:2]:
            raise RuntimeError(
                f"SimCC heads mismatch: {simcc_x.shape} vs {simcc_y.shape}"
            )

        x_idx = np.argmax(simcc_x, axis=-1)
        y_idx = np.argmax(simcc_y, axis=-1)
        x_conf = np.take_along_axis(simcc_x, x_idx[..., None], axis=-1).squeeze(-1)
        y_conf = np.take_along_axis(simcc_y, y_idx[..., None], axis=-1).squeeze(-1)
        width_bins = max(simcc_x.shape[-1] - 1, 1)
        height_bins = max(simcc_y.shape[-1] - 1, 1)
        x_coord = (x_idx / width_bins) * self.input_w
        y_coord = (y_idx / height_bins) * self.input_h
        kp_scores = np.sqrt(np.clip(x_conf * y_conf, 0.0, 1.0))
        boxes = np.stack(
            (
                x_coord.min(axis=1),
                y_coord.min(axis=1),
                x_coord.max(axis=1),
                y_coord.max(axis=1),
            ),
            axis=1,
        )
        pose_scores = kp_scores.mean(axis=1)
        keypoints = np.stack((x_coord, y_coord, kp_scores), axis=-1)
        return boxes, pose_scores, keypoints

    def _detect_onnx(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        img, scale, pad = letterbox(image, (self.input_w, self.input_h))
        blob = img.transpose(2, 0, 1).astype(np.float32) / 255.0
        blob = np.expand_dims(blob, 0)
        outputs = self.session.run(None, {self.input_name: blob})
        if isinstance(outputs, (list, tuple)) and len(outputs) == 2:
            boxes, scores, keypoints = self._decode_simcc(outputs[0], outputs[1])
            boxes_are_xywh = False
        else:
            tensor = outputs[0] if isinstance(outputs, (list, tuple)) else outputs
            tensor = normalise_pose_output(tensor)
            boxes = tensor[:, :4]
            scores = tensor[:, 4]
            keypoints = tensor[:, 5:]
            num_points = keypoints.shape[1] // 3
            keypoints = keypoints.reshape(keypoints.shape[0], num_points, 3)
            boxes_are_xywh = True
        mask = scores >= self.conf_thres
        boxes, scores, keypoints = boxes[mask], scores[mask], keypoints[mask]
        if boxes.size == 0:
            return []
        if keypoints.ndim == 3 and keypoints.shape[2] == 3:
            pass
        else:
            num_points = keypoints.shape[1] // 3
            keypoints = keypoints.reshape(keypoints.shape[0], num_points, 3)
        if boxes_are_xywh:
            boxes = xywh_to_xyxy(boxes)
        boxes -= np.array([pad[0], pad[1], pad[0], pad[1]])
        boxes /= scale
        keypoints[:, :, 0] -= pad[0]
        keypoints[:, :, 1] -= pad[1]
        keypoints[:, :, :2] /= scale
        keep = nms(boxes, scores, self.iou_thres)
        if self.max_det and len(keep) > self.max_det:
            keep = sorted(keep, key=lambda idx: scores[idx], reverse=True)[
                : self.max_det
            ]
        results: List[Dict[str, Any]] = []
        for idx in keep:
            pts = keypoints[idx]
            kpt_list = [(float(x), float(y), float(c)) for x, y, c in pts]
            x1, y1, x2, y2 = boxes[idx]
            results.append(
                {
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "confidence": float(scores[idx]),
                    "keypoints": kpt_list,
                }
            )
        return results

    def _detect_heuristic(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        h, w = image.shape[:2]
        torso_len = h * 0.25
        center_x = w / 2
        center_y = h / 2
        keypoints = [
            (center_x, center_y - torso_len, 0.8),  # head
            (center_x, center_y - torso_len / 2, 0.9),  # neck
            (center_x, center_y, 0.95),  # spine
            (center_x, center_y + torso_len / 2, 0.9),  # pelvis
        ]
        # Fill to 17 keypoints as expected by YOLOv8 pose models
        while len(keypoints) < 17:
            angle = (len(keypoints) - 4) * (math.pi / 6)
            radius = torso_len / 1.5
            keypoints.append(
                (
                    center_x + radius * math.cos(angle),
                    center_y + radius * math.sin(angle),
                    0.6,
                )
            )
        bbox = [
            float(center_x - torso_len / 1.2),
            float(center_y - torso_len * 1.2),
            float(center_x + torso_len / 1.2),
            float(center_y + torso_len * 1.2),
        ]
        return [
            {
                "bbox": bbox,
                "confidence": 0.6,
                "keypoints": keypoints,
            }
        ]


class SimulatedDetector(BaseDetector):
    """Fallback detector used for face/action until dedicated pipelines land."""

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.event_type = config.get("event_type", "object")
        self.interval = int(config.get("interval", 30))
        self._counter = 0

    def detect(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        self._counter += 1
        if self._counter % self.interval != 0:
            return []
        h, w = image.shape[:2]
        return [
            {
                "bbox": [w * 0.25, h * 0.25, w * 0.75, h * 0.75],
                "confidence": 0.4,
                "class_id": 0,
                "class": self.config.get("simulation_class", "event"),
            }
        ]


# --- Face Detection & Recognition Stubs ---
class FaceDetector(BaseDetector):
    event_type = "face"

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.input_w = int(config.get("input", {}).get("width", 640))
        self.input_h = int(config.get("input", {}).get("height", 640))
        self.conf_thres = float(config.get("confidence_threshold", 0.5))
        onnx_path = config.get("onnx_path")
        self.session = load_onnx_session(Path(onnx_path)) if onnx_path else None
        self.input_name = (
            self.session.get_inputs()[0].name if self.session else "images"
        )
        self.input_w, self.input_h = _sync_session_dims(
            self.session, self.input_w, self.input_h
        )
        LOGGER.info("Face detector ready; ONNX=%s", bool(self.session))

    def detect(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        if self.session:
            # TODO: Implement ONNX inference for face detection
            return []
        # Simulate output for now
        h, w = image.shape[:2]
        return [
            {
                "bbox": [w * 0.3, h * 0.3, w * 0.7, h * 0.7],
                "confidence": 0.6,
                "class_id": 0,
                "class": "face",
            }
        ]


class FaceRecognitionDetector(BaseDetector):
    event_type = "face_recognition"

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.input_w = int(config.get("input", {}).get("width", 112))
        self.input_h = int(config.get("input", {}).get("height", 112))
        self.conf_thres = float(config.get("confidence_threshold", 0.5))
        onnx_path = config.get("onnx_path")
        self.session = load_onnx_session(Path(onnx_path)) if onnx_path else None
        self.input_name = (
            self.session.get_inputs()[0].name if self.session else "images"
        )
        self.input_w, self.input_h = _sync_session_dims(
            self.session, self.input_w, self.input_h
        )
        LOGGER.info("Face recognition detector ready; ONNX=%s", bool(self.session))

    def detect(self, image: np.ndarray) -> Iterable[Dict[str, Any]]:
        if self.session:
            # TODO: Implement ONNX inference for face recognition
            return []
        # Simulate output for now
        h, w = image.shape[:2]
        return [
            {
                "bbox": [w * 0.3, h * 0.3, w * 0.7, h * 0.7],
                "confidence": 0.7,
                "embedding": [0.0] * 512,
                "class_id": 0,
                "class": "face_recognition",
            }
        ]


def build_detector(config: Dict[str, Any]) -> BaseDetector:
    task = (config.get("task") or "").lower()
    if task in {"object", "object_detection", "detection"}:
        return ObjectDetector(config)
    if task in {"pose", "pose_detection"}:
        return PoseDetector(config)
    if task in {"face", "face_detection"}:
        return FaceDetector(config)
    if task in {"face_recognition", "frs"}:
        return FaceRecognitionDetector(config)
    return SimulatedDetector(config)


__all__ = [
    "BaseDetector",
    "ObjectDetector",
    "PoseDetector",
    "SimulatedDetector",
    "FaceDetector",
    "FaceRecognitionDetector",
    "build_detector",
]
