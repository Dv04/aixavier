# Implementation Status – 2025-10-31

This document summarises the current state of the Aixavier Edge Analytics stack so a new engineer (human or assistant) can resume work without digging through code history.

## Services Overview

| Service | Code Path | Status | Notes |
|---------|-----------|--------|-------|
| ingest  | `src/ingest_gst/` | Demo-ready | Synthetic + RTSP + `webcam://` capture (needs on-device validation). |
| detect_object | `src/runners/` (config: `configs/detectors/object.yaml`) | ONNX/TRT-capable | Uses shared runner with ONNX fallback and SimpleTracker IDs; requires production engines. |
| detect_pose | `src/runners/` (config: `configs/detectors/pose_velocity.yaml`) | ONNX/TRT-capable | Pose events aligned with object tracks via cached detections; needs real models. |
| detect_face / detect_action | `src/runners/` | Simulated | Still emit synthetic events; promote to real inference later. |
| tracker | `src/trackers/` | ByteTrack-lite | ByteTrack-style matcher with Simple fallback; ReID still pending. |
| rules | `src/rules/engine.py` | Demo-ready | Dwell logic fixed; other rule types awaiting real data. |
| recorder | `src/recorder/` | Stub | Writes JSON; replace with video circular buffer. |
| privacy | `src/privacy/` | Stub | Enrollment + embeddings need hardened store/RBAC. |
| exporter | `src/exporter/` | Stub | Emits simulated metrics; wire to real telemetry. |
| ui | `src/ui/` | Basic | FastAPI endpoints + Streamlit; requires full dashboard build-out. |

## Models & Assets

- Place ONNX exports under `models/usecases/<use-case>/onnx/` (object) or `models/usecases/pose/rtmpose_onnx/` (pose) for CPU dev.
- Stage production TensorRT engines under `models/usecases/<use-case>/fp16/` (INT8 later).
- `models/pose/TODO.md` and `models/yolo/TODO.md` track outstanding work for the two active use cases.
- Calibration datasets should live under `models/<modality>/calib/`.

## Tracking & Pose Association

- `SimpleTracker` assigns persistent IDs per camera and caches the latest object detections under `artifacts/detections/cache/<camera>.json`.
- Pose detections reuse cached `person` boxes for track association; accuracy will improve once ByteTrack + ReID is added.

## Tests

- `pytest` suite covers rule engine, tracker, and (optionally) detector post-processing. Set `AIXAVIER_ENABLE_NUMPY_TESTS=1` when NumPy is available to enable ONNX layout tests.
- Add integration tests once real models are staged.

## Outstanding Work (High Level)

1. Replace simulated face/action detectors with real inference pipelines.
2. Integrate ByteTrack + OSNet ReID for production-grade tracking.
3. Deploy recorder (video), exporter (metrics), privacy (embeddings) with real functionality.
4. Resolve all placeholders via `.env` and the placeholder resolver before production builds.
5. Harden docs/CI: run detector integration tests and enforce placeholder gate in `agent-ci` workflow.
6. INT8 calibration for detectors (object + pose) once datasets are ready.

Refer to `docs/next_steps.md` for the detailed roadmap and `HANDOFF.md` for chronological change logs.
