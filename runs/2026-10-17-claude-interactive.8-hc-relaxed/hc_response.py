"""Hollenbeck-Cantrell 13-mode silica Raman response (intermediate broadening), claude-interactive.8.

h(t) = sum_i c_i exp(-g_i t) exp(-G_i^2 t^2/4) sin(w_i t), t > 0, normalized to int h = 1, with
c_i = A_i (default, as in gnlse-python raman_holltrell and Luna.jl) or c_i = A_i/w_i (sensitivity variant),
w_i = 2 pi c CP_i, g_i = pi c LFWHM_i, G_i = pi c GFWHM_i (c in cm/s, CP and FWHM in cm^-1).
Table values: see config.yaml for the source and access level.
Transfer function (convention int h e^{i Om t} dt) in closed form with the Faddeeva function:
int_0^inf exp(-p t - G^2 t^2/4) dt = (sqrt(pi)/G) w(i p/G).
"""
import numpy as np
from scipy.special import wofz

CCM = 2.99792458e10
CP = np.array([56.25, 100.00, 231.25, 362.50, 463.00, 497.00, 611.50, 691.67, 793.67, 835.50, 930.00, 1080.00, 1215.00])
AMP = np.array([1.00, 11.40, 36.67, 67.67, 74.00, 4.50, 6.80, 4.60, 4.20, 4.50, 2.70, 3.10, 3.00])
GF = np.array([52.10, 110.42, 175.00, 162.50, 135.33, 24.50, 41.50, 155.00, 59.50, 64.30, 150.00, 91.00, 160.00])
LF = np.array([17.37, 38.81, 58.33, 54.17, 45.11, 8.17, 13.83, 51.67, 19.83, 21.43, 50.00, 30.33, 53.33])
WV = 2 * np.pi * CCM * CP
GL = np.pi * CCM * LF
GG = np.pi * CCM * GF


def _G(p, G):
    return np.sqrt(np.pi) / G * wofz(1j * p / G)


def H_raw(Om):
    Om = np.asarray(Om, dtype=float)
    out = np.zeros(Om.shape, dtype=complex)
    for c, w, g, G in zip(COEF, WV, GL, GG):
        out += c / (2j) * (_G(g - 1j * w - 1j * Om, G) - _G(g + 1j * w - 1j * Om, G))
    return out


def set_convention(conv="A"):
    """conv = "A" (default; open-source implementations) or "A_over_w"."""
    global COEF, NORM, KDOT, H2DOT, CONVENTION
    CONVENTION = conv
    COEF = AMP.copy() if conv == "A" else AMP / WV
    NORM = float(np.real(H_raw(np.array([0.0]))[0]))
    KDOT = float(np.sum(COEF * WV) / NORM)               # h'(0+)
    H2DOT = float(np.sum(COEF * (-2 * GL * WV)) / NORM)  # h''(0+)


def H(Om):
    return H_raw(Om) / NORM


def h(t):
    t = np.asarray(t, dtype=float)
    out = np.zeros(t.shape)
    pos = t > 0
    tp = t[pos]
    for c, w, g, G in zip(COEF, WV, GL, GG):
        out[pos] += c * np.exp(-g * tp - G**2 * tp**2 / 4) * np.sin(w * tp)
    return out / NORM


set_convention("A")
