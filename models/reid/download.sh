#!/usr/bin/env bash
set -euo pipefail
mkdir -p weights
curl -L -o weights/osnet_x0_25_msmt17.onnx https://github.com/KaiyangZhou/deep-person-reid/releases/download/model-zoo/osnet_x0_25_msmt17.onnx
