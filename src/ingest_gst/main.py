from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

from common.config import env_or_default, load_yaml
from common.event_bus import Event, FileEventBus

from .pipeline import capture_rtsp, synthetic_frames

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("ingest")


def run(camera_config: Path, output_dir: Path) -> None:
    config = load_yaml(camera_config)
    camera = config["cameras"][0]
    fps_limit = int(camera.get("fps_limit", 25))
    rtsp_url = camera.get("rtsp_url")
    bus = FileEventBus(output_dir, filename="frames.log")
    LOGGER.info("Starting ingest stream", extra={"camera": camera.get("id")})
    generator = (
        capture_rtsp(rtsp_url, output_dir, fps_limit)
        if rtsp_url and not rtsp_url.startswith("demo://")
        else synthetic_frames(output_dir, fps=fps_limit)
    )
    for frame in generator:
        bus.publish(
            Event(
                type="frame",
                payload={
                    "camera_id": camera["id"],
                    "frame_index": frame.index,
                    "timestamp": frame.timestamp,
                    "path": str(frame.path),
                },
            )
        )
        LOGGER.debug("Captured frame %s", frame.index)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--camera-config",
        default=env_or_default("CAMERA_CONFIG", "configs/cameras.yaml"),
    )
    parser.add_argument(
        "--output",
        default=os.getenv("INGEST_OUTPUT", "artifacts/ingest"),
    )
    args = parser.parse_args()
    run(Path(args.camera_config), Path(args.output))


if __name__ == "__main__":
    main()
