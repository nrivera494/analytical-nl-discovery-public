"""Where the best binary filters lose against the parity bound (claude-b, T-20261010-claude-interactive-05).
For the final filter T on the parity-symmetric kept set B: y = T sqrt(nbar), odd fraction f = |y_o|^2/|y|^2,
Rayleigh quotients R_e = y_e^T A y_e/|y_e|^2 and R_o = y_o^T A y_o/|y_o|^2 (A = V_amp), so F = (1-f) R_e + f R_o exactly.
Compared with lambda_even, lambda_odd and F_par. Writes parity_anatomy.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
S = {p["tag"]: p for p in json.load(open(os.path.join(HERE, "summary.json")))["points"]}
PB = json.load(open(os.path.join(HERE, "parity_bound.json")))
out = {}
for tag in ("N10_zr0.7", "N20_zr0.7", "N40_zr0.7", "N20_zr1", "N40_zr1", "N20_zr0.3", "N10_zr2"):
    p = S[tag]
    d = np.load(os.path.join(RAW, p["run"], tag + ".npz"))
    C, nb, keep, w = d["C"], d["nbar"], d["keep"], d["w"]
    T = np.load(os.path.join(RAW, p["run"], tag + "_transfer.npz"))["T"].astype(float)
    dw = 2 * np.pi / p["TW"]
    kk = np.rint(w[keep] / dw).astype(int)
    inB = np.array([(-k in set(kk)) for k in kk])
    C, nb, kk, T = C[np.ix_(inB, inB)], nb[inB], kk[inB], T[inB]
    idx = {k: i for i, k in enumerate(kk)}
    perm = np.array([idx[-k] for k in kk])
    A = C / np.sqrt(nb)[:, None] / np.sqrt(nb)[None, :]
    y = T * np.sqrt(nb)
    ye, yo = (y + y[perm]) / 2, (y - y[perm]) / 2
    f = float(yo @ yo / (y @ y))
    Re = float(ye @ A @ ye / (ye @ ye)); Ro = float(yo @ A @ yo / (yo @ yo)) if f > 0 else float("nan")
    F = float(y @ A @ y / (y @ y))
    out[tag] = dict(F_bin_on_B=F, odd_fraction=f, R_even=Re, R_odd=Ro, lam_even=PB[tag]["lam_even"], lam_odd=PB[tag]["lam_odd"],
                    F_par=PB[tag]["F_par"], check=(1 - f) * Re + f * Ro)
    o = out[tag]
    print(f"{tag:10s} F {F:.4f} f_odd {f:.3f} | R_even {Re:.4f} (lam_even {o['lam_even']:.4f}, x{Re/o['lam_even']:.2f}) | R_odd {Ro:.4f} (lam_odd {o['lam_odd']:.4f}, x{Ro/o['lam_odd']:.1f}) | F_par {o['F_par']:.4f}", flush=True)
json.dump(out, open(os.path.join(HERE, "parity_anatomy.json"), "w"), indent=1)
