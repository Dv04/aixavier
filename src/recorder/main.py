from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from common.config import ensure_dir

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("recorder")


def stream_events(path: Path):
    offset = 0
    while True:
        if not path.exists():
            time.sleep(1)
            continue
        with path.open("r", encoding="utf-8") as fh:
            fh.seek(offset)
            for line in fh:
                offset = fh.tell()
                if not line.strip():
                    continue
                yield json.loads(line)
        time.sleep(0.5)


def main() -> None:
    source = Path("artifacts/events/events.log")
    recordings_dir = ensure_dir("artifacts/recordings")
    for event in stream_events(source):
        clip_path = recordings_dir / f"{event.get('type')}_{int(time.time())}.json"
        clip_path.write_text(json.dumps(event, indent=2), encoding="utf-8")
        LOGGER.info("Recorded artifact %s", clip_path)


if __name__ == "__main__":
    main()
