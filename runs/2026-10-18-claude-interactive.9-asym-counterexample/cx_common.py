"""Shared pieces for the asymmetric-source counterexample to C-20261016-claude-a-01 (claude-interactive.9).

Source S(k) = pi cos(1) e^k sech(pi k/2) >= 0 (unimodal, log-concave). With q(t) = (1/2pi) int S e^{ikt} dk the
TL pulse is exactly q0(t) = cos(1) sech(t - i)  (check below), |q0(0)| = 1, M0 = int |q0|^2 = 2 cot(1).
Line-problem eigenvalues: Boffetta-Osborne on the FFT-built pulse, Richardson over two cell widths.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '2026-10-18-claude-interactive.9-zs-solver-validation'))
from zs import grid, pulse_from_spectrum, fc_eigs, bo_refine

C1 = np.cos(1.0)


def S_src(k):
    # pi cos(1) e^k sech(pi k/2), written without overflow: e^k sech(pi k/2) = 2 e^{k - pi|k|/2} / (1 + e^{-pi|k|})
    a = np.abs(k)
    return np.pi * C1 * 2 * np.exp(k - np.pi * a / 2) / (1 + np.exp(-np.pi * a))


def q_TL(t):
    return C1 / np.cosh(t - 1j)


M0 = 2.0 / np.tan(1.0)


def line_eta(mask_fun, z0, T=96.0, n=4096, both=True):
    """Leading eigenvalue (near z0) of the line potential q_m restricted to [-T/2, T/2), via BO with n and 2n cells
    and Richardson. mask_fun(k) -> complex m(k), |m| <= 1."""
    zs = []
    for nn in ((n, 2 * n) if both else (n,)):
        t, k = grid(nn, T)
        q = pulse_from_spectrum(mask_fun(k) * S_src(k), k, t, T)
        z, ares, it = bo_refine(q, T / nn, z0)
        zs.append(z)
        z0 = z
    if both:
        return (4 * zs[1] - zs[0]) / 3, zs
    return zs[0], zs
