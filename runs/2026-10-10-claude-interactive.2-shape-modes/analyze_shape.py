"""R2/R5 analysis: full-NLSE block maps of (p_l, n_l/eps0) against the reduced block ODE of C-20261008-claude-a-02 (a):
dp/dzeta = kE e^{Gamma zeta}/a * (n/eps0),  d(n/eps0)/dzeta = -l(l+1)/a^2 p,
with a(zeta) the hydrodynamic width started from the simulated seed's rms moments, a'' = 2 kE e^{Gamma zeta}/a^2."""
import json, math
import numpy as np
from scipy.linalg import logm
from scipy.optimize import least_squares


def load(p):
    with open(p) as f:
        return json.load(f)


def sim_maps(d):
    """Returns zeta grid and dict l -> array (nz, 2, 2) of measured maps M(zeta) on (p_l, m_l = n_l/eps0)."""
    eps0 = d["eps0"]; P = d["params"]
    g = P["g"]; sq = eps0  # sqrt(L_D L_NL) in m (T0 = b2 = 1)
    z = np.array(d["ref"]["z"]); zeta = z / sq
    R = d["readouts_p0to4_n0to4"]
    maps = {}; X0s = {}
    for l in range(5):
        ph = np.array(R[f"ph{l}"]); it = np.array(R[f"int{l}"])   # (nz, 10)
        X = np.zeros((len(z), 2, 2))
        X[:, 0, 0] = ph[:, l]; X[:, 1, 0] = ph[:, 5 + l] / eps0
        X[:, 0, 1] = it[:, l]; X[:, 1, 1] = it[:, 5 + l] / eps0
        X0inv = np.linalg.inv(X[0])
        maps[l] = np.einsum("kij,jm->kim", X, X0inv)
        X0s[l] = X[0]
    return zeta, maps, X0s


def background(d):
    eps0 = d["eps0"]; P = d["params"]; Gamma = P["Gamma"]
    ref = d["ref"]
    E0 = ref["E"][0]; Eref = 4 / 3 * P["P0"] * P["T0"]
    kE = E0 / Eref
    a0 = math.sqrt(5 * ref["varT"][0]) / P["T0"]
    ap0 = eps0 * math.sqrt(5) * P["b2"] * ref["cov"][0] / math.sqrt(ref["varT"][0])  # da/dzeta
    return Gamma, kE, a0, ap0


def ode_maps(d, zeta_out, l):
    Gamma, kE, a0, ap0 = background(d)
    n = 40000
    Z = zeta_out[-1]; h = Z / n

    def f(zt, y):
        a, ap, p1, m1, p2, m2 = y
        return np.array([ap, 2 * kE * math.exp(Gamma * zt) / a ** 2,
                         kE * math.exp(Gamma * zt) / a * m1, -l * (l + 1) / a ** 2 * p1,
                         kE * math.exp(Gamma * zt) / a * m2, -l * (l + 1) / a ** 2 * p2])
    y = np.array([a0, ap0, 1.0, 0.0, 0.0, 1.0]); out = [y.copy()]; zz = [0.0]
    for i in range(n):
        zt = i * h
        k1 = f(zt, y); k2 = f(zt + h / 2, y + h / 2 * k1); k3 = f(zt + h / 2, y + h / 2 * k2); k4 = f(zt + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); out.append(y.copy()); zz.append((i + 1) * h)
    out = np.array(out); zz = np.array(zz)
    M = np.zeros((len(zeta_out), 2, 2))
    for j, (r, c) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
        M[:, r, c] = np.interp(zeta_out, zz, out[:, 2 + j])
    a = np.interp(zeta_out, zz, out[:, 0])
    return M, a


def fit_rate(tau, y):
    """Fit y = e^{-alpha tau}(A cos w tau + B sin w tau) (free alpha, w, A, B)."""
    def res(x):
        al, w, A, B = x
        return np.exp(-al * tau) * (A * np.cos(w * tau) + B * np.sin(w * tau)) - y
    best = None
    for w0 in (0.2, 0.5, 0.8, 1.1):
        r = least_squares(res, [0.33, w0, y[0], 0.0], x_scale="jac")
        if best is None or r.cost < best.cost:
            best = r
    return best.x, math.sqrt(2 * best.cost / len(tau)) / (np.max(np.abs(y)) + 1e-300)
