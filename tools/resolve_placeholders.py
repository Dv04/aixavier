#!/usr/bin/env python3
"""Placeholder resolver and reporter.

Features:
- Scan repository for placeholders matching {{UPPER_SNAKE_CASE}}
- List inventory from docs/placeholders.md
- Validate supplied key/values from .env or YAML files
- Append resolution report to HANDOFF.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER_PATTERN = re.compile(r"{{([A-Z0-9_]+)}}")
TABLE_PATH = ROOT / "docs" / "placeholders.md"
HANDOFF_PATH = ROOT / "HANDOFF.md"


def parse_table() -> Dict[str, Dict[str, str]]:
    if not TABLE_PATH.exists():
        return {}
    rows: Dict[str, Dict[str, str]] = {}
    with TABLE_PATH.open("r", encoding="utf-8") as fh:
        lines = [line.strip() for line in fh]
    for line in lines:
        if not line.startswith("| {{"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 11:
            continue
        placeholder = parts[0]
        rows[placeholder] = {
            "paths": parts[1],
            "purpose": parts[2],
            "regex": parts[3].strip("`").strip(),
            "example": parts[4],
            "security": parts[5],
            "who": parts[6],
            "when": parts[7],
            "default": parts[8],
            "status": parts[9],
            "updated": parts[10],
        }
    return rows


def find_placeholders(paths: Iterable[Path]) -> Dict[str, List[Path]]:
    mapping: Dict[str, List[Path]] = {}
    for path in paths:
        if path.is_dir():
            mapping.update(find_placeholders(path.iterdir()))
            continue
        if path.name in {"resolve_placeholders.py", "placeholder_lint.py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in PLACEHOLDER_PATTERN.finditer(text):
            placeholder = match.group(1)
            mapping.setdefault(placeholder, []).append(path)
    return mapping


def load_values(source: Path) -> Dict[str, str]:
    if source.suffix in {".yml", ".yaml"}:
        data = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
        return {k.upper(): str(v) for k, v in data.items()}
    values: Dict[str, str] = {}
    for line in source.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip().upper()] = value.strip()
    return values


def validate(values: Dict[str, str], inventory: Dict[str, Dict[str, str]]) -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    for raw_name, meta in inventory.items():
        name = raw_name.strip("{}")
        regex = meta.get("regex") or ".*"
        try:
            pattern = re.compile(regex)
        except re.error:
            pattern = re.compile(".*")
        target = values.get(name)
        if target is None:
            results.append((raw_name, "missing"))
            continue
        if not pattern.fullmatch(target):
            results.append((raw_name, f"invalid ({target})"))
        else:
            results.append((raw_name, "resolved"))
    return results


def append_report(source: Path, results: List[Tuple[str, str]]) -> None:
    timestamp = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    lines = [f"\n| {timestamp} | placeholder-resolver | Source={source.name} |"]
    for name, status in results:
        lines.append(f"| {name} | {status} |")
    with HANDOFF_PATH.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List known placeholders")
    parser.add_argument("--from", dest="source", help="Load values from file (.env or .yaml)")
    args = parser.parse_args()

    inventory = parse_table()
    if args.list:
        for name, meta in inventory.items():
            print(name, "->", meta.get("status", "unknown"))
        return

    if args.source:
        source_path = (ROOT / args.source).resolve()
        if not source_path.exists():
            print(f"Source {source_path} missing", file=sys.stderr)
            sys.exit(1)
        values = load_values(source_path)
        results = validate(values, inventory)
        all_resolved = True
        for name, status in results:
            print(f"{name}: {status}")
            if status != "resolved":
                all_resolved = False
        append_report(source_path, results)
        if all_resolved:
            os.environ["PLACEHOLDER_RESOLVED"] = "true"
        else:
            sys.exit(1)
        return

    # default: scan repository
    placeholders = find_placeholders([ROOT])
    for name, paths in sorted(placeholders.items()):
        print(f"{name}: {len(paths)} uses")


if __name__ == "__main__":
    main()
