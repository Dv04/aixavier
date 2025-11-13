#!/usr/bin/env bash
set -euo pipefail
mkdir -p onnx engines
python3 - <<'PY'
import subprocess
from pathlib import Path
weights = Path('weights/yolov11n-pose.pt')
if not weights.exists():
    raise SystemExit('Run download.sh first')
onnx = Path('onnx/yolov11n-pose.onnx')
if not onnx.exists():
    subprocess.run([
        'python3', '-m', 'ultralytics', 'export',
        f'model={weights}',
        'format=onnx',
        'imgsz=640'
    ], check=True)
subprocess.run([
    'trtexec',
    f'--onnx={onnx}',
    '--saveEngine=engines/yolov11n-pose-fp16.engine',
    '--fp16',
    '--workspace=4096'
], check=True)
PY
