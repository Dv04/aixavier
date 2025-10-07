# Models

This document is maintained by the agent. Manual notes belong outside auto sections.

<!-- auto:start name=models-matrix -->
| Task | Model | Backbone / Size | Dataset | Latency FP16 (ms) | Latency INT8 (ms) | VRAM (GB) | Params (M) | License | Why Pick | Links |
|------|-------|-----------------|---------|-------------------|-------------------|-----------|------------|---------|---------|-------|
| object_detection | YOLOv8n | Nano | COCO 2017 | ≈9 | ≈6 | 1.0 | 3.2 | AGPL-3.0 | Calibrates easily to Jetson, strong baseline mAP for small objects | https://github.com/ultralytics/ultralytics |
| object_detection | YOLOv8s | Small | COCO 2017 | ≈13 | ≈9 | 1.6 | 11.2 | AGPL-3.0 | Higher mAP for multi-class profiles with modest latency hit | https://github.com/ultralytics/ultralytics |
| face_detection | SCRFD-500M | Custom | WiderFace | ≈4 | ≈3 | 0.6 | 0.5 | MIT | Robust under occlusion, packaged TensorRT exporters available | https://github.com/deepinsight/insightface |
| face_recognition | ArcFace-R100 | ResNet100 | MS1MV3 | ≈6 | ≈4 | 1.2 | 65.0 | MIT | Proven identification accuracy, feature parity with on-prem ArcFace stack | https://github.com/deepinsight/insightface |
| pose_estimation | RTMPose-m | ConvNeXt-m | COCO + Halpe | ≈17 | ≈11 | 2.2 | 35.0 | Apache-2.0 | Multi-pose support with TensorRT tooling and INT8 calibration sets | https://github.com/open-mmlab/mmpose |
| action_recognition | SlowFast-R50 | R50 + Fast pathway | Kinetics-400 | ≈28 | ≈19 | 3.5 | 34.0 | Apache-2.0 | Handles violence/fall cues; pretrained checkpoints maintained upstream | https://github.com/facebookresearch/SlowFast |
| smoke_detection | EfficientNet-B0 FireNet | EfficientNet-B0 | Fire & Smoke v1 (CC BY 4.0) | ≈11 | ≈7 | 1.4 | 5.3 | MIT | Lightweight binary classifier tuned for smoke/flame differentiation | https://github.com/titu1994/keras-firenet |
| violence_detection | X3D-M | Mobile Video Network | XDV (Violence2D) | ≈15 | ≈10 | 2.1 | 3.8 | Apache-2.0 | Efficient spatiotemporal head for real-time violence cues | https://github.com/facebookresearch/SlowFast |
<!-- auto:end -->

Manual notes:
- Latency figures are measured on Jetson Xavier AGX in 30W mode with TensorRT 8.6; expect ±10% variance based on thermal budget.
- INT8 numbers assume calibration datasets shipped under `models/*/calibrate.sh`.
- Alternate object detectors (PP-YOLOE, RT-DETR) and segmentation heads tracked in README Design Notes; promote once agent confirms export stability.
