from src.trackers import ByteTrack
from src.trackers.osnet_reid import OSNetReID
import numpy as np


def test_bytetrack_with_reid_assigns_ids() -> None:
    reid = OSNetReID(engine_path="dummy", threshold=0.4)
    tracker = ByteTrack(
        high_thresh=0.1, low_thresh=0.05, match_iou=0.1, max_age=3, reid_engine=reid
    )
    emb1 = reid.extract_embedding(np.zeros((256, 128, 3)))
    # Create emb2 orthogonal to emb1 for zero similarity
    emb2 = np.zeros_like(emb1)
    emb2[0] = 1.0
    emb2 = emb2 / np.linalg.norm(emb2)
    dets1 = tracker.update(
        [{"bbox": [0, 0, 100, 100], "confidence": 0.9, "embedding": emb1}]
    )
    tid = dets1[0]["track_id"]
    dets2 = tracker.update(
        [{"bbox": [5, 5, 105, 105], "confidence": 0.85, "embedding": emb1}]
    )
    assert dets2[0]["track_id"] == tid
    # Should spawn new ID if embedding is different enough
    dets3 = tracker.update(
        [{"bbox": [10, 10, 110, 110], "confidence": 0.95, "embedding": emb2}]
    )
    assert dets3[0]["track_id"] != tid
