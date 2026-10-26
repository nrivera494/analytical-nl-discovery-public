"""More points for the Raman floor law (claude-b, T-20261010-claude-interactive-05): lambda_min, lambda_pass,
lambda_gen and the centroid with the coth reservoir (300 K) at T0 = 100 fs and 1 ps, no binary search.
Usage: python raman_more.py -> summary_more.json"""
import json, os, time
import numpy as np
import raman_oracle as ro
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for N, zr in ((5, 0.7), (10, 0.3), (10, 1.5), (14, 0.7)):
    t0 = time.time()
    g, J, alpha, W, info = ro.run_point(N, zr, [100.0, 1000.0], Nt=512, every=16)
    k, *_ = ro.chain_with(g, J, alpha, np.zeros_like(W[100.0]))
    res = dict(info, kerr=k)
    for T0 in (100.0, 1000.0):
        ch, *_ = ro.chain_with(g, J, alpha, W[T0])
        res[str(T0)] = ch
        res[str(T0) + "_dlam_min_times_Phi"] = (ch["lam_min"] - k["lam_min"]) * info["Phi"]
    res["wall"] = time.time() - t0
    out[f"N{N}_zr{zr:g}"] = res
    print(f"N{N}_zr{zr:g}", "Phi %.2f Z %.3f" % (info["Phi"], info["Z"]), "kerr lam_min %.5f" % k["lam_min"],
          " | ".join("T0 %g: lam_min %.5f dlam*Phi %.4f lam_gen %.5f" % (T0, res[str(T0)]["lam_min"], res[str(T0) + "_dlam_min_times_Phi"], res[str(T0)]["lam_gen"]) for T0 in (100.0, 1000.0)), "%.0fs" % res["wall"], flush=True)
json.dump(out, open(os.path.join(HERE, "summary_more.json"), "w"), indent=1, default=float)
