#!/usr/bin/env bash
set -euo pipefail
MODEL_WEIGHTS=${1:-weights/yolov8n.pt}
OUT_DIR=engines
mkdir -p onnx "$OUT_DIR"
python3 - <<'PY'
import subprocess
import sys
from pathlib import Path
weights = Path(sys.argv[1])
if not weights.exists():
    print(f"Weights {weights} missing. Run download.sh first.", file=sys.stderr)
    sys.exit(1)
onnx = Path('onnx/yolov8n.onnx')
if not onnx.exists():
    subprocess.run([
        'python3', '-m', 'ultralytics', 'export',
        f'model={weights}',
        'format=onnx',
        'imgsz=640',
        'half=True'
    ], check=True)
engine = Path('engines/yolov8n-fp16.engine')
if not engine.exists():
    subprocess.run([
        'trtexec',
        f'--onnx={onnx}',
        '--saveEngine=engines/yolov8n-fp16.engine',
        '--fp16',
        '--workspace=2048'
    ], check=True)
PY
