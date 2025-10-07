#!/usr/bin/env bash
set -euo pipefail
CALIB_DIR=${DATASET_PATH_FACE_CALIB:-{{DATASET_PATH_FACE_CALIB}}}
mkdir -p engines
if [[ ! -d "$CALIB_DIR" ]]; then
  echo "Calibration directory $CALIB_DIR missing" >&2
  exit 1
fi
trtexec --onnx=weights/scrfd_500m_kps.onnx --saveEngine=engines/scrfd_500m-int8.engine --int8 --workspace=2048 --calib=/tmp/scrfd.calib --calibCache=/tmp/scrfd.cache
trtexec --onnx=weights/arcface_mobilefacenet.onnx --saveEngine=engines/arcface_mobilefacenet-int8.engine --int8 --workspace=1024 --calib=/tmp/arcface.calib --calibCache=/tmp/arcface.cache
