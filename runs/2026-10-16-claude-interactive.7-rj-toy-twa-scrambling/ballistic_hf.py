"""Parameter-free Hartree-Fock prediction of the ballistic mean-field collapse (exploration note, section 3):
-ln coh_p = Var(phi_p) = A_p z^2 / n, A_p = n Var(d_N w_p dN + d_E' w_p dE'), Poisson input statistics.
Condensate (p = 0) crossing coh = 1/2 at z = sqrt(ln2 n / A_0). Compared with part 1 of this run."""
import json, os, numpy as np, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resonant_model as rm
groups, eps, u, S, R = rm.build(4, 400, 0)
M = len(groups); D = M-1; Ep = 0.3
I0 = np.zeros(M); a = Ep/3; i1 = groups==1; i2 = groups==2
I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
varN = np.sum(I0); varE = np.sum(eps**2*I0); covNE = np.sum(eps*I0)          # x 1/n (Poisson)
Sd = np.einsum('ppqq->pq', S)
def omega(N, E):
    m = np.zeros(M); m[1:] = E/(D*eps[1:]); m[0] = N - m[1:].sum()
    return -(np.diag(Sd)*m + 2*(Sd@m - np.diag(Sd)*m))
h = 1e-6
dN = (omega(1+h, Ep) - omega(1-h, Ep))/(2*h); dE = (omega(1, Ep+h) - omega(1, Ep-h))/(2*h)
A = dN**2*varN + dE**2*varE + 2*dN*dE*covNE
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-rj-toy-twa-scrambling')
o = json.load(open(os.path.join(RAW, 'twa_scramble.json'))); z = np.array(o['z'])
out = dict(A_per_mode=[round(float(x), 4) for x in A], rows=[])
for j, (l, n) in enumerate(o['cols']):
    if l != 'coherent': continue
    co0 = np.array([rec[j]['coh'][0] for rec in o['records']]); k = np.argmax(co0 < 0.5)
    zobs = float(z[k-1] + (0.5-co0[k-1])*(z[k]-z[k-1])/(co0[k]-co0[k-1])) if k > 0 else float(z[0])
    out['rows'].append(dict(n=n, predicted_z_coh0_half=float(np.sqrt(np.log(2)*n/A[0])), observed_z_coh0_half=zobs))
json.dump(out, open('ballistic_hf.json', 'w'), indent=1); print(json.dumps(out, indent=1))
