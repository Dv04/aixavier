# Face Detection & Recognition Assets

Default stack: SCRFD-500M (detector) + MobileFaceNet ArcFace head.
- Input size: 320x320 detector, 112x112 embedding
- Latency (FP16): ~6 ms detector + ~2 ms embedding on Xavier AGX
- VRAM: ~1.0 GB including buffers

Scripts:
- `download.sh` – grab SCRFD and MobileFaceNet weights.
- `export_trt.sh` – export combined TensorRT engines (detector + embedding).
- `calibrate.sh` – INT8 calibration using curated face dataset.

Embeddings are stored encrypted on-device (`src/privacy/embeddings_store.py`).
