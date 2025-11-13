#!/usr/bin/env bash
set -euo pipefail
CALIB_DIR=${DATASET_PATH_OBJECT_CALIB:-{{DATASET_PATH_OBJECT_CALIB}}}
ENGINE_OUT=engines/yolov11n-int8.engine
mkdir -p engines
if [[ ! -d "$CALIB_DIR" ]]; then
  echo "Calibration directory $CALIB_DIR missing" >&2
  exit 1
fi
trtexec \
  --onnx=onnx/yolov11n.onnx \
  --int8 \
  --calib=/tmp/yolov11n.calib \
  --saveEngine="$ENGINE_OUT" \
  --workspace=4096 \
  --calibCache=/tmp/yolov11n.cache
