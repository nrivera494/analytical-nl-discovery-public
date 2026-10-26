"""Raman budget on the number of nonlinear lengths in silica fibre (for the lab-test sections).

For quasi-CW light, stimulated Raman scattering from noise reaches threshold when
g_R P L_eff / A_eff ~ 16 (Smith's criterion). With gamma = n2 omega / (c A_eff), the Kerr phase at
threshold is phi_max = gamma P L = 16 n2 omega / (c g_R), independent of power and area.
For a coupled-core array at the balance gamma P = C, phi_max equals the number of coupling
lengths C L available. The numbers below use n2 = 2.6e-20 m^2/W and peak Raman gain
g_R = 1.0e-13 m/W at 1064 nm, 6.0e-14 m/W at 1550 nm (silica, co-polarized; textbook values,
Agrawal, Nonlinear Fiber Optics). Order-of-magnitude only.

Also: incoherent-light weak-turbulence numbers for a PM dispersion-shifted fibre near its zero-
dispersion wavelength (candidate S5), with L_lin = 1/(beta3 dw^3) and eps = L_lin / L_NL.
Run: ~/agent-work/venv/bin/python -W ignore raman_budget.py   (writes raman_budget.json)
"""
import json
import numpy as np

c = 2.998e8
n2 = 2.6e-20
out = {'assumptions': {'n2_m2_per_W': n2, 'gR_1064_m_per_W': 1.0e-13, 'gR_1550_m_per_W': 6.0e-14,
                       'smith_threshold_gain': 16}}
for lam, gR in [(1064e-9, 1.0e-13), (1550e-9, 6.0e-14)]:
    omega = 2 * np.pi * c / lam
    phi_max = 16 * n2 * omega / (c * gR)
    out[f'phi_max_rad_at_{int(lam*1e9)}nm'] = round(float(phi_max), 1)

# S5 numbers: PM-DSF, gamma = 2 /W/km, beta3 = 0.1 ps^3/km, P = 1 W
gamma = 2e-3; beta3 = 0.1e-36 / 1e3; P = 1.0
LNL = 1 / (gamma * P)
s5 = {}
for bw_THz in [0.06, 0.25, 1.0, 2.0]:
    dw = 2 * np.pi * bw_THz * 1e12
    Llin = 1 / (beta3 * dw**3)
    eps = Llin / LNL
    s5[f'{bw_THz}THz'] = {'L_lin_m': float(f'{Llin:.3g}'), 'L_NL_m': LNL, 'eps': float(f'{eps:.3g}'),
                          'L4_m_~LNL/eps': float(f'{LNL/eps:.3g}'),
                          'L6_m_~LNL/eps^3_(delta=1)': float(f'{LNL/eps**3:.3g}')}
out['S5_PM_DSF_gamma2_beta3_0.1ps3perkm_P1W'] = s5
out['S5_note'] = ('L4 and L6 are scaling estimates without prefactors: four-wave kinetic length L_NL/eps and '
                  'six-wave length L_NL/eps^3 (integrability-breaking parameter delta = 1). '
                  'Compare with the Raman budget gamma P L <~ phi_max.')


# Coupled-core array (card -02): with A_j = gamma |E_j|^2 / (2C), a = gamma Pbar / (2C).
# A random-phase launch into k of N cores has h/a^2 = N/k; the lit cores carry P_lit = (N/k) Pbar.
# CW Raman budget on the lit cores: gamma P_lit L <= phi_max  =>  C L <= phi_max k / (2 a N).
cc = {}
for lam_key in ['phi_max_rad_at_1064nm']:
    phi = out[lam_key]
    for a in [0.25, 0.5, 1.0]:
        for kN in [0.2, 1/3, 0.45]:
            cc[f'a={a},k/N={round(kN,2)}'] = round(phi * kN / (2 * a), 1)
out['coupled_core_CW_max_coupling_lengths_CL_at_1064nm'] = cc
# Picosecond pulses: pump-Stokes walk-off length L_W = T0 / (beta2 * Omega_R), beta2 = 20 ps^2/km at 1064 nm,
# Omega_R = 2 pi 13.2 THz; dispersion length L_D = T0^2 / beta2.
beta2 = 20e-27   # s^2/m
OmR = 2 * np.pi * 13.2e12
ps = {}
for T0 in [1e-12, 3e-12, 10e-12]:
    ps[f'T0={T0*1e12:.0f}ps'] = {'L_W_m': round(T0 / (beta2 * OmR), 2), 'L_D_m': round(T0**2 / beta2, 1)}
out['ps_pulse_walkoff_and_dispersion_lengths_1064nm'] = ps

print(json.dumps(out, indent=1))
with open('raman_budget.json', 'w') as f:
    json.dump(out, f, indent=1)
