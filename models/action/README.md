# Violence / Action Recognition Assets

_Status: 2025-11-20 — services still emit simulated action events; real ONNX/TRT exports need to be staged here before enabling production inference._

Default: X3D-S pretrained on Kinetics-400 with fine-tuning hooks for violence/aggression.

- Input: 16 frames @ 224x224
- Latency FP16: ~18 ms per clip on Xavier AGX
- VRAM: ~1.6 GB for batch=1 FP16

Scripts mirror other folders (`download.sh`, `export_trt.sh`, `calibrate.sh`). Alternate lightweight option: MobileNet-TSM.

Next actions:
- Choose the baseline (X3D-S vs MobileNet-TSM) and export ONNX to `models/action/onnx/`.
- Promote validated TensorRT engines into `models/usecases/violence/fp16|int8/` and document latency on target hardware.
