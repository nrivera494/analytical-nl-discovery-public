"""Verifier's own scalar GNLSE (claude-interactive.8), photon-conserving shock form, constant Aeff.

dA/dz = i beta(Om) A + i gamma (1 + Om/w0) F[ A ((1-fR)|A|^2 + fR h*|A|^2) ]
Physics convention A(t) = int A~(Om) exp(-i Om t) dOm/2pi, so in numpy-index space Om_k = -omega_k.
RK4IP with fixed step. Raman: exact analytic transfer H(Om) on the grid (default) or the sampled kernel.
Responses: single Blow-Wood oscillator, or a list of (weight, Hfun, hfun) via `response`.
Diagnostics at every step come from the RK4IP k1 evaluation (the nonlinear RHS at the plane).
"""
import numpy as np
from scipy import fft as sfft

C0 = 299792458.0


def osc_H(Om, tau1, tau2):
    a, b = 1 / tau2, 1 / tau1
    return (a * a + b * b) / ((a - 1j * Om) ** 2 + b * b)


def osc_h(t, tau1, tau2):
    a, b = 1 / tau2, 1 / tau1
    return np.where(t > 0, (a * a + b * b) * np.exp(-a * t) * np.sin(b * t) / b, 0.0)


class GNLSE:
    def __init__(self, n, dt, lam0, beta2, beta3, n2, Aeff, fR, tau1=None, tau2=None,
                 kernel="analytic", Hfun=None, hfun=None, kdot=None, alpha=0.0):
        self.n, self.dt = n, dt
        self.w0 = 2 * np.pi * C0 / lam0
        self.t = (np.arange(n) - n // 2) * dt
        om = 2 * np.pi * sfft.fftfreq(n, dt)
        self.Om = -om                                   # physical offset frequency of numpy bin k
        self.beta = beta2 / 2 * self.Om ** 2 + beta3 / 6 * self.Om ** 3
        self.alpha = alpha
        self.Lop = 1j * self.beta - alpha / 2
        self.gamma = n2 * self.w0 / (C0 * Aeff)
        self.shock = 1 + self.Om / self.w0
        self.fR = fR
        if Hfun is None:
            Hfun = lambda Om: osc_H(Om, tau1, tau2)
            hfun = lambda t: osc_h(t, tau1, tau2)
            kdot = 1 / tau2 ** 2 + 1 / tau1 ** 2
        self.kdot = kdot                                # h'(0+)
        self.Hgrid_exact = Hfun(self.Om)
        if kernel == "analytic":
            self.Hgrid = self.Hgrid_exact
        else:                                           # sampled kernel, h(0)=0, circular
            ts = np.arange(n) * dt
            hs = hfun(ts)
            hs[n // 2:] = 0.0
            self.Hgrid = sfft.fft(hs) * dt              # numpy: sum h e^{-i om t} = H(Om=-om)
        self.Wgrid = self.Om * np.imag(self.Hgrid_exact)  # W(Om) = Om Im H (exact response)
        self.kappa = n2 * fR * kdot / (2 * C0 * Aeff)
        self.coefE = n2 * fR / (C0 * Aeff)              # gamma fR / w0

    # ------------------------------------------------------------------ operators
    def NL(self, Af):
        A = sfft.ifft(Af)
        I = (A * np.conj(A)).real
        conv = sfft.ifft(sfft.fft(I) * self.Hgrid).real
        V = (1 - self.fR) * I + self.fR * conv
        return 1j * self.gamma * self.shock * sfft.fft(A * V), A, I

    def diagnostics(self, A, I, NLf):
        dt, n = self.dt, self.n
        E = I.sum() * dt
        Q = (I * I).sum() * dt / E ** 2
        # dE/dz from the actual nonlinear RHS: 2 Re <A, N(A)>  (dispersion conserves E; loss excluded)
        NLt = sfft.ifft(NLf)
        dEdz_rhs = 2 * np.real(np.vdot(A, NLt)) * dt
        # spectral identity: -(n2 fR/(c Aeff)) int W |I~|^2 dOm/2pi
        If = sfft.fft(I) * dt
        dEdz_spec = -self.coefE * np.sum(self.Wgrid * np.abs(If) ** 2) / (n * dt)
        Af = sfft.fft(A)
        wabs = self.w0 + self.Om
        pos = wabs > 0
        Nph = np.sum(np.abs(Af[pos]) ** 2 / wabs[pos])
        return dict(E=E, Q=Q, Pmax=I.max(), dEdz_rhs=dEdz_rhs, dEdz_spec=dEdz_spec,
                    rho_rhs=-dEdz_rhs / (self.kappa * E * E), rho_spec=-dEdz_spec / (self.kappa * E * E),
                    Nph=Nph, negfrac=np.sum(np.abs(Af[~pos]) ** 2) / np.sum(np.abs(Af) ** 2),
                    edge=float((np.abs(A[: n // 32]) ** 2).sum() + (np.abs(A[-n // 32:]) ** 2).sum()) * dt / E)

    def run(self, A0, L, nsteps, record_every=1, callback=None):
        h = L / nsteps
        Af = sfft.fft(A0)
        eL = np.exp(self.Lop * h / 2)
        rec = []
        for j in range(nsteps + 1):
            k1, A, I = self.NL(Af)
            if j % record_every == 0 or j == nsteps:
                d = self.diagnostics(A, I, k1)
                d["z"] = j * h
                rec.append(d)
                if callback is not None:
                    callback(j * h, A, d)
            if j == nsteps:
                break
            AI = eL * Af
            k1 = eL * k1
            k2 = self.NL(AI + h / 2 * k1)[0]
            k3 = self.NL(AI + h / 2 * k2)[0]
            k4 = self.NL(eL * (AI + h * k3))[0]
            Af = eL * (AI + h / 6 * (k1 + 2 * k2 + 2 * k3)) + h / 6 * k4
        return rec, sfft.ifft(Af)


def sech_launch(sim, N, fwhm, beta2):
    T0 = fwhm / (2 * np.arccosh(np.sqrt(2)))
    P0 = N ** 2 * abs(beta2) / (sim.gamma * T0 ** 2)
    return np.sqrt(P0) / np.cosh(sim.t / T0) + 0j, T0, P0
