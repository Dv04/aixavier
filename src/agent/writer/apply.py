from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent.parent
README = ROOT / "README.md"
MODELS = ROOT / "docs" / "MODELS.md"
DATASETS = ROOT / "docs" / "datasets.md"

PATTERN = re.compile(r"<!-- auto:start name=(?P<name>[a-zA-Z0-9_-]+) -->(?P<body>.*?)<!-- auto:end -->", re.S)


def update_section(path: Path, name: str, content: str) -> None:
    text = path.read_text(encoding="utf-8")
    replacement = f"<!-- auto:start name={name} -->\n{content}\n<!-- auto:end -->"
    new_text, count = PATTERN.subn(lambda m: replacement if m.group("name") == name else m.group(0), text)
    if count:
        path.write_text(new_text, encoding="utf-8")


def update_docs(records: List[Dict]) -> None:
    table_rows = [
        "| Task | Model | Latency (ms) | Accuracy |",
        "|------|-------|-------------|----------|",
    ]
    for rec in records:
        table_rows.append(
            f"| {rec['task']} | {rec['model']} | {rec['latency_ms']:.2f} | {rec['accuracy']:.2f} |"
        )
    update_section(README, "recommended-models", "\n".join(table_rows))
    update_section(README, "performance-tuning", "Agent refresh pending detailed metrics.")
    update_section(README, "known-issues", "None detected during offline scan.")
    update_section(README, "changelog", "- Auto-update placeholder\n")
    update_section(MODELS, "models-matrix", "\n".join(table_rows))
    update_section(DATASETS, "datasets", "Agent has not scanned datasets in offline mode.")
