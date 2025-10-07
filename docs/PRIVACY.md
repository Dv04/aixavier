# Privacy & Security

## Face Recognition
- Enabled by default using SCRFD + ArcFace.
- Embeddings stored encrypted (`src/privacy/embeddings_store.py`) using key `{{SEC_EXPORT_ENCRYPTION_KEY}}`.
- RBAC roles defined in `configs/frs/roles.yaml` (viewer, operator, admin).
- Enrollment API requires `FRS_ENROLLMENT_OPERATOR_NAME` and justification; audit logged to `data/audits/frs_audit.log` and HANDOFF.md.

## Access Controls
- UI served via FastAPI + Streamlit behind OAuth proxy (env placeholders `{{UI_ADMIN_USER}}`, `{{UI_ADMIN_PASS}}`).
- JWT tokens short-lived (15 min) and stored HTTP-only cookies.
- CORS locked to `{{UI_HOST}}` domain.

## Data Handling
- Non-matching faces optionally blurred (per camera config) before storage.
- Clips watermarked and hashed; export requires admin role.
- Chain-of-custody manifest generated alongside exported clip JSON.

## Network
- MQTT requires TLS when `{{MQTT_BROKER_URL}}` scheme is `mqtts://`.
- REST endpoints served on `{{EVENTS_REST_ENDPOINT}}`; enable mTLS for remote listeners.
- Drop Linux capabilities in containers; rootfs mounted read-only except volumes.

## Retention & Pruning
- Embedding TTL default 180 days; expired records shredded nightly.
- Recorder retention controlled by `{{RETENTION_DAYS}}`; optional SSD wear leveling guidelines in `docs/PERFORMANCE.md`.

## Auditing
- Every privileged action appends to HANDOFF.md via agent auto-section.
- Placeholder resolver prevents secrets leaking into repo; CI blocks if unresolved secrets in plain text.

