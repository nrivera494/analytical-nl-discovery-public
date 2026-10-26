"""Convergence of the one case where the GRIN launch beat LP01 by more than 0.02 dB (run
2026-10-04-claude-b-manakov-deviation-edge-scan): p2 = 0.15, delta = 0.942, zeta = 5, effective edge 1.178.
Variants: halfdz (N = 256 over 40 T0, dz = 1e-3), fine (N = 512 over 40 T0), x3 (N = 768 over 120 T0, edge kept at
1.178 by |k| <= 22 on the finer frequency grid; delta = 18 grid units). fine and x3 import twomode_lib with only the line
`N, TW = ...` changed (copies twomode_lib_fine.py, twomode_lib_x3.py in the session scratchpad, as for the scan's
convergence/ folder). Usage: python conv_p2_015.py <halfdz|fine|x3> [scratch_dir]  ->  conv_p2_015_<variant>.json
"""
import importlib, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
which = sys.argv[1]
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-04-claude-b-manakov-deviation-scan"))
if len(sys.argv) > 2:
    sys.path.insert(0, sys.argv[2])
lib = importlib.import_module({"halfdz": "twomode_lib", "fine": "twomode_lib_fine", "x3": "twomode_lib_x3"}[which])
t, w, TW = lib.t, lib.w, lib.TW
dz = 1e-3 if which == "halfdz" else 2e-3
C = [[1, 1], [1, 0.5]]
p2 = 0.15; p1 = 1 - p2; S = p1 * p1 + 2 * p1 * p2 + 0.5 * p2 * p2
unit = 2 * np.pi / TW
kmax = {"halfdz": 7, "fine": 7, "x3": 22}[which]
mask = (np.abs(np.round(w / unit)) <= kmax).astype(float)
d = 6 * 2 * np.pi / 40.0
sech = 1 / np.cosh(t)
Fs = lib.noise(sech + 0j, 0 * sech + 0j, 5.0, dz, C, 0.0, mask, mask)["Fa"]
r = lib.noise(np.sqrt(p1 / S) * sech + 0j, np.sqrt(p2 / S) * sech + 0j, 5.0, dz, C, d, mask, mask)
out = {"which": which, "N": int(lib.N), "TW": float(TW), "dz": dz, "edge": float((kmax + 0.5) * unit), "Fs": Fs, "case": r,
       "Ftot_dB_minus_Fs_dB": float(10 * np.log10(r["Ftot"] / Fs))}
print(json.dumps(out), flush=True)
json.dump(out, open(os.path.join(HERE, f"conv_p2_015_{which}.json"), "w"), indent=1)
