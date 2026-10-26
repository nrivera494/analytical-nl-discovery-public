"""Small algebra/Fourier checks, not a propagation or ZS verification.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import json
import pathlib
import time
import numpy as np

start = time.monotonic()
run = pathlib.Path(__file__).resolve().parent
raw = pathlib.Path('~/analytical-nl-discovery-data') / run.name
raw.mkdir(parents=True, exist_ok=True)
seed = 20261016
rng = np.random.default_rng(seed)
checks = {}
mask_rows = []
raman_rows = []
for size in (2048, 4096):
    window = 80.0
    dt = window / size
    t = np.arange(size) * dt - window / 2
    omega = -2 * np.pi * np.fft.fftfreq(size, dt)
    # q = inverse discrete Fourier transform; FFT sign is explicit above.
    spectrum = np.exp(-omega**2 / 2)
    tl = np.fft.ifft(spectrum)
    peak = np.max(np.abs(tl))
    quartic = dt * np.sum(np.abs(tl)**4)
    for k in range(64):
        coeff = rng.normal(size=4)
        phase = sum(coeff[j] * np.sin((j + 1) * omega / 3) for j in range(4))
        mask = np.exp(1j * phase)
        if k % 2:
            mask *= np.exp(-abs(rng.normal()) * omega**2 / 8)
        q = np.fft.ifft(mask * spectrum)
        mask_rows.append([size, k, np.max(abs(q)) / peak,
                          dt * np.sum(abs(q)**4) / quartic])
    q = 2 / np.cosh(t)
    derivative = np.fft.ifft(-1j * omega * np.fft.fft(q))
    mass = dt * np.sum(abs(q)**2)
    kinetic = dt * np.sum(abs(derivative)**2)
    gn_ratio = dt * np.sum(abs(q)**4) / (mass**1.5 * kinetic**0.5 / np.sqrt(3))
    checks[str(size)] = {'sech_sharp_GN_ratio': float(gn_ratio)}
    carrier, gamma, fraction, damping, resonance = 300., 0.7, 0.18, 0.7, 2.
    assert np.all(carrier + omega > 0)
    h = (damping**2 + resonance**2) / ((damping - 1j * omega)**2 + resonance**2)
    for chirp in (-1., 0., 1.):
        a = np.exp(-t**2 / 2) * np.exp(1j * chirp * t**2 / 2)
        intensity = abs(a)**2
        response = (1 - fraction) * intensity + fraction * np.fft.ifft(h * np.fft.fft(intensity)).real
        ahat = dt * np.fft.fft(a)
        rhs_hat = 1j * gamma * (1 + omega / carrier) * dt * np.fft.fft(a * response)
        rhs = np.fft.ifft(rhs_hat) / dt
        energy = dt * np.sum(intensity)
        number = np.sum(abs(ahat)**2 / (carrier + omega)) / window
        number_dot = 2 * np.real(np.vdot(ahat / (carrier + omega), rhs_hat)) / window
        energy_dot = 2 * dt * np.real(np.vdot(a, rhs))
        intensity_hat = dt * np.fft.fft(intensity)
        expected = -gamma * fraction / (carrier * window) * np.sum(omega * h.imag * abs(intensity_hat)**2)
        mean_dot = (energy_dot * number - energy * number_dot) / number**2
        bound = gamma * fraction * (energy / number / carrier) * max(intensity) * max(omega * h.imag)
        raman_rows.append({'grid': size, 'chirp': chirp,
                          'number_derivative': float(number_dot),
                          'energy_derivative_direct': float(energy_dot),
                          'energy_derivative_spectral': float(expected),
                          'identity_absolute_error': float(abs(energy_dot - expected)),
                          'photon_mean_derivative': float(mean_dot),
                          'mean_rate_over_bound': float(abs(mean_dot) / bound)})

# Moment extremizer: blue point at threshold and complement at its mean.
blue_threshold, recoil, red_drift = 2., 3., 0.4
eta = (recoil - red_drift) / (blue_threshold + recoil)
mean = eta * blue_threshold - (1 - eta) * recoil
# Loss of red photons raises the surviving mean, without frequency conversion.
w, weights, alpha = np.array([1., 3.]), np.array([0.8, 0.2]), np.array([2., 0.])
loss_mean_dot = -(np.dot(weights, w * alpha) - np.dot(weights, w) * np.dot(weights, alpha))
# This sequence defeats only the original, one-inequality relaxation, not the PDE.
tail_rows = []
for epsilon in (0.1, 0.03, 0.01, 0.003):
    freq = np.array([1., -(1 - epsilon) / epsilon])
    weights = np.array([1 - epsilon, epsilon])
    m2 = np.dot(weights, freq**2)
    dispersive = np.dot(weights, freq**2 / 2 + freq**3 / 6)
    tail_rows.append({'epsilon': epsilon, 'band_fraction': 1 - epsilon,
                     'momentum': float(np.dot(weights, freq)),
                     'dispersive_moment': float(dispersive),
                     'original_constraint_lhs_H0': float(dispersive - np.sqrt(m2 / 3) / 2),
                     'fails_omitted_H_le_MK': bool(dispersive < 0)})
np.save(raw / 'mask_checks.npy', np.array(mask_rows))
(raw / 'raman_checks.json').write_text(json.dumps(raman_rows, indent=2) + '\n')
summary = {'run_id': run.name, 'agent': 'gpt-b', 'model': 'gpt-6-astra', 'family': 'gpt',
           'seed': seed, 'wall_seconds': time.monotonic() - start,
           'mask_count': len(mask_rows),
           'max_peak_ratio': max(row[2] for row in mask_rows),
           'max_quartic_ratio': max(row[3] for row in mask_rows),
           'GN_checks': checks, 'raman_checks': raman_rows,
           'moment_bound': {'eta': eta, 'constructed_mean': mean,
                            'target_mean': -red_drift},
           'selective_loss_mean_derivative': float(loss_mean_dot),
           'original_DW_relaxation_tail_sequence': tail_rows,
           'scope': 'Algebra and instantaneous RHS only; no propagation, eigenvalue computation, or claim verification.'}
assert summary['max_peak_ratio'] <= 1 + 1e-12
assert summary['max_quartic_ratio'] <= 1 + 1e-12
assert max(row['identity_absolute_error'] for row in raman_rows) < 1e-12
assert max(abs(row['number_derivative']) for row in raman_rows) < 1e-12
assert all(row['photon_mean_derivative'] < 0 and row['mean_rate_over_bound'] <= 1 for row in raman_rows)
assert abs(mean + red_drift) < 1e-14
assert loss_mean_dot > 0
(run / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
