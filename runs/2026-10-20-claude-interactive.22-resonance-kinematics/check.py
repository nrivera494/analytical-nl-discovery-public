"""Small kinematic checks for the 2026-10-20 longstanding-thermalization scouting review
(T-20261020-claude-interactive-04, agent claude-interactive.22).

(1) Single-mode fibre, k(w) = b2 w^2/2 + b3 w^3/6: factorization of the four-wave
    mismatch on the frequency-conservation shell (candidate S5 in the review).
    Same for k(w) = b2 w^2/2 + b4 w^4/24.
(2) Fibre-loop mesh lattice (Regensburger-type), Floquet bands cos(theta) = cos(beta) cos(Q):
    are quasi-energy "Umklapp" four-wave resonances, theta1+theta2-theta3-theta4 = +-2pi
    with Q1+Q2 = Q3+Q4 (mod 2pi), kinematically open? (candidate N1)
(3) Same lattice on a ring of L sites: number of normal and Umklapp quasi-resonant quartets
    within a tolerance, unweighted and weighted by |T|^2, where T is the on-site Kerr vertex
    T = sum_c phi1c* phi2c* phi3c phi4c over the two loop components c = u, v.

Run: ~/agent-work/venv/bin/python -W ignore check.py   (writes summary.json)
"""
import json
import numpy as np
import sympy as sp

out = {}

# (1) dispersion factorizations
w1, w2, w3, b2, b3, b4 = sp.symbols('w1 w2 w3 b2 b3 b4', real=True)
w4 = w1 + w2 - w3
k3 = lambda w: b2 * w**2 / 2 + b3 * w**3 / 6
k4 = lambda w: b2 * w**2 / 2 + b4 * w**4 / 24
dk3 = sp.factor(sp.expand(k3(w1) + k3(w2) - k3(w3) - k3(w4)))
dk4 = sp.factor(sp.expand(k4(w1) + k4(w2) - k4(w3) - k4(w4)))
expected3 = -(w1 - w3) * (w2 - w3) * (2 * b2 + b3 * (w1 + w2)) / 2
out['beta3_mismatch_factored'] = str(dk3)
out['beta3_equals_-(w1-w3)(w2-w3)(2b2+b3(w1+w2))/2'] = bool(sp.simplify(dk3 - expected3) == 0)
out['beta4_mismatch_factored'] = str(dk4)


# (2) mesh-lattice Floquet bands
def floquet(beta, Q):
    """Eigen-decomposition of the one-step map for plane waves exp(iQn)."""
    M = np.array([[np.exp(1j * Q) * np.cos(beta), 1j * np.exp(1j * Q) * np.sin(beta)],
                  [1j * np.exp(-1j * Q) * np.sin(beta), np.exp(-1j * Q) * np.cos(beta)]])
    lam, vec = np.linalg.eig(M)
    th = np.angle(lam)
    order = np.argsort(-th)          # upper band first
    return th[order], vec[:, order]


kin = {}
for beta_deg in [15, 30, 45, 60, 75]:
    beta = np.deg2rad(beta_deg)
    top = np.pi - beta                # upper band is [beta, pi - beta]
    span = 4 * top                    # max(theta1+theta2) - min(theta3+theta4)
    kin[str(beta_deg)] = {'upper_band_rad': [float(beta), float(top)],
                          'max_mismatch_over_2pi': float(span / (2 * np.pi)),
                          'umklapp_open': bool(span >= 2 * np.pi),
                          'edge_quartet_(Q=pi,Q=pi)->(Q=0,Q=0)_mismatch_over_2pi':
                              float((2 * top - (-2 * beta)) / (2 * np.pi))}
out['mesh_lattice_kinematics'] = kin


# (3) counts on a ring
def count(L, beta, tol):
    Qs = 2 * np.pi * np.arange(L) / L
    th = np.zeros((L, 2)); ph = np.zeros((L, 2, 2), complex)
    for q in range(L):
        t, v = floquet(beta, Qs[q])
        th[q] = t; ph[q] = v
    states = [(q, b) for q in range(L) for b in range(2)]
    n_norm = n_umk = 0; w_norm = w_umk = 0.0
    for i, (q1, s1) in enumerate(states):
        for j in range(i, len(states)):
            q2, s2 = states[j]
            qsum = (q1 + q2) % L
            tsum = th[q1, s1] + th[q2, s2]
            for a, (q3, s3) in enumerate(states):
                q4 = (qsum - q3) % L
                for s4 in range(2):
                    b = 2 * q4 + s4
                    if b < a or {i, j} == {a, b}:
                        continue
                    mism = tsum - th[q3, s3] - th[q4, s4]
                    T = np.sum(np.conj(ph[q1][:, s1]) * np.conj(ph[q2][:, s2]) * ph[q3][:, s3] * ph[q4][:, s4])
                    if abs(mism) < tol:
                        n_norm += 1; w_norm += abs(T) ** 2
                    elif abs(abs(mism) - 2 * np.pi) < tol:
                        n_umk += 1; w_umk += abs(T) ** 2
    return {'normal_nontrivial': n_norm, 'umklapp': n_umk,
            'weighted_normal': round(w_norm, 4), 'weighted_umklapp': round(w_umk, 4),
            'umklapp_to_normal_weighted_ratio': round(w_umk / w_norm, 4) if w_norm else None}


counts = {}
for L in [24, 36]:
    for beta_deg in [30, 45, 60]:
        counts[f'L{L}_beta{beta_deg}deg'] = count(L, np.deg2rad(beta_deg), tol=0.05)
out['ring_counts_tol_0.05rad'] = counts

print(json.dumps(out, indent=1))
with open('summary.json', 'w') as f:
    json.dump(out, f, indent=1)
