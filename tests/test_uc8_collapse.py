from src.models.collapse import CollapseModel


def test_uc8_collapse_scores_high_on_drop_prone() -> None:
    model = CollapseModel(onnx_path=None)
    features = []
    for _ in range(5):
        features.append({"v_mag": 1.0, "a_mag": -2.2, "prone_height_px": 180})
    score = model.score(features)
    assert score >= 0.65
