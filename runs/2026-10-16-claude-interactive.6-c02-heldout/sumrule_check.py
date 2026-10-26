"""Sum rule used by C-20261016-claude-interactive.6-02: int dW/2pi W Im h(W) = h'(0+)/2, and W Im h >= 0,
for the single-oscillator Raman responses used in this task (silica and the fluoride stand-in)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import OscillatorRaman

out = {}
for name, r in [("silica", OscillatorRaman(0.18, 0.0122, 0.032)), ("fluoride_standin", OscillatorRaman(0.20, 0.0209, 0.053))]:
    W = np.linspace(0, 2e5, 4000001)
    f = W * r.h_w(W).imag
    I = 2 * np.trapezoid(f, W) / (2 * np.pi)
    c = f[-1] * W[-1] ** 2
    I += 2 * c / W[-1] / (2 * np.pi)          # 1/W^2 tail beyond the grid
    out[name] = {"integral_per_ps2": float(I), "hprime0_over_2_per_ps2": float(r.hprime0() / 2),
                 "rel_diff": float(I / (r.hprime0() / 2) - 1), "min_W_Imh": float(f.min()), "TR_fs": r.TR() * 1e3}
json.dump(out, open(os.path.join(HERE, "sumrule.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
