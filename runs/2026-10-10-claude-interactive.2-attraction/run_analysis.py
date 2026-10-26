"""R1 (width ODE and attraction), R3 (effective semiclassical parameter), R4 (energy mapping) summaries."""
import sys, os, glob, json, math
import numpy as np
import analyze_attraction as A

D = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/")


def r1_table():
    rows = []
    for p in sorted(glob.glob(D + "att_e*.json")):
        d = A.load(p); c = A.compare(d)
        w = (d["Gamma"] ** 2 / 18) ** (1 / 3)
        rows.append(dict(file=os.path.basename(p), eps0=d["eps0"], Gamma=d["Gamma"], q=d["q"], w=w,
                         s0=float(c["s"][0]), sp0=float(c["sp"][0]), err_s_rel=float(c["err_s_rel"]),
                         err_chirp_rel=float(c["err_chirp_rel"]), V_increase_max=c["V_increase_max"],
                         s_end=float(c["s_end"]), sp_end=float(c["sp_end"]), s_ode_end=float(c["s_ode_end"]),
                         sp_ode_end=float(c["sp_ode_end"]), V0=float(c["V"][0]), Vend=float(c["V"][-1]),
                         energy_err=d["energy_balance_rel_err"], edge_t=d["edge_time"], edge_w=d["edge_freq"]))
    return rows


def r3_table():
    out = {}
    for p in sorted(glob.glob(D + "att_e*_G4.243_q0.333.json")):
        d = A.load(p); r = d["rows"]
        tau = np.array(r["tau"]); vT = np.array(r["varT"]); vW = np.array(r["varW"]); cv = np.array(r["cov"])
        ftl = 1 - cv ** 2 / (vT * vW)
        edge = np.array(r["edge_rho"])
        sel = (tau >= 2) & (tau <= tau[-1])
        sl_tl = np.polyfit(tau[sel], np.log(ftl[sel]), 1)[0]
        sl_edge = np.polyfit(tau[sel], np.log(edge[sel]), 1)[0]
        # predicted local eps_eff^2 = b2/(gam P_pk T_p^2) from the simulated peak and width
        P = d["params"]
        Tp = np.sqrt(5 * vT); pk = np.array(r["fit_peak"])
        eeff = np.sqrt(P["b2"] / (P["gam"] * pk * Tp ** 2))
        sl_eeff = np.polyfit(tau[sel], np.log(eeff[sel]), 1)[0]
        out[d["eps0"]] = dict(tau=tau[::24].tolist(), ftl=ftl[::24].tolist(), edge=edge[::24].tolist(),
                              eeff=eeff[::24].tolist(), slope_ftl=float(sl_tl), slope_edge=float(sl_edge),
                              slope_eeff=float(sl_eeff), ftl_over_eeff2_end=float(ftl[-1] / eeff[-1] ** 2),
                              edge_over_eeff23_end=float(edge[-1] / eeff[-1] ** (2 / 3)))
    return out


def r4_table():
    out = {}
    for e in ("0.1", "0.05", "0.025"):
        fp, fm = D + f"r4_e{e}_E1.001.json", D + f"r4_e{e}_E0.999.json"
        if not (os.path.exists(fp) and os.path.exists(fm)):
            continue
        dp, dm = A.load(fp), A.load(fm)
        rp, rm = dp["rows"], dm["rows"]
        dl = math.log(1.001) - math.log(0.999)
        tau = np.array(rp["tau"])
        f = lambda key, fun: (np.log(fun(rp)) - np.log(fun(rm))) / dl
        Tp = f("w", lambda r: np.sqrt(5 * np.array(r["varT"])))
        pk = f("pk", lambda r: np.array(r["fit_peak"]))
        bw = f("bw", lambda r: np.sqrt(np.array(r["varW"])))
        ch = f("ch", lambda r: np.array(r["cov"]) / np.array(r["varT"]))
        P = dp["params"]
        chirp_val = np.array(rp["cov"]) / np.array(rp["varT"]) / (P["g"] / (3 * P["b2"]))
        # hydrodynamic (width-ODE) prediction of the same log-derivatives, from each run's own initial moments
        hyd = {}
        for lab, d_ in (("p", dp), ("m", dm)):
            t_, s_, sp_, ch_, c_ = A.sim_s(d_)
            so, spo = A.ode_s(s_[0], sp_[0], t_)
            b = c_ * np.exp(t_ / 3) * so
            bp = c_ * np.exp(t_ / 3) * (spo + so / 3)        # db/dtau
            E = np.array(d_["rows"]["E"])
            hyd[lab] = dict(b=b, bp=bp, pk=3 * E / (4 * b))
        hTp = (np.log(hyd["p"]["b"]) - np.log(hyd["m"]["b"])) / dl
        hPk = (np.log(hyd["p"]["pk"]) - np.log(hyd["m"]["pk"])) / dl
        hBW = (np.log(hyd["p"]["bp"]) - np.log(hyd["m"]["bp"])) / dl
        hCh = (np.log(hyd["p"]["bp"] / hyd["p"]["b"]) - np.log(hyd["m"]["bp"] / hyd["m"]["b"])) / dl
        idx = [int(np.argmin(np.abs(tau - t))) for t in (0, 2, 4, 6)]
        # asymptote by linear least squares with the predicted l=2 rate and frequency: y = yinf + e^{-tau/3}(A cos + B sin)
        selr = tau >= 1.0
        w2 = math.sqrt(2) / 3
        X = np.c_[np.ones(selr.sum()), np.exp(-tau[selr] / 3) * np.cos(w2 * tau[selr]), np.exp(-tau[selr] / 3) * np.sin(w2 * tau[selr])]
        yinf = {k: float(np.linalg.lstsq(X, v[selr], rcond=None)[0][0]) for k, v in (("dlnTp", Tp), ("dlnPk", pk), ("dlnBW", bw), ("dlnChirp", ch))}
        res = {k: float(np.sqrt(np.mean((X @ np.linalg.lstsq(X, v[selr], rcond=None)[0] - v[selr]) ** 2)))
               for k, v in (("dlnTp", Tp), ("dlnPk", pk), ("dlnBW", bw), ("dlnChirp", ch))}
        out[e] = dict(asymptote_fit=yinf, asymptote_fit_rms_resid=res, tau=[float(tau[i]) for i in idx], dlnTp=[float(Tp[i]) for i in idx], dlnPk=[float(pk[i]) for i in idx],
                      dlnBW=[float(bw[i]) for i in idx], dlnChirp=[float(ch[i]) for i in idx],
                      chirp_over_g3b2=[float(chirp_val[i]) for i in idx],
                      hydro_dlnTp=[float(hTp[i]) for i in idx], hydro_dlnPk=[float(hPk[i]) for i in idx],
                      hydro_dlnBW=[float(hBW[i]) for i in idx], hydro_dlnChirp=[float(hCh[i]) for i in idx])
    return out


if __name__ == "__main__":
    for r in r1_table():
        print("%-34s w=%.2f q=%5.2f s0=%.3f sp0=%6.3f errs=%.2e errchirp=%.2e dVmax=%.1e s_end=%.4f(ode %.4f) sp_end=%.4f(ode %.4f) V %.4f->%.4f" % (
            r["file"], r["w"], r["q"], r["s0"], r["sp0"], r["err_s_rel"], r["err_chirp_rel"], r["V_increase_max"],
            r["s_end"], r["s_ode_end"], r["sp_end"], r["sp_ode_end"], r["V0"], r["Vend"]))
    print(json.dumps(r3_table(), indent=0)[:1500])
    print(json.dumps(r4_table(), indent=0))
