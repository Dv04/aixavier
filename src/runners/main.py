from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import cv2
import numpy as np
import yaml

from src.trackers import TrackerManager

from src.common.event_bus import Event, FileEventBus
from .detectors import BaseDetector, build_detector
from .pose_assoc import associate_pose_tracks
from .renderer import draw_hud, draw_pose, draw_track_label
from .pose_events import PoseUseCaseMonitor

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("detector-runner")

CACHE_DIR = Path("artifacts/detections/cache")
FRAMES_LOG = Path(os.getenv("INGEST_FRAMES_LOG", "artifacts/ingest/frames.log"))
SHOW_PREVIEW = os.getenv("LIVE_DEMO_SHOW", "").lower() in {"1", "true", "yes"}
RECORD_PATH = os.getenv("LIVE_DEMO_RECORD")
RECORD_FPS = float(os.getenv("LIVE_DEMO_RECORD_FPS", os.getenv("LIVE_DEMO_CAPTURE_FPS", "25")))
PREVIEW_WINDOW = os.getenv("LIVE_DEMO_WINDOW_NAME", "Aixavier Pose Demo")
OBJECT_TRACKERS = TrackerManager(
    algorithm=os.getenv("TRACKER_ALGO", "bytetrack"),
    high_thresh=float(os.getenv("TRACKER_HIGH_THRESH", "0.6")),
    low_thresh=float(os.getenv("TRACKER_LOW_THRESH", "0.1")),
    match_iou=float(os.getenv("TRACKER_MATCH_IOU", "0.3")),
    max_age=int(os.getenv("TRACKER_MAX_AGE", "30")),
)
POSE_TRACKERS = TrackerManager(
    algorithm=os.getenv("POSE_TRACKER_ALGO", "simple"),
    high_thresh=float(os.getenv("POSE_TRACKER_HIGH_THRESH", "0.4")),
    low_thresh=float(os.getenv("POSE_TRACKER_LOW_THRESH", "0.1")),
    match_iou=float(os.getenv("POSE_TRACKER_MATCH_IOU", "0.2")),
    max_age=int(os.getenv("POSE_TRACKER_MAX_AGE", "30")),
)


def stream_frames(path: Path) -> Iterable[Dict[str, object]]:
    offset = 0
    while True:
        if not path.exists():
            time.sleep(1)
            continue
        with path.open("r", encoding="utf-8") as fh:
            fh.seek(offset)
            while True:
                line = fh.readline()
                if not line:
                    break
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
    persons = [
        det
        for det in OBJECT_TRACKERS.latest_detections(camera_id)
        if (det.get("class") or "").lower() == "person"
    ]
    return associate_pose_tracks(persons, detections)


def cleanup_frame(path: str | Path | None, persist: bool) -> None:
    if persist or not path:
        return
    try:
        Path(path).unlink()
    except FileNotFoundError:
        return
    except OSError as exc:
        LOGGER.debug("Failed to delete frame %s: %s", path, exc)


def run() -> None:
    config = load_config()
    detector = build_detector(config)
    pose_monitor: Optional[PoseUseCaseMonitor] = None
    if detector.event_type == "pose":
        fps_hint = float(os.getenv("LIVE_DEMO_CAPTURE_FPS", os.getenv("LIVE_DEMO_RECORD_FPS", "25")))
        pose_monitor = PoseUseCaseMonitor(fps_hint=fps_hint)

    publish_path = config.get("publish_path", "artifacts/detections/events.log")
    publish_dir = Path(publish_path)
    bus = FileEventBus(publish_dir.parent, filename=publish_dir.name)
    log_path = FRAMES_LOG
    interval = int(config.get("interval", 1))
    frame_skip = 0
    render_enabled = SHOW_PREVIEW or bool(RECORD_PATH)
    writer: Optional[cv2.VideoWriter] = None

    LOGGER.info("Starting detector %s; publishing to %s", detector.__class__.__name__, publish_path)

    try:
        for frame in stream_frames(log_path):
            persist_frame = bool(frame.get("persist", True))
            frame_path = frame.get("path")
            if pose_monitor is not None:
                pose_monitor.update_telemetry(frame.get("telemetry"))
            frame_skip = (frame_skip + 1) % interval
            if frame_skip:
                cleanup_frame(frame_path, persist_frame)
                continue
            if not frame_path:
                LOGGER.warning("Frame path missing; skipping frame.")
                continue
            path_obj = Path(frame_path)
            if not path_obj.exists():
                LOGGER.warning("Frame path %s missing; skipping frame.", frame_path)
                cleanup_frame(frame_path, persist_frame)
                continue
            image = cv2.imread(str(path_obj))
            if image is None:
                LOGGER.warning("Failed to read frame %s; skipping.", frame_path)
                cleanup_frame(frame_path, persist_frame)
                continue

            start = time.time()
            timestamp = float(frame.get("timestamp", time.time()))
            camera_id = frame.get("camera_id", "CAM01")
            detections = list(detector.detect(image))
            proc_time = time.time() - start
            fps_est = 1.0 / proc_time if proc_time > 0 else 0.0
            latency_ms = proc_time * 1000.0
            track_labels: Dict[int, str] = {}

            for det in detections:
                det.setdefault("first_seen", timestamp)
                det.setdefault("timestamp", timestamp)
                det.setdefault("latency_ms", latency_ms)
                det.setdefault("detector", detector.config.get("model", detector.__class__.__name__))

            if detector.event_type == "object":
                detections = OBJECT_TRACKERS.update(camera_id, detections)
                update_object_cache(camera_id, timestamp, detections)
            elif detector.event_type == "pose":
                detections = assign_pose_ids(camera_id, detections)
                detections = POSE_TRACKERS.update(camera_id, detections)
                if pose_monitor is not None:
                    pose_monitor.process(camera_id, detections, fps_est or pose_monitor.fps_hint)
                    track_labels = pose_monitor.track_labels()

            vis_frame = None
            if render_enabled:
                vis_frame = image.copy()
                if detector.event_type == "pose":
                    for det in detections:
                        keypoints = det.get("keypoints")
                        if not keypoints:
                            continue
                        vis_frame = draw_pose(
                            vis_frame,
                            np.asarray(keypoints, dtype=np.float32),
                            det.get("bbox"),
                        )
                        if pose_monitor is not None:
                            track_label = track_labels.get(det.get("track_id"))
                            if track_label:
                                vis_frame = draw_track_label(vis_frame, det.get("bbox"), track_label)
                hud_lines = [
                    f"FPS={fps_est:.1f} frame={frame.get('frame_index', '-')}",
                    f"detections={len(detections)} camera={camera_id}",
                ]
                if pose_monitor is not None and detector.event_type == "pose":
                    hud_lines.extend(pose_monitor.hud_lines())
                vis_frame = draw_hud(vis_frame, hud_lines)

            for idx, detection in enumerate(detections):
                payload = build_event_payload(detector, frame, detection, idx)
                payload.setdefault("latency_ms", latency_ms)
                payload.setdefault("detector", detector.config.get("model", detector.__class__.__name__))
                bus.publish(Event(type=detector.event_type, payload=payload))

                # Emit derived pose events (e.g., collapse/gesture/phone) as first-class events
                if detector.event_type == "pose":
                    for evt in detection.get("pose_events", []) or []:
                        derived = {
                            **payload,
                            **evt,
                            "event_parent": "pose",
                        }
                        derived["type"] = evt.get("type", "pose.event")
                        bus.publish(Event(type=derived.pop("type"), payload=derived))

            if SHOW_PREVIEW and vis_frame is not None:
                cv2.imshow(PREVIEW_WINDOW, vis_frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    raise KeyboardInterrupt

            if RECORD_PATH and vis_frame is not None:
                if writer is None:
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                    writer = cv2.VideoWriter(
                        RECORD_PATH,
                        fourcc,
                        RECORD_FPS,
                        (vis_frame.shape[1], vis_frame.shape[0]),
                    )
                    if not writer.isOpened():
                        LOGGER.warning("Failed to open video writer at %s", RECORD_PATH)
                        writer = None
                if writer is not None:
                    writer.write(vis_frame)

            cleanup_frame(frame_path, persist_frame)
    finally:
        if writer is not None:
            writer.release()
        if SHOW_PREVIEW:
            cv2.destroyWindow(PREVIEW_WINDOW)


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        LOGGER.info("Detector interrupted; shutting down.")


if __name__ == "__main__":
    main()
