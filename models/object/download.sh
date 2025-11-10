#!/usr/bin/env bash
set -euo pipefail
mkdir -p weights
if [[ ! -f weights/yolov8n.pt ]]; then
  echo "Downloading YOLOv8n weights" >&2
  curl -L -o weights/yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
else
  echo "weights/yolov8n.pt already exists" >&2
fi
