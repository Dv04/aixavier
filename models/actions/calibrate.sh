#!/usr/bin/env bash
set -euo pipefail
CALIB_DIR=${DATASET_PATH_VIOLENCE:-{{DATASET_PATH_VIOLENCE}}}
mkdir -p engines
if [[ ! -d "$CALIB_DIR" ]]; then
  echo "Calibration dataset missing" >&2
  exit 1
fi
trtexec --onnx=weights/x3d_s.onnx --int8 --saveEngine=engines/x3d_s-int8.engine --workspace=4096 --calib=/tmp/x3d.calib --calibCache=/tmp/x3d.cache
