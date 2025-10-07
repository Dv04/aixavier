#!/usr/bin/env bash
set -euo pipefail
CALIB_DIR=${DATASET_PATH_POSE_CALIB:-{{DATASET_PATH_POSE_CALIB}}}
mkdir -p engines
if [[ ! -d "$CALIB_DIR" ]]; then
  echo "Calibration directory $CALIB_DIR missing" >&2
  exit 1
fi
trtexec --onnx=onnx/yolov8n-pose.onnx --int8 --saveEngine=engines/yolov8n-pose-int8.engine --workspace=4096 --calib=/tmp/yolov8n_pose.calib --calibCache=/tmp/yolov8n_pose.cache
