from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Any, Dict

from src.common.config import load_yaml
from src.common.event_bus import Event, FileEventBus

from .pipeline import capture_rtsp, capture_webcam, synthetic_frames

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("ingest")


def normalize_source(source: str) -> str:
    if source.startswith("webcam://"):
        return source
    if source.startswith("webcam:"):
        return f"webcam://{source.split(':', 1)[1]}"
    return source


def resolve_camera(
    camera_config: Path | None,
    source: str | None,
    *,
    camera_id: str,
    camera_name: str | None,
    fps_limit: int | None,
) -> Dict[str, Any]:
    if source:
        return {
            "id": camera_id,
            "name": camera_name or camera_id,
            "rtsp_url": normalize_source(source),
            "fps_limit": fps_limit or 25,
        }
    if camera_config is None:
        raise RuntimeError("Provide --source or --camera-config.")
    config = load_yaml(camera_config) or {}
    cameras = config.get("cameras") or []
    if not cameras:
        raise RuntimeError(f"No cameras found in {camera_config}")
    camera = dict(cameras[0])
    camera.setdefault("id", camera_id)
    if camera_name:
        camera["name"] = camera_name
    if fps_limit is not None:
        camera["fps_limit"] = fps_limit
    return camera


def run(camera: Dict[str, Any], output_dir: Path, *, log_path: Path | None = None, persist_frames: bool = False) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fps_limit = int(camera.get("fps_limit", 25))
    rtsp_url = camera.get("rtsp_url")
    bus_path = log_path or (output_dir / "frames.log")
    bus_path.parent.mkdir(parents=True, exist_ok=True)
    bus = FileEventBus(bus_path.parent, filename=bus_path.name)
    LOGGER.info("Starting ingest stream", extra={"camera": camera.get("id")})
    if not rtsp_url or rtsp_url.startswith("demo://"):
        generator = synthetic_frames(output_dir, fps=fps_limit, persist=persist_frames)
    elif rtsp_url.startswith("webcam://"):
        try:
            index = int(rtsp_url.split("://", 1)[1])
        except ValueError as exc:  # pragma: no cover - invalid string
            raise RuntimeError(f"Invalid webcam URL: {rtsp_url}") from exc
        generator = capture_webcam(index, output_dir, fps_limit, persist=persist_frames)
    else:
        generator = capture_rtsp(rtsp_url, output_dir, fps_limit, persist=persist_frames)
    for frame in generator:
        bus.publish(
            Event(
                type="frame",
                payload={
                    "camera_id": camera.get("id", "CAM01"),
                    "frame_index": frame.index,
                    "timestamp": frame.timestamp,
                    "path": str(frame.path),
                    "persist": frame.persist,
                },
            )
        )
        LOGGER.debug("Captured frame %s", frame.index)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--camera-config",
        default=os.getenv("CAMERA_CONFIG", "configs/cameras.yaml"),
        help="Path to cameras YAML (defaults to $CAMERA_CONFIG or configs/cameras.yaml when --source not provided).",
    )
    parser.add_argument(
        "--source",
        help="Override source URI (webcam:0, demo://synthetic, rtsp://...).",
    )
    parser.add_argument(
        "--camera-id",
        default=os.getenv("CAMERA_ID", "CAM01"),
        help="Camera ID used when emitting frames (default: %(default)s).",
    )
    parser.add_argument(
        "--camera-name",
        help="Optional camera display name override.",
    )
    parser.add_argument(
        "--fps",
        type=int,
        help="FPS cap override applied to the selected source.",
    )
    parser.add_argument(
        "--output",
        dest="output",
        default=os.getenv("INGEST_OUTPUT", "artifacts/ingest"),
        help="Directory for captured frames.",
    )
    parser.add_argument(
        "--out-dir",
        dest="output",
        help="Alias for --output.",
    )
    parser.add_argument(
        "--log-path",
        default=os.getenv("INGEST_FRAMES_LOG"),
        help="Optional path for the frames log (defaults to <output>/frames.log).",
    )
    parser.add_argument(
        "--save-frames",
        action="store_true",
        help="Persist captured frames on disk (off by default; files are deleted after consumption).",
    )
    args = parser.parse_args()

    camera_cfg = Path(args.camera_config).resolve() if args.camera_config and not args.source else None
    camera = resolve_camera(
        camera_cfg,
        args.source,
        camera_id=args.camera_id,
        camera_name=args.camera_name,
        fps_limit=args.fps,
    )
    log_path = Path(args.log_path).resolve() if args.log_path else None
    run(
        camera,
        Path(args.output).resolve(),
        log_path=log_path,
        persist_frames=bool(args.save_frames),
    )


if __name__ == "__main__":
    main()
