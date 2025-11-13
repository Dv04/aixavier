import numpy as np

try:  # pragma: no cover - optional dependency
    import onnxruntime as ort  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - gracefully degrade when unavailable
    ort = None


class CollapseModel:
    """Score collapse severity using ONNX or heuristic fallback."""

    def __init__(self, onnx_path: str | None = None) -> None:
        self.session = None
        if onnx_path and ort is not None:
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
            try:
                self.session = ort.InferenceSession(onnx_path, providers=providers)
            except Exception:  # pragma: no cover - fallback to heuristic
                self.session = None
        self.min_drop = -1.8
        self.min_prone_px = 220

    def score(self, feature_window: list[dict[str, float]]) -> float:
        if not feature_window:
            return 0.0
        if self.session is not None:
            x = np.asarray(feature_window, dtype=np.float32)
            inp = self.session.get_inputs()[0].name
            out = self.session.get_outputs()[0].name
            return float(self.session.run([out], {inp: x})[0].squeeze())
        recent = feature_window[-3:]
        accel = np.mean([f.get("a_mag", 0.0) for f in recent])
        prone = np.mean([f.get("prone_height_px", self.min_prone_px) for f in recent])
        velocity = np.mean([f.get("v_mag", 0.0) for f in recent])
        score = 0.0
        if accel <= self.min_drop:
            score += 0.55
        if prone <= self.min_prone_px:
            score += 0.35
        if velocity < 3.0:
            score += 0.10
        return max(0.0, min(1.0, score))
