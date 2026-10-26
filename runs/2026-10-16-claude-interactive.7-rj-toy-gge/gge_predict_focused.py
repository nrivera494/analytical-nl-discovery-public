"""Pre-registered GGE predictions for the 'focused' (phase-aligned coherent) launches without disorder,
before running them. Same sampler as gge_shell.py; h_input from the launch."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import resonant_model as rm
rng = np.random.default_rng(10)
out = []
for K, Ep in [(4, 0.9), (5, 0.9), (4, 0.6)]:
    groups, eps, u, S, R = rm.build(K, 400, 0)
    M = len(groups); D = M-1; R2 = R.reshape(M, -1)
    def H(A):
        v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
        return 0.5*np.real(np.einsum('pb,pb->b', A.conj(), R2 @ v))
    I0 = np.zeros(M); a = Ep/3.; i1 = groups==1; i2 = groups==2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
    jstar = np.argmax(np.abs(u.T @ np.sqrt(I0))); phf = np.where(u[:, jstar] >= 0, 0.0, np.pi)
    h_in = H((np.sqrt(I0)*np.exp(1j*phf))[:, None])[0]
    keep = []; nt = 0
    while sum(k.shape[1] for k in keep) < 4000 and nt < 4e6:
        B = 20000; nt += B
        x = rng.dirichlet(np.ones(D), size=B).T
        I = np.zeros((M, B)); I[1:] = Ep*x/eps[1:, None]; I[0] = 1 - I[1:].sum(0)
        A = np.sqrt(I)*np.exp(1j*rng.uniform(0, 2*np.pi, (M, B)))
        hs = H(A); sel = np.abs(hs - h_in) < 0.002
        keep.append(I[:, sel])
    I = np.concatenate(keep, axis=1); m = I.mean(1); g2 = (I**2).mean(1)/m**2
    r = dict(K=K, Eprime=Ep, launch='focused', h_input=float(h_in), n_shell_samples=int(I.shape[1]),
             GGE_mean_N0=float(m[0]), RJ_mean_N0=float(1-Ep*np.sum(1/eps[1:])/D), GGE_g2_exc=float(g2[1:].mean()),
             GGE_group_over_RJ=[round(float(np.mean(m[groups==k]/(Ep/D/k))),3) for k in range(1, K)])
    out.append(r); print(json.dumps(r))
json.dump(out, open('gge_predict_focused.json', 'w'), indent=1)
