#!/usr/bin/env bash
set -euo pipefail
mkdir -p weights
curl -L -o weights/scrfd_500m.bmodel https://github.com/deepinsight/insightface/releases/download/v0.7/scrfd_500m_kps.onnx
curl -L -o weights/arcface_mobilefacenet.onnx https://github.com/deepinsight/insightface/releases/download/v0.7/glintr100.onnx
