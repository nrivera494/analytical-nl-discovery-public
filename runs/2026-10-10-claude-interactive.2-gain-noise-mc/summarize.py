"""summary.json for run 2026-10-10-claude-interactive.2-gain-noise-mc: MC (route i) vs exact energy law and adjoint (route ii)."""
import os, json, math
import numpy as np
from scipy import stats as st
import analyze_mc as M

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = {  # name: (shot-noise scale, GainLangevin n_s, kerr)
    "kerr_ns0.5": (0.5, 0.5, "kerr"), "kerr_ns1.0": (0.5, 1.0, "kerr"), "kerr_vac": (0.5, 0.0, "kerr"),
    "kerr_ase": (0.0, 0.5, "kerr"), "lin_ns0.5": (0.5, 0.5, "lin"), "lin_ns1.0": (0.5, 1.0, "lin")}


def load_all(name):
    parts = []
    for suf in ("", "_b", "_c"):
        p = M.D + name + suf + ".csv"
        if os.path.exists(p) and os.path.getsize(p) > 0:
            parts.append(np.loadtxt(p, delimiter=",", ndmin=2))
    return np.vstack(parts) if parts else None


def main():
    ad = json.load(open(M.D + "mc_adjoint.json"))
    N0 = M.seed_N0()
    G = math.exp(4.0)
    out = dict(run_id="2026-10-10-claude-interactive.2-gain-noise-mc", N0=N0, G=G, nsp_map="n_sp = 2 n_s^2 + 1/2", cases={})
    for name, (sv, ns, k) in CASES.items():
        a = load_all(name)
        if a is None:
            continue
        N, T, W = a[:, 1], a[:, 2], a[:, 3]
        nsp = 2 * ns * ns + 0.5
        f = 2 * nsp - 1 if ns > 0 else 0.0
        vin = 1.0 if sv > 0 else 0.0
        A = ad[k]
        fano = lambda x: N0 * np.var(x, ddof=1) / np.mean(x) ** 2
        F = M.boot(N, fano)
        pred_F = vin + f * (1 - 1 / G)
        res = dict(ntraj=int(len(N)), n_s=ns, n_sp=nsp if ns > 0 else None, shot_noise=sv, kerr=(k == "kerr"),
                   F=F, F_pred_exact=pred_F, F_ratio=F[0] / pred_F, F_ratio_err=F[1] / pred_F)
        for q, key, arr in (("VarTc", "Tc_Tc", T), ("VarWc", "Wc_Wc", W)):
            v = M.boot(arr, lambda x: N0 * np.var(x, ddof=1))
            p = N0 * (vin * A[key][0] + f * A[key][1])
            res[q] = dict(mc=v, adjoint=p, ratio=v[0] / p, ratio_err=v[1] / p)
        c = M.boot(np.c_[T, W], lambda x: N0 * np.cov(x[:, 0], x[:, 1])[0, 1])
        pc = N0 * (vin * A["Tc_Wc"][0] + f * A["Tc_Wc"][1])
        res["CovTW"] = dict(mc=c, adjoint=pc, ratio=c[0] / pc, ratio_err=c[1] / pc)
        res["gaussianity"] = dict(skew_T=float(st.skew(T)), skew_W=float(st.skew(W)), skew_N=float(st.skew(N)),
                                  exkurt_T=float(st.kurtosis(T)), exkurt_W=float(st.kurtosis(W)), exkurt_N=float(st.kurtosis(N)),
                                  skew_se=float(math.sqrt(6 / len(N))), exkurt_se=float(math.sqrt(24 / len(N))))
        out["cases"][name] = res
    # joint weighted fit of MC variances to a*(input part) + b*(2n_sp-1)*(ASE part) of the adjoint (Kerr-on cases)
    fits = {}
    for q, key in (("VarTc", "Tc_Tc"), ("VarWc", "Wc_Wc")):
        X, y, w = [], [], []
        for name, (sv, ns, k) in CASES.items():
            if name not in out["cases"] or k != "kerr":
                continue
            r = out["cases"][name]
            nsp = 2 * ns * ns + 0.5
            f = 2 * nsp - 1 if ns > 0 else 0.0
            vin = 1.0 if sv > 0 else 0.0
            A = ad["kerr"]
            X.append([vin * N0 * A[key][0], f * N0 * A[key][1]]); y.append(r[q]["mc"][0]); w.append(1 / r[q]["mc"][1] ** 2)
        X, y, w = np.array(X), np.array(y), np.array(w)
        Wm = np.diag(w)
        cov = np.linalg.inv(X.T @ Wm @ X)
        ab = cov @ X.T @ Wm @ y
        chi2 = float(((y - X @ ab) ** 2 * w).sum())
        fits[q] = dict(a_input=float(ab[0]), a_err=float(math.sqrt(cov[0, 0])), b_ase=float(ab[1]), b_err=float(math.sqrt(cov[1, 1])),
                       chi2=chi2, dof=int(len(y) - 2))
    out["joint_fit_scale_factors"] = fits
    out["adjoint_parts"] = {k: {q: [N0 * x for x in ad[k][q]] if q != "N_N" else [N0 * x / ad[k]["NL"] ** 2 for x in ad[k][q]]
                                for q in ("N_N", "Tc_Tc", "Wc_Wc", "Tc_Wc")} for k in ("kerr", "lin")}
    with open(os.path.join(HERE, "summary.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    return out


if __name__ == "__main__":
    o = main()
    for k, r in o["cases"].items():
        print("%-11s n=%5d F=%.4f+-%.4f pred %.4f ratio %.3f+-%.3f | T ratio %.3f+-%.3f | W ratio %.3f+-%.3f | C ratio %.3f+-%.3f" % (
            k, r["ntraj"], r["F"][0], r["F"][1], r["F_pred_exact"], r["F_ratio"], r["F_ratio_err"], r["VarTc"]["ratio"],
            r["VarTc"]["ratio_err"], r["VarWc"]["ratio"], r["VarWc"]["ratio_err"], r["CovTW"]["ratio"], r["CovTW"]["ratio_err"]))
