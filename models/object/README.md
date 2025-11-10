# YOLO Detector Assets

Default detector: YOLOv8n (object/person generalist).

- Input size: 640x640
- Expected latency (FP16): ~8 ms per frame on Xavier AGX @ 45W
- Expected latency (INT8): ~5 ms per frame with calibrated dataset
- VRAM usage: ~1.2 GB (TensorRT engine + buffers)

Use the helper scripts:
- `download.sh` – fetch ultralytics weights
- `export_trt.sh` – export ONNX and TensorRT engines (FP16/INT8)
- `calibrate.sh` – run INT8 calibration (requires dataset path placeholder)

Alternate model: RT-DETR-R18-tiny -> document results in `docs/MODELS.md` when agent validates.
