from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict

try:
    from .webscan.scan import ModelScanner  # type: ignore
    from .rank.rank import rank_candidates  # type: ignore
    from .writer.apply import update_docs  # type: ignore
except ImportError:  # pragma: no cover - support script execution
    import sys

    CURRENT_DIR = Path(__file__).resolve().parent
    PACKAGE_ROOT = CURRENT_DIR.parent
    if str(PACKAGE_ROOT) not in sys.path:
        sys.path.append(str(PACKAGE_ROOT))
    from webscan.scan import ModelScanner  # type: ignore
    from rank.rank import rank_candidates  # type: ignore
    from writer.apply import update_docs  # type: ignore

ROOT = Path(__file__).resolve().parent.parent.parent
HANDOFF = ROOT / "HANDOFF.md"


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_pr_body(path: Path, summary: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "## Change Summary",
        "| Item | Count |",
        "|------|-------|",
        f"| Models catalogued | {summary['models_count']} |",
        f"| Datasets catalogued | {summary['datasets_count']} |",
        f"| Placeholder entries | {summary['placeholders_count']} |",
        f"| Issues tracked | {summary['issues_count']} |",
        "",
        "## Sources",
    ]
    if summary.get("sources"):
        lines.extend([f"- {src}" for src in summary["sources"]])
    else:
        lines.append("- (no external sources listed)")
    lines.extend(
        [
            "",
            "## Risk",
            "- Low – documentation and metadata refresh only.",
            "",
            "## Commands",
            "- `python src/agent/main.py`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_handoff(summary: Dict[str, Any], dry_run: bool) -> None:
    timestamp = summary["run_timestamp"]
    row = (
        f"\n| {timestamp} | agent | Auto-refresh analytics catalog | Maintain model/dataset freshness | "
        f"{'; '.join(summary.get('sources', [])) or 'internal catalog'} | python src/agent/main.py | "
        f"artifacts/agent/report.json | Review PR agent/update-{summary['run_date']} ({'dry-run' if dry_run else 'ready'}) |\n"
    )
    with HANDOFF.open("a", encoding="utf-8") as fh:
        fh.write(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default="artifacts/agent/report.json")
    parser.add_argument("--pr-body", default="artifacts/agent/pr_body.md")
    args = parser.parse_args()

    run_ts = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    run_date = run_ts.strftime("%Y%m%d")

    scanner = ModelScanner()
    catalog = scanner.scan()
    models = rank_candidates(catalog.get("models", []))
    datasets = catalog.get("datasets", [])
    issues = catalog.get("issues", [])
    tuning = catalog.get("tuning", [])
    metadata = catalog.get("metadata", {})

    doc_summary = update_docs(
        models=models,
        datasets=datasets,
        issues=issues,
        tuning=tuning,
        metadata=metadata,
        run_timestamp=run_ts,
        apply=not args.dry_run,
    )

    summary = {
        "run_timestamp": run_ts.isoformat().replace("+00:00", "Z"),
        "run_date": run_date,
        "models_count": len(models),
        "datasets_count": len(datasets),
        "placeholders_count": doc_summary.get("placeholders_count", 0),
        "issues_count": len(issues),
        "tuning_count": len(tuning),
        "sources": metadata.get("sources", []),
        "dry_run": args.dry_run,
    }

    write_json(Path(args.output), summary)
    write_pr_body(Path(args.pr_body), summary)
    append_handoff(summary, args.dry_run)


if __name__ == "__main__":
    main()
