"""summary.json for run 2026-10-10-claude-interactive.2-shape-modes (R2, R5) and the C-20261008-claude-a-02 P1 block table."""
import os, glob, json, math
import numpy as np
import run_analysis as R

HERE = os.path.dirname(os.path.abspath(__file__))
C02_P1 = {  # main case, unchirped: theta_L, M_0, M_2, M_3 on (p_l, n_l/eps0)
    2: dict(theta=1.2825, M0=[[1, 1.2825], [0, 1]], M2=[[-0.5929, 0.7947], [-1.4327, 0.2337]], M3=[[-1.4540, 0.4284], [-1.5309, -0.2367]]),
    4: dict(theta=5.8878, M0=[[1, 5.8878], [0, 1]], M2=[[-3.6111, 0.0441], [-0.1567, -0.2750]], M3=[[0.1955, -1.1041], [0.9355, -0.1679]]),
    6: dict(theta=20.4518, M0=[[1, 20.4518], [0, 1]], M2=[[-1.3858, -3.1045], [0.2516, -0.1579]], M3=[[7.7269, -0.4042], [0.1727, 0.1204]]),
}


def slope(e, v):
    e = np.array(e, float); v = np.abs(np.array(v, float))
    return float(np.polyfit(np.log(e), np.log(v), 1)[0]) if len(e) >= 2 else None


def main():
    out = dict(run_id="2026-10-10-claude-interactive.2-shape-modes", asym={}, main={}, eta_check={}, convergence={})
    for p in sorted(glob.glob(R.D + "*.json")):
        name = os.path.basename(p)[:-5]
        if name.startswith("xcheck_"):
            continue
        s = R.summarize(p)
        if name.startswith("conv_"):
            out["convergence"][name] = s
            continue
        tag = "eta1e-4" if name.endswith("eta1e-4") else "eta1e-3"
        if tag == "eta1e-3":
            out["eta_check"][name] = s
            continue
        out[s["case"]][str(s["eps0"])] = s
    # error exponents of the block maps (tau <= 4) over eps0, asymptotic seed
    expo = {}
    asym = out["asym"]
    for l in range(5):
        pts = sorted((float(e), v["blocks"][l]["err_at_tau4"]) for e, v in asym.items())
        if len(pts) >= 2:
            expo[f"l{l}"] = dict(eps0=[p[0] for p in pts], err=[p[1] for p in pts], slope=slope(*zip(*pts)))
    out["block_error_exponents_tau4"] = expo
    # C-02 P1 table against the main-case maps at gL = 2, 4, 6
    tab = {}
    for e, s in out["main"].items():
        rows = {}
        for U in (2, 4, 6):
            for l, key in ((0, "M0"), (2, "M2"), (3, "M3")):
                b = s["blocks"][l]
                Ms = np.array(b["M_sim_end"] if U == 6 else b[f"M_sim_gL{U}"])
                Mt = np.array(C02_P1[U][key])
                rows[f"gL{U}_{key}"] = dict(sim=Ms.tolist(), table=Mt.tolist(),
                                            rel_err=float(np.linalg.norm(Ms - Mt) / np.linalg.norm(Mt)))
        tab[e] = rows
    out["C02_P1_comparison"] = tab
    # linearity: eta = 1e-3 vs 1e-4 block maps
    lin = {}
    for name, s3 in out["eta_check"].items():
        e = str(s3["eps0"])
        if s3["case"] in out and e in out[s3["case"]]:
            s4 = out[s3["case"]][e]
            lin[name] = {l: float(np.linalg.norm(np.array(s3["blocks"][l]["M_sim_end"]) - np.array(s4["blocks"][l]["M_sim_end"])) /
                                  np.linalg.norm(np.array(s4["blocks"][l]["M_sim_end"]))) for l in range(5)}
    out["linearity_eta1e-3_vs_1e-4"] = lin
    try:
        import xcheck_compare as X
        out["second_solver_numpy"] = X.main()
    except Exception as ex:
        out["second_solver_numpy"] = f"not available ({ex})"
    with open(os.path.join(HERE, "summary.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    o = main()
    for k, v in o["block_error_exponents_tau4"].items():
        print(k, v["eps0"], np.round(v["err"], 5), "slope", None if v["slope"] is None else round(v["slope"], 2))
    for e, rows in o["C02_P1_comparison"].items():
        print("main eps0", e, {k: round(v["rel_err"], 4) for k, v in rows.items()})
    print("linearity", {k: {l: round(x, 5) for l, x in v.items()} for k, v in o["linearity_eta1e-3_vs_1e-4"].items()})
