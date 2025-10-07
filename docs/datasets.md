# Datasets

Each use case lists domain-specific and scale/quality datasets. Agent keeps this file current.

<!-- auto:start name=datasets -->
| Use Case | Bucket | Dataset | License | Size | Modality | Indoor/Outdoor | Pros | Cons | Fit | Bias Notes |
|----------|--------|---------|---------|------|---------|----------------|------|------|-----|------------|
| trespassing_on_track | domain | AI City Challenge S06 (Track 2 Rail) | Academic research only (NDA) | ≈1.2 TB video, 1080p | RGB video + annotations | Outdoor rail yards | Contains real trespass events, diverse viewpoints, annotated ROIs | Restricted redistribution; limited night coverage | Strong | Majority North American scenes; sparse representation of rural settings |
| trespassing_on_track | pretrain | UA-DETRAC | CC BY-NC-SA 4.0 | 140k frames @ 960×540 | RGB video | Outdoor urban roads | Dense traffic, weather variation, useful for motion/occlusion pretraining | Vehicle centric, manual rail labels required | Moderate | Heavy focus on vehicular traffic may bias toward road scenarios |
| loitering_platform | domain | CityFlowV2 (AI City S05) | Academic research only (NDA) | 3.5 TB video | RGB video + tracklets | Outdoor transit hubs | Multi-camera re-ID annotations enable persistent ID tracking | Privacy-protected blurred faces reduce identity cues | Strong | Urban US/Asia mix; biased toward commuter rush hours |
| smoke_detection | domain | Fire & Smoke Detection v1 | CC BY 4.0 | 5.3k images | RGB stills | Indoor + Outdoor | Balanced smoke vs fire examples, includes early-stage smoke plumes | Limited industrial rail scenes; requires video augmentation | Strong | Source imagery over-represents wildfire contexts relative to rail depots |
| smoke_detection | synthetic | SmokeSim | MIT | Procedurally generated sequences | RGB video + alpha masks | Indoor | Enables controllable synthetic augmentation of smoke density and airflow | Needs domain randomisation to avoid uncanny valley artefacts | Moderate | Synthetic textures risk biasing model toward simulated lighting |
| violence_detection | domain | Real-Life Violence Situations | CC BY 4.0 | 2k clips @ 480p-720p | RGB video | Indoor + Outdoor | Curated CCTV-style violent/non-violent pairs | Lower resolution, varied compression quality | Strong | Events sourced mostly from public internet; cultural bias toward Western settings |
| violence_detection | supplement | XDV (Violence2D) | Research only | 1.4k clips | RGB video | Indoor + Outdoor | Annotated frame-level violence labels, includes occlusions | License restricts commercial deployment; smaller sample size | Moderate | Actors staged scenarios; may reduce generalisation to real incidents |
| face_recognition | identity | MS1MV3 | Custom (non-commercial) | 5.8M images | RGB stills | Mixed | High-coverage identity dataset aligned with ArcFace training | Licensing constraints require on-prem use only | Strong | Over-represents East Asian faces; supplement with rail staff captures |
| face_detection | pretrain | WiderFace | BSD 3-Clause | 32k images | RGB stills | Mixed | Extreme scale variation, crowd scenes helpful for platforms | No rail-specific context; minimal PPE coverage | Strong | Heavy urban bias; add PPE samples to mitigate false negatives |
| fall_detection | domain | UR Fall Detection | CC BY-NC-ND 4.0 | 70 sequences | RGB + depth | Indoor | Provides depth modality for fall cues; simple to prototype | Older sensors, limited actor diversity, no outdoor data | Moderate | Elderly actors only; calibrate thresholds for worker PPE |
<!-- auto:end -->

Manual guidance:
- Record forensics datasets in addition to training splits.
