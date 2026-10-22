"""Warp copied chorus repeats to their own audio via DTW on spectral features."""
import json, shutil, argparse
import numpy as np
from pathlib import Path

R = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--features', type=Path, required=True, help='Original spectral-feature .npy cache, hop=2048 at 16kHz')
args = parser.parse_args()
F = np.load(args.features)  # 7.8125fps, hop=2048 @16kHz
SEC = 2048 / 16000
t2f = lambda t: int(t / SEC)

shutil.copy(R / "alignment.json", R / "alignment_prewarp.json")
al = json.load(open(R / "alignment.json"))

def seg(a, b):
    return F[t2f(max(0, a)):t2f(b)]

def dtw_path(A, B, band=20):
    n, m = len(A), len(B)
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0.0
    for i in range(1, n + 1):
        for j in range(max(1, i - band), min(m + 1, i + band)):
            c = float(((A[i - 1] - B[j - 1]) ** 2).sum())
            D[i, j] = c + min(D[i - 1, j], D[i, j - 1], D[i - 1, j - 1])
    i, j, path = n, m, []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        steps = [(D[i - 1, j - 1], i - 1, j - 1), (D[i - 1, j], i - 1, j), (D[i, j - 1], i, j - 1)]
        _, i, j = min(steps)
    return list(reversed(path))

choruses = {}
for v in al:
    if v["section"].startswith("chorus"):
        choruses.setdefault(v["section"], []).append(v)
c1 = sorted(choruses["chorus1"], key=lambda v: v["start"])
c1end = max(v["end"] for v in c1)
ref = seg(21.55 - 0.5, c1end + 0.5)
ref_t0 = 21.55 - 0.5

for sec, lines in sorted(choruses.items()):
    if sec == "chorus1":
        continue
    lines = sorted(lines, key=lambda v: v["start"])
    dur = max(v["end"] for v in lines) - min(v["start"] for v in lines)
    tgt_t0 = min(v["start"] for v in lines) - 1.0
    tgt = seg(tgt_t0, tgt_t0 + dur + 2.0)
    path = dtw_path(ref, tgt)
    # ref frame -> median target frame
    from collections import defaultdict
    m = defaultdict(list)
    for i, j in path:
        m[i].append(j)
    ref2tgt = {i: float(np.median(v)) for i, v in m.items()}
    def warp(t):
        i = min(max(int((t - ref_t0) / SEC), 0), len(ref) - 1)
        return tgt_t0 + ref2tgt.get(i, i) * SEC
    v0c1 = min(x["start"] for x in c1)
    v0tgt = min(x["start"] for x in lines)
    for v in lines:
        for w in v["words"]:
            w["start"] = round(warp(w["start"] - v0tgt + v0c1), 3)
            w["end"] = round(warp(w["end"] - v0tgt + v0c1), 3)
        v["start"] = round(min(w["start"] for w in v["words"]), 3)
        v["end"] = round(max(w["end"] for w in v["words"]), 3)

json.dump(al, open(R / "alignment.json", "w"), ensure_ascii=False, indent=1)
print("warped", [s for s in choruses if s != "chorus1"])
for v in sorted([x for s in choruses.values() for x in s if s != "chorus1"], key=lambda x: x["start"])[:4]:
    print(v["section"], v["start"], [(w["word"], w["start"]) for w in v["words"]][:3])
