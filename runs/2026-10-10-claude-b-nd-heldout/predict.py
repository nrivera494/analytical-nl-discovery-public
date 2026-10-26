"""Frozen held-out predictions (claude-b, T-20261010-claude-interactive-05). Run BEFORE the N = 40 cases are computed.

Held-out: N = 40 at z/z_wb = 0.7 and 1.0 (z_wb reference scale xi_wb = 1/sqrt(4 N^2 e^{-3/2} - 1)), Gaussian, pure Kerr,
normal dispersion. Built only from run 2026-10-10-claude-b-nd-oracle (N = 5..28).
Leading-order semiclassical form: N^2 lambda = coefficient(Z) - c / N (first-order correction in 1/N), fitted on the two
largest available N at each z/z_wb (N = 14, 20 for zr = 0.7 and 1.0); lambda_gen uses the mean of N^2 lambda_gen over
N = 10, 14, 20 (its N dependence is irregular); the best single interval uses a linear trend in log N over N = 10..20.
Tolerances: 2% (lambda_min), 3% (lambda_pass), 10% (lambda_gen), 0.06 absolute (best interval).
Writes predictions.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-b-nd-oracle/rows.jsonl")
rows = [json.loads(l) for l in open(RAW)]
pred = {}
for zr in (0.7, 1.0):
    R = {r["N"]: r for r in rows if abs(r["zr"] - zr) < 1e-9}
    out = {}
    for key in ("lam_min", "lam_pass"):
        f14, f20 = 14 ** 2 * R[14][key], 20 ** 2 * R[20][key]
        c = (f20 - f14) / (1 / 14 - 1 / 20)
        coef = f20 + c / 20
        out[key] = dict(coefficient=coef, c=c, N2lam_40=coef - c / 40, pred=(coef - c / 40) / 1600)
    g = np.mean([n ** 2 * R[n]["lam_gen"] for n in (10, 14, 20)])
    out["lam_gen"] = dict(N2lam_mean_10_20=g, pred=g / 1600)
    Ns = np.array([10, 14, 20])
    Fi = np.array([R[n]["F_interval"] for n in Ns])
    a, b = np.polyfit(np.log(Ns), Fi, 1)
    out["F_interval"] = dict(pred=float(a * np.log(40) + b), slope_per_lnN=float(a))
    pred[f"N40_zr{zr:g}"] = out
pred["tolerances"] = dict(lam_min=0.02, lam_pass=0.03, lam_gen=0.10, F_interval_abs=0.06)
pred["frozen_note"] = "Committed before the N = 40 cases were computed."
json.dump(pred, open(os.path.join(HERE, "predictions.json"), "w"), indent=1)
print(json.dumps(pred, indent=1))
