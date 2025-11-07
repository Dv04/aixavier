# Pose Detection – Implementation Notes

This document captures every code/documentation touchpoint that was involved in turning the pose detection pipeline into something runnable (even if the model assets are still placeholders awaiting your calibrated exports).

## Files touched for pose detection

| File | Purpose / Change |
|------|------------------|
| `configs/detectors/pose_velocity.yaml` | Declares the pose detector profile (model name, ONNX/TRT paths, input size, thresholds, publish path, intervals). Update `engine_path` once your FP16 TRT export is ready. |
| `src/runners/detectors.py` | Shared detector runtime. Adds the pose inference path (currently YOLO-style decode pending SimCC implementation) plus input letterboxing, TensorRT/ONNX dispatch, fallback heuristics, and max-detection handling. |
| `src/runners/main.py` | Detector service orchestrator. Reads frames from ingest, runs detectors, hands detections to the tracker manager, and publishes events. Includes pose ↔ person association hooks and cache writes. |
| `src/runners/pose_assoc.py` | Helper module that matches pose detections with the latest tracked person boxes (IoU-based), stamping `track_id`/`first_seen` onto pose events. |
| `src/trackers/bytetrack.py` | Houses the ByteTrack-lite implementation and a SimpleTracker fallback; ensures pose/object detectors get persistent IDs per camera. |
| `src/trackers/__init__.py` | Exposes `TrackerManager`, which builds/configures per-camera trackers (ByteTrack or Simple) based on environment knobs. |
| `src/exporter/main.py` | Emits Prometheus counters/gauges for pose events (`pose_event_total`, `pose_events_per_second`) so you can monitor detection throughput once engines are wired in. |
| `models/pose/README.md` | Documents the current pose model choices (YOLOv8 pose vs RTMPose), input sizes, and the steps for exporting TensorRT engines. |
| `models/pose/TODO.md` | Tracks the outstanding pose work: SimCC decoder, engine exports, calibration datasets, validation, ByteTrack + ReID follow-ups. |
| `models/usecases/README.md` | Defines the shared layout for staging deployable engines/ONNX exports (pose folder included). |
| `docs/IMPLEMENTATION_STATUS.md` | High-level status table noting that pose detection is demo-ready with ONNX/TRT fallback but still needs proper decoding + calibration. |
| `docs/next_steps.md` | Roadmap entry and test matrix updates describing the pose pipeline, tracker state, webcam smoke-test instructions, and remaining blockers. |
| `README.md` | User-facing instructions: how to run pose/object detectors locally (webcam), where to place ONNX/TRT assets, tracker configuration knobs, and overall architecture notes. |
| `tests/test_pose_assoc.py` | Exercises the pose-to-person association helper to ensure matching logic behaves as expected. |
| `tests/test_tracker.py`, `tests/test_tracker_manager.py` | Cover ByteTrack-lite + TrackerManager behaviours that pose detection relies on (persistent IDs, matching). |
| `tests/test_event_bus.py`, `tests/test_healthcheck.py`, `tests/test_exporter.py` | Support files that became indirectly relevant (event publishing, ingest healthcheck, exporter pose metrics). These keep the pose stack’s plumbing testable. |

> Pending change: implement the RTMPose SimCC decoder inside `PoseDetector._detect_onnx` (see `models/pose/TODO.md` for the precise instructions and checklist).

## Implementing other use cases

To bring a new use case (e.g., fire/smoke, PPE detection, fall detection) up to the same standard, follow this template:

1. **Stage model assets**
   - Drop ONNX exports under `models/usecases/<use-case>/onnx/…`.
   - Convert to TensorRT FP16 (and later INT8) under `models/usecases/<use-case>/fp16|int8/…`.
   - Document the source checkpoints + export steps in `models/<use-case>/README.md` and track TODOs in `models/<use-case>/TODO.md`.

2. **Wire configs and runtime**
   - Create/update `configs/detectors/<use-case>.yaml` with the appropriate paths, thresholds, class names, and intervals.
   - Extend `src/runners/detectors.py` (or add a modality-specific module) for any custom decode logic (e.g., classification heads, multi-head outputs).
   - Ensure `docker-compose.yml` has a `<use-case>` service pointing at the right config/Dockerfile.

3. **Tracking & association**
   - Decide whether the use case should share object/person tracks, its own tracker (like pose), or none (e.g., action snippets).
   - If it needs cross-entity association (e.g., objects tied to people), create a helper similar to `src/runners/pose_assoc.py`.

4. **Rules & events**
   - Add or update rule definitions under `configs/usecases/*.yaml` so events produced by the new detector trigger the right logic.
   - Update `src/rules/engine.py` if new rule types are required.

5. **Observability**
   - Extend `src/exporter/main.py` with detector-specific metrics (latency, event rate, error counts).
   - Add health checks (`src/<service>/healthcheck.py`) and tests to guard against regressions.

6. **Testing**
   - Unit tests for decode/post-process logic (`tests/test_<use-case>_decoder.py`).
   - Tracker/association tests if applicable.
   - Smoke tests for ingest/export paths (similar to `tests/test_event_bus.py`, `tests/test_healthcheck.py`).

Iterate on one detector at a time, keeping `docs/IMPLEMENTATION_STATUS.md` and the relevant `models/<use-case>/TODO.md` up to date so future contributors know exactly what remains.
