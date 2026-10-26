"""Mode-resolved weighted detection with walk-off (exploration within T-20261008-claude-b-01; claude-b).
Applies best_mode_resolved() of mode_resolved.py to the stored covariances of run 2026-10-08-claude-b-heldout:
H4 (GRIN LP02, C22 = 1/2, p2 = 0.3, delta = 0.3) and H5 (LP11, C22 = 3/4, p2 = 0.3, delta = 0.588: GIF625 at T0 = 0.227 ps),
at zeta = 2 and 5, against the LP01 optimum over hard symmetric bands (scalar cases of run 2026-10-08-claude-b-kw-map).
Bands are symmetric about the launch carrier for both modes. Writes mode_resolved_walkoff.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load
from mode_resolved import best_mode_resolved, blocks

RAW = os.path.expanduser("~/analytical-nl-discovery-data")
out = {}
for z in (2.0, 5.0):
    zt = f"z{z:g}"
    g, Cs, ns, _ = load("2026-10-08-claude-b-kw-map", f"{zt}_scalar")
    Fs = min(tc.class_sym_hard(g, Cs, ns, range(1, 15)).values())
    for case in ("H4", "H5"):
        nbar, Caa, Cab, Cbb = blocks(os.path.join(RAW, "2026-10-08-claude-b-heldout", f"{case}_{zt}.npz"))
        b = best_mode_resolved(g, nbar, Caa, Cab, Cbb)
        Fcommon = min(tc.class_sym_hard(g, Caa + Cab + Cab.T + Cbb, nbar[0] + nbar[1], range(1, 15)).values())
        out[f"{case}_{zt}"] = dict(F_lp01_best=Fs, F_common_best=Fcommon, gain_common=Fcommon - Fs,
                                   gain_mode_resolved=b["R"] - Fs, gain_mode_resolved_dB=10 * np.log10(b["R"] / Fs), **b)
        print(case, zt, f"LP01 {Fs:.5f} | common {Fcommon:.5f} ({Fcommon - Fs:+.4f}) | mode-resolved {b['R']:.5f} "
              f"({b['R'] - Fs:+.4f}, {10 * np.log10(b['R'] / Fs):+.3f} dB) w_b {b['w'][1]:.3f} bands {b['kmax_a']},{b['kmax_b']}", flush=True)
json.dump(out, open(os.path.join(HERE, "mode_resolved_walkoff.json"), "w"), indent=1, default=float)
