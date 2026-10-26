"""H3(a) in its path-independent form: GNLSE soliton photon number vs its own centre wavelength, compared with the
reduced model's N(lambda) at the SAME wavelength (no z matching).  The GNLSE soliton sheds ~1% of photons into radiation
during the first metre (launch is a bare sech); we report both the raw ratio and the ratio renormalised at 2 m."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h3-edge"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")
pred = json.load(open(os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-predictions", "predictions.json")))["H3_ZrF4"]
out = {}
for tag, col in [("const_dz0.250mm_dt6.0fs", "const_aeff"), ("pc_T020fs_dz0.250mm_dt6.0fs", "aeff_w")]:
    D = json.loads(str(np.load(os.path.join(RAW, tag + ".npz"))["diag"]))
    lam_g = np.array([d["lam_sol"] for d in D]); N_g = np.array([d["Nsol"] for d in D]); z = np.array([d["z"] for d in D])
    tr = np.array(pred[col]["traj_z_lam_Nfrac_Ts"])
    lam_m, N_m = tr[:, 1], tr[:, 2]
    k2 = int(np.argmin(abs(z - 2.0)))
    rows = []
    for k in range(k2, len(D), 10):
        Nm = float(np.interp(lam_g[k], lam_m, N_m))
        Nm2 = float(np.interp(lam_g[k2], lam_m, N_m))
        rows.append([round(float(z[k]), 3), round(float(lam_g[k]), 4), round(float(N_g[k]), 4), round(Nm, 4),
                     round(float(N_g[k] / N_g[k2]), 4), round(Nm / Nm2, 4)])
    r = np.array(rows)
    # loss accumulated after 2 m: GNLSE vs model at equal wavelength
    out[tag] = {"columns": ["z_m", "lam_gnlse_um", "N_gnlse", "N_model_at_same_lam", "N_gnlse_over_N_at_2m", "N_model_over_N_model_at_lam_2m"],
                "rows": rows,
                "max_abs_diff_renormalised": float(np.max(np.abs(r[:, 4] - r[:, 5]))),
                "loss_after_2m_gnlse": float(1 - r[-1, 4]), "loss_after_2m_model_same_lam": float(1 - r[-1, 5])}
    print(tag, out[tag]["max_abs_diff_renormalised"], out[tag]["loss_after_2m_gnlse"], out[tag]["loss_after_2m_model_same_lam"])
json.dump(out, open(os.path.join(HERE, "summary_invariant_post.json"), "w"), indent=1)
