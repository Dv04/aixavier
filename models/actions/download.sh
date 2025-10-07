#!/usr/bin/env bash
set -euo pipefail
mkdir -p weights
curl -L -o weights/x3d_s.onnx https://dl.fbaipublicfiles.com/pytorchvideo/x3d/sota/x3d_s.onnx
