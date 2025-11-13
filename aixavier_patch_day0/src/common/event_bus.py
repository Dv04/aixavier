
from pathlib import Path
import json, time

class FileEventBus:
    """Minimal event bus that writes JSONL events.
    Use for demos/tests without external brokers."""
    def __init__(self, out_dir="./artifacts"):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.out_dir / "events.jsonl"

    def publish(self, topic: str, payload: dict):
        evt = {"ts": time.time(), "topic": topic, "payload": payload}
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(evt) + "\n")
        with open(self.out_dir / "last.json", "w", encoding="utf-8") as f:
            json.dump(evt, f, indent=2)
        return evt
