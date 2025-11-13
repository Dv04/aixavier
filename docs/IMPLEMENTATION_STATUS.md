# Implementation Status – 2025-10-31

This document summarises the current state of the Aixavier Edge Analytics stack so a new engineer (human or assistant) can resume work without digging through code history.

**Status:** Demo-ready for 8 workloads; production requires real models, secrets, and CI hygiene. See [`docs/next_steps.md`](docs/next_steps.md) for prioritized roadmap and [`docs/placeholders.md`](docs/placeholders.md) for live placeholder status. For onboarding, see the [README](../README.md).

## Services Overview

| Service                     | Code Path                                                       | Status           | Notes                                                                                                                          |
| --------------------------- | --------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| ingest                      | `src/ingest_gst/`                                               | Demo-ready       | Synthetic + RTSP + `webcam://` capture (needs on-device validation).                                                           |
| detect_object               | `src/runners/` (config: `configs/detectors/object.yaml`)        | ONNX/TRT-capable | Uses shared runner with ONNX fallback and SimpleTracker IDs; requires production engines.                                      |
| detect_pose                 | `src/runners/` (config: `configs/detectors/pose_velocity.yaml`) | ONNX/TRT-capable | Pose events aligned with object tracks via cached detections; needs real models.                                               |
| detect_face / detect_action | `src/runners/`                                                  | Simulated        | Still emit synthetic events; promote to real inference later.                                                                  |
| tracker                     | `src/trackers/`                                                 | ByteTrack-lite   | ByteTrack-style matcher with Simple fallback; ReID still pending.                                                              |
| rules                       | `src/rules/engine.py`                                           | Demo-ready       | Dwell logic fixed; other rule types awaiting real data.                                                                        |
| recorder                    | `src/recorder/`                                                 | Stub             | Writes JSON; replace with video circular buffer.                                                                               |
| privacy                     | `src/privacy/`                                                  | Stub             | Enrollment + embeddings need hardened store/RBAC.                                                                              |
| exporter                    | `src/exporter/`                                                 | Stub             | Emits simulated metrics; wire to real telemetry.                                                                               |
| ui                          | `src/ui/`                                                       | Basic            | FastAPI endpoints + Streamlit; requires full dashboard build-out.                                                              |
| ui                          | `src/aixavier/ui/`                                              | Basic            | FastAPI endpoints for ROI editor, event browser, and toggles. See module README for API details. Frontend integration planned. |

## Use Case Catalog (22 total)

Use-case metadata is tracked centrally in `assets/usecases/catalog.yaml` (auto-parsed from `All Data Analytics use cases for CCTV under POC.xlsx`) and wired into `src/aixavier/core/usecases.py`. The registry surfaces every workload, their applicability, and now feeds the rule engine + docs in a single place.

### Stage Tracker

| #   | Use Case                                                                                                                   | Stage      | Notes                                                                                                   |
| --- | -------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------- |
| 1   | Trespassing on Railway Track                                                                                               | demo-ready | Uses object detector + ByteTrack in demo profile.                                                       |
| 2   | Stone pelting                                                                                                              | simulated  | Needs action detector + projectile heuristics; current runner emits synthetic action events.            |
| 3   | Camera tampering                                                                                                           | demo-ready | Blur/scene-change rules active via tamper detector.                                                     |
| 4   | People Counting & Occupancy in Locomotives                                                                                 | demo-ready | Object detector + tracker cover threshold counts; needs calibration for real density.                   |
| 5   | Smoke/Fire detection &  Haze / reduction in visibility detection                                                           | demo-ready | Object detector with placeholder smoke config; requires real fire/haze models.                          |
| 6   | Object Identification and classify                                                                                         | planned    | Requires banned-object classifier + rulepack tuning.                                                    |
| 7   | Securing of Coach Doors and the electrical panels in the doorway area.                                                     | planned    | Needs door state/geo-fencing inputs; no telemetry ingestion yet.                                        |
| 8   | Medical emergency detection in Circulation Area                                                                            | demo-ready | Pose detector + velocity drop heuristics wired in demo profile.                                         |
| 9   | Railway Staff Movement (Security Patrol and maintenance staff including coach attendants) Detection during train operation | planned    | Depends on ReID embeddings + tracker persistence (OSNet not wired).                                     |
| 10  | On demand viewing of cameras                                                                                               | planned    | UI/exporter need live switching & secure proxy; only basic API exists.                                  |
| 11  | Unattended baggage detection in circulation area                                                                           | demo-ready | Object dwell rule active; tune timers for real scenes.                                                  |
| 12  | Human aggression or violence detection                                                                                     | simulated  | Action detector simulated; X3D/MobileNet engines not integrated.                                        |
| 13  | Passenger falling from door in moving train                                                                                | planned    | Needs pose + action fusion with GPS speed gate; not wired.                                              |
| 14  | Face Recognition                                                                                                           | partial    | SCRFD/ArcFace pipeline stubbed; privacy service stores encrypted embeddings but matching logic limited. |
| 15  | Cleaning & hygiene monitoring in Circulation Area                                                                          | planned    | Requires change-detection model + ROI config; not implemented.                                          |
| 16  | Child safety monitoring                                                                                                    | planned    | Needs child-specific tracker/dwell logic + guardian detection.                                          |
| 17  | Vandalism detection                                                                                                        | planned    | Needs change/action detectors + ROI masks; not implemented.                                             |
| 18  | Validation of Panic alarm                                                                                                  | planned    | Requires telemetry ingestion + camera correlation; not implemented.                                     |
| 19  | Calling (voice) out signal aspect                                                                                          | planned    | Audio ingestion + ASR classifier missing.                                                               |
| 20  | Hand gesture (for identification of signal)                                                                                | simulated  | Pose runner exists but gesture classifier not trained; rulepack placeholder.                            |
| 21  | Emergency Brake Valve (RS value) operation during SPAD                                                                     | planned    | Needs telemetry + object recognition on cab cameras; not implemented.                                   |
| 22  | Mobile Phone Usage detection                                                                                               | simulated  | Pose/gesture logic missing; action runner simulated.                                                    |

**Snapshot:** 8/22 use cases produce demo events today, 5 rely on simulated detectors, and 9 remain in planning/backlog. Use `UseCaseRegistry().summary()` to pull this table programmatically during CI/tests.

### Applicability / Detector View

| #   | Use Case                                                               | Applicability   | Deployment               | Maturity   | Detectors           |
| --- | ---------------------------------------------------------------------- | --------------- | ------------------------ | ---------- | ------------------- |
| 1   | Trespassing on Railway Track                                           | Loco            | Post Incident Need Based | demo-ready | object, tracker     |
| 2   | Stone pelting                                                          | Loco            | Post Incident Need Based | planned    | object, action      |
| 3   | Camera tampering                                                       | All             | Real Time.               | demo-ready | integrity           |
| 4   | People Counting & Occupancy in Locomotives                             | All             | Real Time.               | demo-ready | object, tracker     |
| 5   | Smoke/Fire detection &  Haze / reduction in visibility detection       | All             | Real Time.               | demo-ready | environment, object |
| 6   | Object Identification and classify                                     | Coach and Locos | Real time.               | planned    | object              |
| 7   | Securing of Coach Doors and the electrical panels in the doorway area. | Coach           | Real time.               | planned    | object, telemetry   |
| 8   | Medical emergency detection in Circulation Area                        | Coach           | Real time.               | demo-ready | pose                |
| 9   | Railway Staff Movement ...                                             | Coach           | Real time.               | planned    | reid, tracker       |
| 10  | On demand viewing of cameras                                           | All             | Both                     | planned    | observability       |
| 11  | Unattended baggage detection in circulation area                       | Coach           | Both                     | demo-ready | object, dwell       |
| 12  | Human aggression or violence detection                                 | All             | Both                     | planned    | action              |
| 13  | Passenger falling from door in moving train                            | All             | Real time.               | planned    | pose, action        |
| 14  | Face Recognition                                                       | All             | Both                     | partial    | frs                 |
| 15  | Cleaning & hygiene monitoring in Circulation Area                      | Coach           | Both                     | planned    | object, change      |
| 16  | Child safety monitoring                                                | Coach           | Both                     | planned    | tracker, dwell      |
| 17  | Vandalism detection                                                    | Coach and Locos | Both                     | planned    | object, action      |
| 18  | Validation of Panic alarm                                              | Coach           | Real time.               | planned    | telemetry, object   |
| 19  | Calling (voice) out signal aspect                                      | Loco            | Both                     | planned    | audio               |
| 20  | Hand gesture (for identification of signal)                            | Loco            | Both                     | planned    | pose, action        |
| 21  | Emergency Brake Value ... SPAD                                         | Loco            | Both                     | planned    | object, telemetry   |
| 22  | Mobile Phone Usage detection                                           | Loco            | Both                     | planned    | pose, action        |

## Models & Assets

- Place ONNX exports under modality folders (`models/object/onnx`, `models/pose/onnx/rtmpose_onnx`, `models/action/onnx`, etc.); promote TensorRT engines into `models/usecases/<use-case>/fp16|int8/` only when they are production-ready.
- Stage production TensorRT engines under `models/usecases/<use-case>/fp16/` (INT8 later).
- `models/pose/TODO.md` and `models/object/TODO.md` track outstanding work for the two active use cases.
- Calibration datasets should live under `models/<modality>/calib/`.
- `configs/detectors/pose_velocity.yaml` now embeds a `person_detector` block (yolov11n by default) so RTMPose runs in a top-down, multi-person configuration—each detected person is cropped before pose inference.

### Model Group Strategy

Group shared models by analytic modality, keep raw ONNX/checkpoints beneath `models/<group>/`, and reserve `models/usecases/<slug>/` for deployable engines + INFO.md metadata. Recommended groups (covering both existing + future workloads):

| Group                       | Folder                                               | Use cases served            | Notes                                                                                                                                                           |
| --------------------------- | ---------------------------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Object detection / tracking | `models/object/...` (ONNX) + shared tracker configs  | 1,4,5,6,7,11,15,16,17,18,21 | Backed by yolov11/YOLOv10 exports; tracker tuned via `configs/tracker.yaml`.                                                                                    |
| Pose & velocity             | `models/pose/onnx/rtmpose_onnx/...`                  | 8,13,20,22                  | RTMPose ONNX feeds TRT engines under `models/usecases/pose/`; multi-person crops come from the shared YOLO person detector (`models/object/onnx/yolo11n.onnx`). |
| Action / clip analytics     | `models/action/onnx/...`                             | 2,12,13,17,20,22            | Hosts X3D-S, MobileNet-TSM, gesture classifiers. Current services still simulated—wire TRT engines + calibration here.                                          |
| Face / ReID                 | `models/face/...`, `models/reid/...`                 | 9,14                        | SCRFD + ArcFace + OSNet_x0_25 assets live here; upgrade once production engines ready.                                                                          |
| Audio / ASR                 | `models/audio/...`                                   | 19                          | Placeholder for future speech-recognition weights used in calling-out-signal-aspect detection.                                                                  |
| Telemetry fusion helpers    | `models/telemetry/...` (placeholder configs/scripts) | 7,18,21                     | Holds ML models or rule scripts that combine vision with door/RS telemetry; currently empty but documented for future work.                                     |

Nothing needs to be deleted: keep the modality folders (`models/object`, `models/pose`, `models/action`, `models/face`, `models/reid`, etc.) and gradually migrate ONNX exports into them. Only place fully vetted TensorRT engines (and their checksums/INFO.md) into `models/usecases/<slug>/`. This keeps the repo lightweight while still exposing a predictable locker for deployment artifacts.

## Tracking & Pose Association

- `SimpleTracker` assigns persistent IDs per camera and caches the latest object detections under `artifacts/detections/cache/<camera>.json`.
- Pose detections reuse cached `person` boxes for track association; accuracy will improve once ByteTrack + ReID is added.

## Tests & CI Gating

- `pytest` suite covers rule engine, tracker, and (optionally) detector post-processing. Set `AIXAVIER_ENABLE_NUMPY_TESTS=1` when NumPy is available to enable ONNX layout tests.
- Add integration tests once real models are staged.
- **Placeholder hygiene is enforced in CI:**
	- The placeholder linter (`tools/placeholder_lint.py`) and smoke test (`tests/test_placeholders_smoke.py`) ensure all secrets and placeholders are either resolved or documented in [`docs/placeholders.md`](docs/placeholders.md).
	- The linter ignores `.venv/`, `site-packages`, and other non-project paths for reliability.
	- CI will fail if unresolved placeholders or undocumented secrets are found.

## Outstanding Work (High Level)

1. Replace simulated face/action detectors with real inference pipelines.
2. Integrate ByteTrack + OSNet ReID for production-grade tracking.
3. Deploy recorder (video), exporter (metrics), privacy (embeddings) with real functionality.
4. Resolve all placeholders via `.env` and the placeholder resolver before production builds.
5. Harden docs/CI: run detector integration tests and enforce placeholder gate in `agent-ci` workflow.
6. INT8 calibration for detectors (object + pose) once datasets are ready.

Refer to `docs/next_steps.md` for the detailed roadmap and `HANDOFF.md` for chronological change logs.
