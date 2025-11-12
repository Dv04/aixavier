"""
UI Toggles API and stub implementation.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()


class Toggle(BaseModel):
    name: str
    enabled: bool


# In-memory store for demo
_toggle_store: Dict[str, bool] = {}


@router.get("/ui/toggles", response_model=Dict[str, bool])
def list_toggles():
    return _toggle_store


@router.post("/ui/toggles", response_model=Toggle)
def set_toggle(toggle: Toggle):
    _toggle_store[toggle.name] = toggle.enabled
    return toggle
