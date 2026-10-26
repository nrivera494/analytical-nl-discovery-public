"""C-03 in the exact GRIN tensor (K=5, no disorder): H_res of the random-phase launch (phase_seed 1) and of a centre-focused
launch (all HG modes with psi_p(0,0) != 0 phased to add at the fibre centre; odd modes keep their random phases),
against the RJ (Dirichlet x uniform phases) distribution; GGE shell predictions written BEFORE the focused dynamics is run."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
from grin_overlaps import grin_tensor, hermite_functions
K = 5
modes, groups, S = grin_tensor(K)
_, eps, _, S4, R = gm.build(K, 0, 0)
M = len(groups); D = M-1; R2 = R.reshape(M, -1)
def H(A):
    v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
    return 0.5*np.real(np.einsum('pb,pb->b', A.conj(), R2 @ v))
psi0 = hermite_functions(K, np.array([0.0]))[:, 0]           # 1D Hermite functions at x = 0
centre = np.array([psi0[nx]*psi0[ny] for nx, ny in modes])
out = []
rng = np.random.default_rng(31)
for Ep in [0.6, 0.9]:
    I0 = np.zeros(M); a = Ep/3.; i1 = groups==1; i2 = groups==2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
    ph_rand = np.random.default_rng(1).uniform(0, 2*np.pi, M)
    ph_foc = ph_rand.copy(); nz = np.abs(centre) > 1e-12
    ph_foc[nz] = np.where(centre[nz] > 0, 0.0, np.pi)
    h_rand = H((np.sqrt(I0)*np.exp(1j*ph_rand))[:, None])[0]; h_foc = H((np.sqrt(I0)*np.exp(1j*ph_foc))[:, None])[0]
    B = 40000
    keep = {'rand': [], 'foc': []}; hs_all = []; I_all = []; nt = 0
    while (min(sum(k.shape[1] for k in keep['rand']), sum(k.shape[1] for k in keep['foc'])) < 3000) and nt < 4e6:
        x = rng.dirichlet(np.ones(D), size=B).T
        I = np.zeros((M, B)); I[1:] = Ep*x/eps[1:, None]; I[0] = 1 - I[1:].sum(0)
        A = np.sqrt(I)*np.exp(1j*rng.uniform(0, 2*np.pi, (M, B)))
        hs = H(A); nt += B
        if len(hs_all) < 3: hs_all.append(hs); I_all.append(I[0])
        for key, h in [('rand', h_rand), ('foc', h_foc)]:
            keep[key].append(I[:, np.abs(hs - h) < 0.002])
    hs0 = np.concatenate(hs_all); i00 = np.concatenate(I_all)
    r = dict(K=K, Eprime=Ep, RJ_N0=float(1-Ep*np.sum(1/eps[1:])/D), H_RJ_mean=float(hs0.mean()), H_RJ_std=float(hs0.std()),
             h_random=float(h_rand), z_random=float((h_rand-hs0.mean())/hs0.std()), h_focused=float(h_foc), z_focused=float((h_foc-hs0.mean())/hs0.std()),
             GGE_N0_random=float(np.concatenate(keep['rand'], 1)[0].mean()), n_random=int(np.concatenate(keep['rand'], 1).shape[1]),
             GGE_N0_focused=float(np.concatenate(keep['foc'], 1)[0].mean()), n_focused=int(np.concatenate(keep['foc'], 1).shape[1]),
             linear_slope=float(np.cov(i00, hs0)[0, 1]/hs0.var()))
    r['linear_N0_random'] = r['RJ_N0'] + r['linear_slope']*(h_rand - hs0.mean()); r['linear_N0_focused'] = r['RJ_N0'] + r['linear_slope']*(h_foc - hs0.mean())
    out.append(r); print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
json.dump(out, open('grin_gge_predict.json', 'w'), indent=1)
