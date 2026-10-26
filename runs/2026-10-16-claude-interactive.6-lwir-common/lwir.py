"""Common library for T-20261016-claude-interactive-04 (long-wavelength photon budget).

Second, independent implementation of the single-mode GNLSE (numpy RK4IP), written for this task
by claude-interactive.6. It is used next to the agents' Julia solver (FastDifferentiableMMNLO-agents).

Conventions (same as the Julia solver):
  spectral field  Aw = ifft(At) (numpy ifft, i.e. sum_t A(t) exp(+i W t) / nt)
  W = offset angular frequency (rad/ps); absolute frequency w = w0 + W; d/dt <-> -i W.
  Field in sqrt(W), time in ps, length in m.  alpha is a POWER loss coefficient (1/m).

Model:
  dAw/dz = [ i(beta(w) - beta0 - beta1 W) - alpha(w)/2 ] Aw
           + i (n2 w / c) * P(w) * ifft[ B(t) ((1-fR)|B|^2 + fR h*|B|^2) ]
  aeff_mode = 'const' : P = 1/Aeff0, B = A   (the Julia solver's model; photon-conserving)
  aeff_mode = 'naive' : P = 1/Aeff(w), B = A (common "gamma(omega)" GNLSE; NOT photon-conserving)
  aeff_mode = 'pc'    : P = Aeff0^{1/4}/(Aeff(w)^{1/4} Aeff0), B = fft[Aw (Aeff0/Aeff(w))^{1/4}]
                        (Laegsgaard 2007 photon-conserving form; reduces to 'const' for constant Aeff)
  shock = False replaces n2 w/c by n2 w0/c (constant gamma; conserves energy, not photon number).
"""
import numpy as np
from scipy import special, optimize

C_UM_PS = 299.792458        # speed of light in um/ps
C_M_PS = 2.99792458e-4      # speed of light in m/ps
HBAR = 1.054571817e-34      # J s

# ----------------------------------------------------------------------------------------------
# Materials and fibres
# Two-term Sellmeier fits of Boilard, Vallee & Bernier, arXiv:2109.13366, Table 2 (full text):
#   n^2 - 1 = sum_i A_i lam^2 / (lam^2 - lam_i^2), cladding glass; core from n1^2 = n2^2 + NA^2.
SELLMEIER = {
    "SiO2": (1.1064, 0.7250, 0.091, 9.11),
    "ZrF4": (1.2350, 0.7520, 0.090, 14.47),
    "InF3": (1.1650, 1.1570, 0.100, 20.90),
}


def n_clad(lam_um, glass):
    A1, A2, l1, l2 = SELLMEIER[glass]
    l2_ = lam_um ** 2
    return np.sqrt(1 + A1 * l2_ / (l2_ - l1 ** 2) + A2 * l2_ / (l2_ - l2 ** 2))


def _lp01_U(V):
    """LP01 eigenvalue U(V) of the weakly guiding step-index fibre."""
    f = lambda U: U * special.j1(U) / special.j0(U) - np.sqrt(V * V - U * U) * special.k1(np.sqrt(V * V - U * U)) / special.k0(np.sqrt(V * V - U * U))
    hi = min(V, 2.404825557695773) * (1 - 1e-12)
    return optimize.brentq(f, 1e-9, hi, xtol=1e-14)


def lp01(lam_um, glass, a_um, NA):
    """Return n_eff, Aeff (um^2) of LP01 at wavelength lam_um (scalar)."""
    n2 = n_clad(lam_um, glass)
    V = 2 * np.pi * a_um / lam_um * NA
    U = _lp01_U(V)
    W = np.sqrt(V * V - U * U)
    b = 1 - U * U / (V * V)
    neff = np.sqrt(n2 ** 2 + b * NA ** 2)
    # effective area from the LP01 field
    r_in = np.linspace(0, a_um, 2001)
    r_out = np.linspace(a_um, a_um * (1 + 40.0 / max(W, 1e-3)), 20001)
    F_in = special.j0(U * r_in / a_um)
    F_out = special.j0(U) / special.k0(W) * special.k0(W * r_out / a_um)
    I2 = np.trapezoid(F_in ** 2 * r_in, r_in) + np.trapezoid(F_out ** 2 * r_out, r_out)
    I4 = np.trapezoid(F_in ** 4 * r_in, r_in) + np.trapezoid(F_out ** 4 * r_out, r_out)
    aeff = 2 * np.pi * I2 ** 2 / I4
    return neff, aeff


class StepIndexFiber:
    """Step-index LP01 fibre tabulated on a wavelength grid and interpolated in absolute angular frequency."""

    def __init__(self, glass, a_um, NA, lam_min=0.6, lam_max=12.0, n=1500, n2=2.6e-20):
        self.glass, self.a_um, self.NA, self.n2 = glass, a_um, NA, n2
        lam_max = min(lam_max, 2 * np.pi * a_um * NA / 0.6)   # keep V >= 0.6 (field beyond is absorbed)
        w = np.linspace(2 * np.pi * C_UM_PS / lam_max, 2 * np.pi * C_UM_PS / lam_min, n)  # rad/ps
        lam = 2 * np.pi * C_UM_PS / w
        ne, ae = np.zeros(n), np.zeros(n)
        for i, l in enumerate(lam):
            ne[i], ae[i] = lp01(l, glass, a_um, NA)
        self.w_tab, self.neff_tab, self.aeff_tab = w, ne, ae
        self.beta_tab = ne * w / C_M_PS            # 1/m
        # smoothing spline for beta(w) to get derivatives
        from scipy.interpolate import CubicSpline
        self._bspl = CubicSpline(w, self.beta_tab)
        self._aspl = CubicSpline(w, np.log(ae))

    def beta(self, w, d=0):
        w = np.asarray(w, float)
        wc = np.clip(w, self.w_tab[0], self.w_tab[-1])
        out = self._bspl(wc, d)
        if d == 0:  # linear extrapolation outside the table (only used where the field is absorbed)
            lo, hi = w < self.w_tab[0], w > self.w_tab[-1]
            out = np.where(lo, self._bspl(self.w_tab[0]) + self._bspl(self.w_tab[0], 1) * (w - self.w_tab[0]), out)
            out = np.where(hi, self._bspl(self.w_tab[-1]) + self._bspl(self.w_tab[-1], 1) * (w - self.w_tab[-1]), out)
        return out

    def aeff_um2(self, w):
        wc = np.clip(np.asarray(w, float), self.w_tab[0], self.w_tab[-1])
        return np.exp(self._aspl(wc))

    def gamma(self, w):
        """gamma(w) = n2 w / (c Aeff(w)) in 1/(W m)."""
        return self.n2 * w / C_M_PS / (self.aeff_um2(w) * 1e-12)

    def beta2(self, w):
        return self.beta(w, 2)   # ps^2/m


def wl_to_w(lam_um):
    return 2 * np.pi * C_UM_PS / lam_um


def w_to_wl(w):
    return 2 * np.pi * C_UM_PS / w


def edge_loss(w, A_dB_per_m, B_um):
    """Exponential multiphonon edge alpha(lambda) = A exp(-B/lambda) (A in dB/m), returned as power loss in 1/m.
    In angular frequency: alpha = A exp(-w / w_e) with w_e = 2 pi c / B."""
    w = np.asarray(w, float)
    lam = np.where(w > 1e-6, 2 * np.pi * C_UM_PS / np.maximum(w, 1e-6), 1e9)
    a_db = A_dB_per_m * np.exp(np.clip(-B_um / lam, -700, 50))
    return a_db * np.log(10) / 10.0


# ----------------------------------------------------------------------------------------------
# Raman response: single damped oscillator (Blow & Wood 1989 form; the solver's AgarwalRaman)
class OscillatorRaman:
    def __init__(self, fR=0.18, tau1=0.0122, tau2=0.032):
        self.fR, self.tau1, self.tau2 = fR, tau1, tau2

    def h_t(self, t):
        t = np.asarray(t, float)
        pre = (self.tau1 ** 2 + self.tau2 ** 2) / (self.tau1 * self.tau2 ** 2)
        return np.where(t >= 0, pre * np.exp(-t / self.tau2) * np.sin(t / self.tau1), 0.0)

    def h_w(self, W):
        """Analytic transform  int h(t) e^{+i W t} dt  (normalised: h_w(0) = 1)."""
        W = np.asarray(W, float)
        a, b = 1 / self.tau2, 1 / self.tau1
        return (a * a + b * b) / ((a - 1j * W) ** 2 + b * b)

    def TR(self):
        """T_R = fR * int t h(t) dt = fR * Im h_w'(0)."""
        a, b = 1 / self.tau2, 1 / self.tau1
        return self.fR * 2 * a / (a * a + b * b)

    def hprime0(self):
        return 1 / self.tau1 ** 2 + 1 / self.tau2 ** 2


# ----------------------------------------------------------------------------------------------
class Grid:
    def __init__(self, nt, dt, w0):
        self.nt, self.dt, self.w0 = nt, dt, w0
        self.t = (np.arange(nt) - nt // 2) * dt
        self.W = 2 * np.pi * np.fft.fftfreq(nt, dt)       # fft order, matches Aw = ifft(At)
        self.w = w0 + self.W
        self.dW = 2 * np.pi / (nt * dt)


class GNLSE:
    """Single-mode GNLSE, RK4IP, numpy.  Spectral state Aw = ifft(At) (fft order)."""

    def __init__(self, grid, beta_w, n2, aeff_w_um2, aeff0_um2, raman=None, alpha_w=None,
                 shock=True, aeff_mode="const", w_ref=None, beta1_ref=None, window=None):
        g = grid
        self.g = g
        bw = beta_w(g.w)
        wr = g.w0 if w_ref is None else w_ref
        # retarded frame: subtract beta(w0) and beta1(w_ref) * W
        b0 = beta_w(np.array([g.w0]))[0]
        if beta1_ref is None:
            eps = 1e-3
            beta1_ref = (beta_w(np.array([wr + eps]))[0] - beta_w(np.array([wr - eps]))[0]) / (2 * eps)
        self.beta1_ref = beta1_ref
        self.alpha = np.zeros(g.nt) if alpha_w is None else alpha_w(g.w)
        self.Lop = 1j * (bw - b0 - beta1_ref * g.W) - self.alpha / 2
        self.raman = raman
        self.fR = 0.0 if raman is None else raman.fR
        if raman is not None:
            self.hw = raman.h_w(g.W)    # continuous transform, sampled
        aeff = aeff_w_um2(g.w) * 1e-12
        aeff0 = aeff0_um2 * 1e-12
        wabs = np.where(g.w > 0, g.w, 0.0)
        if shock:
            nlw = n2 * wabs / C_M_PS
        else:
            nlw = n2 * g.w0 / C_M_PS * np.ones(g.nt)
        if aeff_mode == "const":
            self.P = nlw / aeff0
            self.Bscale = None
        elif aeff_mode == "naive":
            self.P = nlw / aeff
            self.Bscale = None
        elif aeff_mode == "pc":
            s = (aeff0 / aeff) ** 0.25
            self.P = nlw * s / aeff0
            self.Bscale = s
        else:
            raise ValueError(aeff_mode)
        if window is not None:
            self.P = self.P * window
        self.aeff_mode = aeff_mode
        # photon weights per bin (photons = sum |Aw|^2 * nt*dt*1e-12 / (hbar w*1e12)) for w>0
        # energy in bin k = nt*dt*|Aw_k|^2 (pJ)  ->  photons = that * 1e-12 J / (hbar w_k * 1e12 /s)
        self.pw = np.where(g.w > 0, (g.nt * g.dt * 1e-12) / (HBAR * np.maximum(g.w, 1e-30) * 1e12), 0.0)

    def N_op(self, Aw):
        g = self.g
        if self.Bscale is None:
            B = np.fft.fft(Aw)
        else:
            B = np.fft.fft(Aw * self.Bscale)
        I = (B * B.conj()).real
        if self.fR > 0:
            conv = np.fft.fft(self.hw * np.fft.ifft(I)).real   # (h * I)(t) circular, with h normalised
            V = (1 - self.fR) * I + self.fR * conv
        else:
            V = I
        return 1j * self.P * np.fft.ifft(B * V)

    def run(self, A0w, L, dz, n_save=50, callback=None):
        """Propagate; return dict with saved z, spectra (shifted), diagnostics.  callback(z, Aw) -> dict."""
        nsteps = int(np.ceil(L / dz - 1e-9))
        dz = L / nsteps
        Aw = A0w.astype(complex).copy()
        half = np.exp(self.Lop * dz / 2)
        save_every = max(1, nsteps // n_save)
        out = {"z": [], "diag": []}
        if callback is not None:
            out["z"].append(0.0); out["diag"].append(callback(0.0, Aw))
        for k in range(nsteps):
            AI = half * Aw
            k1 = half * self.N_op(Aw)
            k2 = self.N_op(AI + dz / 2 * k1)
            k3 = self.N_op(AI + dz / 2 * k2)
            k4 = self.N_op(half * (AI + dz * k3))
            Aw = half * (AI + dz / 6 * (k1 + 2 * k2 + 2 * k3)) + dz / 6 * k4
            if callback is not None and ((k + 1) % save_every == 0 or k == nsteps - 1):
                z = (k + 1) * dz
                out["z"].append(z); out["diag"].append(callback(z, Aw))
        out["Aw"] = Aw
        out["dz"] = dz
        return out

    # ---- diagnostics
    def photons(self, Aw, mask=None):
        n = np.abs(Aw) ** 2 * self.pw
        return n.sum() if mask is None else n[mask].sum()

    def energy_pJ(self, Aw):
        g = self.g
        return (np.abs(Aw) ** 2).sum() * g.nt * g.dt   # W ps = pJ  (Parseval with numpy ifft)

    def mean_w(self, Aw):
        n = np.abs(Aw) ** 2 * self.pw
        return (n * self.g.w).sum() / n.sum()

    def raman_dissipation_pJ_per_m(self, Aw):
        """Exact identity (const Aeff, shock): dE/dz = -(gamma0 fR / w0) int dW/2pi W Im h(W) |I~(W)|^2,
        returned as the positive dissipation rate  (pJ/m)."""
        g = self.g
        A = np.fft.fft(Aw)
        I = np.abs(A) ** 2
        It = np.fft.ifft(I) * g.nt * g.dt          # I~(W) = int I e^{iWt} dt  (W ps)
        gam_w0 = self.P * np.where(g.w > 0, g.w0 / np.maximum(g.w, 1e-30), 0)  # gamma0 = n2 w0/(c Aeff0)
        gamma0 = gam_w0[0]
        integrand = g.W * self.raman.h_w(g.W).imag * np.abs(It) ** 2
        return gamma0 * self.fR / g.w0 * integrand.sum() * g.dW / (2 * np.pi)


def sech_pulse(grid, P0, T0, W_off=0.0, t_off=0.0, chirp=0.0):
    t = grid.t - t_off
    At = np.sqrt(P0) / np.cosh(t / T0) * np.exp(-1j * W_off * t) * np.exp(-1j * chirp * t ** 2 / (2 * T0 ** 2))
    At = np.fft.ifftshift(At)   # put t=0 at index 0 for fft order consistency
    return np.fft.ifft(At)


def at_from_aw(Aw):
    return np.fft.fftshift(np.fft.fft(Aw))


# ----------------------------------------------------------------------------------------------
# Reduced adiabatic reach model
def sech_raman_rate(Ts, P, raman, gamma_s, w_s, w0_ref=None, npts=40001):
    """Exact-overlap mean-frequency rate (rad/ps per m, negative) of an isolated sech soliton
    I = P sech^2(t/Ts) at absolute frequency w_s, using the shock-form identity
        hbar N dw/dz = -(gamma(w_s) fR / w_s) int dW/2pi W Im h(W) |I~|^2 ,  hbar N = E/w_s,
    i.e. dw/dz = -(gamma(w_s) fR / E) int dW/2pi W Im h |I~|^2  with  I~ = P Ts pi W Ts / sinh(pi W Ts / 2)."""
    W = np.linspace(1e-6, 60.0 / Ts + 6.0 / raman.tau1, npts)
    x = np.pi * W * Ts / 2
    It = P * Ts * np.pi * W * Ts / np.sinh(np.minimum(x, 700)) * (x < 700)
    E = 2 * P * Ts
    integ = W * raman.h_w(W).imag * It ** 2
    val = 2 * np.trapezoid(integ, W) / (2 * np.pi)   # symmetric integrand: both signs of W
    return -gamma_s * raman.fR / E * val


def gordon_rate(Ts, beta2_abs, TR):
    return -8 * TR * beta2_abs / (15 * Ts ** 4)


# ----------------------------------------------------------------------------------------------
class ReachModel:
    """Adiabatic fundamental-soliton reach model with loss (photon-number form).

    State: centre angular frequency w_s (rad/ps), photon number N_s.
      T_s = 2|beta2(w_s)| / (gamma(w_s) hbar w_s N_s)      (fundamental soliton)
      dw_s/dz = rate(T_s, P_s)  ['exact': sech overlap with the full Raman response; 'gordon': -8 T_R|b2|/(15 T^4)]
      dN_s/dz = -<alpha>_s N_s  (alpha averaged over the soliton photon spectrum, sech^2 of width 2/(pi T_s))
      loss-slope drift  dw_s/dz += -cov_s(alpha, w)  (selective loss moves the surviving centroid)
    """

    def __init__(self, fiber, raman, alpha_w=None, rate="exact", aeff_const_um2=None, n2=None, npts=40001):
        self.f, self.r, self.alpha_w, self.rate = fiber, raman, alpha_w, rate
        self.npts = npts
        self.aeff_const = aeff_const_um2
        self.n2 = fiber.n2 if n2 is None else n2
        self._x = np.linspace(-12, 12, 481)   # in units of spectral half-width scale
        self._wt = 1 / np.cosh(self._x) ** 2
        self._wt /= self._wt.sum()

    def gamma(self, w):
        if self.aeff_const is None:
            return self.f.gamma(np.array([w]))[0]
        return self.n2 * w / C_M_PS / (self.aeff_const * 1e-12)

    def soliton(self, w, N):
        b2 = abs(self.f.beta2(np.array([w]))[0])
        g = self.gamma(w)
        E = HBAR * w * 1e12 * N * 1e12   # pJ
        Ts = 2 * b2 / (g * E)
        P = E / (2 * Ts)
        return Ts, P, b2, g, E

    def rhs(self, w, N):
        Ts, P, b2, g, E = self.soliton(w, N)
        if self.rate == "exact":
            dw = sech_raman_rate(Ts, P, self.r, g, w, npts=self.npts)
        else:
            dw = gordon_rate(Ts, b2, self.r.TR())
        dN = 0.0
        if self.alpha_w is not None:
            # photon spectrum of a sech soliton: |A(w)|^2 ~ sech^2(pi Ts (w - w_s)/2)
            ww = w + self._x * 2 / (np.pi * Ts)
            a = self.alpha_w(ww)
            am = (a * self._wt).sum()
            cov = (a * (ww - w) * self._wt).sum()
            dN = -am * N
            dw += -cov
        return dw, dN

    def integrate(self, w0, N0, L, dz=None, n_out=400, w_stop=None):
        """RK4 in z.  Returns arrays z, w, N, Ts."""
        z, w, N = 0.0, w0, N0
        Ts0 = self.soliton(w0, N0)[0]
        if dz is None:
            dz = L / 20000
        zs, ws, Ns, Ts = [0.0], [w0], [N0], [Ts0]
        nst = int(np.ceil(L / dz)); dz = L / nst
        every = max(1, nst // n_out)
        for k in range(nst):
            a1, b1 = self.rhs(w, N)
            a2, b2_ = self.rhs(w + dz / 2 * a1, N + dz / 2 * b1)
            a3, b3 = self.rhs(w + dz / 2 * a2, N + dz / 2 * b2_)
            a4, b4 = self.rhs(w + dz * a3, N + dz * b3)
            w += dz / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
            N += dz / 6 * (b1 + 2 * b2_ + 2 * b3 + b4)
            z += dz
            if (k + 1) % every == 0 or k == nst - 1:
                zs.append(z); ws.append(w); Ns.append(N); Ts.append(self.soliton(w, N)[0])
            if N <= 0 or (w_stop is not None and w <= w_stop):
                break
        return np.array(zs), np.array(ws), np.array(Ns), np.array(Ts)


def gordon_K(fiber, raman, w, gamma_fn=None):
    """K(w) with dw/dz = -K(w) N^4 under Gordon's law:  K = T_R gamma^4 (hbar w)^4 / (30 |beta2|^3)
    (units: N in photons, w rad/ps, z m; hbar w in pJ)."""
    w = np.asarray(w, float)
    g = fiber.gamma(w) if gamma_fn is None else gamma_fn(w)
    b2 = np.abs(fiber.beta2(w))
    hw = HBAR * w * 1e12 * 1e12   # pJ per photon
    return raman.TR() * g ** 4 * hw ** 4 / (30 * b2 ** 3)
