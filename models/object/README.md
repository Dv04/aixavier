# YOLO Detector Assets

_Status: 2025-11-20 — ONNX/TRT exports are still expected; production engines should be staged under `models/usecases/object_detection/fp16|int8/` once validated._

Default detector: yolov11n (object/person generalist).

- Input size: 640x640
- Expected latency (FP16): ~8 ms per frame on Xavier AGX @ 45W
- Expected latency (INT8): ~5 ms per frame with calibrated dataset
- VRAM usage: ~1.2 GB (TensorRT engine + buffers)

Use the helper scripts:
- `download.sh` – fetch ultralytics weights
- `export_trt.sh` – export ONNX and TensorRT engines (FP16/INT8)
- `calibrate.sh` – run INT8 calibration (requires dataset path placeholder)

Next actions:
- Fill `models/object/onnx/` with the chosen baseline (yolov11n or RT-DETR), then export TRT engines into the use-case locker.
- Log the exact model commit/checkpoint and calibration dataset in a short `INFO.md` when you promote an engine.

Alternate model: RT-DETR-R18-tiny -> document results in `docs/MODELS.md` when agent validates.
