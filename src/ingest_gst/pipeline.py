from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2
import numpy as np

from common.config import ensure_dir


@dataclass
class Frame:
    index: int
    timestamp: float
    path: Path


def synthetic_frames(output_dir: Path, fps: int = 25) -> Iterator[Frame]:
    """Generate alternating color frames for demo mode."""
    ensure_dir(output_dir)
    frame_idx = 0
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    base = np.zeros((1080, 1920, 3), dtype=np.uint8)
    while True:
        frame = base.copy()
        color = colors[frame_idx % len(colors)]
        cv2.rectangle(frame, (200, 200), (1720, 880), color, thickness=-1)
        cv2.putText(
            frame,
            f"Frame {frame_idx}",
            (220, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            (255, 255, 255),
            4,
        )
        ts = time.time()
        path = output_dir / f"frame_{frame_idx:06d}.jpg"
        cv2.imwrite(str(path), frame)
        yield Frame(index=frame_idx, timestamp=ts, path=path)
        frame_idx += 1
        time.sleep(1.0 / fps)


def capture_rtsp(rtsp_url: str, output_dir: Path, fps_limit: int = 25) -> Iterator[Frame]:
    """Capture frames from RTSP using OpenCV."""
    ensure_dir(output_dir)
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open stream {rtsp_url}")
    frame_idx = 0
    last_ts = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(1)
            continue
        ts = time.time()
        if fps_limit:
            dt = ts - last_ts
            sleep_for = max(0, (1.0 / fps_limit) - dt)
            if sleep_for > 0:
                time.sleep(sleep_for)
        path = output_dir / f"frame_{frame_idx:06d}.jpg"
        cv2.imwrite(str(path), frame)
        yield Frame(index=frame_idx, timestamp=ts, path=path)
        frame_idx += 1
        last_ts = ts


def capture_webcam(device_index: int, output_dir: Path, fps_limit: int = 25) -> Iterator[Frame]:
    """Capture frames from a local webcam using OpenCV."""
    ensure_dir(output_dir)
    cap = cv2.VideoCapture(device_index)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open webcam index {device_index}")
    frame_idx = 0
    last_ts = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.5)
            continue
        ts = time.time()
        if fps_limit:
            dt = ts - last_ts
            sleep_for = max(0, (1.0 / fps_limit) - dt)
            if sleep_for > 0:
                time.sleep(sleep_for)
        path = output_dir / f"frame_{frame_idx:06d}.jpg"
        cv2.imwrite(str(path), frame)
        yield Frame(index=frame_idx, timestamp=ts, path=path)
        frame_idx += 1
        last_ts = ts
