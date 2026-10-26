"""Exact quantum dynamics of Q excitation quanta above a condensate of N photons (resonant toy model, random tensor, K groups).
The resonant Hamiltonian H = (g/2) sum R_pqrs a+_p a+_q a_r a_s conserves N and E' = sum k_m n_m, so the sector (N, Q) is small.
g = 1/N (classical L_NL ~ 1 for the condensate). Diagonal-ensemble (infinite-time) averages for Fock initial states, compared with
the uniform sector average (quantum microcanonical in E') and with the classical Dirichlet/RJ values."""
import numpy as np, json, itertools, warnings, sys
warnings.filterwarnings('ignore')
import resonant_model as rm
def sector_basis(groups, Q):
    exc = [m for m in range(len(groups)) if groups[m] > 0]
    basis = []
    def rec(i, remaining, occ):
        if i == len(exc):
            if remaining == 0: basis.append(tuple(occ))
            return
        k = groups[exc[i]]
        for n in range(remaining//k + 1):
            occ.append(n); rec(i+1, remaining - n*k, occ); occ.pop()
    rec(0, Q, [])
    return exc, basis
def build_H(K, N, Q, seed=0):
    groups, eps, u, S, R = rm.build(K, 400, seed)
    groups = list(groups.astype(int)); M = len(groups)
    exc, basis = sector_basis(groups, Q)
    full = []
    for b in basis:
        occ = [0]*M
        for m, n in zip(exc, b): occ[m] = n
        occ[0] = N - sum(b); full.append(tuple(occ))
    index = {s: i for i, s in enumerate(full)}
    dim = len(full); H = np.zeros((dim, dim)); g = 1.0/N
    nz = np.argwhere(np.abs(R) > 0)
    for i, s in enumerate(full):
        for (p, q, r, t) in nz:
            # a+_p a+_q a_r a_t |s>
            occ = list(s); amp = 1.0
            if occ[t] == 0: continue
            amp *= np.sqrt(occ[t]); occ[t] -= 1
            if occ[r] == 0: continue
            amp *= np.sqrt(occ[r]); occ[r] -= 1
            occ[q] += 1; amp *= np.sqrt(occ[q]); occ[p] += 1; amp *= np.sqrt(occ[p])
            j = index.get(tuple(occ))
            if j is not None: H[j, i] += 0.5*g*R[p, q, r, t]*amp
    return groups, full, H
def analyze(K=4, N=200, Q=6, inits=None, seed=0):
    groups, full, H = build_H(K, N, Q, seed)
    dim = len(full); assert np.allclose(H, H.T, atol=1e-10)
    w, V = np.linalg.eigh(H)
    occ = np.array(full, float); M = occ.shape[1]
    # uniform sector average (quantum microcanonical in E')
    mean_u = occ.mean(0); n2_u = (occ*(occ-1)).mean(0)
    out = dict(K=K, N=N, Q=Q, dim=dim, uniform_mean=mean_u.tolist(), uniform_g2=(n2_u/np.maximum(mean_u**2, 1e-30)).tolist(), inits=[])
    for name, cfg in inits:
        s = list(full[0]); s = None
        target = None
        for i, f in enumerate(full):
            if f[1:] == tuple(cfg): target = i
        psi0 = np.zeros(dim); psi0[target] = 1.0
        c = V.T @ psi0; p = c**2                      # diagonal ensemble weights
        diagO = (V**2)                                # |<s|E_n>|^2, shape (dim_s, dim_E)
        mean_d = (diagO @ p) @ occ                    # sum_n p_n sum_s |<s|n>|^2 occ_s
        n2_d = (diagO @ p) @ (occ*(occ-1))
        Nex = occ[:, 1:].sum(1); prob_s = diagO @ p
        out['inits'].append(dict(name=name, mean=mean_d.tolist(), g2=(n2_d/np.maximum(mean_d**2, 1e-30)).tolist(),
                                 Nex_mean=float(prob_s @ Nex), Nex_var=float(prob_s @ Nex**2 - (prob_s @ Nex)**2),
                                 participation_ratio=float(1/np.sum(p**2))))
    out['uniform_Nex_mean'] = float(occ[:, 1:].sum(1).mean()); out['uniform_Nex_var'] = float(occ[:, 1:].sum(1).var())
    return out
if __name__ == '__main__':
    K = 4
    groups = list(rm.build(K, 400, 0)[0].astype(int)); M = len(groups); exc = [m for m in range(M) if groups[m] > 0]
    res = []
    for N in [100, 1000]:
        for Q in [2, 4, 6]:
            # initial Fock states: (i) all Q quanta as photons in the first group-1 mode (needs Q quanta: Q photons of energy 1)
            cfg1 = [0]*len(exc); cfg1[0] = Q
            # (ii) Q/2 photons... a group-2 mode holding Q//2 photons (energy 2 each), remainder in group-1 mode
            cfg2 = [0]*len(exc); g2idx = [i for i, m in enumerate(exc) if groups[m] == 2][0]; cfg2[g2idx] = Q//2; cfg2[0] = Q - 2*(Q//2)
            o = analyze(K=K, N=N, Q=Q, inits=[('Q photons in one group-1 mode', cfg1), ('photons in one group-2 mode', cfg2)])
            res.append(o)
            gi = [i for i in range(1, M)]
            print(f"N={N} Q={Q} dim={o['dim']}: uniform <Nex>={o['uniform_Nex_mean']:.3f} Var={o['uniform_Nex_var']:.3f}; " +
                  "; ".join(f"{d['name'][:14]}: PR={d['participation_ratio']:.1f} <Nex>={d['Nex_mean']:.3f} Var={d['Nex_var']:.3f} mean-occ dev={np.max(np.abs(np.array(d['mean'][1:])-np.array(o['uniform_mean'][1:]))):.3f}" for d in o['inits']), flush=True)
    json.dump(res, open('few_quanta_exact.json', 'w'), indent=1)
