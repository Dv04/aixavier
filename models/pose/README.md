# Pose Estimation Assets

Default: yolov11 Pose or RTMPose (see `models/usecases/pose/`).
- Input: 256x192 (RTMPose tiny) or 640x640 (yolov11 Pose)
- Latency FP16: ~11 ms per frame on Xavier AGX (yolov11n pose)
- VRAM: ~1.2–1.5 GB (tensor buffers included)

### How to stage assets
1. Place pretrained weights or ONNX exports under `models/usecases/pose/` (e.g., `rtmpose_onnx/.../end2end.onnx`).
2. Convert to TensorRT (optional but recommended on Jetson):
   ```bash
   trtexec --onnx=models/usecases/pose/rtmpose_onnx/.../end2end.onnx \
           --saveEngine=models/usecases/pose/fp16/rtmpose.engine \
           --fp16 --workspace=4096
   ```
3. Update `configs/detectors/pose_velocity.yaml` if you use a different filename/resolution.
4. Leave INT8 for later (`calibrate.sh` shows the placeholder structure once a calibration set lives in `models/pose/calib/`).
