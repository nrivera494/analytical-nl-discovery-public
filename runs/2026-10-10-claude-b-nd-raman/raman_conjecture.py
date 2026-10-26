"""Test of the conjecture rho(Z) = sqrt(4 Z^2 Lambda(Z)) for the Raman floor Delta lambda_min = rho c_hat(0) / Phi
(claude-b, T-20261010-claude-interactive-05). Predictions are written to conjecture_predictions.json and committed
before the points are computed (mode 'predict'); mode 'run' computes N20 z/z_wb = 0.3 and 1.5 (Nt 1024, 40 T0) and N10
z/z_wb = 3 (Nt 1024, 60 T0) at T0 = 1 ps, 300 K, and scores them (tolerance: |rho/pred - 1| <= 0.15).
Usage: python raman_conjecture.py predict | run"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SC = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-semiclassical")
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import nd_cov as nd
cases = [dict(N=20, zr=0.3, Nt=1024, TW=40.0), dict(N=20, zr=1.5, Nt=1024, TW=40.0), dict(N=10, zr=3.0, Nt=1024, TW=60.0)]
HBAR, KB = 1.054571817e-34, 1.380649e-23
a, b = 1 / 32e-15, 1 / 12.2e-15
c0 = 4 * a * 0.18 * KB * 300.0 / (HBAR * (a * a + b * b))
if sys.argv[1] == "predict":
    cr = sorted(json.load(open(os.path.join(SC, "curve_N200.json")))["rows"], key=lambda r: r["Z"])
    cZ = np.array([r["Z"] for r in cr]); fL = np.array([4 * r["Z"] ** 2 * r["Lambda_red"] for r in cr])
    pred = {}
    for c in cases:
        Z = c["zr"] * c["N"] * nd.xi_wb(c["N"])
        f = float(np.interp(Z, cZ, fL))
        pred[f"N{c['N']}_zr{c['zr']:g}"] = dict(Z=Z, Phi=c["N"] * Z, four_Z2_Lambda=f, rho_pred=float(np.sqrt(f)), c_hat0=c0,
                                                 dlam_min_pred=float(np.sqrt(f)) * c0 / (c["N"] * Z), tolerance_rel=0.15)
    json.dump(pred, open(os.path.join(HERE, "conjecture_predictions.json"), "w"), indent=1)
    print(json.dumps(pred, indent=1))
else:
    import raman_oracle as ro
    pred = json.load(open(os.path.join(HERE, "conjecture_predictions.json")))
    out = {}
    for c in cases:
        tag = f"N{c['N']}_zr{c['zr']:g}"
        g, J, alpha, W, info = ro.run_point(c["N"], c["zr"], [1000.0], Nt=c["Nt"], TW=c["TW"], every=16)
        k, *_ = ro.chain_with(g, J, alpha, np.zeros_like(W[1000.0]))
        r, *_ = ro.chain_with(g, J, alpha, W[1000.0])
        rho = (r["lam_min"] - k["lam_min"]) * info["Phi"] / c0
        p = pred[tag]
        out[tag] = dict(info, kerr=k, raman=r, rho=rho, rho_pred=p["rho_pred"], rel=rho / p["rho_pred"] - 1,
                        pass_=bool(abs(rho / p["rho_pred"] - 1) <= p["tolerance_rel"]))
        print(tag, "rho %.3f pred %.3f rel %+.3f %s" % (rho, p["rho_pred"], rho / p["rho_pred"] - 1, "PASS" if out[tag]["pass_"] else "FAIL"),
              "lam_min kerr %.5f raman %.5f" % (k["lam_min"], r["lam_min"]), flush=True)
    json.dump(out, open(os.path.join(HERE, "conjecture_summary.json"), "w"), indent=1, default=float)
