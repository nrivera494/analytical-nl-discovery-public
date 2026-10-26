"""Generalized NLSE in soliton units, RK4IP (interaction picture), numpy.

d_xi u = (i/2) u_tt + d3 u_ttt + i N^2 (1 + i s d_t)[ u ((1-fR)|u|^2 + fR h * |u|^2) ],   tau = T/T0, xi = z/L_D,
with u(0) normalized to the laser (peak 1 for sech: u = sech(tau)); the ZS potential is q = N u.
Raman: Blow-Wood h(t) = (tau1^2+tau2^2)/(tau1 tau2^2) e^{-t/tau2} sin(t/tau1), applied exactly through its analytic
transfer function on the FFT grid (periodic convolution). s = 1/(omega0 T0), d3 = beta3/(6|beta2| T0).
Photon number for self-steepening: sum |u~(W)|^2 / (1 - s W) is conserved (checked by `photons`); numpy's FFT puts
red frequencies at positive W, so the physical offset is Omega = -W/T0. (Fixed 12:25: the sign was + before, which made
the printed photon_drift wrong, by up to 0.23, for s != 0 runs in h3_relaxed.log; the dynamics were unaffected.)
"""
import numpy as np
from numpy.fft import fft, ifft, fftfreq


def h_bw_tilde(w, tau1=12.2, tau2=32.0):
    """int_0^inf h(t) e^{+i w t} dt, w in rad/fs."""
    a, b = 1.0 / tau2, 1.0 / tau1
    return (tau1**2 + tau2**2) / (tau1 * tau2**2) * b / ((a - 1j * w) ** 2 + b**2)


def h_lin_agrawal_tilde(w, tau1=12.2, tau2=32.0, fb=0.21, taub=96.0):
    """Lin-Agrawal response (normalized): (1 - fb) h_BlowWood + fb h_b, h_b(t) = (2 taub - t)/taub^2 exp(-t/taub)."""
    a = 1.0 / taub - 1j * w
    hb = 2.0 / (taub * a) - 1.0 / (taub**2 * a**2)
    return (1 - fb) * h_bw_tilde(w, tau1, tau2) + fb * hb


class GNLSE:
    def __init__(self, n, width, N, T0_fs, fR=0.18, s=0.0, d3=0.0, raman=True, tau1=12.2, tau2=32.0, response="bw"):
        self.n, self.N, self.T0, self.fR, self.s, self.d3 = n, N, T0_fs, (fR if raman else 0.0), s, d3
        self.dt = width / n
        self.t = (np.arange(n) - n // 2) * self.dt
        self.W = 2 * np.pi * fftfreq(n, self.dt)
        self.Lop = -0.5j * self.W**2 - 1j * d3 * self.W**3
        # numpy forward FFT uses e^{-i W tau}: FFT(h)(W) = H_bw(-W/T0)
        if not raman:
            self.Hr = np.zeros(n)
        elif response == "lin":
            self.Hr = h_lin_agrawal_tilde(-self.W / T0_fs, tau1, tau2)
        else:
            self.Hr = h_bw_tilde(-self.W / T0_fs, tau1, tau2)
        self.ss = 1.0 - s * self.W

    def Nhat(self, u):
        I = np.abs(u) ** 2
        R = (1 - self.fR) * I + (self.fR * np.real(ifft(self.Hr * fft(I))) if self.fR > 0 else 0.0)
        return 1j * self.N**2 * self.ss * fft(u * R)

    def propagate(self, u0, L, h, record=None):
        uh = fft(u0)
        E = np.exp(self.Lop * h / 2)
        nsteps = int(round(L / h))
        recs = []
        for i in range(nsteps):
            uI = E * uh
            k1 = E * self.Nhat(ifft(uh))
            k2 = self.Nhat(ifft(uI + 0.5 * h * k1))
            k3 = self.Nhat(ifft(uI + 0.5 * h * k2))
            k4 = self.Nhat(ifft(E * (uI + h * k3)))
            uh = E * (uI + h / 6 * (k1 + 2 * k2 + 2 * k3)) + h / 6 * k4
            if record and (i + 1) % record == 0:
                recs.append(((i + 1) * h, ifft(uh)))
        return ifft(uh), recs

    def photons(self, u):
        U = fft(u)
        return float(np.sum(np.abs(U) ** 2 / np.maximum(1 - self.s * self.W, 1e-12)))


def peak_window(t, u, half):
    k = int(np.argmax(np.abs(u)))
    sel = np.abs(t - t[k]) <= half
    return sel, t[k]
