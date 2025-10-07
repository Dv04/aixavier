#!/usr/bin/env python3
"""Placeholder linter enforcing naming, docs coverage, and secret hygiene."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Set

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER_PATTERN = re.compile(r"{{([A-Z0-9_]+)}}")
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
DOC_TABLE = ROOT / "docs" / "placeholders.md"
SECRET_PATTERN = re.compile(r"(?i)(apikey|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{12,}")


def scan_placeholders() -> Dict[str, Set[Path]]:
    mapping: Dict[str, Set[Path]] = {}
    for path in ROOT.rglob("*"):
        if path.is_dir():
            continue
        if path.suffix == ".pyc":
            continue
        if path.match(".git/*"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in PLACEHOLDER_PATTERN.finditer(text):
            mapping.setdefault(match.group(1), set()).add(path)
    return mapping


def parse_docs() -> Set[str]:
    if not DOC_TABLE.exists():
        return set()
    entries: Set[str] = set()
    for line in DOC_TABLE.read_text(encoding="utf-8").splitlines():
        if line.startswith("| {{"):
            placeholder = line.split("|", 2)[1].strip()
            entries.add(placeholder.strip())
    return entries


def check_prefix(name: str) -> bool:
    return any(name.startswith(prefix) for prefix in ALLOWED_PREFIXES | EXEMPT_PREFIXES)


def detect_cleartext_secrets(paths: Iterable[Path]) -> List[str]:
    findings: List[str] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in SECRET_PATTERN.finditer(text):
            findings.append(f"{path}: {match.group(0)}")
    return findings


def main() -> None:
    fail = False
    mapping = scan_placeholders()
    docs_entries = parse_docs()

    for name, locations in mapping.items():
        if not name.isupper():
            print(f"[ERROR] Placeholder {name} is not upper case", file=sys.stderr)
            fail = True
        if not check_prefix(name):
            print(f"[ERROR] Placeholder {name} lacks approved prefix", file=sys.stderr)
            fail = True
        wrapped = f"{{{{{name}}}}}"
        if wrapped not in docs_entries:
            print(f"[ERROR] Placeholder {name} missing from docs/placeholders.md", file=sys.stderr)
            fail = True
        for path in locations:
            if "docs" in path.parts and "placeholders.md" in path.name:
                continue
            # No plaintext secrets detection for docs to avoid noise
    secret_findings = detect_cleartext_secrets(ROOT.glob("**/*"))
    for finding in secret_findings:
        print(f"[ERROR] Potential secret detected: {finding}", file=sys.stderr)
        fail = True

    if fail:
        sys.exit(1)
    print("Placeholder lint OK")


if __name__ == "__main__":
    main()
