"""Mode-resolved readouts (exploration within T-20261008-claude-b-01; run 2026-10-08-claude-b-optimum, claude-b).

Readout X = w_a N_a(T_a) + w_b N_b(T_b) with hard symmetric bands |k| <= kmax_a, kmax_b per mode and weights w; noise
ratio R = Var(X) / sum_m w_m^2 <N_m(T_m)> (the coherent-state reference; R = F for w = (1, 1) and a common band).
Var(X) = w^T-weighted sum of the per-mode bin covariance blocks. For given bands the optimal weight ratio minimizes a
ratio of quadratic forms in w (2x2 generalized eigenproblem). Compared with the LP01 optimum over the same band family
(common band) and over any transmission (class C), and with a Manakov control: for Manakov overlaps and delta = 0 the
launch is unitarily a scalar soliton plus vacuum, so no mode-resolved band/weight choice can beat the scalar's optimum
over soft filters. Cases: zeta = 2 GRIN (C22 = 1/2) p2 = 0.3, 0.75 (this run); Manakov control p2 = 0.3, zeta = 2 is
computed here. Writes mode_resolved.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, scalar_optima

RID = "2026-10-08-claude-b-optimum"
RAW = os.path.expanduser("~/analytical-nl-discovery-data")


def blocks(path):
    d = np.load(path)
    N = int(d["N"])
    C = d["Cov"]
    return d["nbar"], C[:N, :N], C[:N, N:], C[N:, N:]


def best_mode_resolved(g, nbar, Caa, Cab, Cbb, kmax_max=14):
    best = None
    for ka in range(0, kmax_max):
        Ta = (np.abs(g.k) <= ka).astype(float)
        for kb in range(-1, kmax_max):          # kb = -1: mode b not detected
            Tb = (np.abs(g.k) <= kb).astype(float)
            V = np.array([[Ta @ Caa @ Ta, Ta @ Cab @ Tb], [Ta @ Cab @ Tb, Tb @ Cbb @ Tb]])
            S = np.diag([Ta @ nbar[0], Tb @ nbar[1]])
            if S[1, 1] <= 1e-12 * S[0, 0]:
                R, w = V[0, 0] / S[0, 0], (1.0, 0.0)
            else:
                ev, evec = np.linalg.eig(np.linalg.solve(S, V))
                i = int(np.argmin(ev.real))
                R, w = float(ev.real[i]), tuple(float(x) for x in evec[:, i].real / evec[0, i].real)
            # equal weights for reference
            R11 = (V.sum()) / (S[0, 0] + S[1, 1])
            if best is None or R < best["R"]:
                best = dict(R=float(R), kmax_a=ka, kmax_b=kb, w=w)
            if ka == kb and (best.get("R_equal") is None or R11 < best["R_equal"]):
                best["R_equal"], best["k_equal"] = float(R11), ka
    return best



def main():
    out = {}
    g, Cs, ns, _ = load(RID, "z2_scalar")
    opt = scalar_optima(g, Cs, ns)
    out["lp01"] = {k: float(v[0]) for k, v in opt.items()}
    for p2 in (0.3, 0.75):
        nbar, Caa, Cab, Cbb = blocks(os.path.join(RAW, RID, f"z2_p2_{p2:g}.npz"))
        out[f"grin_p2_{p2:g}"] = best_mode_resolved(g, nbar, Caa, Cab, Cbb)
        print(f"GRIN p2={p2}:", out[f"grin_p2_{p2:g}"], flush=True)
    # Manakov control
    a0, b0, _ = tc.launch(g, 0.3, [[1, 1], [1, 1]])
    nb, Cov = tc.bin_covariance(g, a0, b0, 2.0, 2e-3, [[1, 1], [1, 1]], 0.0)
    N = g.N
    out["manakov_p2_0.3"] = best_mode_resolved(g, nb, Cov[:N, :N], Cov[:N, N:], Cov[N:, N:])
    print("Manakov p2=0.3:", out["manakov_p2_0.3"], "LP01 optima:", out["lp01"], flush=True)
    json.dump(out, open(os.path.join(HERE, "mode_resolved.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
