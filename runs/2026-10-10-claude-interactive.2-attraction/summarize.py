"""summary.json for run 2026-10-10-claude-interactive.2-attraction (R1, R3, R4)."""
import os, json, math
import numpy as np
import run_analysis as R

HERE = os.path.dirname(os.path.abspath(__file__))


def slope(e, v):
    e = np.array(e, float); v = np.abs(np.array(v, float))
    return float(np.polyfit(np.log(e), np.log(v), 1)[0]) if len(e) >= 2 else None


def main():
    r1 = R.r1_table()
    groups = {}
    for r in r1:
        groups.setdefault((round(r["Gamma"], 3), round(r["q"], 3)), []).append(r)
    expo = {}
    for k, v in groups.items():
        v = sorted(v, key=lambda x: x["eps0"])
        if len(v) >= 2:
            expo[f"Gamma{k[0]}_q{k[1]}"] = dict(eps0=[x["eps0"] for x in v], err_s_rel=[x["err_s_rel"] for x in v],
                                                 err_chirp=[x["err_chirp_rel"] for x in v],
                                                 slope_s=slope([x["eps0"] for x in v], [x["err_s_rel"] for x in v]),
                                                 slope_chirp=slope([x["eps0"] for x in v], [x["err_chirp_rel"] for x in v]))
    import glob as _g
    longr = {}
    for p in sorted(_g.glob(R.D + "long_*.json")):
        d = R.A.load(p); c = R.A.compare(d)
        idx = [int(np.argmin(np.abs(c["tau"] - t))) for t in (0, 2, 4, 6, 8, 10)]
        longr[os.path.basename(p)[:-5]] = dict(tau=[float(c["tau"][i]) for i in idx], s=[float(c["s"][i]) for i in idx],
                                               s_ode=[float(c["s_ode"][i]) for i in idx], sp=[float(c["sp"][i]) for i in idx],
                                               V=[float(c["V"][i]) for i in idx], err_s_rel=float(c["err_s_rel"]),
                                               V_increase_max=c["V_increase_max"], energy_err=d["energy_balance_rel_err"])
    out = dict(run_id="2026-10-10-claude-interactive.2-attraction", R1_long=longr, R1_runs=r1, R1_error_exponents=expo,
               R1_max_V_increase=max(r["V_increase_max"] for r in r1),
               R3=R.r3_table(), R4=R.r4_table())
    with open(os.path.join(HERE, "summary.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    o = main()
    for k, v in sorted(o["R1_error_exponents"].items()):
        print(k, v["eps0"], np.round(v["err_s_rel"], 5), "slope_s", None if v["slope_s"] is None else round(v["slope_s"], 2),
              "chirp", np.round(v["err_chirp"], 4), "slope", None if v["slope_chirp"] is None else round(v["slope_chirp"], 2))
    print("max V increase", o["R1_max_V_increase"])
    for e, v in o["R3"].items():
        print("R3", e, "slope_ftl %.3f slope_edge %.3f slope_eeff %.3f" % (v["slope_ftl"], v["slope_edge"], v["slope_eeff"]))
    for e, v in o["R4"].items():
        print("R4", e, {k: round(x, 4) for k, x in v["asymptote_fit"].items()})
