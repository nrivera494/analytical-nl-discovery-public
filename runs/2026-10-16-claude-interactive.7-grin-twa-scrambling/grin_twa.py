"""Truncated-Wigner ensemble with the exact GRIN tensor (K=5), E'=0.6, sigma=0.3, coherent input, n in {1e6..1e12}."""
import numpy as np, json, time, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
K, Eprime, sigma, B, zmax, dz, rec = 5, 0.6, 0.3, 32, 1500., 0.05, 10.
groups, eps, _, S, R = gm.build(K, 0, 0)
M = len(groups); R2 = R.reshape(M, -1)
blocks = [np.where(groups==k)[0] for k in range(K) if np.sum(groups==k) > 1]
I0 = np.zeros(M); a = Eprime/3.; i1 = groups==1; i2 = groups==2
I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
ph0 = np.random.default_rng(1).uniform(0, 2*np.pi, M)
ncells = [1e6, 1e8, 1e10, 1e12]
nrng = np.random.default_rng(777)
A = [np.sqrt(I0)*np.exp(1j*ph0)]
for n in ncells:
    base = np.tile((np.sqrt(I0)*np.exp(1j*ph0))[:, None], (1, B))
    A.append(base + (nrng.standard_normal((M, B)) + 1j*nrng.standard_normal((M, B)))*np.sqrt(1/(4*n)))
A = np.concatenate([A[0][:, None]] + A[1:], axis=1)
def rhs(A):
    v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1); return 1j*(R2 @ v)
drng = np.random.default_rng(7)
def unitaries():
    Us = []
    for b in blocks:
        nb = len(b); Z = (drng.standard_normal((nb,nb)) + 1j*drng.standard_normal((nb,nb)))/2
        Hh = (Z + Z.conj().T)/np.sqrt(2); w, V = np.linalg.eigh(Hh); Us.append((V*np.exp(-1j*sigma*np.sqrt(dz)*w)) @ V.conj().T)
    return Us
zs, recs = [], []; t0 = time.time(); every = int(round(rec/dz))
for s in range(1, int(round(zmax/dz))+1):
    k1 = rhs(A); k2 = rhs(A+0.5*dz*k1); k3 = rhs(A+0.5*dz*k2); k4 = rhs(A+dz*k3); A = A + dz*(k1+2*k2+2*k3+k4)/6
    for b, U in zip(blocks, unitaries()): A[b, :] = U @ A[b, :]
    if s % every == 0:
        zs.append(s*dz); row = []
        for j in range(len(ncells)):
            X = A[:, 1+j*B:1+(j+1)*B]; I = np.abs(X)**2
            row.append(dict(coh=(np.abs(X.mean(1))**2/I.mean(1)).tolist(), relvar=(I.var(1)/I.mean(1)**2).tolist()))
        recs.append(row)
json.dump(dict(K=K, Eprime=Eprime, sigma=sigma, B=B, zmax=zmax, dz=dz, rec=rec, ncells=ncells, z=zs, records=recs, wall_s=time.time()-t0), open('grin_twa.json', 'w'))
print('done', time.time()-t0)
