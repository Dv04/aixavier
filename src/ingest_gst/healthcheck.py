from __future__ import annotations

import json
import sys
from pathlib import Path

from common.config import ensure_dir


def main() -> None:
    base = ensure_dir("artifacts/ingest")
    events = base / "frames.log"
    if not events.exists():
        print("no events yet", file=sys.stderr)
        sys.exit(1)
    *_, last = events.read_text(encoding="utf-8").strip().splitlines()
    if not last:
        sys.exit(1)
    data = json.loads(last)
    if "frame_index" not in data:
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
