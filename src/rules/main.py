from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from common.config import env_or_default
from common.event_bus import Event, FileEventBus

from .engine import RuleEngine

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("rules")


def stream_events(source: Path):
    offset = 0
    while True:
        if not source.exists():
            time.sleep(1)
            continue
        with source.open("r", encoding="utf-8") as fh:
            fh.seek(offset)
            for line in fh:
                offset = fh.tell()
                if not line.strip():
                    continue
                yield json.loads(line)
        time.sleep(0.2)


def main() -> None:
    configs_dir = Path(env_or_default("RULES_DIR", "configs/usecases"))
    profile_config = Path(env_or_default("PROFILE_CONFIG", "configs/profile_demo.yaml"))
    profile = profile_config.read_text(encoding="utf-8")
    LOGGER.info("Loading rule engine with profile %s", profile_config.name)
    engine = RuleEngine(configs_dir)
    source_log = Path("artifacts/tracker/events.log")
    sink = FileEventBus(Path("artifacts/events"))
    for event in stream_events(source_log):
        for triggered in engine.evaluate(event):
            LOGGER.info("Triggered %s", triggered.type)
            sink.publish(Event(type=triggered.type, payload=triggered.payload))


if __name__ == "__main__":
    main()
