#!/usr/bin/env bash
set -euo pipefail
mkdir -p onnx engines
SCRFD=weights/scrfd_500m_kps.onnx
EMBED=weights/arcface_mobilefacenet.onnx
if [[ ! -f "$SCRFD" || ! -f "$EMBED" ]]; then
  echo "Missing weights; run download.sh" >&2
  exit 1
fi
trtexec --onnx="$SCRFD" --saveEngine=engines/scrfd_500m-fp16.engine --fp16 --workspace=2048
trtexec --onnx="$EMBED" --saveEngine=engines/arcface_mobilefacenet-fp16.engine --fp16 --workspace=1024
