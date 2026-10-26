"""Compare the independent numpy split-step run with the FastDifferentiableMMNLO run (asymptotic seed, eps0 = 0.1, gL = 6)."""
import json, os
import numpy as np
import analyze_shape as A

D = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/")


def main():
    ref = A.load(D + "sm_asym_e0.1_g6_eta1e-4.json")
    zeta, maps, X0 = A.sim_maps(ref)
    M2s = maps[2]
    out = {}
    for n in (24000, 48000):
        p = D + f"xcheck_numpy_e0.1_n{n}.json"
        if not os.path.exists(p):
            continue
        x = json.load(open(p))
        M2n = np.array(x["M2"])
        err = [float(np.linalg.norm(M2n[k] - M2s[k]) / np.linalg.norm(M2s[k])) for k in range(len(M2s))]
        dT = float(np.max(np.abs(np.array(x["varT"]) / np.array(ref["ref"]["varT"]) - 1)))
        dW = float(np.max(np.abs(np.array(x["varW"]) / np.array(ref["ref"]["varW"]) - 1)))
        dC = float(np.max(np.abs(np.array(x["cov"]) - np.array(ref["ref"]["cov"])) / np.abs(np.array(ref["ref"]["cov"][1:]).min())))
        out[n] = dict(M2_max_rel_diff=max(err), varT_max_rel_diff=dT, varW_max_rel_diff=dW, cov_max_rel_diff=dC,
                      numpy_energy_err=x["energy_err"])
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
