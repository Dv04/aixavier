# Pose Detection TODO

## Owner: You
- **Fix decoder**: Implement SimCC decoding for the RTMPose ONNX (two outputs: `simcc_x`, `simcc_y`) so keypoints are real rather than YOLO-style placeholders.
- **Generate engines**: Convert the staged RTMPose ONNX to a TensorRT FP16 engine (`models/usecases/pose/fp16/rtmpose.engine`) and point `configs/detectors/pose_velocity.yaml` at it. Keep INT8 in backlog.
- **Consistency sweep**: Decide on the canonical pose model (RTMPose-m vs YOLO-pose) and make config/input sizes match. Remove/rename leftover checkpoints to avoid confusion.
- **Validation**: Capture webcam/RTSP clips, verify keypoints overlay correctly, and tune `confidence_threshold`, `nms_iou_threshold`, and rule parameters based on real footage.
- **Calibration prep** (later): start collecting frames for `models/pose/calib/` to enable INT8 export once accuracy is locked in.
- **Smoke test**: run `CAMERA_RTSP_URL_01=webcam://0` with the new engine to ensure the pipeline works before moving back to RTSP feeds.

## Owner: Assistant
- ✅ ByteTrack-lite manager in place; next step is wiring OSNet ReID once embeddings/models are available (leave placeholder in configs).
- Add a regression test that loads the RTMPose ONNX/TRT engine, runs SimCC decode, and asserts K×3 keypoints on a known frame (after the decoder lands).
- Extend exporter metrics further (per-model latency, queue depth) once real TRT engines are staged.
