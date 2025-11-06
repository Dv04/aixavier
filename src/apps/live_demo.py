"""
Launch a self-contained live demo by orchestrating ingest + detector.

Usage:
    python -m src.apps.live_demo --config configs/detectors/pose_velocity.yaml --source webcam:0
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Sequence, Tuple


DEFAULT_CONFIG = "configs/detectors/pose_velocity.yaml"
DEFAULT_OUTPUT = "artifacts/live_demo"


def parse_args(argv: Sequence[str] | None = None) -> Tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(description="Run a detector locally with an auto-launched ingest loop.")
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help="Detector config YAML; exported as DETECTOR_CONFIG (default: %(default)s).",
    )
    parser.add_argument(
        "--source",
        default="webcam:0",
        help="Input source hint (webcam:N, demo://synthetic, rtsp://, file path).",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Base directory for live demo artifacts (frames, logs).",
    )
    parser.add_argument(
        "--camera-id",
        default="CAM_WEB",
        help="Camera ID recorded in emitted events.",
    )
    parser.add_argument(
        "--camera-name",
        default="Live Demo Camera",
        help="Human-friendly camera label stored in the temporary config.",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=25,
        help="Capture FPS limit passed to ingest.",
    )
    parser.add_argument(
        "--save-frames",
        action="store_true",
        help="Keep captured frames on disk (default: delete after detector consumes them).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Open a live preview window with pose overlays.",
    )
    parser.add_argument(
        "--record",
        default="",
        help="Path to save annotated MP4 (requires OpenCV VideoWriter).",
    )
    return parser.parse_known_args(argv)


def normalize_source(source: str) -> str:
    if source.startswith("webcam://"):
        return source
    if source.startswith("webcam:"):
        return f"webcam://{source.split(':', 1)[1]}"
    return source


def reset_frames_log(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        log_path.unlink()
    except FileNotFoundError:
        pass


def launch_ingest(
    source: str,
    output_dir: Path,
    frames_log: Path,
    *,
    camera_id: str,
    camera_name: str,
    fps: int,
    save_frames: bool,
    env: dict[str, str],
) -> subprocess.Popen:
    cmd = [
        sys.executable,
        "-m",
        "src.ingest_gst.main",
        "--source",
        source,
        "--camera-id",
        camera_id,
        "--camera-name",
        camera_name,
        "--fps",
        str(fps),
        "--output",
        str(output_dir),
        "--log-path",
        str(frames_log),
    ]
    if save_frames:
        cmd.append("--save-frames")
    proc = subprocess.Popen(cmd, env=env)
    # Give the subprocess a moment to fail fast if configuration is invalid.
    time.sleep(0.5)
    if proc.poll() is not None:
        raise RuntimeError(f"Ingest process exited immediately with code {proc.returncode}.")
    return proc


def terminate_process(proc: subprocess.Popen | None, name: str) -> None:
    if not proc:
        return
    if proc.poll() is not None:
        return
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def main(argv: Sequence[str] | None = None) -> int:
    args, passthrough = parse_args(argv)
    env = os.environ.copy()
    detector_config = Path(args.config).resolve()
    output_dir = Path(args.output).resolve()
    ingest_dir = output_dir / "ingest"
    frames_log = ingest_dir / "frames.log"
    reset_frames_log(frames_log)

    normalized_source = normalize_source(args.source)
    env["DETECTOR_CONFIG"] = str(detector_config)
    env["LIVE_DEMO_SOURCE"] = normalized_source
    env["INGEST_OUTPUT"] = str(ingest_dir)
    env["INGEST_FRAMES_LOG"] = str(frames_log)
    if args.show:
        env["LIVE_DEMO_SHOW"] = "1"
    if args.record:
        env["LIVE_DEMO_RECORD"] = str(Path(args.record).resolve())
        env["LIVE_DEMO_RECORD_FPS"] = str(args.fps)

    ingest_proc: subprocess.Popen | None = None
    return_code = 1
    try:
        ingest_proc = launch_ingest(
            normalized_source,
            ingest_dir,
            frames_log,
            camera_id=args.camera_id,
            camera_name=args.camera_name,
            fps=args.fps,
            save_frames=args.save_frames,
            env=env,
        )
        cmd = [sys.executable, "-m", "src.runners.main", *passthrough]
        return_code = subprocess.call(cmd, env=env)
    except KeyboardInterrupt:
        return_code = 130
    finally:
        terminate_process(ingest_proc, "ingest")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
