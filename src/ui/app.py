from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Edge CCTV UI API")


def read_events(limit: int = 20) -> list[dict]:
    path = Path("artifacts/normalized/events.log")
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    events = [json.loads(line) for line in lines if line]
    return events[-limit:]


@app.get("/healthz")
def health() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
def ready() -> dict:
    return {"ready": True}


@app.get("/events")
def events(limit: int = 20) -> JSONResponse:
    return JSONResponse(read_events(limit))


@app.get("/config/placeholders")
def placeholders() -> JSONResponse:
    table = Path("docs/placeholders.md").read_text(encoding="utf-8")
    return JSONResponse({"markdown": table})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
