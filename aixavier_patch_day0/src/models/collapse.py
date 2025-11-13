
import numpy as np
try:
    import onnxruntime as ort
except Exception:
    ort = None

class CollapseModel:
    def __init__(self, onnx_path: str | None = None):
        self.sess = None
        if onnx_path and ort is not None:
            self.sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
        self.min_drop = -1.8
        self.min_prone_px = 220

    def score(self, feature_window):
        if self.sess is not None:
            x = np.asarray(feature_window, dtype=np.float32)
            inp = self.sess.get_inputs()[0].name
            out = self.sess.get_outputs()[0].name
            return float(self.sess.run([out], {inp: x})[0].squeeze())
        a = np.mean([f["a_mag"] for f in feature_window[-3:]])
        prone = np.mean([f["prone_height_px"] for f in feature_window[-3:]])
        v = np.mean([f["v_mag"] for f in feature_window[-3:]])
        score = 0.0
        if a <= self.min_drop: score += 0.55
        if prone <= self.min_prone_px: score += 0.35
        if v < 3.0: score += 0.10
        return max(0.0, min(1.0, score))
