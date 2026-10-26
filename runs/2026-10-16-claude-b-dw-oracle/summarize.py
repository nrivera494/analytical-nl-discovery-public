"""Collect the numbers quoted in claims/logs into summary.json (run 2026-10-16-claude-b-dw-oracle)."""
import json, glob, os, numpy as np
from lawfit import load, fit3, local_slopes
S = dict(run_id='2026-10-16-claude-b-dw-oracle', agent='claude-b', model='claude-opus-5-5', family='claude')
S['unit_checks'] = json.load(open('test_lib.json'))
S['two_integrators_M0'] = json.load(open('m0_two_integrators.json'))
v = json.load(open('singularity_validation.json'))['sech2']
S['strip_fit_validation_N2'] = dict(max_abs_err_near_min=max(abs(r['d_fit'] - r['d_exact']) for r in v if 0.65 <= r['xi'] <= 0.9))
dd = {}
for f in ['dstar2_gauss3.json', 'dstar2_gauss4.json', 'dstar2_sech3.json', 'dstar_gauss3_second_compression.json']:
    if os.path.exists(f):
        dd[f] = [dict((k, r[k]) for k in ('Nt', 'TW', 'h', 'xi_star', 'd_star') if k in r) for r in json.load(open(f))]
d2 = json.load(open('dstar_sech2_sech3.json'))['sech2']
dd['sech2'] = [dict(Nt=r['Nt'], TW=r['TW'], h=r['h'], xi_star=r['xi_star'], d_star=r['d_star']) for r in d2]
S['dstar'] = dd
S['dscan_full'] = {k: json.load(open(f))['local_minima'] for k, f in [('gauss3_xi2', 'dscan_full_gauss3.json'), ('gauss4_xi1', 'dscan_full_gauss4.json')] if os.path.exists(f)}
def lawset(files, dstar):
    d3, eta, conv, g5 = load(files)
    mid, s = local_slopes(d3, eta)
    return dict(d3=d3.tolist(), eta_DW=eta.tolist(), step_conv=conv.tolist(), fit3=fit3(d3, eta, 3), fit4=fit3(d3, eta, 4),
                fit5=fit3(d3, eta, 5), slope_mid=mid.tolist(), slope=s.tolist(), dstar=dstar)
S['law'] = dict(sech2=lawset(['yield_sech2a.json', 'yield_sech2b.json', 'yield_roy.json'], 0.374664),
                sech3=lawset(['yield_s3.json'], 0.1997), gauss4_xi1=lawset(['yield_g4.json'], 0.1322),
                gauss3_xi2=lawset(['yield_g3.json'], 0.1923), gauss3_xi1=lawset(['yield_g3L1.json'], 0.2015))
roy = json.load(open('yield_roy.json'))
S['roy_reproduction'] = [dict(d3=r['d3'], nsr_dB=r['h2']['nsr_dB_input'], dnuT0=r['h2']['nsr_dnuT0'], eta_B=r['h2']['eta_B']['4'],
                              eta_DW=r['h2']['eta_DW'], roy_TODonly_digitised_dB={0.02: -22, 0.03: -14, 0.04: -12, 0.06: -10, 0.1: -6}[r['d3']],
                              roy_eq6_dB=float(10*np.log10((5*np.pi*2/(4*r['d3']))**2*(1 - 2*np.pi/5*3*r['d3'])**2*np.exp(-np.pi/(2*3*r['d3'])))))
                         for r in roy]
card = []
for f in ['yield_cardA.json', 'yield_cardB.json']:
    for r in json.load(open(f)):
        card.append(dict(N=r['N'], d3=r['d3'], eta_B=r['h2']['eta_B'], eta_DW=r['h2']['eta_DW'], leak0=r['h2']['leak0'],
                         step_conv=r['conv_eta_B'], dH_rel=r['h2']['dH_rel'], dE_rel=r['h2']['dE_rel'], dP=r['h2']['dP']))
S['card_grid_TL'] = card
for f in ['gdd_curve_N3_d0.01.json', 'gdd_curve_N3_d0.006.json']:
    if os.path.exists(f): S[f[:-5]] = json.load(open(f))
for f in ['dstar_chirp_N3_a.json', 'dstar_chirp_N3_b.json']:
    if os.path.exists(f): S.setdefault('dstar_chirp', []).extend(json.load(open(f))['res'])
for f in ['h4_raman_roy.json', 'h4_raman_card.json', 'h4_dstar_m1.json']:
    if os.path.exists(f):
        x = json.load(open(f))
        S[f[:-5]] = x if f != 'h4_dstar_m1.json' else {k: v['min_blue'] for k, v in x.items()}
m1 = []
for f in sorted(glob.glob('h4_law_m1_*.json')):
    for r in json.load(open(f)): m1.append(dict(d3=r['d3'], eta_DW=r['h2']['eta_DW'], eta_B=r['h2']['eta_B'], kernel_dt_fs=r['h2']['kernel_dt_fs']))
S['m1_sech2_sweep'] = sorted(m1, key=lambda r: r['d3'])
g = []
for f in sorted(glob.glob('h4_g3_m1_*.json')):
    for r in json.load(open(f)): g.append(dict(d3=r['d3'], eta_DW=r['h2']['eta_DW'], eta_DW_tg20=r['h2']['eta_DW_tg20'], conv=r['conv_eta_DW'], kernel_dt_fs=r['h2']['kernel_dt_fs']))
S['m1_gauss3_heldout'] = sorted(g, key=lambda r: r['d3'])
if len(g) >= 3:
    d3 = np.array([r['d3'] for r in S['m1_gauss3_heldout']]); eta = np.array([r['eta_DW'] for r in S['m1_gauss3_heldout']])
    S['m1_gauss3_fit4'] = fit3(d3, eta, min(4, len(d3)))
if len(m1) >= 3:
    d3 = np.array([r['d3'] for r in S['m1_sech2_sweep']]); eta = np.array([r['eta_DW'] for r in S['m1_sech2_sweep']])
    S['m1_sech2_fit4'] = fit3(d3, eta, 4); S['m1_sech2_slopes'] = dict(zip(['mid', 'slope'], [x.tolist() for x in local_slopes(d3, eta)]))
for f in ['n1_flux_a.json', 'n1_flux_b.json']:
    if os.path.exists(f): S.setdefault('n1_flux', []).extend(json.load(open(f)))
for f in sorted(glob.glob('poly_yield_*.json')): S[f[:-5]] = json.load(open(f))
for f in ['dstar_poly_a.json', 'dstar_poly_b.json']:
    if os.path.exists(f): S.setdefault('dstar_poly_robust', []).extend([{k: v for k, v in r.items() if k != 'curve'} for r in json.load(open(f))])
if os.path.exists('gdd_vs_dstar.json'): S['gdd_vs_dstar'] = json.load(open('gdd_vs_dstar.json'))
if os.path.exists('../2026-10-16-claude-b-dw-shaping/window_check.json'): S['window_check'] = json.load(open('../2026-10-16-claude-b-dw-shaping/window_check.json'))
S['law']['sech4_xi2_A11'] = lawset(['yield_s4a.json', 'yield_s4b.json'], 0.1342)
S['law']['sech4_xi2_with_exploration'] = lawset(['yield_s4a.json', 'yield_s4b.json', 'yield_s4c.json', 'yield_s4d.json'], 0.13335)
for f in ['dscan_sech4.json']:
    if os.path.exists(f): S['dscan_sech4_local_minima'] = json.load(open(f))['local_minima'][:12]
for f in sorted(glob.glob('dstar_card_*.json')): S.setdefault('dstar_card', []).extend(json.load(open(f)))
for f in ['dstar_fine_N8.json']:
    if os.path.exists(f):
        J = json.load(open(f)); S['dstar_fine_N8'] = [dict(Nt=r['Nt'], TW=r['TW'], min=min([c for c in r['curve'] if c[1] == c[1]], key=lambda t: t[1])) for r in J]
if os.path.exists('collapse.json'):
    C = json.load(open('collapse.json')); S['collapse'] = dict(dstar=C['dstar'], median_spread_x=float(np.median(C['spread_x'])), max_spread_x=float(max(C['spread_x'])),
                                                             median_spread_roy=float(np.median(C['spread_roy'])), max_spread_roy=float(max(C['spread_roy'])), points=C['points'])
for f in sorted(glob.glob('rk4ip_heldout_*.json')): S[f[:-5]] = json.load(open(f))
json.dump(S, open('summary.json', 'w'), indent=1, default=float)
print('written', {k: (v if not isinstance(v, (list, dict)) else '...') for k, v in S.items()})
print('M1 sech2 fit4', S.get('m1_sech2_fit4')); print('M1 gauss3 fit', S.get('m1_gauss3_fit4'))
