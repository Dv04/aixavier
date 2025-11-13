#!/usr/bin/env bash
set -euo pipefail
mkdir -p weights
curl -L -o weights/yolov11n-pose.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov11n-pose.pt
