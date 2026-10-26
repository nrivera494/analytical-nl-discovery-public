"""Summary and pre-registered checks (predictions.md T1-T5) for ensemble_thermalization.jsonl -> summary.json, summary.txt.
Also Q6 (Sagnac floor of the Dirichlet condensate) of ../2026-10-17-claude-interactive.7-ensemble-squeezing/predictions.md, from E1 at E' = 0.6."""
import json, numpy as np
rows = [json.loads(l) for l in open('ensemble_thermalization.jsonl')]
def grp(ens, kind, Ep, sigma):
    return [r for r in rows if r['ens'] == ens and r['kind'] == kind and abs(r['Eprime'] - Ep) < 1e-3 and r['sigma'] == sigma]
def stats(g):
    I0 = np.array([r['I0'] for r in g]); d = np.array([r['I0'] - r['I0_D'] for r in g]); g2 = np.array([r['g2_ex'] for r in g])
    v = np.array([r['VarI0']/r['VarI0_D'] for r in g]); DR = np.array([r['D_RJ'] for r in g]); be = np.array([r['block_err_I0'] for r in g])
    Lr = [r['L_rel'] for r in g]; zon = [r['z_on'] for r in g]
    return dict(n=len(g), I0_mean=float(I0.mean()), I0_sd=float(I0.std(ddof=1)), dI0_mean=float(d.mean()), dI0_maxabs=float(np.abs(d).max()),
                g2_mean=float(g2.mean()), g2_sd=float(g2.std(ddof=1)), g2_min=float(g2.min()), g2_max=float(g2.max()),
                VarRatio_mean=float(v.mean()), VarRatio_sd=float(v.std(ddof=1)), VarRatio_min=float(v.min()), VarRatio_max=float(v.max()),
                DRJ_median=float(np.median(DR)), DRJ_max=float(DR.max()), DRJ_min=float(DR.min()), block_err_median=float(np.median(be)),
                L_rel=Lr, z_on=zon, I0_max=[r['I0_max'] for r in g], I0_D=g[0]['I0_D'] if g else None)
out = dict(groups={}, checks={})
for ens, kind, Eps, sig in [('E1', 'deph', [0.3, 0.6, 0.9], 0.3), ('E2', 'deph', [0.3, 0.6, 0.9], 0.3), ('E3', 'deph', [0.3, 0.6, 0.9], 0.0),
                            ('E4', 'G1', [1.0], 0.3), ('E4', 'G1', [1.0], 0.0), ('E5', 'focused', [0.6, 0.9], 0.3), ('E5', 'focused', [0.6, 0.9], 0.0)]:
    for Ep in Eps:
        g = grp(ens, kind, Ep, sig)
        if g: out['groups'][f'{ens}_{kind}_E{Ep}_s{sig}'] = stats(g)
G = out['groups']; C = out['checks']
def chk(name, ok, detail): C[name] = dict(pass_=bool(ok), detail=detail)
for ens in ['E1', 'E2']:
    for Ep in [0.6, 0.9]:
        k = f'{ens}_deph_E{Ep}_s0.3'; g = grp(ens, 'deph', Ep, 0.3); s = G.get(k)
        if not s: continue
        n_in = sum(abs(r['I0'] - r['I0_D']) <= 0.015 for r in g); n_drj = sum(r['D_RJ'] <= 0.15 for r in g)
        g2ok = abs(s['g2_mean'] - 1.8667) <= 0.03 and all(abs(r['g2_ex'] - 1.8667) <= 0.06 for r in g)
        vok = abs(s['VarRatio_mean'] - 1) <= 0.15 and all(abs(r['VarI0']/r['VarI0_D'] - 1) <= 0.35 for r in g)
        chk(f'T1_{ens}_E{Ep}', n_in >= 11 and s['I0_sd'] <= 0.01 and g2ok and vok and n_drj >= 11,
            f"|dI0|<=0.015: {n_in}/{s['n']}; SD(I0) {s['I0_sd']:.4f}; g2 mean {s['g2_mean']:.3f} range [{s['g2_min']:.3f}, {s['g2_max']:.3f}]; Var/Var_D mean {s['VarRatio_mean']:.2f} range [{s['VarRatio_min']:.2f}, {s['VarRatio_max']:.2f}]; D_RJ<=0.15: {n_drj}/{s['n']}")
    g = grp(ens, 'deph', 0.3, 0.3); s = G.get(f'{ens}_deph_E0.3_s0.3')
    if s:
        n_in = sum(abs(r['I0'] - 0.8696) <= 0.03 for r in g); n_drj = sum(r['D_RJ'] <= 0.25 for r in g)
        chk(f'T1b_{ens}_E0.3', n_in >= 11 and n_drj >= 11, f"|dI0|<=0.03: {n_in}/{s['n']}; D_RJ<=0.25: {n_drj}/{s['n']}; D_RJ median {s['DRJ_median']:.3f} max {s['DRJ_max']:.3f}")
    for Ep in [0.3, 0.6, 0.9]:
        s = G.get(f'{ens}_deph_E{Ep}_s0.3')
        if s: chk(f'T2_{ens}_E{Ep}', s['I0_sd'] <= 2*s['block_err_median'], f"SD(I0) {s['I0_sd']:.4f} vs 2 x median block error {2*s['block_err_median']:.4f}")
for Ep in [0.3, 0.6, 0.9]:
    g = grp('E3', 'deph', Ep, 0.0); s3 = G.get(f'E3_deph_E{Ep}_s0.0'); s2 = G.get(f'E2_deph_E{Ep}_s0.3')
    if s3 and s2:
        n_dev = sum(r['D_RJ'] > 0.15 for r in g)
        chk(f'T3_E{Ep}', n_dev >= 9 and s3['I0_sd'] >= 2*s2['I0_sd'], f"D_RJ>0.15: {n_dev}/{s3['n']} (median {s3['DRJ_median']:.3f}); SD(I0) Kerr-only {s3['I0_sd']:.4f} vs with disorder {s2['I0_sd']:.4f}")
g = grp('E4', 'G1', 1.0, 0.3)
if g: chk('T4_sigma0.3', all(r['z_on'] is not None and r['z_on'] <= 1500 and abs(r['I0'] - 0.5655) <= 0.02 for r in g),
          f"z_on {[r['z_on'] for r in g]}; <I0> {[round(r['I0'], 3) for r in g]}")
g = grp('E4', 'G1', 1.0, 0.0)
if g: chk('T4_sigma0', all(r['I0_max'] < 0.01 for r in g), f"max I0 over z: {[round(r['I0_max'], 4) for r in g]}; <I0> {[round(r['I0'], 3) for r in g]}")
for Ep, c03 in [(0.6, 0.700), (0.9, 0.582)]:
    g = grp('E5', 'focused', Ep, 0.3); s = G.get(f'E5_focused_E{Ep}_s0.3')
    if s: chk(f'T5_E{Ep}_sigma0.3', sum(abs(r['I0'] - r['I0_D']) <= 0.015 for r in g) >= 11, f"|dI0|<=0.015: {sum(abs(r['I0'] - r['I0_D']) <= 0.015 for r in g)}/{s['n']}; mean <I0> {s['I0_mean']:.4f} (D {s['I0_D']:.4f}), SD {s['I0_sd']:.4f}")
    g0 = grp('E5', 'focused', Ep, 0.0)
    if g0: chk(f'T5_E{Ep}_sigma0', abs(g0[0]['I0'] - c03) <= 0.01, f"<I0> {g0[0]['I0']:.4f} vs C-03 {c03}")
g = grp('E1', 'deph', 0.6, 0.3)
if g:
    rv = np.array([r['relvar0'] for r in g]); rvD = 1.481e-3/0.7393**2
    fl = 10*np.log10(rv); flD = 10*np.log10(rvD)
    out['sagnac_floor_Dirichlet'] = dict(relvar0_mean=float(rv.mean()), relvar0_sd=float(rv.std(ddof=1)), relvar0_D=rvD, floor_dB_mean=float(10*np.log10(rv.mean())),
                                         floor_dB_min=float(fl.min()), floor_dB_max=float(fl.max()), floor_dB_D=float(flD))
    chk('Q6_sagnac_floor', abs(rv.mean()/rvD - 1) <= 0.2 and np.all(np.abs(fl - flD) <= 1.5), f"relvar0 mean {rv.mean():.2e} (D {rvD:.2e}); floor {10*np.log10(rv.mean()):.1f} dB, realizations [{fl.min():.1f}, {fl.max():.1f}] dB vs {flD:.1f}")
json.dump(out, open('summary.json', 'w'), indent=1)
lines = []
for k, s in G.items():
    lines.append(f"{k}: n={s['n']} <I0> {s['I0_mean']:.4f} +- {s['I0_sd']:.4f} (D {s['I0_D']:.4f}; max|d| {s['dI0_maxabs']:.4f}) g2 {s['g2_mean']:.3f} +- {s['g2_sd']:.3f} "
                 f"Var/D {s['VarRatio_mean']:.2f} +- {s['VarRatio_sd']:.2f} D_RJ median {s['DRJ_median']:.3f} [{s['DRJ_min']:.3f}, {s['DRJ_max']:.3f}] blockerr {s['block_err_median']:.4f}")
lines.append('--- pre-registered checks ---')
for k, c in C.items(): lines.append(f"{k}: {'PASS' if c['pass_'] else 'FAIL'} | {c['detail']}")
if 'sagnac_floor_Dirichlet' in out: lines.append(f"Sagnac floor (Dirichlet condensate, E1 E'=0.6): {json.dumps(out['sagnac_floor_Dirichlet'])}")
open('summary.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
