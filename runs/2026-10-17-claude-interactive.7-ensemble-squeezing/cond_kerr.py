"""Can the thermalized condensate be squeezed by a subsequent single-mode Kerr stage?
Pre-scrambling (large n): the linearized state of the GRIN resonant model (exact Hermite-Gauss Kerr tensor, K = 5) from the
classical tangent map, exactly as in runs/2026-10-16-claude-interactive.7-grin-gaussian-state (same launch, disorder, dz = 0.02),
so the trajectories are the same. At checkpoints, the condensate's reduced 2x2 covariance is rotated to the frame of its own mean
field: X = amplitude quadrature, P = phase quadrature, vacuum variance 1. Reported: V_X (= Fano factor), V_P, C, the conditional phase
noise V_P|X = V_P - C^2/V_X, the symplectic eigenvalue nu (mixedness; 1 = pure), and for a subsequent single-mode Kerr stage with
nonlinear phase Phi (linearized: P -> P + 2 Phi X, same sign as the fibre's own Kerr) the smallest quadrature variance lambda_min(Phi)
and the Phi needed for -3 dB and -10 dB below vacuum. Reference: a coherent state needs Phi = 0.35 and 1.42.
Second part: balanced Sagnac (self-referenced) Kerr squeezer driven by a pump whose power varies from shot to shot by a relative RMS
eps: dark-port variance at the angle optimal for the mean power, averaged over the pump spread (coherent-state algebra per shot)."""
import numpy as np, json, time, warnings
warnings.filterwarnings('ignore')
import grin_model as gm

def lam_min_after_kerr(V, Phi):
    Kd = np.array([[1.0, 0.0], [2*Phi, 1.0]]); W = Kd @ V @ Kd.T
    return float(np.linalg.eigvalsh(W)[0])

def phi_needed(V, target):
    if lam_min_after_kerr(V, 0.0) <= target: return 0.0
    lo, hi = 0.0, 1.0
    while lam_min_after_kerr(V, hi) > target:
        hi *= 2
        if hi > 1e7: return None
    for _ in range(80):
        mid = 0.5*(lo + hi)
        if lam_min_after_kerr(V, mid) > target: lo = mid
        else: hi = mid
    return hi

def run(K=5, Eprime=0.6, sigma=0.3, dz=0.02, checkpoints=(1, 2, 5, 10, 20, 50, 100, 200, 300), phase_seed=1, dis_seed=7):
    groups, eps, _, S4, R = gm.build(K, 0, 0)
    M = len(groups); R2 = R.reshape(M, -1); RR = R.reshape(M*M, M*M)
    rng = np.random.default_rng(phase_seed)
    I0 = np.zeros(M); a = Eprime/3.; i1 = groups == 1; i2 = groups == 2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1 - I0.sum()
    A = np.sqrt(I0)*np.exp(1j*rng.uniform(0, 2*np.pi, M))
    Smat = np.eye(2*M)
    drng = np.random.default_rng(dis_seed)
    blocks = [np.where(groups == k)[0] for k in range(K) if np.sum(groups == k) > 1]
    def fA(A):
        v = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1); return 1j*(R2 @ v)
    def Lmat(A):
        P = (RR @ np.outer(A, A).reshape(-1)).reshape(M, M)
        Q = 2*np.einsum('pqrs,q,r->ps', R, A.conj(), A, optimize=True)
        Qr, Qi, Pr, Pi = Q.real, Q.imag, P.real, P.imag
        return np.block([[-(Qi + Pi), -(Qr - Pr)], [(Qr + Pr), (Pi - Qi)]])
    def deriv(A, Sm): return fA(A), Lmat(A) @ Sm
    out = []; cps = sorted(checkpoints); ci = 0; zmax = max(cps)
    for n in range(1, int(round(zmax/dz)) + 1):
        k1 = deriv(A, Smat); k2 = deriv(A + 0.5*dz*k1[0], Smat + 0.5*dz*k1[1])
        k3 = deriv(A + 0.5*dz*k2[0], Smat + 0.5*dz*k2[1]); k4 = deriv(A + dz*k3[0], Smat + dz*k3[1])
        A = A + dz*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])/6
        Smat = Smat + dz*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])/6
        if sigma > 0:
            for b in blocks:
                nb = len(b); Z = (drng.standard_normal((nb, nb)) + 1j*drng.standard_normal((nb, nb)))/2
                Hh = (Z + Z.conj().T)/np.sqrt(2); w_, V_ = np.linalg.eigh(Hh)
                U = (V_*np.exp(-1j*sigma*np.sqrt(dz)*w_)) @ V_.conj().T
                A[b] = U @ A[b]
                Ur, Ui = U.real, U.imag
                xb, yb = Smat[b, :].copy(), Smat[M + b, :].copy()
                Smat[b, :] = Ur @ xb - Ui @ yb; Smat[M + b, :] = Ui @ xb + Ur @ yb
        z = n*dz
        if ci < len(cps) and z >= cps[ci] - 1e-9:
            ci += 1
            V = Smat @ Smat.T          # vacuum variance 1 units (= 2 x the 1/2-normalized V)
            ph = np.angle(A[0]); Rt = np.array([[np.cos(ph), np.sin(ph)], [-np.sin(ph), np.cos(ph)]])
            Vloc = Rt @ V[np.ix_([0, M], [0, M])] @ Rt.T
            VX, VP, C = Vloc[0, 0], Vloc[1, 1], Vloc[0, 1]
            nu = float(np.sqrt(max(np.linalg.det(Vloc), 1.0)))
            out.append(dict(z=z, f0=float(abs(A[0])**2/np.sum(abs(A)**2)), V_X=float(VX), V_P=float(VP), C=float(C), V_P_given_X=float(VP - C**2/VX),
                            nu=nu, own_min_quad_dB=float(10*np.log10(np.linalg.eigvalsh(Vloc)[0])),
                            Phi_3dB=phi_needed(Vloc, 0.5), Phi_10dB=phi_needed(Vloc, 0.1),
                            lam_min_dB_at_Phi={str(p): float(10*np.log10(lam_min_after_kerr(Vloc, p))) for p in (1, 3, 10, 30, 100)}))
    return dict(K=K, M=M, Eprime=Eprime, sigma=sigma, dz=dz, records=out)

def sagnac_floor(Phi, eps_rms, nsamp=20001):
    """Coherent pump per shot; dark-port covariance [[1, 2F],[2F, 1+4F^2]] with F = Phi (1 + e), e ~ N(0, eps_rms^2);
    measured at the angle optimal for F = Phi; returns the shot-averaged variance."""
    def cov(F): return np.array([[1.0, 2*F], [2*F, 1 + 4*F**2]])
    w, U = np.linalg.eigh(cov(Phi)); u = U[:, 0]
    e = np.random.default_rng(3).standard_normal(nsamp)*eps_rms
    return float(np.mean([u @ cov(Phi*(1 + x)) @ u for x in e]))

if __name__ == '__main__':
    t0 = time.time(); res = []
    ref = np.eye(2)
    print(f"coherent-state reference: Phi for -3 dB {phi_needed(ref, 0.5):.3f}, for -10 dB {phi_needed(ref, 0.1):.3f}")
    for Ep in [0.3, 0.6]:
        for sig in [0.3, 0.0]:
            o = run(Eprime=Ep, sigma=sig); res.append(o)
            for r in o['records']:
                print(f"E'={Ep} sigma={sig} z={r['z']:5.0f} f0={r['f0']:.3f}: V_X={r['V_X']:9.3g} V_P={r['V_P']:9.3g} V_P|X={r['V_P_given_X']:9.3g} nu={r['nu']:8.3g} "
                      f"own min {r['own_min_quad_dB']:6.1f} dB | Phi for -3 dB {r['Phi_3dB'] if r['Phi_3dB'] is not None else float('nan'):8.3g}, -10 dB {r['Phi_10dB'] if r['Phi_10dB'] is not None else float('nan'):8.3g}", flush=True)
    sag = []
    for eps_rms in [0.0, 0.01, 0.02, 0.052]:
        for Phi in [3.0, 10.0, 30.0]:
            v = sagnac_floor(Phi, eps_rms); sag.append(dict(eps_rms=eps_rms, Phi=Phi, var=v, dB=float(10*np.log10(v)), predicted=float(1/(1 + 2*Phi**2 + 2*Phi*np.sqrt(1 + Phi**2)) + eps_rms**2)))
            print(f"Sagnac: pump RMS {eps_rms:.3f}, Phi {Phi:5.1f}: dark-port variance {v:.4g} ({10*np.log10(v):.1f} dB); V_min + eps^2 = {sag[-1]['predicted']:.4g}")
    json.dump(dict(cases=res, sagnac=sag, coherent_reference=dict(Phi_3dB=phi_needed(ref, 0.5), Phi_10dB=phi_needed(ref, 0.1))), open('cond_kerr.json', 'w'), indent=1)
    print('wall', time.time() - t0)
