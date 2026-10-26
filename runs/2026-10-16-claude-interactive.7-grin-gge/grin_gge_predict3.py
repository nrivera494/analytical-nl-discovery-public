"""Pre-registered GGE predictions (exact GRIN tensor, K=5, no disorder) for the 'groups 1+4' launch, E'=0.9, centre-focused and
random phases (from grin_gge_screen.json). Written before the dynamics run (grin_gge_run3.py)."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
K = 5; _, eps, _, S4, R = gm.build(K, 0, 0)
groups = gm.build(K, 0, 0)[0]; M = len(groups); D = M-1; R2 = R.reshape(M, -1)
def H(A):
    v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
    return 0.5*np.real(np.einsum('pb,pb->b', A.conj(), R2 @ v))
cands = [c for c in json.load(open('grin_gge_screen.json')) if c['name'] == 'groups 1+4']
rng = np.random.default_rng(61); Ep = 0.9
keep = {c['phases']: [] for c in cands}; nt = 0
while min(sum(k.shape[1] for k in v) for v in keep.values()) < 3000 and nt < 1.2e7:
    B = 40000; nt += B
    x = rng.dirichlet(np.ones(D), size=B).T
    I = np.zeros((M, B)); I[1:] = Ep*x/eps[1:, None]; I[0] = 1 - I[1:].sum(0)
    A = np.sqrt(I)*np.exp(1j*rng.uniform(0, 2*np.pi, (M, B))); hs = H(A)
    for c in cands: keep[c['phases']].append(I[:, np.abs(hs - c['h_in']) < 0.002])
out = []
for c in cands:
    Ik = np.concatenate(keep[c['phases']], 1)
    out.append(dict(phases=c['phases'], z_h=c['z_h'], h_in=c['h_in'], RJ_N0=float(1-Ep*np.sum(1/eps[1:])/D), GGE_N0=float(Ik[0].mean()), n_shell=int(Ik.shape[1]), I0=c['I0'], ph=c['ph']))
    print(f"groups 1+4, {c['phases']}: z_h={c['z_h']:+.2f}  GGE <I_0>={Ik[0].mean():.4f} (n={Ik.shape[1]})  RJ={1-Ep*np.sum(1/eps[1:])/D:.4f}")
json.dump(out, open('grin_gge_predict3.json', 'w'), indent=1)
