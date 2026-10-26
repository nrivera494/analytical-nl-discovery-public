"""Summarize gauss_state.json (raw_location) into summary.json: per case and checkpoint, the multimode squeezing,
the photon-counting bound lambda_gen, and condensate (mode 0) diagnostics; plus a log-log slope of lambda_gen vs z."""
import json, os, numpy as np
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-grin-gaussian-state')
here = os.path.dirname(os.path.abspath(__file__))
res = json.load(open(os.path.join(RAW, 'gauss_state.json')))
cases = []
for o in res:
    rec = []
    for r in o['records']:
        m = {mm['group']: mm for mm in r['modes']}
        rec.append(dict(z=r['z'], multimode_min_quad_dB=round(r['multimode_min_quad_dB'], 1), lambda_gen_dB=round(r['lambda_gen_dB'], 1),
                        Fano_N=round(r['Fano_N'], 4), condensate_S_ent=round(m[0]['S_ent'], 2), condensate_min_quad_dB=round(m[0]['min_quad_dB'], 2),
                        condensate_Fano=round(m[0]['Fano'], 2), group1_S_ent=round(m[1]['S_ent'], 2), log_sigma_max=round(r['log_sigma_max'], 2)))
    z = np.array([x['z'] for x in rec]); lg = np.array([x['lambda_gen_dB'] for x in rec])
    sel = z >= 10
    slope = float(np.polyfit(np.log10(z[sel]), lg[sel], 1)[0])
    best_cond = float(min(x['condensate_min_quad_dB'] for x in rec if x['z'] <= 100))
    cases.append(dict(K=o['K'], M=o['M'], Eprime=o['Eprime'], sigma=o['sigma'], dz=o['dz'],
                      lambda_gen_dB_per_decade_z_ge_10=round(slope, 1), best_condensate_quad_dB_z_le_100_at_checkpoints=round(best_cond, 1),
                      records=rec))
json.dump(dict(note="Linearized (pre-scrambling) Gaussian state from the classical tangent map; vacuum units, n-independent; valid while single-mode Fano factors << photons per mode per cell. Ideal: no loss, no Raman. Checkpoints z = 1,2,5,10,20,50,100,200,300,400 L_NL only.", cases=cases),
          open(os.path.join(here, 'summary.json'), 'w'), indent=1)
for c in cases: print(c['Eprime'], c['sigma'], 'lam_gen slope dB/decade', c['lambda_gen_dB_per_decade_z_ge_10'], 'best condensate quad dB (z<=100)', c['best_condensate_quad_dB_z_le_100_at_checkpoints'])
