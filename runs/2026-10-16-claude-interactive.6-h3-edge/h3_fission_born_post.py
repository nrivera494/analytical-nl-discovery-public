"""Post-processing of the fission-born run (v2 leading-soliton rule): separation plane by (A) the frozen criterion
(f1 <= 1.05 f1(L) and ring < 0.05) and (B) a loss-independent criterion (ring < 0.05 and |delta f1| < 1% over three
consecutive saved planes).  Full-response ODE with loss from each z_s, compared at 2, 4, 6, 8 m."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-interactive.6-h3-edge")
fz = StepIndexFiber("ZrF4", 3.75, 0.30, n=600, n2=2.1e-20)
rz = OscillatorRaman(0.20, 0.0209, 0.053)
B = 92.0; A = 1.0 * np.exp(B / 4.2)
alpha = lambda w: edge_loss(w, A, B)
wp = wl_to_w(2.8)
aeff0 = float(fz.aeff_um2(np.array([wp]))[0])
D = json.loads(str(np.load(os.path.join(RAW, "fission_born_N2_T40fs_v3.npz"))["diag"]))
z = np.array([d["z"] for d in D]); N1 = np.array([d["N"] for d in D]); w1 = np.array([d["w"] for d in D])
Ntot = D[0]["Nall"]; f1 = N1 / Ntot; iso = np.array([d["iso"] for d in D]); P = np.array([d["P"] for d in D])
L = z[-1]
kc = int(np.argmax(P[: len(P) // 2 + 1]))
crit = {"A_frozen": next((k for k in range(kc + 1, len(D)) if f1[k] <= 1.05 * f1[-1] and iso[k] < 0.05), None),
        "B_stability": next((k for k in range(kc + 1, len(D) - 3) if iso[k] < 0.05 and
                             all(abs(f1[k + j + 1] / f1[k + j] - 1) < 0.01 for j in range(3))), None)}
res = {"f1_final": float(f1[-1]), "lam1_final_um": float(w_to_wl(w1[-1])), "z_compression_m": float(z[kc]),
       "f1_trajectory": [[round(float(z[k]), 3), round(float(f1[k]), 4), round(float(w_to_wl(w1[k])), 4), round(float(iso[k]), 4)] for k in range(0, len(D), 8)]}
for name, ks in crit.items():
    if ks is None:
        res[name] = None; continue
    m = ReachModel(fz, rz, alpha_w=alpha, rate="exact", aeff_const_um2=aeff0, npts=6001)
    zr, wr, Nr, Tr = m.integrate(w1[ks], N1[ks], L - z[ks], dz=(L - z[ks]) / 4000, n_out=800)
    zr = zr + z[ks]
    cmp_ = {}
    for zq in [2.0, 4.0, 6.0, 8.0]:
        if zq < z[ks]:
            continue
        k = int(np.argmin(abs(z - zq))); km = int(np.argmin(abs(zr - zq)))
        cmp_[str(zq)] = {"N1_rel_gnlse": float(N1[k] / N1[ks]), "N1_rel_model": float(Nr[km] / N1[ks]),
                         "lam1_gnlse_um": float(w_to_wl(w1[k])), "lam1_model_um": float(w_to_wl(wr[km]))}
    res[name] = {"z_sep_m": float(z[ks]), "f1_at_sep": float(f1[ks]), "lam1_at_sep_um": float(w_to_wl(w1[ks])),
                 "comparison": cmp_,
                 "max_abs_dN_rel": max(abs(v["N1_rel_gnlse"] - v["N1_rel_model"]) for v in cmp_.values()) if cmp_ else None,
                 "max_abs_dlam_um": max(abs(v["lam1_gnlse_um"] - v["lam1_model_um"]) for v in cmp_.values()) if cmp_ else None}
json.dump(res, open(os.path.join(HERE, "summary_fission_born_post.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "f1_trajectory"}, indent=1))
print("trajectory (z, f1, lam1, ring):", res["f1_trajectory"])
