"""Summaries for R2/R5 from shapemodes.jl outputs: block-map errors, rates, gains, mixing."""
import sys, json, math, glob, os
import numpy as np
import analyze_shape as A
from scipy.linalg import logm

D = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/")
OM = {2: math.sqrt(2) / 3, 3: math.sqrt(5) / 3, 4: 1.0}


def summarize(path):
    d = A.load(path)
    eps0 = d["eps0"]; g = d["params"]["g"]
    zeta, maps, X0 = A.sim_maps(d)
    tau = np.array(d["ref"]["tau"])
    E = np.array(d["ref"]["E"]); G = E / E[0]
    out = dict(eps0=eps0, case=d["case"], tau_end=float(tau[-1]), blocks={})
    R = d["readouts_p0to4_n0to4"]
    for l in range(5):
        Mo, a = A.ode_maps(d, zeta, l)
        Ms = maps[l]
        err = np.array([np.linalg.norm(Ms[k] - Mo[k]) / np.linalg.norm(Mo[k]) for k in range(len(zeta))])
        sv_s = np.linalg.svd(Ms[-1], compute_uv=False); sv_o = np.linalg.svd(Mo[-1], compute_uv=False)
        U = math.log(G[-1])
        expo = lambda sv: [(U + 2 * math.log(s)) / U for s in sv]   # photon-normalized power-gain exponents
        blk = dict(max_rel_err=float(err.max()), end_rel_err=float(err[-1]), err_at_tau4=float(err[tau <= 4 + 1e-9].max()), M_sim_end=Ms[-1].tolist(), M_ode_end=Mo[-1].tolist(),
                   det_sim_end=float(np.linalg.det(Ms[-1])), gain_exp_sim=expo(sv_s), gain_exp_ode=expo(sv_o))
        for gl in (2.0, 4.0):
            k = int(np.argmin(np.abs(tau - gl)))
            blk[f"M_sim_gL{int(gl)}"] = Ms[k].tolist(); blk[f"M_ode_gL{int(gl)}"] = Mo[k].tolist()
        if l >= 2:
            # generator of the late-window map in scaled variables (P, M) = (e^{-tau/3} p, e^{tau/3} n/eps0):
            # on the exact asymptote it is constant with eigenvalues +-i (1/3) sqrt(l(l+1)/2 - 1); n_l then decays at
            # 1/3 - tr(K)/2 and oscillates at Im(eig)
            def gen(Mz):
                k1 = int(np.argmin(np.abs(tau - 3.0))); k2 = len(tau) - 1
                Sc = lambda k: np.diag([math.exp(-tau[k] / 3), math.exp(tau[k] / 3)])
                Phi = Sc(k2) @ Mz[k2] @ np.linalg.inv(Mz[k1]) @ np.linalg.inv(Sc(k1))
                K = logm(Phi).real / (tau[k2] - tau[k1])
                ev = np.linalg.eigvals(K)
                return dict(decay=float(1 / 3 - np.trace(K) / 2), omega=float(np.max(np.abs(ev.imag))),
                            eig=[complex(x).real for x in ev] + [complex(x).imag for x in ev])
            blk["generator_tau3to6"] = dict(sim=gen(Ms), ode=gen(Mo))
            fits = {}
            for lab, col in (("ph", 0), ("int", 1)):
                ys = Ms[:, 1, col]; yo = Mo[:, 1, col]       # n_l/eps0 response
                xs, rs = A.fit_rate(tau, ys); xo, ro = A.fit_rate(tau, yo)
                fits[lab] = dict(sim_alpha=float(xs[0]), sim_omega=float(abs(xs[1])), sim_resid=float(rs),
                                 ode_alpha=float(xo[0]), ode_omega=float(abs(xo[1])), ode_resid=float(ro))
            blk["rate_fit"] = fits; blk["pred_alpha"] = 1 / 3; blk["pred_omega"] = OM[l]
        out["blocks"][l] = blk
    # mixing: int_l launches excite blocks l-2, l+2; compare measured response there with that block's own map
    mix = {}
    for l in range(5):
        it = np.array(R[f"int{l}"])
        for lp in (l - 2, l + 2, l - 1, l + 1):
            if lp < 0 or lp > 4:
                continue
            x0 = np.array([it[0, lp], it[0, 5 + lp] / eps0]); xe = np.array([it[-1, lp], it[-1, 5 + lp] / eps0])
            pred = maps[lp][-1] @ x0
            scale = np.linalg.norm(maps[l][-1] @ np.array([it[0, l], it[0, 5 + l] / eps0]))
            mix[f"int{l}->block{lp}"] = dict(meas=xe.tolist(), pred=pred.tolist(),
                                             resid_rel_to_driven=float(np.linalg.norm(xe - pred) / scale))
        ph = np.array(R[f"ph{l}"])
        for lp in range(5):
            if lp == l:
                continue
            xe = np.array([ph[-1, lp], ph[-1, 5 + lp] / eps0])
            scale = np.linalg.norm(maps[l][-1] @ np.array([ph[0, l], ph[0, 5 + l] / eps0]))
            x0 = np.array([ph[0, lp], ph[0, 5 + lp] / eps0])
            pred = maps[lp][-1] @ x0
            mix[f"ph{l}->block{lp}"] = dict(resid_rel_to_driven=float(np.linalg.norm(xe - pred) / scale))
    out["mixing"] = mix
    out["mixing_max"] = max(v["resid_rel_to_driven"] for v in mix.values())
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        s = summarize(p)
        print(os.path.basename(p), "eps0", s["eps0"], "mixing_max %.2e" % s["mixing_max"])
        for l, b in s["blocks"].items():
            line = "  l=%d maxrelerr=%.3e end=%.3e det=%.6f gainexp sim=%s ode=%s" % (
                l, b["max_rel_err"], b["end_rel_err"], b["det_sim_end"],
                np.round(b["gain_exp_sim"], 4), np.round(b["gain_exp_ode"], 4))
            print(line)
            if "rate_fit" in b:
                for lab, f in b["rate_fit"].items():
                    print("     %s: sim alpha=%.4f omega=%.4f (res %.1e) | ode alpha=%.4f omega=%.4f | pred 0.3333 %.4f" % (
                        lab, f["sim_alpha"], f["sim_omega"], f["sim_resid"], f["ode_alpha"], f["ode_omega"], b["pred_omega"]))
