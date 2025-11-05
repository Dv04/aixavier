# Pose Detection TODO

## Owner: You
- Gather/calibrate real pose datasets (`models/pose/calib/`) for INT8 export.
- Export production TensorRT engines (FP16/INT8) into `models/usecases/pose_estimation/fp16|int8/`.
- Collect validation clips and verify pose accuracy/latency on target Jetson hardware.
- Swap the heuristic fallback for actual TRT inference in configs once engines are staged.
- Tune velocity/fall detection thresholds against real video and update rule configs.
- Smoke-test the detector with `CAMERA_RTSP_URL_01=webcam://0` before moving to RTSP feeds.

## Owner: Assistant
- Wire pose-to-person association to ByteTrack/ReID when the full tracker lands.
- Add automated pose integration tests once production assets exist.
- Extend exporter metrics to expose pose-specific latency/FPS once real pipelines run.
