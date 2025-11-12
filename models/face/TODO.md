# TODO: Face Detection & ReID Integration – November 2025

This file tracks all missing components and integration points required to move the face detection and person re-identification (ReID) pipeline from stub/demo to production-ready.

---
## Task Division

### Agent Tasks (Automatable by Copilot)
- Update detector configs (`configs/detectors/face.yaml`) with real model paths and runtime parameters (once provided).
- Update use case configs (`configs/usecases/face_recognition.yaml`) for thresholds and event triggers.
- Extend `src/runners/detectors.py` to load and run face detection and recognition models (ONNX/TRT).
- Integrate ReID model inference into the tracker pipeline.
- Implement encrypted embedding store in `src/privacy/store.py`.
- Wire FastAPI endpoints for enrollment, match, whitelist, and blacklist.
- Enforce RBAC and per-camera privacy settings.
- Extend `src/rules/engine.py` for advanced face recognition rules (similarity, dwell, event triggers).
- Add unit/integration tests for face detection, recognition, and ReID.
- Validate output normalization, accuracy, and performance (with provided models/data).
- Add CI checks for model presence and runtime health.
- Update docs with progress and integration notes.
- Ensure all secrets and placeholders are resolved/documented.

### User/Owner Tasks (Require Your Intervention)
- Export ONNX models for face detection (SCRFD) and face recognition (ArcFace) and provide them in `models/face/onnx/`.
- Export ONNX models for ReID (OSNet) and provide them in `models/reid/onnx/`.
- Convert ONNX models to TensorRT engines for deployment and place in `models/usecases/face_recognition/` and `models/usecases/reid/`.
- Document model input/output formats and calibration requirements (if not standard).
- Populate FRS configs (`configs/frs/`) with real embeddings, names, and threshold values.
- Validate model loading and inference on Jetson Xavier (hardware access required).
- Provide real test data for accuracy/performance validation.

---

## Implementation Outline

### 1. Model Preparation
- Export ONNX models for face detection (SCRFD) and face recognition (ArcFace).
- Export ONNX models for ReID (OSNet).
- Convert ONNX models to TensorRT engines for deployment.
- Document model input/output formats and calibration requirements.

### 2. Configuration & Wiring
- Update detector configs (`configs/detectors/face.yaml`) with real model paths and runtime parameters.
- Update use case configs (`configs/usecases/face_recognition.yaml`) for thresholds and event triggers.
- Ensure FRS configs (`configs/frs/`) have real embeddings and names.

### 3. Runtime Integration
- Extend `src/runners/detectors.py` to load and run face detection and recognition models (ONNX/TRT).
- Integrate ReID model inference into the tracker pipeline.
- Validate model loading and inference on Jetson Xavier.

### 4. Privacy & FRS Logic
- Implement encrypted embedding store in `src/privacy/store.py`.
- Wire FastAPI endpoints for enrollment, match, whitelist, and blacklist.
- Enforce RBAC and per-camera privacy settings.

### 5. Rule Engine & Event Handling
- Extend `src/rules/engine.py` for advanced face recognition rules (similarity, dwell, event triggers).
- Validate rulepack YAMLs against real events.

### 6. Testing & Validation
- Add unit/integration tests for face detection, recognition, and ReID.
- Validate output normalization, accuracy, and performance.
- Add CI checks for model presence and runtime health.

### 7. Documentation & Hygiene
- Update docs with progress and integration notes.
- Ensure all secrets and placeholders are resolved/documented.

---

## 1. Model Integration
- [ ] Export and stage ONNX models for face detection (e.g., SCRFD) and face recognition (e.g., ArcFace) in `models/face/onnx/`.
- [ ] Export and stage ONNX models for ReID (e.g., OSNet) in `models/reid/onnx/`.
- [ ] Convert ONNX models to TensorRT engines and place in `models/usecases/face_recognition/` and `models/usecases/reid/`.
- [ ] Document model input/output formats and calibration requirements.

## 2. Runtime Wiring
- [ ] Update `configs/detectors/face.yaml` to reference real model paths, thresholds, and runtime parameters.
- [ ] Update `src/runners/detectors.py` to load and run face detection and recognition models (ONNX/TRT).
- [ ] Integrate ReID model loading and inference into the tracker pipeline.
- [ ] Validate model loading and inference on target hardware (Jetson Xavier).

## 3. Privacy & FRS Logic
- [ ] Implement encrypted embedding store in `src/privacy/store.py`.
- [ ] Wire FastAPI endpoints for enrollment, match, whitelist, and blacklist in `src/privacy/`.
- [ ] Enforce RBAC and per-camera privacy settings (blur non-matches, approval for exports).
- [ ] Populate `configs/frs/` with real embeddings, names, and threshold values.

## 4. Rule Engine & Use Case
- [ ] Extend `src/rules/engine.py` to support advanced face recognition rules (similarity, dwell, event triggers).
- [ ] Validate rulepack YAMLs in `configs/usecases/face_recognition.yaml` against real events.

## 5. Testing & Validation
- [ ] Add unit and integration tests for face detection, recognition, and ReID in `tests/test_detectors.py` and new test modules.
- [ ] Validate output normalization, accuracy, and performance.
- [ ] Add CI checks for model presence and runtime health.

## 6. Documentation & Hygiene
- [ ] Update `docs/IMPLEMENTATION_STATUS.md` and `docs/next_steps.md` with progress and integration notes.
- [ ] Ensure all secrets and placeholders are resolved/documented in `docs/placeholders.md`.

---
_Last updated: 2025-11-11_
