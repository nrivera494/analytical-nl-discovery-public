"""Independent library for verifying C-20261017-gpt-d-01 and -02 (claude-interactive.8).

Written from the claim statements and the verifier's own derivation; no proposer code used.

Units: tau1 = 1 (b = 1/tau1 = 1), so a = 1/tau2 = r = tau1/tau2 and T = x = T/tau1.
Response: h(t) = (a^2+b^2) exp(-a t) sin(b t)/b, k = h'(0+) = a^2+b^2.
Transfer (convention F[f](W) = int f(t) exp(i W t) dt):
    H(W) = (a^2+b^2)/((a - i W)^2 + b^2),  Wt(W) := W Im H(W) = 2 a w0^2 W^2/((w0^2-W^2)^2 + 4 a^2 W^2).
rho = (2/k) int Wt(W) |p^(W)|^2 dW/(2 pi),  p = I/E.
"""
import mpmath as mp

mp.mp.dps = 40


# ---------------------------------------------------------------- claim formula (C-...-01)
def rho_closed(r, x):
    """Claim's boxed formula, tau1 = 1: s = (a - i b) T, a = r, b = 1, T = x."""
    r = mp.mpf(r); x = mp.mpf(x)
    s = (r - 1j) * x
    val = (1 + 1j * r) * (1 - s + s**2 / 2 * mp.psi(1, 1 + s / 2))
    return mp.re(val)


def rho_long_lead(r, x):
    r = mp.mpf(r); x = mp.mpf(x)
    return 16 * r / (15 * (1 + r**2) ** 2) * x ** -3


def rho_long_two(r, x):
    r = mp.mpf(r); x = mp.mpf(x)
    return rho_long_lead(r, x) * (1 + 40 * (1 - r**2) / (7 * (1 + r**2) ** 2) * x ** -2)


def rho_short_series(r, x, order):
    """1 - 2 r x + pi^2 (3r^2-1)/12 x^2 + 2 r (1-r^2) zeta(3) x^3, truncated after x^order."""
    r = mp.mpf(r); x = mp.mpf(x)
    terms = [mp.mpf(1), -2 * r * x, mp.pi**2 * (3 * r**2 - 1) / 12 * x**2,
             2 * r * (1 - r**2) * mp.zeta(3) * x**3]
    return sum(terms[: order + 1])


# ---------------------------------------------------------------- independent quadratures
def Wt(Om, a, b):
    w02 = a * a + b * b
    return 2 * a * w02 * Om**2 / ((w02 - Om**2) ** 2 + 4 * a * a * Om**2)


def sech_spec2(Om, T):
    """|p^(Om)|^2 for p = sech^2(t/T)/(2T): ((pi Om T/2)/sinh(pi Om T/2))^2."""
    y = mp.pi * Om * T / 2
    if y == 0:
        return mp.mpf(1)
    return (y / mp.sinh(y)) ** 2


def rho_spectral(r, x, a=None, b=1):
    """(2/k) int_{-inf}^{inf} Wt |p^|^2 dOm/2pi = (2/k)(1/pi) int_0^inf Wt |p^|^2 dOm (positive integrand)."""
    a = mp.mpf(r) if a is None else a
    b = mp.mpf(b); T = mp.mpf(x)
    k = a * a + b * b
    w0 = mp.sqrt(k)
    f = lambda Om: Wt(Om, a, b) * sech_spec2(Om, T)
    # breakpoints: spectral scale 1/T and resonance w0 (width ~ a)
    pts = sorted(set([mp.mpf(0), min(w0, 1 / T), max(w0, 1 / T), w0 - a if w0 > a else w0 / 2,
                      w0 + a, 4 / T, 20 / T, 60 / T, 4 * w0, 40 * w0]))
    pts = [p for p in pts if p >= 0]
    val = mp.quad(f, pts + [mp.inf])
    return 2 / k * val / mp.pi


def q_diff(v):
    """density of U1-U2, U ~ sech^2(u)/2: (v coth v - 1)/sinh^2 v, smooth at 0 (=1/3)."""
    v = mp.mpf(v)
    if abs(v) < mp.mpf('1e-6'):
        return mp.mpf(1) / 3 - mp.mpf(2) / 15 * v**2
    return (v * mp.coth(v) - 1) / mp.sinh(v) ** 2


def rho_time(r, x):
    """(2/k) int_0^inf h'(T v) q(v) dv: the autocorrelation (time-domain) form."""
    a = mp.mpf(r); b = mp.mpf(1); T = mp.mpf(x)
    k = a * a + b * b
    hp = lambda t: k / b * mp.exp(-a * t) * (b * mp.cos(b * t) - a * mp.sin(b * t))
    f = lambda v: hp(T * v) * q_diff(v)
    # split at oscillation half-periods of h'(T v) up to where exp/ q kill the integrand
    vmax = mp.mpf(60)
    nper = int(min(4000, max(8, mp.ceil(vmax * b * T / mp.pi))))
    pts = [vmax * i / nper for i in range(nper + 1)]
    return 2 / k * mp.quad(f, pts)


# ---------------------------------------------------------------- general response moments
def osc_moment(j, a, b):
    """mu_j = int_0^inf t^j h(t) dt for the oscillator."""
    a = mp.mpf(a); b = mp.mpf(b)
    return (a * a + b * b) / b * mp.factorial(j) * mp.im(1 / (a - 1j * b) ** (j + 1))


# ---------------------------------------------------------------- C-...-02 bound
def F_arctan(tau2Q):
    return 2 / mp.pi * mp.atan(mp.pi * mp.mpf(tau2Q) / 2)
