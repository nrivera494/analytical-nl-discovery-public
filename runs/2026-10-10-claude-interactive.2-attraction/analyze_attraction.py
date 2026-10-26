"""R1/R3/R4 analysis: compare full-NLSE rms width and chirp with the width ODE
s'' + (2/3) s' + s/9 = 1/(9 s^2), s = b/(c e^{tau/3}), b = sqrt(5 varT), c^3 = 27 gam b2 E0/(2 g^2)."""
import json, math
import numpy as np


def load(p):
    with open(p) as f:
        return json.load(f)


def sim_s(d):
    r = d["rows"]; P = d["params"]
    g, b2, gam = P["g"], P["b2"], P["gam"]
    E0 = r["E"][0]
    c = (27 * gam * b2 * E0 / (2 * g * g)) ** (1 / 3)
    tau = np.array(r["tau"])
    varT = np.array(r["varT"]); cov = np.array(r["cov"])
    b = np.sqrt(5 * varT)
    dbdz = math.sqrt(5) * b2 * cov / np.sqrt(varT)        # exact virial: d varT/dz = 2 b2 cov
    s = b / (c * np.exp(tau / 3))
    sp = (dbdz / g) / (c * np.exp(tau / 3)) - s / 3          # ds/dtau
    chirp = b2 * cov / varT                                   # (d omega/dT) * b2 = b'/b  [1/m]
    return tau, s, sp, chirp, c


def ode_s(s0, sp0, tau):
    """RK4 on a fine grid, sampled at tau."""
    n = 20000
    T = tau[-1]; h = T / n
    f = lambda y: np.array([y[1], -2 / 3 * y[1] - y[0] / 9 + 1 / (9 * y[0] ** 2)])
    y = np.array([s0, sp0]); ys = [y.copy()]; ts = [0.0]
    for i in range(n):
        k1 = f(y); k2 = f(y + h / 2 * k1); k3 = f(y + h / 2 * k2); k4 = f(y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); ys.append(y.copy()); ts.append((i + 1) * h)
    ys = np.array(ys); ts = np.array(ts)
    return np.interp(tau, ts, ys[:, 0]), np.interp(tau, ts, ys[:, 1])


def compare(d):
    tau, s, sp, chirp, c = sim_s(d)
    so, spo = ode_s(s[0], sp[0], tau)
    g = d["params"]["g"]
    chirp_ode = g * (spo / so + 1 / 3)
    V = 0.5 * sp ** 2 + s ** 2 / 18 + 1 / (9 * s)
    return dict(tau=tau, s=s, sp=sp, s_ode=so, sp_ode=spo, err_s=np.max(np.abs(s - so)),
                err_s_rel=np.max(np.abs(s / so - 1)), err_chirp_rel=np.max(np.abs(chirp - chirp_ode)) / (g / 3),
                V=V, V_increase_max=float(np.max(np.diff(V))), s_end=s[-1], sp_end=sp[-1],
                s_ode_end=so[-1], sp_ode_end=spo[-1])
