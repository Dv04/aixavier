# Placeholders Inventory

_Current unresolved placeholders: 40 (see table below)._ The detector services now read engines/ONNX files from `models/usecases/` and `models/*/onnx/`; populate those paths and update this index as new model-specific secrets are introduced.

<!-- auto:start name=placeholder-index -->
| Placeholder | File path(s) | Purpose | Required format / regex | Example | Security level | Who provides | When required | Default | Resolution status | Last updated |
|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| {{CAMERA_ONVIF_HOST_01}} | .env.example<br>configs/cameras.yaml | ONVIF host/IP | `^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$` | 10.0.0.10 | secret | Video team | run | none | unresolved | 2025-10-07 |
| {{CAMERA_ONVIF_PASS}} | .env.example<br>configs/cameras.yaml<br>docs/TROUBLESHOOT.md | ONVIF password | `^.{8,}$` | ******** | secret | Video team | run | none | unresolved | 2025-10-07 |
| {{CAMERA_ONVIF_USER}} | .env.example<br>configs/cameras.yaml<br>docs/TROUBLESHOOT.md | ONVIF username | `^[A-Za-z0-9_]+$` | cameraadmin | secret | Video team | run | none | unresolved | 2025-10-07 |
| {{CAMERA_RTSP_URL_01}} | .env.example<br>configs/cameras.yaml | Primary RTSP stream URL | `^rtsp://.+$` | rtsp://10.0.0.10/stream1 | secret | Video team | run | none | unresolved | 2025-10-07 |
| {{DATASET_PATH_FACE_CALIB}} | .env.example<br>models/face/calibrate.sh | Face calibration dataset | `^/.+` | /data/datasets/face_calib | internal | ML | bootstrap | none | unresolved | 2025-10-07 |
| {{DATASET_PATH_FIRE_SMOKE}} | .env.example | Calibration dataset directory | `^/.+` | /data/datasets/fire | internal | ML | bootstrap | none | unresolved | 2025-10-07 |
| {{DATASET_PATH_OBJECT_CALIB}} | .env.example<br>models/yolo/calibrate.sh | Object calibration dataset | `^/.+` | /data/datasets/object_calib | internal | ML | bootstrap | none | unresolved | 2025-10-07 |
| {{DATASET_PATH_POSE_CALIB}} | .env.example<br>models/pose/calibrate.sh | Pose calibration dataset | `^/.+` | /data/datasets/pose_calib | internal | ML | bootstrap | none | unresolved | 2025-10-07 |
| {{DATASET_PATH_REID_CALIB}} | .env.example<br>models/reid/calibrate.sh | ReID calibration dataset | `^/.+` | /data/datasets/reid_calib | internal | ML | bootstrap | none | unresolved | 2025-10-07 |
| {{DATASET_PATH_VIOLENCE}} | .env.example<br>models/actions/calibrate.sh | Violence dataset path | `^/.+` | /data/datasets/violence | internal | ML | bootstrap | none | unresolved | 2025-10-07 |
| {{EVENTS_REST_ENDPOINT}} | .env.example<br>configs/usecases/camera_tampering.yaml<br>configs/usecases/coach_door_panel_security.yaml<br>configs/usecases/face_recognition.yaml<br>configs/usecases/human_aggression_violence.yaml<br>configs/usecases/people_counting_occupancy.yaml<br>configs/usecases/smoke_fire_haze.yaml<br>configs/usecases/trespassing_on_track.yaml<br>docs/PRIVACY.md | REST target for events | `^https://.+$` | https://event-bus/api | secret | Platform | run | none | unresolved | 2025-10-07 |
| {{FRS_BLACKLIST_EMBEDDING_01}} | configs/frs/blacklist.yaml | Base64 embedding | `^[A-Za-z0-9+/=]+$` | QVNEMTI= | secret | Security | run | none | unresolved | 2025-10-07 |
| {{FRS_BLACKLIST_NAME_01}} | configs/frs/blacklist.yaml | Blacklisted identity name | `^[A-Za-z ]+$` | Suspicious Person | secret | Security | run | none | unresolved | 2025-10-07 |
| {{FRS_BLACKLIST_REASON_01}} | configs/frs/blacklist.yaml | Reason text | `^.{5,}$` | Trespass history | internal | Security | run | none | unresolved | 2025-10-07 |
| {{FRS_ENROLLMENT_OPERATOR_NAME}} | .env.example | Operator attribution for enrollment | `^[A-Za-z ]+$` | Priya Sharma | secret | Security | run | none | unresolved | 2025-10-07 |
| {{FRS_STAFF_EMBEDDING_01}} | configs/frs/staff_whitelist.yaml | Staff embedding | `^[A-Za-z0-9+/=]+$` | QlJEUw== | secret | HR | run | none | unresolved | 2025-10-07 |
| {{FRS_STAFF_EMPLOYEE_ID_01}} | configs/frs/staff_whitelist.yaml | Employee ID | `^[A-Z0-9_-]+$` | AG1234 | internal | HR | run | none | unresolved | 2025-10-07 |
| {{FRS_STAFF_NAME_01}} | configs/frs/staff_whitelist.yaml | Staff name | `^[A-Za-z ]+$` | Anita Singh | public | HR | run | none | unresolved | 2025-10-07 |
| {{FRS_THRESHOLD}} | .env.example<br>configs/frs/config.yaml<br>configs/usecases/face_recognition.yaml | FRS similarity threshold | `^0\.[0-9]{2}$` | 0.47 | public | Security | run | 0.47 | unresolved | 2025-10-07 |
| {{FRS_WHITELIST_EMBEDDING_01}} | configs/frs/whitelist.yaml<br>src/runners/main.py | Base64 face embedding | `^[A-Za-z0-9+/=]+$` | QkNEMTA= | secret | Security | run | none | unresolved | 2025-10-07 |
| {{FRS_WHITELIST_EXPIRY_01}} | configs/frs/whitelist.yaml | Expiry date | `^20[0-9]{2}-[0-9]{2}-[0-9]{2}$` | 2025-12-31 | public | Security | run | 2099-12-31 | unresolved | 2025-10-07 |
| {{FRS_WHITELIST_NAME_01}} | configs/frs/whitelist.yaml | Whitelisted identity name | `^[A-Za-z ]+$` | Ravi Kumar | secret | Security | run | none | unresolved | 2025-10-07 |
| {{GIT_REMOTE_URL}} | .env.example<br>docs/SETUP.md | Git remote for cloning | `^https://.+\.git$` | https://github.com/example/edge-cctv-jetson.git | public | DevOps | setup | existing remote | unresolved | 2025-10-07 |
| {{INSTALL_PREFIX}} | .env.example<br>deploy/systemd/detect.service<br>deploy/systemd/ingest.service<br>deploy/systemd/ui.service | Install location for systemd units | `^/.+` | /opt | internal | Ops | prod | /opt | unresolved | 2025-10-07 |
| {{METRICS_PUSH_URL}} | .env.example | Optional pushgateway URL | `^https?://.+$` | https://metrics-gw/push | internal | Platform | optional | none | unresolved | 2025-10-07 |
| {{MQTT_BROKER_HOST}} | .env.example<br>docs/TROUBLESHOOT.md | Broker hostname for CLI tools | `^[A-Za-z0-9_.-]+$` | 10.0.0.20 | secret | Platform | setup | none | unresolved | 2025-10-07 |
| {{MQTT_BROKER_PASS}} | .env.example | MQTT auth password | `^.{12,}$` | ******** | secret | Platform | setup | none | unresolved | 2025-10-07 |
| {{MQTT_BROKER_URL}} | .env.example<br>configs/usecases/calling_out_signal_aspect.yaml<br>configs/usecases/camera_tampering.yaml<br>configs/usecases/child_safety_monitoring.yaml<br>configs/usecases/cleaning_hygiene_monitoring.yaml<br>configs/usecases/coach_door_panel_security.yaml<br>configs/usecases/emergency_brake_valve_spad.yaml<br>configs/usecases/face_recognition.yaml<br>configs/usecases/hand_gesture_signal_identification.yaml<br>configs/usecases/human_aggression_violence.yaml<br>configs/usecases/medical_emergency_collapse.yaml<br>configs/usecases/mobile_phone_usage_detection.yaml<br>configs/usecases/object_identification_classification.yaml<br>configs/usecases/on_demand_viewing.yaml<br>configs/usecases/panic_alarm_validation.yaml<br>configs/usecases/passenger_falling_from_door.yaml<br>configs/usecases/people_counting_occupancy.yaml<br>configs/usecases/smoke_fire_haze.yaml<br>configs/usecases/staff_movement_tracking.yaml<br>configs/usecases/stone_pelting.yaml<br>configs/usecases/trespassing_on_track.yaml<br>configs/usecases/unattended_baggage.yaml<br>configs/usecases/vandalism_detection.yaml<br>docs/PRIVACY.md | MQTT broker URI | `^mqtts?://.+$` | mqtts://10.0.0.20:8883 | secret | Platform | setup | none | unresolved | 2025-10-07 |
| {{MQTT_BROKER_USER}} | .env.example | MQTT auth username | `^[A-Za-z0-9_\-]+$` | edgeops | secret | Platform | setup | none | unresolved | 2025-10-07 |
| {{ORG_NAME}} | .env.example<br>README.md | Organization identifier for branding | `^[A-Z0-9_\-]+$` | METRO_RAIL_CORP | public | Ops | setup | none | unresolved | 2025-10-07 |
| {{PROMETHEUS_SCRAPE_PORT}} | .env.example<br>README.md | Exporter port | `^[0-9]{4,5}$` | 9100 | public | Platform | run | 9100 | unresolved | 2025-10-07 |
| {{RETENTION_DAYS}} | .env.example<br>configs/cameras.yaml<br>docs/PERFORMANCE.md<br>docs/PRIVACY.md | Clip retention policy | `^[0-9]+$` | 30 | public | Ops | prod | 7 | unresolved | 2025-10-07 |
| {{SEC_EXPORT_ENCRYPTION_KEY}} | .env.example<br>docs/PRIVACY.md | Encryption key for exports | `^[A-F0-9]{64}$` | DEADBEEF... | secret | Security | prod | none | unresolved | 2025-10-07 |
| {{STORAGE_CLIPS_PATH}} | .env.example<br>configs/cameras.yaml<br>docs/SETUP.md | Clip storage mount | `^/.+` | /media/ssd/clips | internal | Ops | setup | /var/lib/edge-cctv/clips | unresolved | 2025-10-07 |
| {{STORAGE_EXPORT_PATH}} | .env.example<br>configs/cameras.yaml | Export directory | `^/.+` | /media/ssd/exports | internal | Ops | setup | /var/lib/edge-cctv/exports | unresolved | 2025-10-07 |
| {{TIME_SYNC_SOURCE}} | .env.example<br>deploy/flash-checklist.md<br>docs/SETUP.md | Time synchronization authority | `^.+$` | PTP-GRANDMASTER-01 | public | Ops | setup | GPS | unresolved | 2025-10-07 |
| {{UI_ADMIN_PASS}} | .env.example<br>docs/PRIVACY.md | Admin password | `^.{12,}$` | ******** | secret | Security | run | none | unresolved | 2025-10-07 |
| {{UI_ADMIN_USER}} | .env.example<br>docs/PRIVACY.md | Admin username | `^[A-Za-z0-9_.-]+$` | admin | secret | Security | run | none | unresolved | 2025-10-07 |
| {{UI_HOST}} | .env.example<br>docs/PRIVACY.md | TODO - document | .+ | - | public | TODO | setup | none | unknown | 2025-10-07 |
| {{UI_PORT}} | .env.example | Dashboard port | `^[0-9]{2,5}$` | 8443 | public | Ops | run | 8080 | unresolved | 2025-10-07 |
<!-- auto:end -->
