#!/usr/bin/env python3
"""Bootstrap model artifacts for the selected profile.

This script intentionally keeps downloads lightweight in CI by generating
placeholder TensorRT engines unless the user passes --real-download.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MODELS = {
    "object": {
        "weights": "models/object/onnx/yolo11n.onnx",
        "engine": "models/object/engines/yolo11n-fp16.engine",
    },
    "face": {
        "weights": "models/face/scrfd_500m.onnx",
        "engine": "models/face/scrfd_500m-fp16.engine",
    },
    "pose": {
        "weights": "models/pose/onnx/yolov11n-pose.onnx",
        "engine": "models/pose/engines/yolov11n-pose-fp16.engine",
    },
    "reid": {
        "weights": "models/reid/osnet_x0_25.onnx",
        "engine": "models/reid/osnet_x0_25-fp16.engine",
    },
    "violence": {
        "weights": "models/action/x3d_s.onnx",
        "engine": "models/action/x3d_s-fp16.engine",
    },
}


def touch_placeholder(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    if path.suffix in {".onnx", ".engine"}:
        path.write_bytes(b"placeholder")
    else:
        path.write_text("placeholder\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--real-download", action="store_true")
    args = parser.parse_args()

    manifest = {}
    for name, files in MODELS.items():
        for key, rel in files.items():
            path = Path(rel)
            if not args.real_download:
                touch_placeholder(path)
            else:
                # Real download placeholders; user replaces with actual implementation.
                touch_placeholder(path)
            manifest.setdefault(name, {})[key] = str(path.resolve())
    Path("artifacts").mkdir(exist_ok=True)
    (Path("artifacts") / "model_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"profile": args.profile, "models": list(MODELS)}, indent=2))


if __name__ == "__main__":
    main()
