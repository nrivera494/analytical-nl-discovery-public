#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.

T-20261008-gpt-b-01: stationary XPM family, exact generalized adjoint modes,
and source-resolved covariance. This is a research evaluator, not a solver patch.
Fourier convention: F[k] = integral f(t) exp(-i*k*t) dt.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import expm

HBAR = 1.054571817e-34
KB = 1.380649e-23
IDENTITY = dict(agent="gpt-b", model="gpt-6-astra", family="gpt")


def dump(path, value):
    def convert(x):
        if isinstance(x, np.ndarray):
            return x.tolist()
        if isinstance(x, np.generic):
            return x.item()
        raise TypeError(type(x))
    # Keep a numerical row on one line, so a covariance summary is reviewable.
    native = json.loads(json.dumps(value, default=convert, allow_nan=False))
    def pretty(x, depth=0):
        pad = '  '*depth
        if isinstance(x, dict):
            return '{\n'+',\n'.join('  '*(depth+1)+json.dumps(k)+': '+pretty(v,depth+1)
                                    for k,v in x.items())+'\n'+pad+'}'
        if isinstance(x, list):
            if all(not isinstance(v,(dict,list)) for v in x):
                return json.dumps(x, separators=(', ', ': '), allow_nan=False)
            return '[\n'+',\n'.join('  '*(depth+1)+pretty(v,depth+1) for v in x)+'\n'+pad+']'
        return json.dumps(x, allow_nan=False)
    Path(path).write_text(pretty(native) + "\n")


def family(C, N, b=(1., 1.), halfwindow=24., tol=2e-10, nt=512, scaled_sensitivities=False):
    """Positive even fundamental branch, with both modal energies prescribed.

    Lplus a_j = -f_m K_mj, 2 integral f_m a_jm = delta_mj.
    Sensitivities solve an augmented linear BVP, not differenced pulse fits.
    """
    C, N, b = np.asarray(C), np.asarray(N), np.asarray(b)
    m = len(N)
    x = np.linspace(0, halfwindow, 401)
    E = sum(N)
    p = N / E
    width = E * (p @ C @ p) / 2
    f = np.sqrt(N[:, None] * width / 2) / np.cosh(width*x)
    fp = -width * np.tanh(width*x) * f
    integ = N[:, None] * np.tanh(width*x)

    def fun(t, y, lam):
        u = y[:m]
        up = y[m:2*m]
        v = np.einsum("mn,nt->mt", C, u*u)
        return np.vstack((up, 2/b[:, None]*(lam[:, None]-v)*u, 2*u*u))

    def bc(ya, yb, lam):
        return np.r_[ya[m:2*m], yb[:m], ya[2*m:], yb[2*m:]-N]

    sol = solve_bvp(fun, bc, x, np.vstack((f, fp, integ)),
                    p=np.full(m, width*width/2), tol=tol, max_nodes=30000)
    if not sol.success:
        raise RuntimeError(sol.message)
    if np.min(sol.y[:m]) < -1e-8:
        raise RuntimeError("Stationary solution is not the positive branch")
    K = np.zeros((m, m))
    sens = []
    ascale=np.sqrt(N) if scaled_sensitivities else np.ones(m)
    for j in range(m):
        def sf(t, y, kap):
            u = sol.sol(t)[:m]
            v = np.einsum("mn,nt->mt", C, u*u)
            a = y[:m]/ascale[:,None]
            app = 2/b[:, None]*((sol.p[:, None]-v)*a
                    -2*u*(np.einsum("mn,nt->mt", C, u*a)) + u*kap[:, None])
            return np.vstack((y[m:2*m], app*ascale[:,None], 4*u*a))
        def sbc(ya, yb, kap):
            return np.r_[ya[m:2*m], yb[:m], ya[2*m:],
                         yb[2*m:]-np.eye(m)[:, j]]
        so = solve_bvp(sf, sbc, sol.x, np.zeros_like(sol.y),
                      p=np.zeros(m), tol=tol, max_nodes=30000)
        if not so.success:
            raise RuntimeError(so.message)
        K[:, j] = so.p
        sens.append(so)
    t = np.arange(-nt//2, nt//2) * (2*halfwindow/nt)
    u = sol.sol(np.abs(t))[:m].T
    up = (sol.sol(np.abs(t))[m:2*m] * np.sign(t)).T
    a = np.stack([(s.sol(np.abs(t))[:m]/ascale[:,None]).T for s in sens], axis=-1)
    dt = t[1]-t[0]
    mass = np.sum(N/b)
    # Base coordinates: N_m, theta_m, T, v. Re integral g* du.
    g = np.zeros((nt, m, 2*m+2), complex)
    tang = np.zeros_like(g)
    for j in range(m):
        g[:, j, j] = 2*u[:, j]
        g[:, :, m+j] = 2j*a[:, :, j]
        tang[:, :, j] = a[:, :, j]
        tang[:, j, m+j] = 1j*u[:, j]
    g[:, :, -2] = 2*t[:, None]*u/b[None, :]/mass
    g[:, :, -1] = -2j*up/mass
    tang[:, :, -2] = -up
    tang[:, :, -1] = 1j*t[:, None]*u/b[None, :]
    A = np.zeros((2*m+2, 2*m+2))
    A[m:2*m, :m] = K.T
    A[-2, -1] = 1
    biorth = dt*np.real(np.einsum("tma,tmb->ab", g.conj(), tang))
    k = 2*np.pi*np.fft.fftfreq(nt, dt)
    u2 = np.fft.ifft(-k[:, None]**2*np.fft.fft(u, axis=0), axis=0).real
    residual = b[None, :]*u2/2-u*sol.p[None, :]+u*np.einsum("tn,mn->tm",u*u,C)
    # A^T g = L^* g, in the real pairing. Check actual differential identities.
    def lstar(z):
        R, I = z.real, z.imag
        Rpp = np.fft.ifft(-k[:, None]**2*np.fft.fft(R, axis=0), axis=0).real
        Ipp = np.fft.ifft(-k[:, None]**2*np.fft.fft(I, axis=0), axis=0).real
        v = np.einsum("tn,mn->tm",u*u,C)
        minus_Lp_I = b*Ipp/2+(v-sol.p)*I+2*u*np.einsum("tn,mn->tm",u*I,C)
        Lm_R = -b*Rpp/2+(sol.p-v)*R
        return minus_Lp_I+1j*Lm_R
    err = np.stack([lstar(g[:, :, j]) for j in range(2*m+2)], axis=-1)
    err -= np.einsum("tmj,ij->tmi", g, A)
    sech = np.sqrt(N[None, :]*width/2)/np.cosh(width*t[:, None])
    widths = np.sqrt(12/np.pi**2 * dt*np.sum(t[:, None]**2*u*u, axis=0)/N)
    return dict(t=t, dt=dt, k=k, f=u, fp=up, a=a, g=g, tangents=tang,
                C=C, N=N, b=b, K=K, A=A, lam=sol.p, mass=mass,
                residual_relative=np.linalg.norm(residual)/np.linalg.norm(u),
                dual_identity_relative=np.linalg.norm(err)/np.linalg.norm(g),
                biorth_error=np.max(np.abs(biorth-np.eye(2*m+2))),
                K_symmetry_error=np.max(np.abs(K-K.T)),
                common_sech_relative=np.linalg.norm(u-sech)/np.linalg.norm(u),
                width_rms_equivalent=widths, bvp_nodes=len(sol.x))


def spectrum(k, t0=.5, temperature=300., fraction=.18):
    w = k/t0
    aa, bb = 1/.032, 1/.0122
    H = fraction*(aa*aa+bb*bb)/((aa-1j*w)**2+bb*bb)
    tr = fraction*2*aa/(aa*aa+bb*bb)
    ans = np.zeros_like(k)
    mask = k != 0
    if temperature > 0:
        ans[mask] = np.abs(H[mask].imag)/np.tanh(HBAR*np.abs(w[mask])*1e12/(2*KB*temperature))
        ans[~mask] = 2*KB*temperature/HBAR*tr*1e-12
    else:
        ans[mask] = np.abs(H[mask].imag)
    return ans


def diffusion(fam, s, d, gain=(.1, .1), t0=.5, temperature=300., white=False, g=None):
    """D/q. Secular local scalar Raman bath; diagonal noises remain correlated.

    Offdiagonal dW12 is circular, with <|dW12|^2>=q*s12*R dz;
    each of its real quadratures has half that covariance.
    """
    g = fam["g"] if g is None else g
    f, t, k, dt = fam["f"], fam["t"], fam["k"], fam["dt"]
    psd = spectrum(k, t0, temperature)
    if white:
        psd[:] = spectrum(np.array([0.]), t0, temperature)[0]
    diag = g.imag*f[:, :, None]
    Fdiag = dt*np.fft.fft(diag, axis=0)
    Ddiag = np.real(np.einsum("kma,mn,knb,k->ab", Fdiag.conj(), s, Fdiag, psd))/(len(t)*dt)
    Dex = np.zeros_like(Ddiag)
    for m in range(f.shape[1]):
        for n in range(m+1, f.shape[1]):
            qdiff = -d[n]/fam["b"][n]+d[m]/fam["b"][m]
            H = (g[:, m, :].imag*f[:, n, None]+g[:, n, :].imag*f[:, m, None]
                 +1j*(g[:, m, :].real*f[:, n, None]-g[:, n, :].real*f[:, m, None]))
            H *= np.exp(1j*qdiff*t[:, None])
            HF = dt*np.fft.fft(H, axis=0)
            Dex += s[m, n]/2*np.real(np.einsum("ka,k,kb->ab", HF.conj(), psd, HF))/(len(t)*dt)
    Dgain = dt/2*np.real(np.einsum("tma,m,tmb->ab", g.conj(), gain, g))
    return dict(gain=Dgain, raman=Ddiag+Dex, raman_diagonal=Ddiag, raman_exchange=Dex)


def readout(fam, d):
    """Y=(E, theta, T, V=J/E, p2, phi=theta2-theta1).

    theta uses nominal fraction weights. Phases refer to the carrier at a
    fixed time origin, not to the moving pulse centre.
    """
    N, b = fam["N"], fam["b"]
    E, p = N.sum(), N/N.sum()
    q0 = -np.asarray(d)/b
    mat = np.zeros((6, 6))
    mat[0, :2] = 1
    mat[1, 2:4] = p
    mat[2, 4] = 1
    mat[3, :2] = (q0-p@q0)/E
    mat[3, 5] = np.sum(p/b)
    mat[4, :2] = (-p[1]/E, p[0]/E)
    mat[5, 2:4] = (-1, 1)
    return mat


def centre_phase_map(N, b, d):
    """Map Y to phases at the moving pulse centre, linearized at T=v=0."""
    p=np.asarray(N)/np.sum(N);k0=-np.asarray(d)/np.asarray(b)
    mat=np.eye(6)
    mat[1,2]=p@k0
    mat[5,2]=k0[1]-k0[0]
    return mat


def polynomial(A, D):
    return np.array((D, (A@D+D@A.T)/2, A@D@A.T/3))


def raman_drift(fam, s, d, t0=.5):
    """Projection of the exact delayed secular Raman correction, not a fit.

    hR transform includes fR. Multiplication uses the negative-transform FFT,
    hence conj(H) for the causal convolution h(t')f(t-t').
    """
    t, k, f, dt = fam["t"], fam["k"], fam["f"], fam["dt"]
    aa, bb, frac = 1/.032, 1/.0122, .18
    H = frac*(aa*aa+bb*bb)/((aa+1j*k/t0)**2+bb*bb)
    conv = lambda x: np.fft.ifft(H*np.fft.fft(x))
    slopes = -np.asarray(d)/fam["b"]
    R = np.zeros_like(f, dtype=complex)
    for m in range(f.shape[1]):
        for n in range(f.shape[1]):
            R[:, m] += 1j*s[m, n]*f[:, m]*(conv(f[:, n]**2)-frac*f[:, n]**2)
            if n != m:
                phase = np.exp(1j*(slopes[m]-slopes[n])*t)
                prod = f[:, m]*f[:, n]*phase
                R[:, m] += 1j*s[m, n]*f[:, n]/phase*(conv(prod)-frac*prod)
    return dt*np.real(np.einsum("tma,tm->a", fam["g"].conj(), R))


def one_case(name, C, s, p, d, b, nt, window, out):
    fam = family(C, [2*(1-p), 2*p], b, nt=nt, halfwindow=window/2)
    X = readout(fam, d)
    AY = X@fam["A"]@np.linalg.inv(X)
    ds = diffusion(fam, s, np.asarray(d))
    dw = diffusion(fam, s, np.asarray(d), white=True)
    DY = {k: X@v@X.T for k, v in ds.items()}
    co = {k: polynomial(AY, v) for k, v in DY.items()}
    row = dict(name=name, p=p, delta=d, b=b, C=C, s=s,
               N=fam["N"], lam=fam["lam"], K=fam["K"], A=AY,
               diffusion_over_q=DY, coefficients_over_q=co,
               drift_raman=X@raman_drift(fam, s, d),
               white_diffusion_over_q={k:X@v@X.T for k,v in dw.items()},
               **{k:fam[k] for k in ("residual_relative", "dual_identity_relative", "biorth_error",
                   "K_symmetry_error", "common_sech_relative", "width_rms_equivalent", "bvp_nodes")})
    if out:
        np.savez_compressed(Path(out)/f"{name}.npz", **fam, readout=X, d=d, s=s)
        dump(Path(out)/f"{name}.json", {**IDENTITY, **row})
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--material", required=True)
    ap.add_argument("--nt", type=int, default=512)
    ap.add_argument("--window", type=float, default=48.)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    rows = []
    mats = {}
    for pair, mode, index in (("grin02", "grin", 1), ("grin11", "grin", 2), ("step11", "step", 1)):
        ar = np.load(Path(args.material)/f"{mode}_257.npz")
        inds = [0, index]
        S, beta = ar["S"], ar["beta"]
        s = np.array([[S[m,m,n,n]/S[0,0,0,0] for n in inds] for m in inds])
        C = 2*s-np.diag(np.diag(s))
        d = (beta[1,inds]-beta[1,0])*.5/abs(beta[2,0])
        b = beta[2,inds]/beta[2,0]
        mats[pair] = dict(C=C, s=s, d=d, b=b)
    mats["manakov"] = dict(C=np.ones((2,2)), s=np.array([[1.,.5],[.5,1.]]),
                           d=np.array([0.,1.]), b=np.ones(2))
    for pair in mats:
        mat = mats[pair]
        for p in ((.2,) if args.quick else (.03,.1,.2,.4)):
            for physical in ([False] if pair=="manakov" else ([True] if args.quick else [False,True])):
                b = mat["b"] if physical else np.ones(2)
                d = mat["d"] if physical else np.array([0.,1.])
                name=f"{pair}_p{p:g}_"+("physical" if physical else "equalb")
                row=one_case(name,mat["C"],mat["s"],p,d,b,args.nt,args.window,out)
                rows.append(row)
                print(name,"residual",row["residual_relative"],"dual",row["dual_identity_relative"],
                      "gain timing cubic",row["coefficients_over_q"]["gain"][2,2,2],flush=True)
    dump(out/"summary.json", dict(**IDENTITY, task="T-20261008-gpt-b-01",
        coordinates=["E","theta","T","V","p2","phi"], nt=args.nt, window=args.window,
        T0_ps=.5, temperature_K=300., gain_complex_psd_over_q=[.1,.1],
        comparator_raman="unitarily invariant Hermitian bath: s11=s22=1, s12=1/2",
        rows=rows, elapsed_seconds=time.time()-started))


if __name__ == "__main__":
    main()
