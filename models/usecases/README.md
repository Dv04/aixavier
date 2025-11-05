# 22-Use-Case Model Locker

This directory is reserved for the deployable inference assets (TensorRT engines, ONNX exports, calibration caches) that back each of the 22 railway CCTV analytics pipelines. Populate the subfolders below with the production-ready artifacts you generate from the workflows in `models/*/`:

```
models/usecases/
  ├─ object_detection/
  │    ├─ fp16/   # e.g., yolov8n.engine
  │    └─ onnx/   # ONNX export
  ├─ pose/
  │    ├─ fp16/
  │    └─ rtmpose_onnx/
  ├─ face_recognition/
  ├─ reid/
  ├─ fire_smoke/
  ├─ violence/
  ├─ fall_detection/
  ├─ ppe_compliance/
  └─ ... (fill out all 22 use cases)
```

Recommended practice:

1. Store FP16 engines in `fp16/`, optional INT8 variants in `int8/`, plus calibration sets in `calib/`.
2. Keep a short `INFO.md` per use case capturing the exact commit, dataset, and calibration profile used to generate the engine.
3. Do **not** check in proprietary weights; reference secure object storage locations in the documentation instead.
4. Ensure `configs/detectors/*.yaml` point to the appropriate engine paths inside this folder when promoting models to production.
