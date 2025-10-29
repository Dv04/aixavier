# Models

This document is maintained by the agent. Manual notes belong outside auto sections.

<!-- auto:start name=models-matrix -->
| Task | Model | Backbone/Size | Training Data | Benchmark | Latency (FP16/INT8 ms) | VRAM (GB) | Params (M) | License | Why pick | Links |
|------|-------|----------------|---------------|-----------|------------------------|-----------|------------|---------|----------|-------|
| face_recognition | MobileFaceNet ArcFace | MobileFaceNet | Glint360K | LFW / IJB-C TAR@FAR=1e-4 | 2.10/1.50 | 0.40 | 1.30 | MIT | Lightweight embeddings yield sub-3 ms inference with acceptable verification accuracy. | https://github.com/deepinsight/insightface |
| reid | OSNet_x0_25 | OSNet x0.25 | MSMT17 + pretrain | MSMT17 mAP | 1.90/1.30 | 0.35 | 0.70 | MIT | Tiny footprint while keeping >50% mAP for staff tracking/association. | https://github.com/KaiyangZhou/deep-person-reid |
| face_detection | SCRFD-500M | Custom (MobileNet) | WiderFace | WiderFace easy/medium/hard | 6.20/4.10 | 0.90 | 0.50 | MIT | Best balance of recall vs throughput for FRS entry point; stable InsightFace tooling. | https://github.com/deepinsight/insightface |
| fire_smoke_detection | EfficientNet-B0 Fire | EfficientNet-B0 | FIReS + custom rail smoke | FIReS F1 | 9.80/6.70 | 1.00 | 5.30 | Apache-2.0 | Temporal smoothing friendly; consistent with haze detection heuristics. | https://github.com/google/automl |
| violence_detection | MobileNet-TSM | MobileNetV2 + Temporal Shift | RWF-2000 | RWF-2000 accuracy | 12.90/9.00 | 1.10 | 2.20 | Apache-2.0 | Use when action queue saturates; 30% lighter than X3D-S. | https://github.com/mit-han-lab/temporal-shift-module |
| pose_estimation | YOLOv8n-pose | YOLOv8 nano pose | COCO keypoints | COCO AP | 11.30/7.90 | 1.40 | 3.00 | GPLv3 | Supports skeleton velocity pipeline with unified pre-processing with detector. | https://github.com/ultralytics/ultralytics |
| object_detection | YOLOv10n | YOLOv10 nano | COCO 2017 | COCO mAP@0.5:0.95 | 7.40/4.90 | 1.30 | 3.30 | GPLv3 | Edge-optimised upgrade with minor latency gain and better mAP; requires latest TensorRT parser. | https://github.com/THU-MIG/yolov10 |
| object_detection | YOLOv8n | YOLOv8 nano | COCO 2017 | COCO mAP@0.5:0.95 | 8.10/5.20 | 1.20 | 3.20 | GPLv3 | Baseline detector with mature TensorRT export path and excellent throughput on Xavier. | https://github.com/ultralytics/ultralytics |
| violence_detection | X3D-S | X3D | Kinetics-400 fine-tuned on RWF-2000 | RWF-2000 accuracy | 18.40/12.60 | 1.60 | 3.80 | Apache-2.0 | High recall for aggression with manageable latency using clip_stride=2. | https://github.com/facebookresearch/pytorchvideo |
| open_vocabulary | YOLO-World-s | YOLO-World small | Objects365 + ImageNet-22K | OVAD mAP | 15.60/11.10 | 1.80 | 11.00 | Apache-2.0 | Optional exploratory classes for post-incident analytics; disabled by default. | https://github.com/AILab-CVC/YOLO-World |
<!-- auto:end -->

Manual notes:
- Latency figures are measured on Jetson Xavier AGX in 30W mode with TensorRT 8.6; expect ±10% variance based on thermal budget.
- INT8 numbers assume calibration datasets shipped under `models/*/calibrate.sh`.
- Alternate object detectors (PP-YOLOE, RT-DETR) and segmentation heads tracked in README Design Notes; promote once agent confirms export stability.
