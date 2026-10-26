"""CW sideband growth rate lambda(Omega) for the GRIN resonant model (exact HG overlaps, S_0000 = 1, units L_NL = 1).
delta A_p = u_p e^{-i Omega t} + conj(v_p) e^{+i Omega t};
  du_p/dz = -i D_p(+Omega) u_p + i [P v + Q u]_p,   dv_p/dz = +i D_p(-Omega) v_p - i [conj(P) u + conj(Q) v]_p
  with P_pq = sum_rs R_pqrs A_r A_s, Q_ps = 2 sum_qr R_pqrs conj(A_q) A_r,  D_p(Omega) = w * k_p * Omega + b Omega^2/2.
Only relative walk-off matters; w is the walk-off per mode group. Growth rates from periodic renormalization."""
import numpy as np, json, sys, time, warnings
warnings.filterwarnings('ignore')
import grin_model as gm

def run(K=5, Eprime=0.6, sigma=0.3, xs=(0.0, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0), mode='walkoff', zmax=3000., zburn=300.,
        dz=0.05, phase_seed=1, dis_seed=7, seed=3):
    groups, eps, _, S, R = gm.build(K, 0, 0)
    M = len(groups); R2 = R.reshape(M, -1)
    rng = np.random.default_rng(phase_seed)
    I0 = np.zeros(M); a = Eprime/3.; i1 = groups==1; i2 = groups==2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
    A = np.sqrt(I0)*np.exp(1j*rng.uniform(0, 2*np.pi, M))
    nO = len(xs); xs = np.array(xs)
    # D_p(+-Omega): walk-off mode: D = x * k_p * (+-1); gvd mode: D = x (same sign for +-Omega), x = b Omega^2/2
    if mode == 'walkoff':
        Dp = np.outer(groups, xs); Dm = -Dp
    else:
        Dp = np.tile(xs, (M, 1)).astype(float); Dm = Dp.copy()
    trng = np.random.default_rng(seed)
    u = trng.standard_normal((M, nO)) + 1j*trng.standard_normal((M, nO))
    v = trng.standard_normal((M, nO)) + 1j*trng.standard_normal((M, nO))
    nrm = np.sqrt(np.sum(abs(u)**2 + abs(v)**2, 0)); u /= nrm; v /= nrm
    drng = np.random.default_rng(dis_seed)
    blocks = [np.where(groups==k)[0] for k in range(K) if np.sum(groups==k) > 1]
    def mats(A):
        AA = np.outer(A, A).reshape(-1)
        P = (R.reshape(M*M, M*M) @ AA).reshape(M, M)              # P_pq = sum_rs R_pqrs A_r A_s
        Q = 2*np.einsum('pqrs,q,r->ps', R, A.conj(), A, optimize=True)
        return P, Q
    def f(A, u, v):
        v3 = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1)
        dA = 1j*(R2 @ v3)
        P, Q = mats(A)
        du = -1j*Dp*u + 1j*(P @ v + Q @ u)
        dv = +1j*Dm*v - 1j*(P.conj() @ u + Q.conj() @ v)
        return dA, du, dv
    logs = np.zeros(nO); zacc = 0.0; nsteps = int(zmax/dz); ren = int(1.0/dz)
    for n in range(1, nsteps+1):
        k1 = f(A, u, v)
        k2 = f(A+0.5*dz*k1[0], u+0.5*dz*k1[1], v+0.5*dz*k1[2])
        k3 = f(A+0.5*dz*k2[0], u+0.5*dz*k2[1], v+0.5*dz*k2[2])
        k4 = f(A+dz*k3[0], u+dz*k3[1], v+dz*k3[2])
        A = A + dz*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6
        u = u + dz*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6
        v = v + dz*(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6
        if sigma > 0:
            for b in blocks:
                nb = len(b); Z = (drng.standard_normal((nb,nb)) + 1j*drng.standard_normal((nb,nb)))/2
                Hh = (Z + Z.conj().T)/np.sqrt(2); w_, V = np.linalg.eigh(Hh)
                U = (V*np.exp(-1j*sigma*np.sqrt(dz)*w_)) @ V.conj().T
                A[b] = U @ A[b]; u[b] = U @ u[b]; v[b] = U.conj() @ v[b]
        if n % ren == 0:
            nrm = np.sqrt(np.sum(abs(u)**2 + abs(v)**2, 0))
            if n*dz > zburn:
                logs += np.log(nrm); zacc += ren*dz
            u /= nrm; v /= nrm
    return dict(K=K, Eprime=Eprime, sigma=sigma, mode=mode, xs=list(map(float, xs)), zmax=zmax, zburn=zburn,
                lam=(logs/zacc).tolist())

if __name__ == '__main__':
    out = []
    t0 = time.time()
    for mode in ['walkoff', 'gvd']:
        o = run(mode=mode); out.append(o); print(json.dumps(o), flush=True)
    json.dump(out, open('cw_sidebands.json', 'w'), indent=1); print('wall', time.time()-t0)
