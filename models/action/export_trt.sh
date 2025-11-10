#!/usr/bin/env bash
set -euo pipefail
mkdir -p engines
MODEL=weights/x3d_s.onnx
if [[ ! -f "$MODEL" ]]; then
  echo "Missing action model; run download.sh" >&2
  exit 1
fi
trtexec --onnx="$MODEL" --saveEngine=engines/x3d_s-fp16.engine --fp16 --workspace=4096
