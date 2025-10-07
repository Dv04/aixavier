# Violence / Action Recognition Assets

Default: X3D-S pretrained on Kinetics-400 with fine-tuning hooks for violence/aggression.

- Input: 16 frames @ 224x224
- Latency FP16: ~18 ms per clip on Xavier AGX
- VRAM: ~1.6 GB for batch=1 FP16

Scripts mirror other folders (`download.sh`, `export_trt.sh`, `calibrate.sh`). Alternate lightweight option: MobileNet-TSM.
