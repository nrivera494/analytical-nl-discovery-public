"""Monte Carlo statistics (route i) with bootstrap errors, against the exact energy law and the adjoint (route ii)."""
import json, math, os
import numpy as np

HBAR = 1.054571817e-34
D = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/")


def seed_N0(eps0=0.1, Nt=1024, win=16.0, gam=1e-5, omega0=1e8):
    dt = win / Nt
    t = (np.arange(Nt) - Nt // 2) * dt
    P0 = 1.0 / (gam * eps0 ** 2)
    d = 0.5 * eps0 ** (2 / 3)
    u = 1 - t ** 2
    sp = np.where(u > 30 * d, u, d * np.log1p(np.exp(np.minimum(u / d, 700))))
    E = np.sum(P0 * sp) * dt
    return E * 1e-12 / (HBAR * omega0 * 1e12)


def load(case):
    a = np.loadtxt(D + case + ".csv", delimiter=",")
    return a[:, 1], a[:, 2], a[:, 3]


def boot(x, f, nb=400, seed=1):
    r = np.random.default_rng(seed)
    n = len(x)
    vals = [f(x[r.integers(0, n, n)]) for _ in range(nb)]
    return f(x), float(np.std(vals))


def stats(case, N0):
    N, T, W = load(case)
    fano = lambda x: N0 * np.var(x, ddof=1) / np.mean(x) ** 2
    return dict(n=len(N), F=boot(N, fano), VarT=boot(T, lambda x: N0 * np.var(x, ddof=1)),
                VarW=boot(W, lambda x: N0 * np.var(x, ddof=1)),
                Cov=boot(np.c_[T, W], lambda x: N0 * np.cov(x[:, 0], x[:, 1])[0, 1]))
