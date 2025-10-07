#!/usr/bin/env bash
set -euo pipefail
CALIB_DIR=${DATASET_PATH_OBJECT_CALIB:-{{DATASET_PATH_OBJECT_CALIB}}}
ENGINE_OUT=engines/yolov8n-int8.engine
mkdir -p engines
if [[ ! -d "$CALIB_DIR" ]]; then
  echo "Calibration directory $CALIB_DIR missing" >&2
  exit 1
fi
trtexec \
  --onnx=onnx/yolov8n.onnx \
  --int8 \
  --calib=/tmp/yolov8n.calib \
  --saveEngine="$ENGINE_OUT" \
  --workspace=4096 \
  --calibCache=/tmp/yolov8n.cache
