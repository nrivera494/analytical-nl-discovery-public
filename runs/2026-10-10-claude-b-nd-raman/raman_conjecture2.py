"""Second frozen test of C-20261010-claude-b-03 (claude-b, T-20261010-claude-interactive-05): N = 28, z/z_wb = 0.7,
T0 = 1 ps, 300 K, Nt 1024 over 40 T0. Prediction (mode 'predict', committed before 'run'): rho = sqrt(4 Z^2 Lambda(Z))
within 10 %. Usage: python raman_conjecture2.py predict | run"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SC = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-semiclassical")
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import nd_cov as nd
HBAR, KB = 1.054571817e-34, 1.380649e-23
a, b = 1 / 32e-15, 1 / 12.2e-15
c0 = 4 * a * 0.18 * KB * 300.0 / (HBAR * (a * a + b * b))
N, zr = 28, 0.7
if sys.argv[1] == "predict":
    cr = sorted(json.load(open(os.path.join(SC, "curve_N200.json")))["rows"], key=lambda r: r["Z"])
    cZ = np.array([r["Z"] for r in cr]); fL = np.array([4 * r["Z"] ** 2 * r["Lambda_red"] for r in cr])
    Z = zr * N * nd.xi_wb(N)
    f = float(np.interp(Z, cZ, fL))
    pred = dict(N=N, zr=zr, Z=Z, Phi=N * Z, rho_pred=float(np.sqrt(f)), c_hat0=c0, tolerance_rel=0.10)
    json.dump(pred, open(os.path.join(HERE, "conjecture2_predictions.json"), "w"), indent=1)
    print(pred)
else:
    import raman_oracle as ro
    p = json.load(open(os.path.join(HERE, "conjecture2_predictions.json")))
    g, J, alpha, W, info = ro.run_point(N, zr, [1000.0], Nt=1024, every=16)
    k, *_ = ro.chain_with(g, J, alpha, np.zeros_like(W[1000.0]))
    r, *_ = ro.chain_with(g, J, alpha, W[1000.0])
    rho = (r["lam_min"] - k["lam_min"]) * info["Phi"] / c0
    out = dict(info, kerr=k, raman=r, rho=rho, rho_pred=p["rho_pred"], rel=rho / p["rho_pred"] - 1,
               pass_=bool(abs(rho / p["rho_pred"] - 1) <= p["tolerance_rel"]))
    json.dump(out, open(os.path.join(HERE, "conjecture2_summary.json"), "w"), indent=1, default=float)
    print("rho %.4f pred %.4f rel %+.4f %s" % (rho, p["rho_pred"], out["rel"], "PASS" if out["pass_"] else "FAIL"))
