# Status & Roadmap
_Date: 2025-11-20_

## TL;DR
- Demo-ready for 8/22 use cases; face/action still simulated; secrets unresolved (40 placeholders).
- Day-0 demo heuristics for UC8/20/22 ride on object+pose runners (see Demo Heuristics below).
- Use-case registry lives at `assets/usecases/catalog.yaml` via `src/aixavier/core/usecases.py`.

## Services at a Glance
| Service | Path | Status | Notes |
| --- | --- | --- | --- |
| ingest | src/ingest_gst/ | Demo-ready | Synthetic/RTSP/webcam; needs on-device validation |
| detect_object | src/runners/ (configs/detectors/object.yaml) | ONNX/TRT-capable | Needs production engines |
| detect_pose | src/runners/ (configs/detectors/pose_velocity.yaml) | ONNX/TRT-capable | Multi-person top-down; needs real models |
| detect_face / detect_action | src/runners/ | Simulated | Replace with real inference |
| tracker | src/trackers/ | ByteTrack-lite | ReID pending |
| rules | src/rules/engine.py | Demo-ready | Expand handlers/tests |
| recorder | src/recorder/ | Stub | Replace with video circular buffer |
| privacy | src/privacy/ | Stub | Harden embeddings/RBAC |
| exporter | src/exporter/ | Stub | Simulated metrics |
| ui | src/aixavier/ui/ | Basic | FastAPI ROI/events/toggles |

## Demo Heuristics (UC8, UC20, UC22)
- Collapse velocity, gesture placeholders, and phone-usage heuristics are for demos only.
- Offline synthetic loop:
  ```bash
  export AIX_ARTIFACTS=./artifacts_demo
  python src/apps/demo_runner.py
  # watch events in $AIX_ARTIFACTS/events.jsonl
  ```

## Placeholder & Secrets Snapshot
- Distinct placeholders: ~40. Run `make placeholders:list` and `make placeholders:check`.
- Live inventory: `docs/placeholders.md`.

## Use-Case Stage Tracker (22)
| # | Use Case | Stage | Notes |
| -- | --- | --- | --- |
|1|Trespassing on Railway Track|demo-ready|Object detector + tracker demo profile|
|2|Stone pelting|simulated|Needs action detector + projectile heuristics|
|3|Camera tampering|demo-ready|Blur/scene-change rules active|
|4|People Counting & Occupancy|demo-ready|Object detector + tracker|
|5|Smoke/Fire & Haze|demo-ready|Placeholder smoke config; needs real models|
|6|Object identification/classify|planned|Needs banned-object classifier|
|7|Securing coach doors/panels|planned|Needs telemetry + ROI|
|8|Medical emergency (collapse)|demo-ready|Pose velocity heuristic|
|9|Staff movement (patrol)|planned|Needs ReID embeddings|
|10|On-demand viewing|planned|UI/exporter switching|
|11|Unattended baggage|demo-ready|Object dwell rule|
|12|Aggression/violence|simulated|Action detector simulated|
|13|Passenger fall from door|planned|Pose+action+GPS speed gate|
|14|Face recognition|partial|SCRFD/ArcFace stub; matching limited|
|15|Cleaning/hygiene|planned|Change-detection needed|
|16|Child safety|planned|Child-specific tracker/dwell|
|17|Vandalism|planned|Change/action detectors|
|18|Panic alarm validation|planned|Telemetry ingestion|
|19|Calling out signal aspect|planned|Audio/ASR missing|
|20|Hand gesture identification|simulated|Pose runner; heuristic labels only|
|21|Emergency brake valve SPAD|planned|Telemetry + object|
|22|Mobile phone usage|simulated|Heuristic phone-use events only|

## Applicability / Detector View
| # | Use Case | Applicability | Deployment | Maturity | Detectors |
| -- | --- | --- | --- | --- | --- |
|1|Trespassing on Railway Track|Loco|Post Incident|demo-ready|object, tracker|
|2|Stone pelting|Loco|Post Incident|planned|object, action|
|3|Camera tampering|All|Real Time|demo-ready|integrity|
|4|People Counting & Occupancy|All|Real Time|demo-ready|object, tracker|
|5|Smoke/Fire & Haze|All|Real Time|demo-ready|environment, object|
|6|Object identification/classify|Coach/Loco|Real Time|planned|object|
|7|Coach doors/panels|Coach|Real Time|planned|object, telemetry|
|8|Medical emergency|Coach|Real Time|demo-ready|pose|
|9|Staff movement|Coach|Real Time|planned|reid, tracker|
|10|On-demand viewing|All|Both|planned|observability|
|11|Unattended baggage|Coach|Both|demo-ready|object, dwell|
|12|Aggression/violence|All|Both|planned|action|
|13|Passenger fall|All|Real Time|planned|pose, action|
|14|Face Recognition|All|Both|partial|frs|
|15|Cleaning/hygiene|Coach|Both|planned|object, change|
|16|Child safety|Coach|Both|planned|tracker, dwell|
|17|Vandalism|Coach/Loco|Both|planned|object, action|
|18|Panic alarm validation|Coach|Real Time|planned|telemetry, object|
|19|Calling signal aspect|Loco|Both|planned|audio|
|20|Hand gesture|Loco|Both|planned|pose, action|
|21|Emergency brake SPAD|Loco|Both|planned|object, telemetry|
|22|Mobile phone usage|Loco|Both|planned|pose, action|

## Outstanding Work (P0)
1) Replace simulated face/action with real ONNX/TRT pipelines; stage engines under `models/usecases/*`.
2) Validate RTSP/ONVIF ingest on device; confirm camera configs.
3) Add ReID (OSNet) into tracker and validate long-term IDs.
4) Expand rule handlers and tests; validate rulepacks.
5) Implement video recorder, real exporter metrics, hardened privacy store/RBAC.
6) Resolve placeholders via `.env` + resolver before production.

## Legacy Context
- Project codename “Project Dhi” (hardware-agnostic brand) retained in `docs/summary.md`.
- Streamlit/FastAPI prototype that read events/placeholders was non-unique; no runtime code lost.

> Replaces `docs/next_steps.md` and `docs/IMPLEMENTATION_STATUS.md`.
