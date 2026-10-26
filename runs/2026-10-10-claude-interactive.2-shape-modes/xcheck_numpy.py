"""Second-solver cross-check (independent numpy code, not FastDifferentiableMMNLO).

Symmetric split-step Fourier (Strang: half linear step with dispersion and gain, exact Kerr phase, half linear step)
for dA/dz = -(i/2) b2 A_TT + i gam |A|^2 A + (g/2) A, convention A ~ exp(-i w t). Same normalized units, seed and
readouts as shapemodes.jl. Runs the asymptotic seed at eps0 = 0.1, gL = 6 (reference, and +-eta launches for l = 2)
and writes rms moments and the l = 2 block map at the 61 planes used by shapemodes.jl.
Usage: python xcheck_numpy.py <outjson> [nsteps]
"""
import sys, json, math
import numpy as np

out = sys.argv[1]
nsteps = int(sys.argv[2]) if len(sys.argv) > 2 else 24000
eps0, Gamma, q, gL, eta = 0.1, math.sqrt(18), 1 / 3, 6.0, 1e-4
gam, b2, T0 = 1e-5, 1.0, 1.0
P0 = b2 / (gam * eps0 ** 2 * T0 ** 2)
g = Gamma / eps0
L = gL / g
window, Nt = 32.0, 4096        # same as shapemodes.jl at eps0 = 0.1 (window 2*ceil(1.45 a_max + 5), 2.4x Nyquist margin)
dt = window / Nt
t = (np.arange(Nt) - Nt // 2) * dt
w = 2 * np.pi * np.fft.fftfreq(Nt, d=dt)      # numpy fft: A_w = fft(A_t) uses exp(-i w t) for ifft(.. e^{+iwt}); see below
# Convention: A(t) = sum_k Ak exp(-i w_k t)  <=>  Ak = ifft-like. With numpy, ifft(Ak) = (1/N) sum Ak e^{+2pi i k n/N}.
# Use A_t = fft(Ak) (sum Ak e^{-2pi i k n/N}) and Ak = ifft(A_t): then d/dt <-> -i w.
lin_half = np.exp((1j * b2 / 2 * w ** 2 + g / 2) * (L / nsteps) / 2)   # dAk/dz = i b2/2 w^2 Ak + g/2 Ak


def softplus(x, d):
    return np.where(x > 30 * d, x, d * np.log1p(np.exp(np.minimum(x / d, 700))))


delta = 0.5 * eps0 ** (2 / 3)
A0 = np.sqrt(P0 * softplus(1 - (t / T0) ** 2, delta)) * np.exp(-1j * q * g * t ** 2 / (2 * b2))
nz = 61
save_every = nsteps // (nz - 1)
assert save_every * (nz - 1) == nsteps


def propagate(A):
    Ak = np.fft.ifft(A)
    dz = L / nsteps
    saved = [A.copy()]
    for s in range(nsteps):
        Ak = lin_half * Ak
        At = np.fft.fft(Ak)
        At = At * np.exp(1j * gam * np.abs(At) ** 2 * dz)
        Ak = lin_half * np.fft.ifft(At)
        if (s + 1) % save_every == 0:
            saved.append(np.fft.fft(Ak))
    return saved


def iddt(A):
    return np.fft.fft(w * np.fft.ifft(A))


def moments(A):
    rho = np.abs(A) ** 2
    E = rho.sum() * dt
    Tc = (t * rho).sum() * dt / E
    varT = ((t - Tc) ** 2 * rho).sum() * dt / E
    B = iddt(A); cur = np.real(np.conj(A) * B)
    Wc = cur.sum() * dt / E
    cov = ((t - Tc) * (cur - Wc * rho)).sum() * dt / E
    varW = (np.abs(B - Wc * A) ** 2).sum() * dt / E
    return E, Tc, varT, Wc, varW, cov


P = {0: lambda x: 1.0 + 0 * x, 1: lambda x: x, 2: lambda x: (3 * x ** 2 - 1) / 2}
dP = {1: lambda x: 1.0 + 0 * x, 2: lambda x: 3 * x}

ref = propagate(A0)
mref = [moments(A) for A in ref]
E0, Tc0, varT0 = mref[0][0], mref[0][1], mref[0][2]
xi0 = (t - Tc0) / math.sqrt(5 * varT0)
cut = np.exp(-(np.maximum(np.abs(xi0) - 1.3, 0) / 0.1) ** 2)


def readout2(Ap, Am, k):
    E, Tc, varT, Wc, varW, cov = mref[k]
    Tp = math.sqrt(5 * varT); Tpp = math.sqrt(5) * b2 * cov / math.sqrt(varT)
    x = t - Tc; xi = x / Tp
    drho = (np.abs(Ap) ** 2 - np.abs(Am) ** 2) / 2
    cur = lambda A: b2 * np.real(np.conj(A) * iddt(A))
    dj = (cur(Ap) - cur(Am)) / 2
    l = 2
    n2 = (2 * l + 1) / 2 * 4 / (3 * E) * (P[2](xi) * drho).sum() * dt
    p2 = (2 * l + 1) / (2 * b2 * l * (l + 1)) * 4 * Tp / (3 * E) * ((Tpp / Tp) * (dP[2](xi) * x * drho).sum() * dt - (dP[2](xi) * dj).sum() * dt)
    return p2, n2 / eps0


X = np.zeros((nz, 2, 2))
for col, typ in enumerate(("ph", "int")):
    def pert(sg):
        return A0 * np.exp(1j * sg * eta * P[2](xi0) * cut) if typ == "ph" else A0 * np.sqrt(1 + sg * eta * P[2](xi0) * cut)
    Ap = propagate(pert(1.0)); Am = propagate(pert(-1.0))
    for k in range(nz):
        X[k, :, col] = readout2(Ap[k], Am[k], k)
M = np.einsum("kij,jm->kim", X, np.linalg.inv(X[0]))
res = dict(eps0=eps0, gL=gL, Nt=Nt, window=window, nsteps=nsteps, method="numpy Strang split-step",
           E=[m[0] for m in mref], varT=[m[2] for m in mref], varW=[m[4] for m in mref], cov=[m[5] for m in mref],
           M2=M.tolist(), energy_err=float(mref[-1][0] / (mref[0][0] * math.exp(gL)) - 1))
json.dump(res, open(out, "w"))
print("done energy_err", res["energy_err"], "M2 end", np.round(M[-1], 5).tolist())
