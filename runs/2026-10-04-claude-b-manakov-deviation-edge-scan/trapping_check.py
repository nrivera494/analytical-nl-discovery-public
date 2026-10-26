"""Where do the two carriers sit after propagation with walk-off? (run 2026-10-04-claude-b-manakov-deviation-edge-scan)
Mean-field propagation only (no noise): p2 = 0.3, delta = 0.942, zeta = 2 and 5. Reports the spectral peak and the
centroid of each mode's output, and the peak separation, to compare with soliton trapping (carrier separation = delta).
Usage: python trapping_check.py  ->  trapping_check.json
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-04-claude-b-manakov-deviation-scan"))
from twomode_lib import propagate, t, w, TW

C_GRIN = [[1, 1], [1, 0.5]]
p2 = 0.3; p1 = 1 - p2
S = p1 * p1 + 2 * p1 * p2 + 0.5 * p2 * p2
sech = 1 / np.cosh(t)
a0, b0 = np.sqrt(p1 / S) * sech + 0j, np.sqrt(p2 / S) * sech + 0j
d = 6 * 2 * np.pi / TW
out = {"p2": p2, "delta": d, "cases": []}
for z in (2.0, 5.0):
    a, b = propagate(a0[None], b0[None], z, 2e-3, C_GRIN, d)
    row = {"zeta": z}
    for name, f in (("LP01", a[0]), ("LP02", b[0])):
        Sp = np.abs(np.fft.fft(f)) ** 2
        row[name] = {"peak": float(w[np.argmax(Sp)]), "centroid": float(np.sum(w * Sp) / np.sum(Sp))}
    row["peak_separation"] = row["LP01"]["peak"] - row["LP02"]["peak"]
    out["cases"].append(row)
    print(json.dumps(row), flush=True)
json.dump(out, open(os.path.join(HERE, "trapping_check.json"), "w"), indent=1)
