#!/usr/bin/env bash
set -euo pipefail
CALIB_DIR=${DATASET_PATH_REID_CALIB:-{{DATASET_PATH_REID_CALIB}}}
mkdir -p engines
if [[ ! -d "$CALIB_DIR" ]]; then
  echo "Missing calibration dir" >&2
  exit 1
fi
trtexec --onnx=weights/osnet_x0_25_msmt17.onnx --int8 --saveEngine=engines/osnet_x0_25-int8.engine --workspace=1024 --calib=/tmp/osnet.calib --calibCache=/tmp/osnet.cache
