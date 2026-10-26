"""Is the RJ (polytope + random phases) ensemble compatible with the conserved resonant Kerr energy of the input?
Sample the exact condensed-regime Dirichlet ensemble (E' <= kappa N) with uniform phases, compute H_res, and compare
with the input's H_res for the launches used in the toy runs (no disorder: H_res is exactly conserved)."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import resonant_model as rm
rng = np.random.default_rng(5)
out = []
for K, Ep in [(4, 0.3), (4, 0.9), (5, 0.9), (4, 0.6)]:
    groups, eps, u, S, R = rm.build(K, 400, 0)
    M = len(groups); D = M-1; R2 = R.reshape(M, -1)
    def H(A):   # A: (M, B)
        v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
        return 0.5*np.real(np.einsum('pb,pb->b', A.conj(), R2 @ v))
    # input (same launch as resonant_model.run, phase_seed=1 'dephased' and 'focused')
    I0 = np.zeros(M); a = Ep/3.; i1 = groups==1; i2 = groups==2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
    prng = np.random.default_rng(1); ph = prng.uniform(0, 2*np.pi, M)
    h_deph = H((np.sqrt(I0)*np.exp(1j*ph))[:, None])[0]
    jstar = np.argmax(np.abs(u.T @ np.sqrt(I0))); phf = np.where(u[:, jstar] >= 0, 0.0, np.pi)
    h_foc = H((np.sqrt(I0)*np.exp(1j*phf))[:, None])[0]
    # RJ ensemble: x ~ Dirichlet(1^D), I_m = E' x_m/eps_m, I_0 = 1 - sum, uniform phases
    B = 20000
    x = rng.dirichlet(np.ones(D), size=B).T
    I = np.zeros((M, B)); I[1:] = Ep*x/eps[1:, None]; I[0] = 1 - I[1:].sum(0)
    A = np.sqrt(I)*np.exp(1j*rng.uniform(0, 2*np.pi, (M, B)))
    hs = H(A)
    r = dict(K=K, Eprime=Ep, H_input_dephased=float(h_deph), H_input_focused=float(h_foc),
             H_RJ_mean=float(hs.mean()), H_RJ_std=float(hs.std()),
             z_dephased=float((h_deph-hs.mean())/hs.std()), z_focused=float((h_foc-hs.mean())/hs.std()),
             frac_RJ_below_dephased_input=float(np.mean(hs < h_deph)))
    out.append(r); print(json.dumps(r))
json.dump(out, open('hres_rj_check.json', 'w'), indent=1)
