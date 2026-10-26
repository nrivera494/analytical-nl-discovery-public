"""Summary of exact_vs_twa_*.json: exact quantum vs truncated Wigner (TWA) for the 4-mode resonant toy.
Adds the closed forms for SPM/XPM-only ("frozen-power") dynamics about the input powers, theta_q = Lambda_0q z:
  exact: -ln coh_0 = 4 sum_q n_q sin^2(theta_q/2)
  TWA:   -ln coh_0 = sum_q n_q theta_q^2/(1 + theta_q^2/4) + 2 ln(1 + theta_0^2/4) + sum_{q>0} ln(1 + theta_q^2/4)
(Gaussian Wigner function of the coherent input, variance 1/2 per mode; the Weyl-ordering terms only add deterministic phases.)
Writes summary.json."""
import json, numpy as np, glob
import exact_vs_twa as ev
S_TOY = ev.S.copy(); M = ev.M
import exact_vs_twa_grin as eg   # note: this import resets ev's tensor globals to the GRIN subset
S_GRIN = eg.S.copy()
out = {}
for fn in sorted(glob.glob('exact_vs_twa_*.json')):
    for r in json.load(open(fn)):
        n = r['n']; z = np.array(r['z']); g = 1.0/n; nq = n*np.array(r['frac']); S = S_GRIN if r.get('tensor') == 'grin4' else S_TOY
        th = np.outer(z, [g*S[0, 0, 0, 0]] + [2*g*S[0, 0, q, q] for q in range(1, M)])
        ex_fr = np.exp(-4*np.sum(nq*np.sin(th/2)**2, 1))
        tw_fr = np.exp(-(np.sum(nq*th**2/(1 + th**2/4), 1) + 2*np.log(1 + th[:, 0]**2/4) + np.sum(np.log(1 + th[:, 1:]**2/4), 1)))
        ce, cw, ecw = np.array(r['coh_exact']), np.array(r['coh_twa_weyl']), np.array(r['coh_twa_weyl_err'])
        cb, ecb = np.array(r['coh_twa_bare']), np.array(r['coh_twa_bare_err'])
        fe, fw, efw = np.array(r['fano_exact']), np.array(r['fano_twa_weyl']), np.array(r['fano_twa_weyl_err'])
        d = ce - cw; i = int(np.argmax(np.abs(d)))
        key = f"{r['tag']}_n{n}"
        # Fano: where the exact curve has its minimum, and the TWA minimum (depth and position)
        ie, iw = int(np.argmin(fe)), int(np.argmin(fw))
        out[key] = dict(tag=r['tag'], tensor=r.get('tensor', 'toy4'), n=n,
            fano_exact_min=float(fe[ie]), fano_exact_min_z=float(z[ie]), fano_twa_weyl_min=float(fw[iw]), fano_twa_weyl_min_z=float(z[iw]),
            fano_exact_max_z=float(z[int(np.argmax(fe))]), fano_twa_weyl_max=float(fw.max()), fano_twa_weyl_max_z=float(z[int(np.argmax(fw))]), frac=r['frac'], z_max=float(z[-1]),
            captured_norm=r['exact_info']['norm'], max_sector_dim=r['exact_info']['maxdim'],
            zhalf_over_sqrt_n=dict(exact=r['zhalf_exact'] and r['zhalf_exact']/np.sqrt(n), twa_weyl=r['zhalf_twa_weyl'] and r['zhalf_twa_weyl']/np.sqrt(n),
                                   twa_bare=r['zhalf_twa_bare'] and r['zhalf_twa_bare']/np.sqrt(n), frozen_exact=r['zhalf_frozen'] and r['zhalf_frozen']/np.sqrt(n)),
            max_abs_coh_exact_minus_twa_weyl=float(np.abs(d).max()), at_z=float(z[i]), coh_exact_there=float(ce[i]),
            twa_weyl_err_there=float(ecw[i]), max_abs_dev_in_sigma=float(np.max(np.abs(d)/np.maximum(ecw, 1e-12))),
            rms_coh_exact_minus_twa_weyl=float(np.sqrt(np.mean(d**2))), rms_twa_weyl_err=float(np.sqrt(np.mean(ecw**2))),
            max_abs_coh_twa_weyl_minus_bare=float(np.abs(cw - cb).max()),
            max_abs_coh_exact_minus_frozen_exact=float(np.abs(ce - ex_fr).max()),
            max_abs_coh_twa_weyl_minus_frozen_twa=float(np.abs(cw - tw_fr).max()),
            max_abs_frozen_exact_minus_frozen_twa=float(np.abs(ex_fr - tw_fr).max()),
            fano_exact_max=float(fe.max()), fano_exact_end=float(fe[-1]), fano_twa_weyl_end=float(fw[-1]), fano_twa_weyl_err_end=float(efw[-1]),
            max_abs_fano_exact_minus_twa_weyl=float(np.abs(fe - fw).max()), max_fano_dev_in_sigma=float(np.max(np.abs(fe - fw)/np.maximum(efw, 1e-12))),
            coh_exact_end=float(ce[-1]), coh_twa_weyl_end=float(cw[-1]))
for tag in sorted({v['tag'] for v in out.values()}):
    rows = sorted([v for v in out.values() if v.get('tag') == tag], key=lambda v: v['n'])
    if len(rows) >= 2:
        ns = np.array([v['n'] for v in rows]); dm = np.array([v['max_abs_coh_exact_minus_twa_weyl'] for v in rows])
        dfr = np.array([v['max_abs_frozen_exact_minus_frozen_twa'] for v in rows])
        out[f'{tag}_exponent'] = dict(n=ns.tolist(), slope_loglog_max_abs_dcoh=float(np.polyfit(np.log(ns), np.log(dm), 1)[0]),
                                      slope_loglog_frozen_closed_form=float(np.polyfit(np.log(ns), np.log(dfr), 1)[0]),
                                      n_times_max_abs_dcoh=(ns*dm).tolist(), n_times_frozen_closed_form=(ns*dfr).tolist())
json.dump(out, open('summary.json', 'w'), indent=1)
for k, v in out.items():
    if k.endswith('_exponent'): print(k, json.dumps(v)); continue
    zh = v['zhalf_over_sqrt_n']
    print(f"{k}: norm {v['captured_norm']:.8f} dim<= {v['max_sector_dim']}; zhalf/sqrt(n) ex {zh['exact']}, weyl {zh['twa_weyl']}, frozen {zh['frozen_exact']}; "
          f"max|dcoh| {v['max_abs_coh_exact_minus_twa_weyl']:.4f} at z {v['at_z']:.1f} (coh {v['coh_exact_there']:.3f}, err {v['twa_weyl_err_there']:.4f}, {v['max_abs_dev_in_sigma']:.1f} sigma max); "
          f"rms dcoh {v['rms_coh_exact_minus_twa_weyl']:.4f} vs rms err {v['rms_twa_weyl_err']:.4f}; weyl-bare {v['max_abs_coh_twa_weyl_minus_bare']:.4f}; "
          f"ex-frozen {v['max_abs_coh_exact_minus_frozen_exact']:.4f}; frozen ex-twa (closed form) {v['max_abs_frozen_exact_minus_frozen_twa']:.4f}; "
          f"Fano ex max {v['fano_exact_max']:.2f} end {v['fano_exact_end']:.2f} vs TWA {v['fano_twa_weyl_end']:.2f}+-{v['fano_twa_weyl_err_end']:.2f}; coh end ex {v['coh_exact_end']:.3f} TWA {v['coh_twa_weyl_end']:.3f}")
