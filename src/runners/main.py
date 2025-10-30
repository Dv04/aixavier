from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, Iterable, List

import cv2
import yaml

from trackers import SimpleTracker

from common.event_bus import Event, FileEventBus
from .detectors import BaseDetector, build_detector

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("detector-runner")

CACHE_DIR = Path("artifacts/detections/cache")
TRACKERS: Dict[str, SimpleTracker] = {}
POSE_TRACKERS: Dict[str, SimpleTracker] = {}


def stream_frames(path: Path) -> Iterable[Dict[str, object]]:
    offset = 0
    while True:
        if not path.exists():
            time.sleep(1)
            continue
        with path.open("r", encoding="utf-8") as fh:
            fh.seek(offset)
            for line in fh:
                offset = fh.tell()
                if not line.strip():
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    LOGGER.warning("Skipping malformed frame entry: %s", line)
        time.sleep(0.1)


def load_config() -> Dict[str, object]:
    cfg_path = os.environ.get("DETECTOR_CONFIG")
    if not cfg_path:
        raise RuntimeError("DETECTOR_CONFIG environment variable is required.")
    path = Path(cfg_path)
    if not path.exists():
        raise FileNotFoundError(f"Detector config {path} not found")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def build_event_payload(detector: BaseDetector, frame: Dict[str, object], detection: Dict[str, object], idx: int) -> Dict[str, object]:
    camera_id = frame.get("camera_id", "CAM01")
    timestamp = frame.get("timestamp", time.time())
    frame_index = frame.get("frame_index", idx)
    payload = {
        "camera_id": camera_id,
        "timestamp": timestamp,
        "frame_index": frame_index,
    }
    payload.update(detection)
    payload.setdefault("first_seen", detection.get("first_seen", timestamp))
    track_id = payload.get("track_id")
    if track_id is None:
        bbox = detection.get("bbox")
        bbox_key = tuple(bbox) if isinstance(bbox, (list, tuple)) else bbox
        payload["track_id"] = hash((camera_id, frame_index, bbox_key)) % 10_000
    else:
        payload["track_id"] = int(track_id)
    return payload


def update_object_cache(camera_id: str, timestamp: float, detections: List[Dict[str, object]]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{camera_id}.json"
    temp = path.with_suffix(".tmp")
    payload = {
        "timestamp": timestamp,
        "detections": detections,
    }
    try:
        temp.write_text(json.dumps(payload), encoding="utf-8")
        temp.replace(path)
    except OSError as exc:  # pragma: no cover - filesystem edge
        LOGGER.warning("Failed to update object cache for %s: %s", camera_id, exc)


def load_object_cache(camera_id: str) -> List[Dict[str, object]]:
    path = CACHE_DIR / f"{camera_id}.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("detections", [])
    except (OSError, json.JSONDecodeError):  # pragma: no cover - corrupted cache
        return []


def assign_pose_ids(camera_id: str, detections: List[Dict[str, object]]) -> List[Dict[str, object]]:
    persons = [det for det in load_object_cache(camera_id) if (det.get("class") or "").lower() == "person"]
    if not persons:
        return detections

    def iou(a: List[float], b: List[float]) -> float:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        inter_w = max(0.0, min(ax2, bx2) - max(ax1, bx1))
        inter_h = max(0.0, min(ay2, by2) - max(ay1, by1))
        inter = inter_w * inter_h
        if inter <= 0:
            return 0.0
        area_a = max(0.0, (ax2 - ax1)) * max(0.0, (ay2 - ay1))
        area_b = max(0.0, (bx2 - bx1)) * max(0.0, (by2 - by1))
        return inter / (area_a + area_b - inter + 1e-6)

    for pose in detections:
        best_iou, best_track = 0.0, None
        for person in persons:
            person_bbox = person.get("bbox")
            if not person_bbox:
                continue
            score = iou(person_bbox, pose.get("bbox", person_bbox))
            if score > best_iou:
                best_iou = score
                best_track = person.get("track_id")
                if person.get("first_seen") is not None:
                    pose["first_seen"] = person.get("first_seen")
        if best_track is not None and best_iou >= 0.1:
            pose["track_id"] = best_track
    return detections


def run() -> None:
    config = load_config()
    detector = build_detector(config)

    publish_path = config.get("publish_path", "artifacts/detections/events.log")
    publish_dir = Path(publish_path)
    bus = FileEventBus(publish_dir.parent, filename=publish_dir.name)
    log_path = Path("artifacts/ingest/frames.log")
    interval = int(config.get("interval", 1))
    frame_skip = 0

    LOGGER.info("Starting detector %s; publishing to %s", detector.__class__.__name__, publish_path)

    for frame in stream_frames(log_path):
        frame_skip = (frame_skip + 1) % interval
        if frame_skip:
            continue
        frame_path = frame.get("path")
        if not frame_path or not Path(frame_path).exists():
            LOGGER.warning("Frame path %s missing; skipping frame.", frame_path)
            continue
        image = cv2.imread(str(frame_path))
        if image is None:
            LOGGER.warning("Failed to read frame %s; skipping.", frame_path)
            continue
        timestamp = float(frame.get("timestamp", time.time()))
        camera_id = frame.get("camera_id", "CAM01")
        detections = list(detector.detect(image))
        for det in detections:
            det.setdefault("first_seen", timestamp)
            det.setdefault("timestamp", timestamp)

        if detector.event_type == "object":
            tracker = TRACKERS.setdefault(camera_id, SimpleTracker())
            detections = tracker.update(detections)
            update_object_cache(camera_id, timestamp, detections)
        elif detector.event_type == "pose":
            detections = assign_pose_ids(camera_id, detections)
            tracker = POSE_TRACKERS.setdefault(camera_id, SimpleTracker())
            detections = tracker.update(detections)

        for idx, detection in enumerate(detections):
            payload = build_event_payload(detector, frame, detection, idx)
            bus.publish(Event(type=detector.event_type, payload=payload))


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        LOGGER.info("Detector interrupted; shutting down.")


if __name__ == "__main__":
    main()
