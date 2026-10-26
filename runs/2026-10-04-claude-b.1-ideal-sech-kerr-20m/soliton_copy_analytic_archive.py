"""Analytical soliton-continuum benchmark for coherent-input-copy photon counting.

No NLSE/GNLSE propagation and no fitted covariance matrices. All longitudinal
optical evolution is an explicit fundamental-soliton Green function, evaluated
by Fourier quadrature. Raman noise is projected from the full damped-oscillator
causal response on the unperturbed soliton Green function.

LIMITS: The executable benchmark uses an exact sech fundamental soliton,
second-order dispersion and instantaneous deterministic Kerr evolution. Raman
bath is included to leading perturbative order. Deterministic Raman drift,
prepared-pulse residual, higher-order dispersion, shock, and exact optical
photon-frequency weighting are NOT included here. Do not label its outputs
as the fully corrected prediction for the measured/prepared input. Nor is a
length/soliton-family scan a fixed-width input-power scan.

Requirements: Python 3.10+, numpy, scipy. Run: python soliton_copy_analytic.py
Conventions: x=t/T0, zeta=z/LD; coherent Re/Im field covariance I/4;
Q=4 Cov(X,Y), X,Y measured in the normalized sech/sqrt(2) mode.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
hbar = 6.62607015e-34/(2*np.pi)
Boltzmann = 1.380649e-23
c = 299792458.0  # exact SI constants; local replacement for SciPy constants only

BETA2_ABS = 0.0280886649  # ps^2 / m
GAMMA = 0.000529330575   # W^-1 m^-1
T0_PS = 0.22691853
FREP_HZ = 80e6
LAMBDA_M = 1550e-9
ETA = 0.995
R = 0.7017289851
PSI = -2.181661565
LD_M = T0_PS**2 / BETA2_ABS
PPEAK_W = BETA2_ABS / (GAMMA * T0_PS**2)
PIN_SECH_MW = 1e3 * FREP_HZ * 2 * PPEAK_W * T0_PS * 1e-12


def sech(x: np.ndarray) -> np.ndarray:
    e = np.exp(-np.abs(np.asarray(x)))
    return 2 * e / (1 + e * e)


def kernels(zeta: float, *, dx: float = .04, nx: int = 16384):
    """Return x, k (FFT order), backward kernels h_u,h_v for output Y.

    Y_out = integral (h_u Re(delta b_in) + h_v Im(delta b_in)) dx.
    Includes soliton Jordan modes AND their correlated continuum completion.
    Fourier integration is numerical quadrature, not longitudinal propagation.
    """
    if zeta < 0 or dx <= 0 or nx < 256 or nx % 2:
        raise ValueError('Require zeta>=0, dx>0, even nx>=256.')
    x = (np.arange(nx) - nx // 2) * dx
    k = 2 * np.pi * np.fft.fftfreq(nx, dx)
    dk = 2 * np.pi / (nx * dx)
    s, t = sech(x), np.tanh(x)
    a = s * (1 - x * t)
    spectral = sech(np.pi * k / 2) / (1 + k*k)
    spectral = spectral * np.exp(-.5j * (1 + k*k) * zeta)
    i0 = np.fft.fftshift(np.fft.fft(spectral)) * dk
    i1 = np.fft.fftshift(np.fft.fft(k * spectral)) * dk
    i2 = np.fft.fftshift(np.fft.fft(k*k * spectral)) * dk
    f = i2 - i0 - 2j * t * i1
    hu = np.sqrt(2) * zeta * s - f.imag / (2*np.sqrt(2))
    hv = np.sqrt(2) * a - (f + 2*s*s*i0).real / (2*np.sqrt(2))
    return x, k, hu, hv


def optical_covariance(zeta: float, **grid) -> np.ndarray:
    x, _, hu, hv = kernels(zeta, **grid)
    dx = x[1] - x[0]
    f = sech(x)/np.sqrt(2)
    return np.array([[1., np.sum(f*hu)*dx],
                     [np.sum(f*hu)*dx, np.sum(hu*hu+hv*hv)*dx]])


def causal_raman_H(k: np.ndarray, *, t0_ps: float = T0_PS,
                   tau1_ps: float = .0122, tau2_ps: float = .032):
    """H(Omega)=integral_0^inf h(t)exp(+i Omega t)dt, H(0)=1."""
    om = k / t0_ps
    a, b = 1/tau2_ps, 1/tau1_ps
    return (a*a+b*b)/((a-1j*om)**2+b*b)


def raman_spectrum(k: np.ndarray, *, temperature_K: float = 300.,
                   t0_ps: float = T0_PS, fR: float = .18,
                   tau1_ps: float = .0122, tau2_ps: float = .032):
    """n_* times the normalized real phase-force spectrum.

    Replace this function with fR*abs(Im H_actual(k/T0))*coth(...) for
    another causal kernel; preserve its exact low-frequency limit.
    """
    if temperature_K < 0:
        raise ValueError('Temperature must be nonnegative.')
    H = causal_raman_H(k, t0_ps=t0_ps, tau1_ps=tau1_ps,
                       tau2_ps=tau2_ps)
    spectrum = fR * np.abs(H.imag)
    if temperature_K:
        arg = hbar*np.abs(k)/(t0_ps*1e-12)/(2*Boltzmann*temperature_K)
        nz = arg > 1e-10
        spectrum[nz] /= np.tanh(arg[nz])
        mean_delay_s = 2*tau1_ps**2*tau2_ps/(tau1_ps**2+tau2_ps**2)*1e-12
        spectrum[~nz] = fR*mean_delay_s*2*Boltzmann*temperature_K/hbar
    return spectrum


def raman_Qyy(zeta: float, *, temperature_K: float = 300.,
               nquad: int = 96, dx: float = .04, nx: int = 16384,
               spectrum_function=None) -> float:
    """Return 4 Var(Y)_R by analytic Green-function and bath quadrature.

    The entire completed h_v is used BEFORE squaring: this retains the
    correlations between reservoir-induced soliton and continuum components.
    """
    if zeta == 0:
        return 0.
    if nquad < 8:
        raise ValueError('Use at least 8 longitudinal quadrature nodes.')
    nodes, weights = leggauss(nquad)
    total = 0.
    for tau, weight in zip((nodes+1)*zeta/2, weights*zeta/2):
        x, k, _, hv = kernels(float(tau), dx=dx, nx=nx)
        w = sech(x)*hv
        wk = np.fft.fft(np.fft.ifftshift(w))*dx
        spectrum = (raman_spectrum(k, temperature_K=temperature_K)
                    if spectrum_function is None else spectrum_function(k))
        dk = 2*np.pi/(nx*dx)
        total += weight*np.sum(spectrum*np.abs(wk)**2)*dk/(2*np.pi)
    return float(4*total)


def readout(Q: np.ndarray, length_m: float, *, eta: float = ETA,
            r: float = R, psi: float = PSI) -> dict:
    """Direct count readout of signal plus independent coherent input copy."""
    if not 0 < eta < 1 or r < 0:
        raise ValueError('Require 0<eta<1 and r>=0.')
    zeta = length_m/LD_M
    d = np.sqrt(eta)+np.sqrt(1-eta)*r*np.exp(1j*(psi-zeta/2))
    theta = float(np.angle(d))
    v = np.array([np.cos(theta), np.sin(theta)])
    return dict(F=float(1-eta+eta*(v@Q@v)), theta_rad=theta,
                power_ratio=float(abs(d)**2),
                output_mW_exact_sech=float(PIN_SECH_MW*abs(d)**2))


def benchmark(length_m: float = 20., **grid) -> dict:
    zeta = length_m/LD_M
    Q = optical_covariance(zeta, **grid)
    Ryy = raman_Qyy(zeta, **grid)
    Qtotal = Q + np.diag([0., Ryy])
    optical = readout(Q, length_m)
    total = readout(Qtotal, length_m)
    values, vectors = np.linalg.eigh(Qtotal)
    theta_opt = float(np.arctan2(vectors[1,0], vectors[0,0]))
    theta_opt = (theta_opt+np.pi/2)%np.pi-np.pi/2
    return dict(length_m=length_m, LD_m=LD_M, zeta=zeta,
                exact_sech_input_mW=PIN_SECH_MW, Q_optical=Q.tolist(),
                Raman_Qyy=Ryy, optical_plus_BS=optical,
                Raman_F=total['F']-optical['F'], total=total,
                unrestricted_quadrature_min_F=float(1-ETA+ETA*values[0]),
                optimal_quadrature_angle_rad=theta_opt,
                accessible_angle_max_rad=float(np.arcsin(np.sqrt((1-ETA)/ETA)*R)))


if __name__ == '__main__':
    Q0 = optical_covariance(0.)
    assert np.max(np.abs(Q0-np.eye(2))) < 1e-9, Q0
    result = benchmark()
    print(json.dumps(result, indent=2))
    Path('soliton_copy_analytic_benchmark.json').write_text(json.dumps(result, indent=2))
