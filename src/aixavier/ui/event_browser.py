"""
Event Browser API and stub implementation.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


class Event(BaseModel):
    id: str
    timestamp: str
    type: str
    details: str


# In-memory store for demo
_event_store: List[Event] = []


@router.get("/ui/events", response_model=List[Event])
def list_events():
    return _event_store


@router.post("/ui/events", response_model=Event)
def add_event(event: Event):
    _event_store.append(event)
    return event
