"""
ROI Editor API and stub implementation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Tuple

router = APIRouter()


class ROI(BaseModel):
    id: str
    points: List[Tuple[int, int]]
    label: str


# In-memory store for demo
roi_store: List[ROI] = []


@router.get("/ui/roi", response_model=List[ROI])
def list_rois():
    return roi_store


@router.post("/ui/roi", response_model=ROI)
def add_roi(roi: ROI):
    roi_store.append(roi)
    return roi


@router.delete("/ui/roi/{roi_id}")
def delete_roi(roi_id: str):
    global roi_store
    roi_store = [r for r in roi_store if r.id != roi_id]
    return {"status": "deleted"}
