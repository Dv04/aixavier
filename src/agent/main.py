from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from .webscan.scan import ModelScanner
from .rank.rank import rank_candidates
from .writer.apply import update_docs

ROOT = Path(__file__).resolve().parent.parent.parent
HANDOFF = ROOT / "HANDOFF.md"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default="artifacts/agent/report.json")
    args = parser.parse_args()

    scanner = ModelScanner()
    findings = scanner.scan()
    ranked = rank_candidates(findings)
    if not args.dry_run:
        update_docs(ranked)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(ranked, indent=2), encoding="utf-8")
    with HANDOFF.open("a", encoding="utf-8") as fh:
        fh.write(
            f"\n| {dt.datetime.utcnow().isoformat(timespec='seconds')}Z | agent | dry_run={args.dry_run} | findings={len(ranked)} |\n"
        )


if __name__ == "__main__":
    main()
