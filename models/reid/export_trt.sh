#!/usr/bin/env bash
set -euo pipefail
mkdir -p engines
MODEL=weights/osnet_x0_25_msmt17.onnx
if [[ ! -f "$MODEL" ]]; then
  echo "Missing ReID weights; run download.sh" >&2
  exit 1
fi
trtexec --onnx="$MODEL" --saveEngine=engines/osnet_x0_25-fp16.engine --fp16 --workspace=1024
