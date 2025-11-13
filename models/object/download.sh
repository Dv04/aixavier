#!/usr/bin/env bash
set -euo pipefail
mkdir -p weights
if [[ ! -f weights/yolov11n.pt ]]; then
  echo "Downloading yolov11n weights" >&2
  curl -L -o weights/yolov11n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov11n.pt
else
  echo "weights/yolov11n.pt already exists" >&2
fi
