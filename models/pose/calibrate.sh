#!/usr/bin/env bash
set -euo pipefail
CALIB_DIR=${DATASET_PATH_POSE_CALIB:-{{DATASET_PATH_POSE_CALIB}}}
mkdir -p engines
if [[ ! -d "$CALIB_DIR" ]]; then
  echo "Calibration directory $CALIB_DIR missing" >&2
  exit 1
fi
trtexec --onnx=onnx/yolov11n-pose.onnx --int8 --saveEngine=engines/yolov11n-pose-int8.engine --workspace=4096 --calib=/tmp/yolov11n_pose.calib --calibCache=/tmp/yolov11n_pose.cache
