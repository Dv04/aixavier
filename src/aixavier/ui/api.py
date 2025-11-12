"""
FastAPI router aggregator for UI endpoints.
"""

from fastapi import APIRouter
from .roi_editor import router as roi_router
from .event_browser import router as event_router
from .toggles import router as toggles_router

router = APIRouter()
router.include_router(roi_router)
router.include_router(event_router)
router.include_router(toggles_router)
