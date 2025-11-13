
import time, os, random
from pathlib import Path

from src.common.event_bus import FileEventBus
from src.telemetry.ingest import Telemetry
from src.models.collapse import CollapseModel
from src.models.gesture import GestureModel
from src.models.phone import PhoneUsage

def _fake_pose_sequence(n=180, w=640, h=360):
    kps = [[w*0.5, h*0.5] for _ in range(17)]
    for t in range(n):
        for i in range(17):
            kps[i][0] += random.uniform(-0.6,0.6)
            kps[i][1] += random.uniform(-0.6,0.6)
        if 40 <= t <= 50:
            kps[11][1] += 8.0; kps[12][1] += 8.0
        if 51 <= t <= 70:
            for i in (0,1,2,3,4,5,6,11,12):
                kps[i][1] = min(h-5, kps[i][1] + 4.5)
        yield [[float(x), float(y)] for x,y in kps]

def run_demo(out_dir="./artifacts", fps=15):
    bus = FileEventBus(out_dir)
    tele = Telemetry()
    collapse = CollapseModel(onnx_path=None)
    gesture = GestureModel()
    phone = PhoneUsage(fps=fps)

    feat_ring = []
    prev_midhip = None
    for kps in _fake_pose_sequence():
        midhip = ((kps[11][0]+kps[12][0])/2.0, (kps[11][1]+kps[12][1])/2.0)
        if prev_midhip is None:
            v = 0.0; a = 0.0
        else:
            v = ((midhip[0]-prev_midhip[0])**2 + (midhip[1]-prev_midhip[1])**2) ** 0.5 * fps
            a = v - feat_ring[-1]["v_mag"] if feat_ring else 0.0
        prev_midhip = midhip
        bbox_h = max(1.0, abs(kps[0][1]-((kps[11][1]+kps[12][1])/2.0))) * 2.0
        feat = {"v_mag": v, "a_mag": a, "prone_height_px": bbox_h}
        feat_ring.append(feat)
        if len(feat_ring) > 90: feat_ring.pop(0)

        score = collapse.score(feat_ring[-15:]) if len(feat_ring) >= 15 else 0.0
        if score >= 0.65:
            bus.publish("pose/collapse", {"score": score, "prone_px": bbox_h})

        label, gscore = gesture.predict(kps)
        if gscore >= 0.6 and label != "unknown":
            bus.publish("pose/gesture", {"label": label, "score": gscore})

        pscore, active = phone.score(kps)
        if active:
            bus.publish("pose/phone_usage", {"score": pscore})

        time.sleep(1.0/fps)

if __name__ == "__main__":
    out = os.environ.get("AIX_ARTIFACTS", "./artifacts")
    Path(out).mkdir(parents=True, exist_ok=True)
    run_demo(out_dir=out)
