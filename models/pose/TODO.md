# Pose & Velocity Delivery Plan (Use Cases 8, 13, 20, 22) — updated 2025-11-20

The pose stack underpins four railway analytics workloads:
- **UC8 – Medical emergency detection (collapse velocity)**
- **UC13 – Passenger falling from door (pose + telemetry)**
- **UC20 – Hand gesture identification (signal compliance)**
- **UC22 – Mobile phone usage detection (driver distraction)**

This document is the single source of truth for their current maturity, the remaining work, and the concrete implementation plan. Treat it like a runbook: every dependency, artifact, and validation step must be checked off before the use cases move from “planned/simulated” to “demo-ready/production”.

---

## 1. Implementation Pipeline (current status per use case)

| Use Case | Stage | Current pipeline snapshot |
|----------|-------|---------------------------|
| **8 – Medical emergency detection** | Simulated (demo-ready only for basic velocity drop) | RTMPose-based detector emits keypoints + a heuristic “velocity_drop” metric (derivative of hip/knee displacement) in `src/runners/main.py`. Rule engine (`configs/usecases/medical_emergency_collapse.yaml`) simply thresholds that value. No dedicated classifier, no TRT engine beyond generic RTMPose, no labeled collapse dataset, and no validation on real collapse clips. Latency/telemetry metrics are logged but not verified. |
| **13 – Passenger falling from door** | Planned | Config exists, but the runtime lacks the telemetry join (train speed, door open state) and fall classifier. Pose runner does not compute out-of-car trajectory, and there is no GPS-aware gating. Use case remains a placeholder in rules. |
| **20 – Hand gesture identification** | Simulated | Pose keypoints are produced, but no gesture classifier consumes them. `configs/detectors/gesture.yaml` still points to a simulated action engine (X3D proxy). Rulepack only checks for mock gesture labels. No labeled dataset of standardized railway hand signals. |
| **22 – Mobile phone usage detection** | Simulated | Uses the action simulator (`configs/detectors/action.yaml`) to emit fake “violence/fall” scores. No phone-specific detector, no pose-based proximity logic, and rules are placeholders referencing synthetic events. |

Key runtime components already in place and reusable for all four:
- SimCC decoder + RTMPose inference (`src/runners/detectors.py`)
- Tracker/pose association layer (`src/runners/main.py`, `src/runners/pose_assoc.py`)
- Use case registry with metadata (`src/aixavier/core/usecases.py`)
- Event bus + rule engine infrastructure (`src/common/event_bus.py`, `src/rules/engine.py`)

Gaps specific to each use case are detailed in the next sections.

---

## 2. Steps to Complete (detailed requirements per use case)

### UC8 – Medical emergency detection (collapse velocity)
1. **Data acquisition**: Collect annotated clips showing collapses vs normal movement inside coaches; at least several hundred events with diverse lighting. Capture ground truth timestamps and bounding boxes.
2. **Feature engineering**: Define per-track features (velocity magnitude, acceleration drops, torso angle variance, dwell near floor). Instrument `src/runners/main.py` to emit these in debug mode for dataset export.
3. **Model training**: Train a small classifier (LSTM/Temporal CNN/Gradient Boosting) that ingests a sliding window of pose features (Kx3 keypoints + derived metrics). Export ONNX to `models/pose/onnx/collapse_classifier.onnx` and document version.
4. **Runtime integration**: Load the classifier in `src/runners/main.py` after pose detection; produce an `event_type='pose'` payload with `collapse_score` and state enumerations.
5. **Rule calibration**: Update `configs/usecases/medical_emergency_collapse.yaml` with new thresholds (score, minimum dwell) and add tests in `tests/test_rules.py` verifying triggers.
6. **Validation**: Run `make live` and RTSP replays against recorded collapse clips; log precision/recall. Update `docs/IMPLEMENTATION_STATUS.md` once demo-ready.

### UC13 – Passenger falling from door (pose + telemetry)
1. **Telemetry ingestion**: Expose train speed, GPS position, and door-open status via MQTT/REST → ingest in `src/common/config.py` or new `src/telemetry/` helper.
2. **ROI + trajectory logic**: Mark door ROIs per camera in configs. Implement trajectory calculation (vector from pelvis/feet keypoints across consecutive frames) to detect motion outward.
3. **Classifier**: Train a binary model combining pose velocity, door state, and speed (only fire when train speed > threshold). Export ONNX to `models/pose/onnx/fall_classifier.onnx`.
4. **Runtime**: Embed telemetry snapshot into each pose event; call classifier and emit `fall_score`, `door_id`, `train_speed`.
5. **Rules**: Extend `configs/usecases/passenger_falling_from_door.yaml` with combined conditions (score, speed, open door). Add `_handle_fall_detection` to `RuleEngine` + tests.
6. **Field validation**: Re-run with telemetry playback files; confirm false positives are within acceptable bounds.

### UC20 – Hand gesture identification
1. **Dataset**: Record standardized hand signals (stop, proceed, caution, etc.) from staff in realistic environments. Annotate gesture labels per frame sequence.
2. **Model**: Use normalized keypoints (shoulder/elbow/wrist) to train a gesture classifier (e.g., temporal ConvNet). Export ONNX to `models/action/onnx/gesture_classifier.onnx` (or `models/pose/onnx/`).
3. **Runtime**: Add an optional `gesture_classifier_path` to `configs/detectors/pose_velocity.yaml` (or dedicated `gesture` detector). Load ONNX via onnxruntime, infer gesture label per track, and attach to pose payloads.
4. **Rules/Alerts**: Update `configs/usecases/hand_gesture_signal_identification.yaml` to map gestures → severity (e.g., missing “proceed” call-out). Add rule handler `_handle_gesture_score`.
5. **Visualization**: Extend renderer to overlay recognized gesture for debugging.
6. **Testing**: Synthetic unit tests verifying classifier integration + rule triggers.

### UC22 – Mobile phone usage detection
1. **Data**: Capture driver cab footage with/without phone usage (handset at ear, texting, hands-free). Label bounding boxes and pose states.
2. **Detector**: Option A – fine-tune a YOLO variant to detect phones + hands, export ONNX (`models/object/onnx/phone_detector.onnx`). Option B – pose-based classifier that ingests keypoints + phone detection probabilities.
3. **Runtime**: Run the phone detector periodically (share object runner) and associate detections with pose tracks. Compute features such as hand-to-ear distance, head tilt, and phone proximity.
4. **Rules**: Enhance `configs/usecases/mobile_phone_usage_detection.yaml` with thresholds for confidence + dwell, optionally gating by train speed.
5. **Auditing**: Log video snippets for human review to fine-tune thresholds.

Across all four use cases, remember to:
- Promote the trained TRT engines into `models/usecases/<slug>/fp16/` and document them (e.g., `INFO.md`).
- Update `docs/IMPLEMENTATION_STATUS.md` stage tracker once each reaches demo-ready.
- Refresh `HANDOFF.md` with the changes for traceability.

---

## 3. How-To (step-by-step execution guide)

1. **Baseline engine (shared)**
   - Run `python models/bootstrap_models.py --profile demo` to create placeholder files.
   - Replace `models/pose/onnx/.../end2end.onnx` with the real RTMPose export.
   - Convert to TRT: `trtexec --onnx=models/pose/onnx/rtmpose_onnx/.../end2end.onnx --saveEngine=models/usecases/pose/fp16/rtmpose.engine --fp16 --workspace=4096`.
   - Update `configs/detectors/pose_velocity.yaml` → `engine_path: models/usecases/pose/fp16/rtmpose.engine` (already done) and verify via `make live`.

2. **Dataset pipeline**
   - Use `src/apps/live_demo.py --save-frames` to capture synchronized frames + pose JSON for later labeling.
   - Store labeled data under `datasets/pose/collapse`, `datasets/pose/fall`, `datasets/pose/gesture`, `datasets/pose/phone` (external to repo but documented).
   - Record telemetry snapshots (speed, door state) in parallel; align timestamps.

3. **Training & export**
   - Implement training scripts (PyTorch/onnx) per classifier; keep them in a separate private repo or under `models/pose/training/` if needed.
   - Export ONNX with static input shapes; place under `models/pose/onnx/` (collapse/fall) or `models/action/onnx/` (gesture) / `models/object/onnx/` (phone).
   - Convert to TRT (optional but recommended) and drop into `models/usecases/<slug>/fp16/`.
   - Document each export in `INFO.md` (model version, dataset hash, metrics).

4. **Runtime integration**
   - Extend `src/runners/main.py`:
     - Load optional classifier sessions based on new config keys (e.g., `collapse_classifier_path`).
     - Compute derived features (velocity, door proximity) and feed them to classifiers.
     - Attach scores/labels to event payloads (`payload["collapse_score"]`, etc.).
   - Enhance telemetry ingestion (new module or extend ingest runner) to read door/speed metrics and inject into frame metadata.
   - Update `src/rules/engine.py` with handlers for new payload fields.
   - Ensure `FileEventBus` logs include the new fields for debugging.

5. **Configuration & rules**
   - Update relevant YAMLs under `configs/detectors/` and `configs/usecases/` with classifier paths, thresholds, ROI definitions, and telemetry requirements.
   - Document required env vars/placeholders (door sensor topics, telemetry endpoints) in `.env.example` + `docs/placeholders.md`.

6. **Testing**
   - Add unit tests:
     - `tests/test_detectors.py`: simulate classifier outputs to ensure inference paths work.
     - `tests/test_rules.py`: feed sample events with new payload fields and assert rule triggers.
   - Integration smoke tests: `pytest -k pose` with `AIXAVIER_ENABLE_NUMPY_TESTS=1` once numpy is available.

7. **Validation & tuning**
   - Replay annotated datasets through the pipeline (could add a `tools/replay_pose.py`).
   - Measure precision/recall, adjust thresholds, and log results in `docs/IMPLEMENTATION_STATUS.md`.
   - Capture demos (video + screenshots) for documentation.

8. **Deployment readiness**
   - Ensure TRT engines and configs are staged under `models/usecases/<slug>/` with checksums.
  - Update `docs/status.md` to move the four use cases from P0 backlog to “demo-ready”.
   - Append a `HANDOFF.md` entry summarizing the implementation.

Following this plan keeps the pose group aligned with the rest of the repo (absolute imports, UseCaseRegistry metadata, shared telemetry). No further TODO items outside these sections should be needed; update this file whenever scope changes.
