"""Second integrator (RK4 in the interaction picture, fixed step) for model M0 and for model M1 = M0 + causal Raman:
    i u_xi + u_tt/2 + N^2 [(1-fR)|u|^2 + fR (hR * |u|^2)] u = i delta3 u_ttt,
hR(t) = (t1^2+t2^2)/(t1 t2^2) exp(-t/t2) sin(t/t1) Theta(t), normalized to unit area on the grid; t1 = 12.2 fs/T0,
t2 = 32 fs/T0 (T0 = 50 fs by default, Roy et al.'s value); fR = 0.18. Self-steepening off. Used (i) with fR = 0 as an
independent check of the Yoshida split-step of dw_lib, (ii) for H4 (Raman)."""
import numpy as np
from dw_lib import grid, Dfun, fft, ifft, band_fraction, gated_fraction, nsr_peak, spectrum

class RK4IP:
    def __init__(self, Nt, TW, N, d3, xi, h, fR=0.18, T0fs=50.0, t1fs=12.2, t2fs=32.0):
        self.tau, self.dt, self.w = grid(Nt, TW)
        self.Nt, self.N2, self.d3, self.fR = Nt, N*N, d3, fR
        self.nsteps = max(1, int(np.ceil(xi/h - 1e-9))); self.h = xi/self.nsteps
        self.Eh = np.exp(1j*Dfun(self.w, d3)*self.h/2)
        self.wz = 1/(6*d3) if d3 > 0 else np.inf
        if fR > 0:
            t1, t2 = t1fs/T0fs, t2fs/T0fs
            s = np.arange(Nt)*self.dt
            s[Nt//2:] = -1.0       # negative lags (circular), zero response
            hr = np.where(s >= 0, (t1**2 + t2**2)/(t1*t2**2)*np.exp(-np.clip(s, 0, None)/t2)*np.sin(np.clip(s, 0, None)/t1), 0.0)
            hr /= hr.sum()*self.dt
            self.HR = fft(hr)*self.dt
            self.raman_kernel_dt_fs = self.dt*T0fs
        else:
            self.HR = None

    def NL(self, u):
        I = u.real**2 + u.imag**2
        if self.HR is None:
            return 1j*self.N2*I*u
        R = ifft(self.HR*fft(I)).real
        return 1j*self.N2*((1 - self.fR)*I + self.fR*R)*u

    def run(self, u0, record=()):
        u = u0.astype(complex).copy(); h = self.h
        rec = {int(round(x/h)): x for x in record}; snaps = {}
        if 0 in rec: snaps[rec[0]] = u.copy()
        L = lambda v: ifft(self.Eh*fft(v))
        for s in range(1, self.nsteps + 1):
            uI = L(u)
            k1 = L(self.NL(u))*h
            k2 = self.NL(uI + k1/2)*h
            k3 = self.NL(uI + k2/2)*h
            k4 = self.NL(L(uI + k3))*h
            u = L(uI + k1/6 + k2/3 + k3/3) + k4/6
            if s in rec: snaps[rec[s]] = u.copy()
        return u, snaps
