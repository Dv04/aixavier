import numpy as np


class GestureModel:
    """Predict simple hand gesture labels from pose keypoints."""

    LABELS = ("unknown", "halt", "proceed", "reverse", "caution")

    def __init__(self) -> None:
        pass

    @staticmethod
    def _y(kps: np.ndarray, idx: int) -> float:
        return float(kps[idx][1])

    def predict(self, kps: np.ndarray) -> tuple[str, float]:
        try:
            right_wrist = self._y(kps, 10)
            right_shoulder = self._y(kps, 6)
            left_wrist = self._y(kps, 9)
            left_shoulder = self._y(kps, 5)
        except Exception:  # pragma: no cover - malformed keypoints
            return ("unknown", 0.0)
        if right_wrist < right_shoulder - 10:
            return ("halt", 0.8)
        if left_wrist < left_shoulder - 10:
            return ("proceed", 0.7)
        return ("unknown", 0.1)
