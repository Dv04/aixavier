# Re-Identification Assets

_Status: 2025-11-20 — OSNet assets not yet wired into the tracker; export ONNX/TRT and stage them here before enabling ReID in ByteTrack._

Default: OSNet_x0_25 (lightweight, suitable for Xavier NX).
- Input size: 256x128 crops
- Latency FP16: ~1.7 ms per crop
- VRAM: ~0.4 GB for batch of 16

Scripts: `download.sh`, `export_trt.sh`, `calibrate.sh`.
