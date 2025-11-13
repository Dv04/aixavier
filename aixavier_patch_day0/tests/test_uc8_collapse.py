
from src.models.collapse import CollapseModel

def test_uc8_collapse_scores_high_on_drop_prone():
    m = CollapseModel(onnx_path=None)
    feats = []
    for _ in range(5):
        feats.append({"v_mag": 1.0, "a_mag": -2.2, "prone_height_px": 180})
    s = m.score(feats)
    assert s >= 0.65
