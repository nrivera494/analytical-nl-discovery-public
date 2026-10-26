"""Microcanonical GGE test: uniform measure on the (N, E', H_res) shell, obtained by conditioning the exact
condensed-regime (N, E') ensemble (Dirichlet intensities x uniform phases) on |H_res - h_input| < delta.
Compare <I_0>, mean excited g2 and group occupations with the disorder-free toy's long-z time averages."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import resonant_model as rm
rng = np.random.default_rng(9)
toy = {}
import os
for l in open(os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-rj-toy-thermalization/final_toy.jsonl')):
    o = json.loads(l)
    if o['sigma'] == 0.0: toy[(o['K'], o['Eprime'])] = o
out = []
for (K, Ep), o in sorted(toy.items()):
    groups, eps, u, S, R = rm.build(K, 400, 0)
    M = len(groups); D = M-1; R2 = R.reshape(M, -1)
    def H(A):
        v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
        return 0.5*np.real(np.einsum('pb,pb->b', A.conj(), R2 @ v))
    h_in = o['H0']; keep = []; nt = 0
    while sum(k.shape[1] for k in keep) < 4000 and nt < 4e6:
        B = 20000; nt += B
        x = rng.dirichlet(np.ones(D), size=B).T
        I = np.zeros((M, B)); I[1:] = Ep*x/eps[1:, None]; I[0] = 1 - I[1:].sum(0)
        A = np.sqrt(I)*np.exp(1j*rng.uniform(0, 2*np.pi, (M, B)))
        hs = H(A); sel = np.abs(hs - h_in) < 0.002
        keep.append(I[:, sel])
    I = np.concatenate(keep, axis=1)
    m = I.mean(1); g2 = (I**2).mean(1)/m**2
    grp = [float(np.mean(m[groups==k]/(Ep/D/k))) for k in range(1, K)]
    toy_grp = [float(np.mean(np.array(o['mean_exc_over_RJ'])[groups[1:]==k])) for k in range(1, K)]
    r = dict(K=K, Eprime=Ep, h_input=h_in, n_shell_samples=int(I.shape[1]), n_tried=int(nt),
             GGE_mean_N0=float(m[0]), toy_mean_N0=o['mean_N0'], RJ_mean_N0=float(1-Ep*np.sum(1/eps[1:])/D),
             GGE_g2_exc=float(g2[1:].mean()), toy_g2_exc=o['g2_exc_mean'],
             GGE_group_over_RJ=[round(x,3) for x in grp], toy_group_over_RJ=[round(x,3) for x in toy_grp])
    out.append(r); print(json.dumps(r))
json.dump(out, open('gge_shell.json', 'w'), indent=1)
