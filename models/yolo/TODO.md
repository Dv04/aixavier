# Object Detection TODO

## Owner: You
- Fine-tune or select production weights that include PPE/rail-specific classes and export ONNX/TRT models.
- Populate `models/usecases/object_detection/fp16|int8/` with validated engines and update `configs/detectors/object.yaml` paths.
- Build calibration set under `models/yolo/calib/` for INT8 accuracy.
- Validate detections on real RTSP feeds and tune `confidence_threshold`, `nms_iou_threshold`, and class list per deployment.

## Owner: Assistant
- Integrate full ByteTrack + OSNet ReID once approved weights are available.
- Add end-to-end detector regression tests once production assets are staged.
- Expand exporter metrics to capture object detector latency/FPS and drop-rate after real models are integrated.
