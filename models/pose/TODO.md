# Pose Detection TODO

## Owner: You

### Must-haves for use cases 8, 13, 20, 22
- **✅ Fix decoder**: SimCC decoding now lives in `src/runners/detectors.py` (auto-detects `simcc_x/simcc_y` heads, rebuilds bboxes/keypoints). Validate on more clips and revert to heuristic only if fallback is needed.
- **Generate engines**: Convert the staged RTMPose ONNX to a TensorRT FP16 engine (`models/usecases/pose/fp16/rtmpose.engine`) and point `configs/detectors/pose_velocity.yaml` at it.
- **Provide collapse/fall/gesture/phone datasets**: Labelled clips for collapse vs normal posture, fall-from-door sequences with GPS/speed annotations, standardized hand signals, and driver mobile-phone usage scenarios.
- **Train & export classifiers/detectors**:
  - Collapse velocity classifier → `models/pose/onnx/collapse_classifier.onnx` + TRT artifact.
  - Fall detector (pose + telemetry) → `models/pose/onnx/fall_classifier.onnx`.
  - Gesture recognizer → `models/action/onnx/gesture_classifier.onnx` (or `models/pose/onnx/`).
  - Mobile-phone usage detector → `models/object/onnx/phone_detector.onnx` (or pose-based classifier) plus TRT export.
- **Telemetry feeds**: Provide real-time train speed, GPS and door-state signals (MQTT/REST) so fall detection can gate alerts.
- **Threshold tuning**: Run the new models on real rolling-stock footage to tune dwell durations, velocity-drop limits, phone-confidence scores, etc., and update `configs/usecases/*.yaml`.
- **Validation & smoke runs**: After plugging in each model, run `python -m src.apps.live_demo ...` (or RTSP ingest) to ensure pose overlays, detections, and rule triggers behave correctly.

### Enhancements / nice-to-haves
- **Consistency sweep**: Decide on the canonical pose backbone (RTMPose-m vs YOLO-pose) and align configs/input sizes; clean up legacy checkpoints.
- **Calibration prep**: Collect frames for `models/pose/calib/` (and equivalents for object/action) to enable INT8 exports later.
- **Demo polish**: Record annotated MP4s or screenshots using `SHOW=1/RECORD=... make live` and embed them in docs once TRT inputs are final.
- **Audio/ASR feed**: Optional unless we pair gestures with spoken call-outs (use case 19).

## Owner: Assistant
- ✅ ByteTrack-lite manager in place; next step is wiring OSNet ReID once embeddings/models are available (leave placeholder in configs).
- Add a regression test that loads the RTMPose ONNX/TRT engine, runs SimCC decode, and asserts K×3 keypoints on a known frame (now unblocked by decoder work).
- Extend exporter metrics further (per-model latency, queue depth) once real TRT engines are staged.
