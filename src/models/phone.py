import numpy as np


def _dist(a: np.ndarray, b: np.ndarray) -> float:
    ax, ay = float(a[0]), float(a[1])
    bx, by = float(b[0]), float(b[1])
    return float(((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5)


class PhoneUsage:
    """Heuristic detector for prolonged hand-to-ear proximity."""

    def __init__(
        self, hand_to_ear_px: float = 80.0, dwell_s: float = 2.0, fps: int = 15
    ) -> None:
        self.hand_to_ear_px = hand_to_ear_px
        self.dwell_frames = max(1, int(dwell_s * fps))
        self._counter = 0
        self.last_dwell_frames = 0

    def score(self, keypoints: np.ndarray) -> tuple[float, bool]:
        idx = {"right_wrist": 10, "right_ear": 4, "left_wrist": 9, "left_ear": 3}
        try:
            right = _dist(keypoints[idx["right_wrist"]], keypoints[idx["right_ear"]])
            left = _dist(keypoints[idx["left_wrist"]], keypoints[idx["left_ear"]])
        except Exception:  # pragma: no cover - malformed keypoints
            return (0.0, False)
        near = (right < self.hand_to_ear_px) or (left < self.hand_to_ear_px)
        self._counter = self._counter + 1 if near else 0
        self.last_dwell_frames = self._counter
        if self._counter >= self.dwell_frames:
            return (0.7, True)
        return (0.2 if near else 0.0, False)
