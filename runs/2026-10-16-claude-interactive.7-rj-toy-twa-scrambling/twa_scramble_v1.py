"""Truncated-Wigner ensemble for the resonant toy model with fixed intra-group disorder.
Units: N = sum|A|^2 = 1 for the mean field; Wigner vacuum noise per mode has E|delta|^2 = 1/(2 n_cell_total)
where n_cell_total = photons per cell (all modes). Coherent input: fixed amplitudes + vacuum noise.
Dephased input: random phases per trajectory + vacuum noise.
Records, every `rec` units of z, the ensemble relative variance of each mode's intensity and |<A_p>|^2/<I_p>.
"""
import numpy as np, json, sys, time, warnings
warnings.filterwarnings('ignore')
import resonant_model as rm

def run(K=4, Eprime=0.3, sigma=0.3, ncells=(1e4, 1e6, 1e8), B=48, zmax=6000., dz=0.05, rec=20., seed=0, dis_seed=7,
        phase_seed=1, launches=('coherent', 'dephased')):
    groups, eps, u, S, R = rm.build(K, 400, seed)
    M = len(groups); R2 = R.reshape(M, -1); g = 1.0
    blocks = [np.where(groups==k)[0] for k in range(K) if np.sum(groups==k) > 1]
    I0 = np.zeros(M); a = Eprime/3.
    i1 = np.where(groups==1)[0]; i2 = np.where(groups==2)[0]
    I0[i1] = a/len(i1); I0[i2] = a/len(i2); I0[0] = 1. - I0.sum()
    prng = np.random.default_rng(phase_seed)
    ph0 = prng.uniform(0, 2*np.pi, M)              # the coherent input's (fixed) phases: same as 'dephased' launch of run()
    def rhs(A):
        v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
        return 1j*g*(R2 @ v)
    def step(A):
        k1 = rhs(A); k2 = rhs(A+0.5*dz*k1); k3 = rhs(A+0.5*dz*k2); k4 = rhs(A+dz*k3)
        return A + dz*(k1+2*k2+2*k3+k4)/6
    out = dict(K=K, M=M, Eprime=Eprime, sigma=sigma, B=B, zmax=zmax, dz=dz, rec=rec, seed=seed, dis_seed=dis_seed,
               phase_seed=phase_seed, runs=[])
    # columns: [classical reference] + for each (launch, ncell): B trajectories
    cols = [('ref', 0.0)] + [(l, n) for l in launches for n in ncells]
    nrng = np.random.default_rng(12345)
    A = [np.sqrt(I0)*np.exp(1j*ph0)]
    for l, n in cols[1:]:
        if l == 'coherent':
            base = np.tile((np.sqrt(I0)*np.exp(1j*ph0))[:,None], (1, B))
        else:
            base = np.sqrt(I0)[:,None]*np.exp(1j*nrng.uniform(0, 2*np.pi, (M, B)))
        noise = (nrng.standard_normal((M, B)) + 1j*nrng.standard_normal((M, B)))*np.sqrt(1/(4*n))   # E|d|^2 = 1/(2n)
        A.append(base + noise)
    A = np.concatenate([A[0][:,None]] + A[1:], axis=1)
    drng = np.random.default_rng(dis_seed)
    def unitaries():
        Us = []
        for b in blocks:
            nb = len(b); Z = (drng.standard_normal((nb,nb)) + 1j*drng.standard_normal((nb,nb)))/2
            Hh = (Z + Z.conj().T)/np.sqrt(2); w, V = np.linalg.eigh(Hh)
            Us.append((V*np.exp(-1j*sigma*np.sqrt(dz)*w)) @ V.conj().T)
        return Us
    nsteps = int(round(zmax/dz)); every = int(round(rec/dz)); zs = []; recs = []
    t0 = time.time()
    for s in range(1, nsteps+1):
        A = step(A)
        if sigma > 0:
            for b, U in zip(blocks, unitaries()):
                A[b, :] = U @ A[b, :]
        if s % every == 0:
            zs.append(s*dz); row = []
            for j, (l, n) in enumerate(cols[1:]):
                X = A[:, 1+j*B:1+(j+1)*B]; I = np.abs(X)**2
                relvar = I.var(1)/I.mean(1)**2
                coh = np.abs(X.mean(1))**2/I.mean(1)
                row.append(dict(relvar=relvar.tolist(), coh=coh.tolist()))
            recs.append(row)
    out['z'] = zs; out['cols'] = [list(c) for c in cols[1:]]; out['records'] = recs; out['wall_s'] = time.time()-t0
    return out

if __name__ == '__main__':
    kw = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    json.dump(run(**kw), open(kw.get('outfile', 'twa_scramble.json') if False else 'twa_scramble.json', 'w'))
    print('done')
