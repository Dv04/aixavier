# 22-Use-Case Model Locker

This directory is reserved for the deployable inference assets (TensorRT engines, ONNX exports, calibration caches) that back each of the 22 railway CCTV analytics pipelines. Populate the subfolders below with the production-ready artifacts you generate from the workflows in `models/*/`:

```
models/usecases/
  ├─ object_detection/        # e.g., yolov8n / RT-DETR engines
  ├─ pose_estimation/         # e.g., yolov8n-pose / RTMPose
  ├─ face_recognition/        # SCRFD + ArcFace engines
  ├─ reid/                    # OSNet embeddings
  ├─ fire_smoke/              # EfficientNet-B0 fire/smoke detector
  ├─ violence/                # X3D-S / MoViNet-A0/A2 engines
  ├─ fall_detection/          # Pose velocity calibrations
  ├─ ppe_compliance/          # PPE classifiers or detectors
  └─ ... (fill out all 22 use cases)
```

Recommended practice:

1. Store FP16 engines in `fp16/`, optional INT8 variants in `int8/`, plus calibration sets in `calib/`.
2. Keep a short `INFO.md` per use case capturing the exact commit, dataset, and calibration profile used to generate the engine.
3. Do **not** check in proprietary weights; reference secure object storage locations in the documentation instead.
4. Ensure `configs/detectors/*.yaml` point to the appropriate engine paths inside this folder when promoting models to production.
