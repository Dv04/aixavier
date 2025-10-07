from __future__ import annotations

import asyncio
import json
import logging
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from common.event_bus import Event, FileEventBus
from .store import EmbeddingStore
from common.config import load_yaml

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
LOGGER = logging.getLogger("privacy")

app = FastAPI(title="FRS Service")
store = EmbeddingStore(Path("artifacts/privacy/embeddings.json"))
audit_path = Path("artifacts/privacy/frs_audit.log")
audit_path.parent.mkdir(parents=True, exist_ok=True)
tracker_bus = FileEventBus(Path("artifacts/tracker"))
frs_config = load_yaml("configs/frs/config.yaml")
try:
    threshold = float(str(frs_config.get("threshold", "0.47")).strip("{}"))
except ValueError:
    threshold = 0.47

whitelist = load_yaml("configs/frs/whitelist.yaml") or {}
for person in whitelist.get("people", []):
    store.enroll(person.get("name", "unknown"), person.get("embedding", ""))


class EnrollRequest(BaseModel):
    name: str
    embedding: str
    operator: str
    reason: str


@app.post("/enroll")
def enroll(request: EnrollRequest) -> dict:
    if not request.name:
        raise HTTPException(status_code=400, detail="Name required")
    store.enroll(request.name, request.embedding)
    with audit_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "ts": time.time(),
            "name": request.name,
            "operator": request.operator,
            "reason": request.reason,
        }) + "\n")
    return {"status": "ok"}


async def frs_worker() -> None:
    source = Path("artifacts/detections/events.log")
    offset = 0
    while True:
        if not source.exists():
            await asyncio.sleep(1)
            continue
        with source.open("r", encoding="utf-8") as fh:
            fh.seek(offset)
            for line in fh:
                offset = fh.tell()
                if not line.strip():
                    continue
                event = json.loads(line)
                if event.get("type") != "embedding":
                    continue
                embedding = event.get("embedding")
                match = store.match(embedding, threshold)
                if match:
                    tracker_bus.publish(
                        Event(
                            type="frs",
                            payload={
                                "camera_id": event.get("camera_id"),
                                "identity": match["identity"],
                                "score": match["score"],
                            },
                        )
                    )
        await asyncio.sleep(0.5)


@app.on_event("startup")
async def startup_event() -> None:
    asyncio.create_task(frs_worker())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
