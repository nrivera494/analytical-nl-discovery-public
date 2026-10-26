"""Check of the card's remark under (B): the passive-mask majorant ||q_m||_p <= ||q_0||_p (S >= 0, |m| <= 1) holds for even
p but fails in general for other real p.  Source: S(k) = sum_j a_j exp(-(k - k_j)^2 / (2 s^2)) with a_j > 0, i.e. a TL
pulse g(t) sum_j a_j e^{i k_j t} under a Gaussian envelope g; a phase-only mask m = e^{i phi_j} on bump j.
Random search over (a_j, phi_j) on frequencies k_j in {0, 1, 3} (and {0, 1, 2, 4}) for ||q_m||_p / ||q_0||_p > 1 at
p = 3, 2.5, 5; the best case is then re-evaluated on a fine line grid and checked at p = 2, 4, 6 (where the ratio must be <= 1).
"""
import json
import numpy as np

rng = np.random.default_rng(31)
s = 0.08                      # bump width in k: envelope g(t) = exp(-s^2 t^2 / 2), width ~ 1/s
T, n = 400.0, 2 ** 15
t = (np.arange(n) - n // 2) * (T / n)


def norms(a, phi, ks, p_list):
    env = np.exp(-(s * t) ** 2 / 2) * s / np.sqrt(2 * np.pi) * np.sqrt(2 * np.pi)   # (1/2pi) int Gaussian bump -> s/sqrt(2pi) g(t)
    q0 = env * np.sum(a[:, None] * np.exp(1j * np.outer(ks, t)), axis=0)
    qm = env * np.sum((a * np.exp(1j * phi))[:, None] * np.exp(1j * np.outer(ks, t)), axis=0)
    dt = T / n
    return {p: (np.sum(np.abs(qm) ** p) * dt / (np.sum(np.abs(q0) ** p) * dt)) ** (1 / p) for p in p_list}


out = {"s": s, "cases": []}
for ks in (np.array([0.0, 1.0, 3.0]), np.array([0.0, 1.0, 2.0, 4.0])):
    for p in (3.0, 2.5, 5.0):
        best = (0, None)
        for trial in range(400):
            a = rng.uniform(0.2, 1.0, len(ks))
            phi = rng.uniform(0, 2 * np.pi, len(ks))
            r = norms(a, phi, ks, [p])[p]
            if r > best[0]:
                best = (r, (a, phi))
        a, phi = best[1]
        r_all = norms(a, phi, ks, [2.0, 2.5, 3.0, 4.0, 5.0, 6.0])
        out['cases'].append({"k_j": ks.tolist(), "p_search": p, "a": a.tolist(), "phi": phi.tolist(),
                             "ratio_qm_over_q0": {str(k): float(v) for k, v in r_all.items()}})
        print('k=%s p=%.1f: best ||q_m||_p/||q_0||_p = %.6f;  at p=2,4,6: %.12f %.12f %.12f' % (
            ks, p, best[0], r_all[2.0], r_all[4.0], r_all[6.0]), flush=True)
json.dump(out, open('summary_majorant_realp.json', 'w'), indent=1)
