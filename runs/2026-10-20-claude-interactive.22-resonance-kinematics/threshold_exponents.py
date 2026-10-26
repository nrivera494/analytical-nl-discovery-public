"""Length exponent of the Kerr self-cleaning threshold from published two-length data (card -01).

If P_c is proportional to L^(-x), two lengths give x = ln(P1/P2) / ln(L2/L1).
Kinetic (weak-disorder wave turbulence, L_kin ~ Delta_beta L_NL^2 / S^2, Garnier et al. PRA 100, 053835 (2019))
predicts x = 1/2; an onset at a fixed number of nonlinear lengths (gamma P L = const) gives x = 1.

Inputs are the numbers stated in the sources (no digitizing):
- Pourbeyram et al., Nat. Phys. 18, 685 (2022), arXiv:2012.12110, Fig. 4 caption: RJ reached at ~52 kW in 0.5 m
  (only at the highest power, so an upper bound), onset ~17 kW in 1.5 m.
- Krupa et al., Nat. Photon. 11, 237 (2017), Supplementary Information (as read by helper claude-interactive.22.1):
  12 m: cleaning appears at 0.6 kW, beam-width fluctuations collapse above 2 kW; 3 m: cleaned at 7 kW,
  M^2 stationary at ~10 kW. Different criteria are paired in the range below.
Also the ratio D = L_NL / L_d with the disorder length L_d = 0.4 m estimated by Fusaro et al., PRL 122, 123902 (2019)
for a typical GRIN fibre (not measured in these two experiments; illustrative only).
Run: ~/agent-work/venv/bin/python -W ignore threshold_exponents.py   (writes threshold_exponents.json)
"""
import json
import math


def x(P1, L1, P2, L2):
    return math.log(P1 / P2) / math.log(L2 / L1)


out = {
    'pourbeyram2022_x': round(x(52, 0.5, 17, 1.5), 2),
    'pourbeyram2022_note': '0.5 m value is an upper bound on P_c, so x is an upper bound up to the power-step size',
    'krupa2017_x_like_with_like_(2.0-2.5kW@12m vs 10kW@3m)': [round(x(10, 3, 2.5, 12), 2), round(x(10, 3, 2.0, 12), 2)],
    'krupa2017_x_full_range_(0.6-2.5kW@12m vs 7-10kW@3m)': [round(x(7, 3, 2.5, 12), 2), round(x(10, 3, 0.6, 12), 2)],
    'kinetic_prediction_x': 0.5,
    'fixed_nonlinear_phase_prediction_x': 1.0,
    'pourbeyram_factor_predicted_by_kinetic_for_Lx3': round(3 ** 0.5, 2),
    'pourbeyram_factor_observed': round(52 / 17, 2),
    'D_equals_LNL_over_Ld_illustrative': {
        'pourbeyram_LNL_0.05m_at_top_energy': round(0.05 / 0.4, 3),
        'krupa_LC_0.3m_at_2.5kW': round(0.3 / 0.4, 3),
        'kinetic_theory_requires': 'D >> 1 (L_d << L_NL)',
    },
}

# Onset in units of the nonlinear length. Pourbeyram 2022 main text: L_NL ~ 5 cm at 70 kW (L ~ 30 L_NL in 1.5 m),
# so L_NL(P) = 0.05 m * 70 kW / P. Krupa 2017 SI: L_C ~ 0.3 m at 2.5 kW (fundamental-mode estimate) in 12 m.
LNL = lambda P: 0.05 * 70.0 / P
out['onset_L_over_LNL'] = {
    'pourbeyram_1.5m_17kW': round(1.5 / LNL(17), 1),
    'pourbeyram_0.5m_52kW_(upper bound on P_c, so this is an upper bound)': round(0.5 / LNL(52), 1),
    'krupa_12m_2.5kW_with_LC_0.3m': round(12 / 0.3, 0),
    'note': 'different L_NL definitions (effective areas) in the two papers; only the within-paper constancy matters',
}
print(json.dumps(out, indent=1))
with open('threshold_exponents.json', 'w') as f:
    json.dump(out, f, indent=1)
