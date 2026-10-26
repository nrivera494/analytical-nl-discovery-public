"""Conservation + redistribution part of the photon-counting squeezing: for the exactly conserved, intensity-only quantities N and E',
the photon count sum_p (a + b eps_p) delta I_p keeps its input variance sum (a+b eps)^2 I_p(0) (coherent input) while its shot-noise
normalization is sum (a+b eps)^2 I_p(z). Best ratio over (a, b) along the classical trajectory (GRIN K=5, E'=0.6, sigma in {0.3, 0})."""
import numpy as np, warnings, os, sys
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grin_model as gm
from scipy.linalg import eigh
K = 5; groups, eps, _, S4, R = gm.build(K, 0, 0); M = len(groups); R2 = R.reshape(M, -1)
for Ep, sig in [(0.6, 0.3), (0.6, 0.0)]:
    I0 = np.zeros(M); a = Ep/3.; i1 = groups==1; i2 = groups==2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
    A = np.sqrt(I0)*np.exp(1j*np.random.default_rng(1).uniform(0, 2*np.pi, M)); Iin = np.abs(A)**2
    drng = np.random.default_rng(7); blocks = [np.where(groups==k)[0] for k in range(K) if np.sum(groups==k) > 1]
    dz = 0.02; cps = [10, 50, 100, 200, 400]; ci = 0; res = []
    def fA(A):
        v = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1); return 1j*(R2 @ v)
    for n in range(1, int(400/dz)+1):
        k1 = fA(A); k2 = fA(A+0.5*dz*k1); k3 = fA(A+0.5*dz*k2); k4 = fA(A+dz*k3); A = A + dz*(k1+2*k2+2*k3+k4)/6
        if sig > 0:
            for b in blocks:
                nb = len(b); Z = (drng.standard_normal((nb,nb)) + 1j*drng.standard_normal((nb,nb)))/2
                Hh = (Z + Z.conj().T)/np.sqrt(2); w_, V_ = np.linalg.eigh(Hh); U = (V_*np.exp(-1j*sig*np.sqrt(dz)*w_)) @ V_.conj().T
                A[b] = U @ A[b]
        if ci < len(cps) and n*dz >= cps[ci]-1e-9:
            ci += 1; Iz = np.abs(A)**2; F = np.stack([np.ones(M), eps])
            lam = eigh((F*Iin) @ F.T, (F*Iz) @ F.T, eigvals_only=True)[0]; res.append(f"z={n*dz:.0f}: {10*np.log10(lam):.1f} dB")
    print(f"E'={Ep} sigma={sig}: N,E' redistribution bound: " + ", ".join(res))
