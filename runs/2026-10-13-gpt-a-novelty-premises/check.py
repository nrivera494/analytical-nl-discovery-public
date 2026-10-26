"""Cheap premise checks. Agent gpt-a; model gpt-6-astra; family gpt.

Run with ~/agent-work/venv/bin/python runs/<run-id>/check.py.
No repository or solver state is mutated except this run's summary and metadata.
"""
import json
import platform
from pathlib import Path
import subprocess
import time

import numpy as np
from scipy.integrate import quad, solve_ivp

started = time.perf_counter()
here = Path(__file__).resolve().parent
root = here.parents[1]
cfg = json.loads((here / "config.json").read_text())
raw = Path(cfg["raw_location"])
raw.mkdir(parents=True, exist_ok=True)

g = cfg["gaussian"]
P, T, b2, gamma = (g[k] for k in ("P0", "T0", "beta2", "gamma"))
W = g["half_window_T0"] * T
integrate = lambda f: quad(f, -W, W, epsabs=1e-12, epsrel=1e-12)[0]
I = lambda t: P * np.exp(-(t / T) ** 2)
E = integrate(I)
quartic = integrate(lambda t: I(t) ** 2)
gaussian = []
for C in g["chirps"]:
    derivative_norm = integrate(lambda t: (1 + C*C) * t*t / T**4 * I(t))
    H = b2 * derivative_norm / 2 + gamma * quartic / 2
    variance = integrate(lambda t: t*t * I(t)) / E
    predicted = b2 * (1 + C*C) / (4*T*T) + gamma*P/(2*np.sqrt(2))
    gaussian.append(dict(chirp=C, energy=E, temporal_variance=variance,
                         spectral_second_moment=derivative_norm/E,
                         H_over_E=H/E, analytic_H_over_E=predicted))
assert max(abs(x["H_over_E"]-x["analytic_H_over_E"]) for x in gaussian) < 1e-11

p = cfg["recoil"]
b, c = p["b"], p["c"]
beta = lambda w: -b*w*w/2 + c*w**3/6
beta_prime = lambda w: -b*w + c*w*w/2
recoil = []
for r in p["redshifts"]:
    soliton = -r
    corrected = 3*b/c + 3*r
    proposed = 3*b/c + 4*r
    mismatch = lambda d: beta(soliton+d)-beta(soliton)-beta_prime(soliton)*d
    recoil.append(dict(redshift=r, corrected_relative_detuning=corrected,
                       proposed_relative_detuning=proposed,
                       corrected_phase_mismatch=mismatch(corrected),
                       proposed_phase_mismatch=mismatch(proposed),
                       corrected_lab_detuning=corrected-r))
assert max(abs(x["corrected_phase_mismatch"]) for x in recoil) < 1e-11

p = cfg["blue_budget"]
eta, edge, blue, red = (p[k] for k in ("eta", "blue_edge", "blue_conditional_mean", "red_conditional_mean_magnitude"))
mu = eta*blue - (1-eta)*red
D = -mu
budget = dict(centroid=mu, edge_expression=eta*edge-(1-eta)*red,
              exact_conditional_mean_identity=(red-D)/(blue+red),
              corrected_edge_upper_bound=(red-D)/(edge+red), eta=eta)
assert abs(budget["exact_conditional_mean_identity"]-eta) < 1e-12
assert eta <= budget["corrected_edge_upper_bound"]
p = cfg["selective_loss"]
Qr = p["initial_red"]*p["red_transmission"]
Qb = p["initial_blue"]*p["blue_transmission"]
loss = dict(survival_fraction=Qr+Qb, blue_fraction_of_launch=Qb,
            blue_fraction_of_survivors=Qb/(Qr+Qb),
            input_centroid=p["initial_red"]*p["red_frequency"]+p["initial_blue"]*p["blue_frequency"],
            output_centroid=(Qr*p["red_frequency"]+Qb*p["blue_frequency"])/(Qr+Qb))
assert loss["output_centroid"] > loss["input_centroid"]

# Counterexample to an implication, not to a fiber model:
# x'=v0-k*x; S'=-2*k*S+(c/N)*(v0-k*x). ND/v=c locally.
p = cfg["toy_covariance"]
L, N, coeff, target = (p[k] for k in ("L", "Nph", "c", "target_shift"))
toy = []
for k in p["k"]:
    v0 = target*k/(-np.expm1(-k*L))
    def rhs(z, y):
        drift = v0-k*y[0]
        return [drift, -2*k*y[1]+coeff*drift/N]
    sol = solve_ivp(rhs, [0, L], [0, 0], rtol=1e-11, atol=1e-14, dense_output=True)
    x, S = sol.y[:, -1]
    ratio = N*S/x
    predicted = coeff*np.exp(-k*L)
    toy.append(dict(k=k, v0=v0, shift=x, variance=S, final_ratio=ratio,
                    predicted_ratio=predicted, local_ratio=coeff))
    z = np.linspace(0, L, 501)
    np.savez(raw / f"toy-k-{k:g}.npz", z=z, state=sol.sol(z))
assert max(abs(x["final_ratio"]-x["predicted_ratio"]) for x in toy) < 1e-8

# Instantaneous balance-law check for a periodic, band-limited field. Physical
# frequency detuning is minus numpy's FFT frequency (A ~ exp(-i*Omega*t)).
# No integration in z and no solver claim: this checks the nonlinear generator.
raman = []
for points in [256, 512]:
    period = 2*np.pi
    dt = period/points
    t = np.arange(points)*dt
    omega = -2*np.pi*np.fft.fftfreq(points, dt)
    A = np.exp(-1j*t) + (0.4+0.2j)*np.exp(2j*t) + 0.3*np.exp(-3j*t)
    intensity = abs(A)**2
    tau1, tau2, carrier, gamma, fraction = 0.2, 0.4, 300.0, 1.0, 0.18
    h = (tau1**-2+tau2**-2)/((1/tau2-1j*omega)**2+tau1**-2)
    response = np.fft.ifft(h*np.fft.fft(intensity)).real
    nonlinear = A*((1-fraction)*intensity+fraction*response)
    derivative = lambda v: np.fft.ifft(-1j*omega*np.fft.fft(v))
    Af = np.fft.fft(A)
    Q = dt/points*np.sum(abs(Af)**2/(carrier+omega))  # hbar=1
    dissipation = dt/points*np.sum(omega*h.imag*abs(np.fft.fft(intensity))**2)
    for shock in [False, True]:
        Az = 1j*gamma*nonlinear-(gamma/carrier*derivative(nonlinear) if shock else 0)
        Azf = np.fft.fft(Az)
        Ez = 2*dt*np.real(np.vdot(A, Az))
        Qz = 2*dt/points*np.sum(np.real(Af.conj()*Azf)/(carrier+omega))
        expected_Ez = -gamma*fraction/carrier*dissipation if shock else 0.0
        raman.append(dict(points=points, self_steepening=shock, photon_number=Q,
                           energy_rate=Ez, analytic_energy_rate=expected_Ez,
                           photon_number_rate=Qz, positive_raman_integral=dissipation))
        assert abs(Ez-expected_Ez) < 1e-11
        if shock:
            assert abs(Qz) < 1e-12
            assert Ez < 0
        else:
            assert abs(Qz) > 1e-9

summary = dict(run_id=here.name, agent="gpt-a", model="gpt-6-astra", family="gpt",
               scope=cfg["scope"], gaussian=gaussian, recoil=recoil,
               blue_budget=budget, selective_loss=loss, toy_covariance=toy,
               raman_generator=raman,
               passed=True)
(here / "summary.json").write_text(json.dumps(summary, indent=2)+"\n")
(raw / "results.json").write_text(json.dumps(summary, indent=2)+"\n")
solver_commit = subprocess.check_output(["git", "-C", str(root/"solver"), "rev-parse", "HEAD"], text=True).strip()
solver_dirty = bool(subprocess.check_output(["git", "-C", str(root/"solver"), "status", "--porcelain"], text=True).strip())
meta = dict(run_id=here.name, agent="gpt-a", model="gpt-6-astra", family="gpt",
            task="T-20261013-gpt-a-01", solver_commit=solver_commit,
            solver_dirty=solver_dirty, solver_used=False,
            hardware=platform.platform()+"; "+platform.machine(),
            machine=platform.node(), wall_time_seconds=time.perf_counter()-started,
            raw_location=str(raw), seed=cfg["seed"],
            exploration="Premise checks for four chi3 frequency-conversion problem cards")
import yaml
(here / "meta.yaml").write_text(yaml.safe_dump(meta, sort_keys=False))
print(json.dumps(summary, indent=2))
