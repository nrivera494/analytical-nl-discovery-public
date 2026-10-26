"""Classical resonant (time-averaged) Kerr dynamics of K degenerate, equidistant mode groups
(GRIN-like degeneracy g_k = k+1, eps'_k = k*kappa) with a random, fully symmetric, positive
overlap tensor S_pqrs = sum_j u_pj u_qj u_rj u_sj (no GRIN symmetries: no L_z, Kohn or breathing invariants).

Resonant system: dA_p/dz = i g sum_{qrs} R_pqrs A_q^* A_r A_s, R = S restricted to eps_p+eps_q = eps_r+eps_s.
Exactly conserved: N = sum |A|^2, E' = sum eps'|A|^2, H_res = (g/2) sum R A*A*AA.
Purpose: test whether long-z single-trajectory statistics in the condensed regime (E' <= kappa N) match the
Dirichlet (uniform-polytope) predictions, and whether coherent inputs with atypical H_res differ (GGE effect).
"""
import numpy as np, json, sys, time

def build(K, J, seed):
    """GRIN version: exact Hermite-Gauss Kerr tensor (J, seed unused); u = None (no 'focused' launch)."""
    from grin_overlaps import grin_tensor
    modes, groups, S = grin_tensor(K)
    eps = groups.astype(float)
    res = (eps[:,None,None,None] + eps[None,:,None,None]) == (eps[None,None,:,None] + eps[None,None,None,:])
    R = np.where(res, S, 0.0)
    return groups, eps, None, S, R

def rhs(A, R, g):
    # R2 is R reshaped to (M, M^3); v = conj(A) (x) A (x) A
    M = A.shape[0]
    v = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1)
    return 1j*g*(R.reshape(M, -1) @ v)

def hres(A, R, g):
    return 0.5*g*np.real(np.einsum('pqrs,p,q,r,s->', R, A.conj(), A.conj(), A, A, optimize=True))

def rk4(A, R, g, dz):
    k1 = rhs(A, R, g); k2 = rhs(A+0.5*dz*k1, R, g); k3 = rhs(A+0.5*dz*k2, R, g); k4 = rhs(A+dz*k3, R, g)
    return A + dz*(k1+2*k2+2*k3+k4)/6

def run(K=5, J=400, seed=0, g=1.0, Eprime=0.3, launch='dephased', zmax=3000., dz=0.01,
        zburn=500., sample_every=0.5, lyap=True, phase_seed=1, sigma=0.0, dis_seed=7):
    groups, eps, u, S, R = build(K, J, seed)
    M = len(groups); D = M-1
    rng = np.random.default_rng(phase_seed)
    # launch: power split between group-1 and group-2 modes to give E' (N=1): put fraction a in group 1, b in group 2
    # with a*1 + b*2 = E', a = b  -> a = b = E'/3
    I0 = np.zeros(M)
    if Eprime <= 1.0:   # equal power in groups 1 and 2: a*1 + a*2 = E'
        a = Eprime/3.; ga, gb = 1, 2
    else:               # equal power in groups 2 and 3: a*2 + a*3 = E'
        a = Eprime/5.; ga, gb = 2, 3
    i1 = np.where(groups==ga)[0]; i2 = np.where(groups==gb)[0]
    I0[i1] = a/len(i1); I0[i2] = a/len(i2); I0[0] = 1. - I0.sum()
    assert I0[0] >= 0
    if launch == 'dephased':
        ph = rng.uniform(0, 2*np.pi, M)
    elif launch == 'focused':      # all phases aligned at the pixel where sum_p u_pj sqrt(I_p) is largest
        jstar = np.argmax(np.abs(u.T @ np.sqrt(I0)))
        ph = np.where(u[:, jstar] >= 0, 0.0, np.pi)
    elif launch == 'antifocused':  # phases chosen to minimize the local intensity at every pixel (greedy random search)
        best = None
        for _ in range(4000):
            php = rng.uniform(0, 2*np.pi, M); A = np.sqrt(I0)*np.exp(1j*php); h = hres(A, R, g)
            if best is None or h < best[0]: best = (h, php)
        ph = best[1]
    A = np.sqrt(I0)*np.exp(1j*ph)
    N0 = np.sum(np.abs(A)**2); E0 = np.sum(eps*np.abs(A)**2); H0 = hres(A, R, g)
    # random-phase reference for H_res at the launch intensities
    hs = [hres(np.sqrt(I0)*np.exp(1j*rng.uniform(0,2*np.pi,M)), R, g) for _ in range(400)]
    # Lyapunov via a shadow trajectory
    d0 = 1e-9
    if lyap:
        w = rng.standard_normal(M) + 1j*rng.standard_normal(M); w -= np.vdot(A, w)/np.vdot(A, A)*A
        B = A + d0*w/np.linalg.norm(w); lsum = 0.0; nren = 0
    drng = np.random.default_rng(dis_seed)
    blocks = [np.where(groups==k)[0] for k in range(K) if np.sum(groups==k) > 1]
    def disorder(X, Hs):
        for b, Hb in zip(blocks, Hs):
            X[b] = Hb @ X[b]
        return X
    def draw_unitaries():
        Us = []
        for b in blocks:
            n = len(b); Z = (drng.standard_normal((n,n)) + 1j*drng.standard_normal((n,n)))/2
            Hh = (Z + Z.conj().T)/np.sqrt(2)
            w, V = np.linalg.eigh(Hh); Us.append((V*np.exp(-1j*sigma*np.sqrt(dz)*w)) @ V.conj().T)
        return Us
    Hs_series = []
    nsteps = int(round(zmax/dz)); every = int(round(sample_every/dz)); renorm = int(round(1.0/dz))
    samples = []
    t0 = time.time()
    for n in range(1, nsteps+1):
        A = rk4(A, R, g, dz)
        if sigma > 0:
            Us = draw_unitaries(); A = disorder(A, Us)
        if lyap:
            B = rk4(B, R, g, dz)
            if sigma > 0: B = disorder(B, Us)
            if n % renorm == 0:
                d = np.linalg.norm(B-A); lsum += np.log(d/d0); nren += 1; B = A + (B-A)*d0/d
        if n*dz >= zburn and n % every == 0:
            samples.append(np.abs(A)**2)
    X = np.array(samples)
    drift = dict(N=float(np.sum(np.abs(A)**2)-N0), E=float(np.sum(eps*np.abs(A)**2)-E0), H=float(hres(A,R,g)-H0))
    mean = X.mean(0); g2 = (X**2).mean(0)/mean**2
    # block statistics (10 contiguous blocks) for error bars on the headline numbers
    nb = 10; L = len(X)//nb; blk = []
    for b in range(nb):
        Y = X[b*L:(b+1)*L]; mY = Y.mean(0)
        crossb = [np.mean(Y[:,p]*Y[:,q])/(mY[p]*mY[q]) for p in range(1, M) for q in range(p+1, M)]
        blk.append(dict(g2m=float(np.mean((Y[:,1:]**2).mean(0)/mY[1:]**2)), cross=float(np.mean(crossb)),
                        varN0=float(Y[:,0].var()), N0=float(mY[0]),
                        maxdev=float(np.max(np.abs(mY[1:]/(E0/D/eps[1:]) - 1))),
                        group_mean_over_RJ=[float(np.mean(mY[groups==k]/(E0/D/k))) for k in range(1, K)]))
    def se(key):
        v = np.array([b_[key] for b_ in blk]); return float(v.std(ddof=1)/np.sqrt(nb))
    exc = np.arange(1, M)
    cross = []
    for p in exc:
        for q in exc:
            if q > p: cross.append(np.mean(X[:,p]*X[:,q])/(mean[p]*mean[q]))
    Ep = E0
    S1 = np.sum(1/eps[1:]); S2 = np.sum(1/eps[1:]**2)
    pred = dict(g2=2-2/M, cross=1-1/M, var_N0=(Ep/D)**2*(D*S2-S1**2)/(D+1), mean_exc=[Ep/D/e for e in eps[1:]])
    out = dict(sigma=sigma, K=K, M=M, J=J, seed=seed, phase_seed=phase_seed, g=g, Eprime=Eprime, launch=launch, zmax=zmax, dz=dz, zburn=zburn,
               nsamples=len(X), wall_s=time.time()-t0,
               H0=H0, H_randphase_mean=float(np.mean(hs)), H_randphase_std=float(np.std(hs)),
               lyapunov=(lsum/(nren*1.0)) if lyap else None,
               drift=drift,
               mean_exc_over_RJ=[float(mean[p]/(Ep/D/eps[p])) for p in exc],
               g2_exc=[float(x) for x in g2[exc]], g2_exc_mean=float(np.mean(g2[exc])),
               cross_mean=float(np.mean(cross)), var_N0=float(np.var(X[:,0])), mean_N0=float(mean[0]),
               pred=pred,
               block_se=dict(g2_exc_mean=se('g2m'), cross_mean=se('cross'), var_N0=se('varN0'), mean_N0=se('N0')),
               blocks=blk,
               max_rel_dev_mean_from_RJ=float(np.max(np.abs(mean[1:]/(E0/D/eps[1:]) - 1))))
    return out

if __name__ == '__main__':
    kw = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    print(json.dumps(run(**kw)))
