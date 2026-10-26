"""H2.3 post-processing of the saved fission diagnostics (no new GNLSE runs).
The in-run separation criterion (ring < 2% of peak) fired at the compression point, where the whole pulse is one
isolated peak; this script uses the corrected criterion recorded in the log:
  z_s = first saved plane after the peak-power maximum with f1 <= 1.05 f1(L) and ring/peak < 0.05.
Then the exact-overlap (and Gordon) reduced model is integrated from (z_s, w1, N1) to L."""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h2-fission"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")
fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
ram = OscillatorRaman(0.18, 0.0122, 0.032)
wp = wl_to_w(1.55)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
alpha = lambda w: edge_loss(w, 7.81e8, 48.48)
out = []
for f in sorted(glob.glob(os.path.join(RAW, "N*_T*fs_L*m*.npz"))):
    D = json.loads(str(np.load(f)["diag"]))
    z = np.array([d["z"] for d in D]); N1 = np.array([d["N"] for d in D]); Nt0 = D[0]["Ntot"]
    f1 = N1 / Nt0; iso = np.array([d["iso"] for d in D]); P = np.array([d["P"] for d in D]); w1 = np.array([d["w"] for d in D])
    kc = int(np.argmax(P[: len(P) // 2 + 1]))
    ks = next((k for k in range(kc + 1, len(D)) if f1[k] <= 1.05 * f1[-1] and iso[k] < 0.05), None)
    name = os.path.basename(f)[:-4]
    rec = {"case": name, "f1_final": float(f1[-1]), "z_compression_m": float(z[kc])}
    if ks is None:
        rec["note"] = "no separation plane found"; out.append(rec); print(rec); continue
    Ls = z[-1] - z[ks]
    rec.update({"z_sep_m": float(z[ks]), "f1_at_sep": float(f1[ks]), "lam1_at_sep_um": float(w_to_wl(w1[ks])),
                "lam1_final_um": float(w_to_wl(w1[-1])), "f1_growth_after_sep": float(f1[-1] / f1[ks] - 1)})
    sh_g = w1[ks] - w1[-1]
    for rate in ["exact", "gordon"]:
        m = ReachModel(fib, ram, alpha_w=alpha, rate=rate, aeff_const_um2=aeff0, npts=6001)
        zr, wr, Nr, Tr = m.integrate(w1[ks], N1[ks], Ls, dz=Ls / 2000)
        rec[f"model_{rate}_lam_final_um"] = float(w_to_wl(wr[-1]))
        rec[f"reach_rel_err_{rate}"] = float(((w1[ks] - wr[-1]) - sh_g) / sh_g)
        # same, but with the soliton's final photon number (upper allowance for Raman transfer after separation)
        zr2, wr2, Nr2, Tr2 = m.integrate(w1[ks], N1[-1] * np.exp(0), Ls, dz=Ls / 2000)
        rec[f"reach_rel_err_{rate}_Nfinal"] = float(((w1[ks] - wr2[-1]) - sh_g) / sh_g)
    rec["shift_after_sep_gnlse"] = float(sh_g)
    out.append(rec)
    print(json.dumps(rec), flush=True)
json.dump({"run_id": RUN, "criterion": "first plane after peak-power max with f1 <= 1.05 f1(L) and ring/peak < 0.05", "cases": out},
          open(os.path.join(HERE, "summary_reach_post.json"), "w"), indent=1)
