"""Screen launches (exact GRIN tensor, K=5) for the most atypical resonant Kerr energy z_h, then pre-register the GGE prediction."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
from grin_overlaps import grin_tensor, hermite_functions
K = 5; modes, groups, S = grin_tensor(K)
_, eps, _, S4, R = gm.build(K, 0, 0)
M = len(groups); D = M-1; R2 = R.reshape(M, -1)
def H(A):
    v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
    return 0.5*np.real(np.einsum('pb,pb->b', A.conj(), R2 @ v))
psi0 = hermite_functions(K, np.array([0.0]))[:, 0]; centre = np.array([psi0[nx]*psi0[ny] for nx, ny in modes])
rng = np.random.default_rng(51)
def rj_stats(Ep, B=60000):
    x = rng.dirichlet(np.ones(D), size=B).T
    I = np.zeros((M, B)); I[1:] = Ep*x/eps[1:, None]; I[0] = 1 - I[1:].sum(0)
    A = np.sqrt(I)*np.exp(1j*rng.uniform(0, 2*np.pi, (M, B))); hs = H(A); return hs.mean(), hs.std()
cands = []
for name, gsel, Ep in [('groups 2+3', (2, 3), 0.9), ('group 4 only', (4,), 0.8), ('groups 1+4', (1, 4), 0.9), ('group 2 only', (2,), 0.8)]:
    I0 = np.zeros(M); per = Ep/sum(gsel)
    for gk in gsel: I0[groups==gk] = per/np.sum(groups==gk)
    I0[0] = 1 - I0.sum()
    for phname in ['focused', 'random']:
        ph = np.random.default_rng(3).uniform(0, 2*np.pi, M)
        if phname == 'focused':
            nz = np.abs(centre) > 1e-12; ph[nz] = np.where(centre[nz] > 0, 0.0, np.pi)
        h = H((np.sqrt(I0)*np.exp(1j*ph))[:, None])[0]; mu, sd = rj_stats(Ep)
        cands.append(dict(name=name, phases=phname, Eprime=Ep, z_h=float((h-mu)/sd), h_in=float(h), I0=I0.tolist(), ph=ph.tolist()))
        print(f"{name:13s} {phname:8s} E'={Ep}: z_h={(h-mu)/sd:+.2f}")
json.dump(cands, open('grin_gge_screen.json', 'w'), indent=1)
