from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[3]
README = ROOT / "README.md"
MODELS = ROOT / "docs" / "MODELS.md"
DATASETS = ROOT / "docs" / "datasets.md"
PLACEHOLDERS = ROOT / "docs" / "placeholders.md"

PATTERN = re.compile(r"<!-- auto:start name=(?P<name>[a-zA-Z0-9_-]+) -->(?P<body>.*?)<!-- auto:end -->", re.S)
PLACEHOLDER_PATTERN = re.compile(r"{{([A-Z0-9_]+)}}")
PLACEHOLDER_COLUMNS = [
    "Placeholder",
    "File path(s)",
    "Purpose",
    "Required format / regex",
    "Example",
    "Security level",
    "Who provides",
    "When required",
    "Default",
    "Resolution status",
    "Last updated",
]
ALLOWED_PREFIXES = {
    "CAMERA_",
    "DATASET_",
    "FRS_",
    "MQTT_",
    "UI_",
    "ORG_",
    "STORAGE_",
    "SEC_",
    "METRICS_",
    "EVENTS_",
    "RETENTION_",
    "TIME_SYNC_",
    "INSTALL_",
    "GIT_",
}
EXEMPT_PREFIXES = {"PROMETHEUS_", "HANDOFF_"}


def _allowed_placeholder(name: str) -> bool:
    return any(name.startswith(prefix) for prefix in ALLOWED_PREFIXES | EXEMPT_PREFIXES)


def _extract_section(path: Path, name: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = PATTERN.search(text)
    if not match:
        return ""
    # There may be multiple sections; iterate all matches
    for m in PATTERN.finditer(text):
        if m.group("name") == name:
            return m.group("body").strip()
    return ""


def update_section(path: Path, name: str, content: str) -> None:
    text = path.read_text(encoding="utf-8")
    replacement = f"<!-- auto:start name={name} -->\n{content}\n<!-- auto:end -->"
    new_text, count = PATTERN.subn(lambda m: replacement if m.group("name") == name else m.group(0), text)
    if count == 0:
        raise ValueError(f"Auto section '{name}' not found in {path}")
    path.write_text(new_text, encoding="utf-8")


def _render_recommended_models(models: List[Dict[str, Any]], limit: int = 6) -> str:
    header = "| Rank | Task | Model | FP16 (ms) | INT8 (ms) | Accuracy | License | Last Checked |"
    divider = "|------|------|-------|-----------|-----------|----------|---------|--------------|"
    rows = [header, divider]
    for rec in models[:limit]:
        rows.append(
            "| {rank} | {task} | {model} | {fp16:.2f} | {int8:.2f} | {acc:.3f} | {license} | {checked} |".format(
                rank=rec.get("rank", "-"),
                task=rec.get("task", "-"),
                model=rec.get("model", "-"),
                fp16=rec.get("latency_fp16_ms", rec.get("latency_ms", 0.0)),
                int8=rec.get("latency_int8_ms", rec.get("latency_ms", 0.0)),
                acc=rec.get("accuracy", 0.0),
                license=rec.get("license", "-"),
                checked=rec.get("last_checked", "-"),
            )
        )
    return "\n".join(rows)


def _render_models_matrix(models: List[Dict[str, Any]]) -> str:
    header = (
        "| Task | Model | Backbone/Size | Training Data | Benchmark | Latency (FP16/INT8 ms) | VRAM (GB) | Params (M) | License | Why pick | Links |"
    )
    divider = "|------|-------|----------------|---------------|-----------|------------------------|-----------|------------|---------|----------|-------|"
    rows = [header, divider]
    for rec in models:
        links = rec.get("links", [])
        link_str = "<br>".join(links)
        rows.append(
            "| {task} | {model} | {backbone} | {train} | {benchmark} | {lat_fp16:.2f}/{lat_int8:.2f} | {vram:.2f} | {params:.2f} | {license} | {why} | {links} |".format(
                task=rec.get("task", "-"),
                model=rec.get("model", "-"),
                backbone=rec.get("backbone", "-"),
                train=rec.get("training_data", "-"),
                benchmark=rec.get("benchmark", "-"),
                lat_fp16=rec.get("latency_fp16_ms", 0.0),
                lat_int8=rec.get("latency_int8_ms", rec.get("latency_fp16_ms", 0.0)),
                vram=rec.get("vram_gb", 0.0),
                params=rec.get("params_m", 0.0),
                license=rec.get("license", "-"),
                why=rec.get("why", "-"),
                links=link_str or "-",
            )
        )
    return "\n".join(rows)


def _render_datasets(datasets: List[Dict[str, Any]]) -> str:
    header = (
        "| Use Case | Bucket | Dataset | License | Size | Modality | Indoor/Outdoor | Pros | Cons | Fit | Bias Notes |"
    )
    divider = "|----------|--------|---------|---------|------|---------|----------------|------|------|-----|------------|"
    rows = [header, divider]
    for item in datasets:
        name = item.get("name", "-")
        link = item.get("link")
        dataset_cell = f"[{name}]({link})" if link else name
        rows.append(
            "| {use_case} | {bucket} | {dataset} | {license} | {size} | {modality} | {io} | {pros} | {cons} | {fit} | {bias} |".format(
                use_case=item.get("use_case", "-"),
                bucket=item.get("bucket", "-"),
                dataset=dataset_cell,
                license=item.get("license", "-"),
                size=item.get("size", "-"),
                modality=item.get("modality", "-"),
                io=item.get("indoor_outdoor", "-"),
                pros=item.get("pros", "-"),
                cons=item.get("cons", "-"),
                fit=item.get("fit", "-"),
                bias=item.get("bias_notes", "-"),
            )
        )
    return "\n".join(rows)


def _render_performance_tuning(tuning: List[Dict[str, Any]]) -> str:
    if not tuning:
        return "- No automated tuning recommendations captured in the latest run."
    lines = []
    for item in tuning:
        topic = item.get("topic", "Tuning")
        recommendation = item.get("recommendation", "")
        impact = item.get("impact", "")
        lines.append(f"- **{topic}**: {recommendation} (_Impact_: {impact})")
    return "\n".join(lines)


def _render_known_issues(issues: List[Dict[str, Any]]) -> str:
    if not issues:
        return "- No outstanding issues recorded by the agent."
    lines = []
    for issue in issues:
        title = issue.get("title", "Issue")
        impact = issue.get("impact", "")
        workaround = issue.get("workaround", "")
        severity = issue.get("severity", "info").upper()
        link = issue.get("link")
        description = issue.get("description", "").rstrip()
        impact_text = issue.get("impact", "").rstrip()
        workaround = issue.get("workaround", "").rstrip()
        body = f"**[{severity}] {title}** — {description.rstrip('.')}"
        if description:
            body += "."
        if impact_text:
            body += f" _Impact_: {impact_text.rstrip('.')}."
        if workaround:
            body += f" _Workaround_: {workaround.rstrip('.')}."
        if link:
            body += f" [Details]({link})"
        lines.append(f"- {body}")
    return "\n".join(lines)


def _render_changelog(run_date: datetime, models_count: int, datasets_count: int, placeholders_count: int) -> str:
    previous = _extract_section(README, "changelog")
    entries = [line.strip() for line in previous.splitlines() if line.strip()]
    new_entry = (
        f"- {run_date.strftime('%Y-%m-%d')}: Catalog refresh (models={models_count}, datasets={datasets_count}, placeholders={placeholders_count})."
    )
    entries = [new_entry] + [entry for entry in entries if entry != new_entry]
    return "\n".join(entries[:10])  # keep latest 10 entries


def _load_placeholder_metadata() -> Dict[str, Dict[str, str]]:
    table = _extract_section(PLACEHOLDERS, "placeholder-index")
    metadata: Dict[str, Dict[str, str]] = {}
    if not table:
        return metadata
    lines = [line for line in table.splitlines() if line.startswith("|")]
    for line in lines[2:]:  # skip header/divider
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != len(PLACEHOLDER_COLUMNS):
            continue
        entry = dict(zip(PLACEHOLDER_COLUMNS, parts))
        metadata[entry["Placeholder"]] = entry
    return metadata


def _scan_placeholder_usage(root: Path) -> Dict[str, List[str]]:
    usage: Dict[str, set[str]] = {}
    skip_dirs = {".git", "artifacts", "__pycache__", "engines", "weights"}
    for path in root.rglob("*"):
        if path.is_dir():
            if path.name in skip_dirs:
                continue
            if any(part in skip_dirs for part in path.parts):
                continue
            continue
        if path == PLACEHOLDERS:
            continue
        if path.suffix in {".png", ".jpg", ".jpeg", ".mp4", ".onnx", ".engine"}:
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in PLACEHOLDER_PATTERN.finditer(text):
            raw_name = match.group(1)
            if not _allowed_placeholder(raw_name):
                continue
            placeholder = f"{{{{{raw_name}}}}}"
            usage.setdefault(placeholder, set()).add(str(path.relative_to(ROOT)))
    return {key: sorted(values) for key, values in usage.items()}


def _render_placeholder_table(run_date: datetime) -> Dict[str, Any]:
    metadata = _load_placeholder_metadata()
    usage = _scan_placeholder_usage(ROOT)
    for placeholder, paths in usage.items():
        entry = metadata.setdefault(
            placeholder,
            {
                "Placeholder": placeholder,
                "File path(s)": "",
                "Purpose": "TODO - document",
                "Required format / regex": ".+",
                "Example": "",
                "Security level": "public",
                "Who provides": "TODO",
                "When required": "setup",
                "Default": "none",
                "Resolution status": "unknown",
                "Last updated": run_date.strftime("%Y-%m-%d"),
            },
        )
        entry["File path(s)"] = "<br>".join(paths)
        entry["Last updated"] = run_date.strftime("%Y-%m-%d")
        if not entry.get("Resolution status"):
            entry["Resolution status"] = "unknown"
    rows = [
        "| " + " | ".join(PLACEHOLDER_COLUMNS) + " |",
        "|" + "-------------|" * len(PLACEHOLDER_COLUMNS),
    ]
    filtered_keys = [key for key in metadata.keys() if _allowed_placeholder(key.strip("{}"))]
    for key in sorted(filtered_keys):
        entry = metadata[key]
        row = "| " + " | ".join(entry.get(col, "") or "-" for col in PLACEHOLDER_COLUMNS) + " |"
        rows.append(row)
    return {"table": "\n".join(rows), "count": len(filtered_keys)}


def update_docs(
    *,
    models: List[Dict[str, Any]],
    datasets: List[Dict[str, Any]],
    issues: List[Dict[str, Any]],
    tuning: List[Dict[str, Any]],
    metadata: Dict[str, Any],
    run_timestamp: datetime,
    apply: bool = True,
) -> Dict[str, Any]:
    recommended = _render_recommended_models(models)
    matrix = _render_models_matrix(models)
    dataset_table = _render_datasets(datasets)
    tuning_md = _render_performance_tuning(tuning)
    issues_md = _render_known_issues(issues)
    placeholder_payload = _render_placeholder_table(run_timestamp)
    changelog_md = _render_changelog(run_timestamp, len(models), len(datasets), placeholder_payload["count"])

    if apply:
        update_section(README, "recommended-models", recommended)
        update_section(README, "performance-tuning", tuning_md)
        update_section(README, "known-issues", issues_md)
        update_section(README, "changelog", changelog_md)
        update_section(MODELS, "models-matrix", matrix)
        update_section(DATASETS, "datasets", dataset_table)
        update_section(PLACEHOLDERS, "placeholder-index", placeholder_payload["table"])

    return {
        "placeholders_count": placeholder_payload["count"],
        "models_matrix_rows": len(models),
        "datasets_rows": len(datasets),
        "tuning_count": len(tuning),
        "issues_count": len(issues),
    }
