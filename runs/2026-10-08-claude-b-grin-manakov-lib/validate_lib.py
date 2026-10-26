"""Validation of twomode_cov.py (run 2026-10-08-claude-b-grin-manakov-lib).
1. zeta -> 0: F = 1 for every filter (shot noise).
2. Manakov identity: C22 = 1, delta = 0, p2 = 0.3 gives the same all-mode per-bin covariance and F as the scalar launch.
3. Reproduction of round-1 numbers (run 2026-10-04-claude-b-manakov-deviation-edge-scan, zeta = 2, p2 = 0.3, delta = 0,
   C22 = 1/2, edges kmax = 3..7): F_tot and F_s per edge.
4. Fractional-edge and interval classes contain the hard symmetric band (consistency of the optimizers).
Writes validation.json next to this file.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import twomode_cov as tc

g = tc.Grid(256, 40.0)
out = {}
# 1. shot noise at zeta = dz (one step)
a0, b0, _ = tc.launch(g, 0.3, [[1, 1], [1, 0.5]])
nbar, Cov = tc.bin_covariance(g, a0, b0, 2e-3, 2e-3, [[1, 1], [1, 0.5]], 0.0)
Ct, nt = tc.totals(nbar, Cov, g.N)
Fs = [tc.fano((np.abs(g.k) <= km).astype(float), Ct, nt) for km in (2, 5, 10)]
out["shot_noise_one_step_F"] = Fs

# 2. Manakov identity at zeta = 2
s = 1 / np.cosh(g.t) + 0j
nb_s, Cov_s = tc.bin_covariance(g, s, 0 * s, 2.0, 2e-3, [[1, 1], [1, 1]], 0.0)
Ct_s, nt_s = tc.totals(nb_s, Cov_s, g.N)
a0, b0, _ = tc.launch(g, 0.3, [[1, 1], [1, 1]])
nb_m, Cov_m = tc.bin_covariance(g, a0, b0, 2.0, 2e-3, [[1, 1], [1, 1]], 0.0)
Ct_m, nt_m = tc.totals(nb_m, Cov_m, g.N)
out["manakov_max_abs_dC_over_max_C"] = float(np.max(np.abs(Ct_m - Ct_s)) / np.max(np.abs(Ct_s)))
out["manakov_max_abs_dn_over_max_n"] = float(np.max(np.abs(nt_m - nt_s)) / np.max(nt_s))
out["manakov_F_pairs"] = [(km, tc.fano((np.abs(g.k) <= km).astype(float), Ct_s, nt_s),
                           tc.fano((np.abs(g.k) <= km).astype(float), Ct_m, nt_m)) for km in (3, 5, 7)]

# 3. reproduction of round 1 (C22 = 1/2, p2 = 0.3, zeta = 2, delta = 0)
a0, b0, _ = tc.launch(g, 0.3, [[1, 1], [1, 0.5]])
nb_g, Cov_g = tc.bin_covariance(g, a0, b0, 2.0, 2e-3, [[1, 1], [1, 0.5]], 0.0)
Ct_g, nt_g = tc.totals(nb_g, Cov_g, g.N)
r1 = json.load(open(os.path.join(HERE, "..", "2026-10-04-claude-b-manakov-deviation-edge-scan", "summary_zeta2.json")))
rep = []
for c in r1["cases"]:
    if c["delta"] > 0:
        continue
    km = c["kmax"]
    T = (np.abs(g.k) <= km).astype(float)
    rep.append(dict(kmax=km, F_tot_now=tc.fano(T, Ct_g, nt_g), F_tot_round1=c["computed"]["Ftot"],
                    F_s_now=tc.fano(T, Ct_s, nt_s), F_s_round1=c["Fs_LP01"]))
out["round1_reproduction"] = rep
out["round1_max_rel_diff"] = max(max(abs(r["F_tot_now"] / r["F_tot_round1"] - 1), abs(r["F_s_now"] / r["F_s_round1"] - 1)) for r in rep)

# 4. optimizer consistency on the scalar case
A = tc.class_sym_hard(g, Ct_s, nt_s, range(0, 20))
Abest = min(A.values())
Ap, _ = tc.class_sym_frac(g, Ct_s, nt_s, range(0, 20))
B = tc.class_interval(g, Ct_s, nt_s)
Cbest, Topt = tc.class_any(g, Ct_s, nt_s, [(np.abs(g.k) <= min(A, key=A.get)).astype(float)])
out["scalar_zeta2_best"] = dict(sym_hard=Abest, sym_hard_kmax=min(A, key=A.get), sym_frac=Ap, interval=B, any=Cbest)
out["optimizer_order_ok"] = bool(Ap["F"] <= Abest + 1e-12 and B["F"] <= Abest + 1e-12 and Cbest["F"] <= min(Ap["F"], B["F"]) + 1e-9)
json.dump(out, open(os.path.join(HERE, "validation.json"), "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
