#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Compile registered numerical evidence without copying raw arrays into git."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy import linalg as la
import tomli

ROOT=Path(__file__).resolve().parents[1]
RUN='2026-10-10-gpt-a-readout-reference'
DEST=ROOT/'runs'/RUN
RAW=Path('~/analytical-nl-discovery-data')/RUN

def read_toml(path):
    with path.open('rb') as f:return tomli.load(f)

def collect():
    config=read_toml(DEST/'config-main.toml')
    rows=[]
    for case in config['cases']:
        label=case['label'];p=RAW/(label+'.bounds.json')
        if not p.exists():continue
        r=json.loads(p.read_text());t=read_toml(RAW/(label+'.toml'))
        d=np.load(RAW/(label+'.npz'));n=d['nbar'];a=d['V'][:len(n),:len(n)]
        negative=np.minimum(a,0);np.fill_diagonal(negative,np.diag(a))
        sign_bound=float(la.eigh(negative,subset_by_index=(0,0),eigvals_only=True)[0])-1e-9*max(1,la.norm(negative,np.inf))
        r['cheap_certificates']['nonnegative_vector_bound']=sign_bound
        r['best_bound_method']='projective moment/RLT dual or eigenvalue certificate'
        tri=RAW/(label+'.triangles.json')
        if tri.exists():
            r['triangle_certificate']=json.loads(tri.read_text())
            if r['triangle_certificate']['bound']>r['best_bound']:
                r['best_bound']=r['triangle_certificate']['bound']
                r['best_bound_method']='projective moment/RLT plus triangle dual'
        r['best_bound']=max(r['best_bound'],sign_bound)
        r['gap_bound_dB']=float(10*np.log10(r['best_binary_F']/r['best_bound']))
        mask=np.load(RAW/(label+'.bounds.npz'))['best_mask'].astype(bool)
        r['binary_intervals']=int(np.count_nonzero(mask & ~np.r_[False,mask[:-1]]))
        r['config']=case
        for k in ['dt_fs','mean_photons','sampled_raman_integral','temporal_edge_fraction',
                  'spectral_edge_fraction','filter_contraction_error','full_count_F','elapsed_seconds']:
            r['covariance_'+k]=t[k]
        r['faint_formal_mask']=r['transmitted_photons']<1
        r['quantum_counting_caveat']='Formal linearized value; inspect the Gaussian diagnostic and convergence before interpreting as measurable counts.'
        gauss=RAW/(label+'.gaussian.json')
        if gauss.exists():r['gaussian_count_diagnostic']=json.loads(gauss.read_text())
        r['cheap_comparisons']={k:dict(above_field_minimum=bool(v>r['lambda_min']+1e-7),
                    above_generalized_minimum=bool(v>r['lambda_gen']+1e-7))
                    for k,v in r['cheap_certificates'].items() if k in ['full_Weyl','amplitude_Weyl',
                    'amplitude_uncertainty','Temple','nonnegative_vector_bound'] and v is not None}
        if r['faint_formal_mask']:
            omega=d['omega_rad_ps'][mask]
            r['selected_detunings_rad_ps']=omega.tolist()
            r['pair_dispersion_phase_per_step_over_2pi']=(abs(case['beta2_ps2_per_m'])*omega**2*
                case['length_m']/case['steps']/(2*np.pi)).tolist()
        # Histories remain in raw JSON; the summary keeps final certificate facts.
        for key in ['moment_certificate','triangle_certificate']:
            if key in r:
                block=r[key]
                for h in ['history','full_grid_smooth_dual']:
                    if h in block:del block[h]
        rows.append(r)
    convergence=[]
    for path in sorted(RAW.glob('*_mf_*.toml')):
        c=read_toml(path)
        if not c.get('complete'):continue
        sc=path.with_suffix('.core.score.json')
        if sc.exists():
            s=json.loads(sc.read_text())
            c['core_transmitted_photons']=s['transmitted_photons']
            c['core_only_bound']=s['core_only_dual_value']
        gc=path.with_suffix('.core.gaussian.json')
        if gc.exists():c['core_Gaussian_count_diagnostic']=json.loads(gc.read_text())
        convergence.append(c)
    checks={}
    for name in ['gate_weak_power','pilot_kerr_phi1','notebook_discrete_gate','matrixfree-gates','fixed-filter-step-audit','strang-crosscheck']:
        p=RAW/(name+'.toml')
        if p.exists():checks[name]=read_toml(p)
    for name in ['synthetic-checks-final','algebra-checks','finite-port-check','DC-reservoir-check']:
        p=RAW/(name+'.json')
        if p.exists():checks[name]=json.loads(p.read_text())
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((ROOT/'scripts').glob('readout_*')) if p.is_file()}
    vendor=RAW/'raman_bath_spectrum.jl'
    hashes['fetched_raman_bath_spectrum.jl']=hashlib.sha256(vendor.read_bytes()).hexdigest()
    result=dict(run_id=RUN,agent='gpt-a',model='gpt-6-astra',family='gpt',
        expected_reference_points=len(config['cases']),completed_reference_points=len(rows),
        status='exploratory finite-grid reference; convergence qualifications required',
        numerical_certificate_caveat='Dual formulas are rigorous for the supplied covariance. Floating-point eigensolves and Cholesky checks are not interval enclosures of the continuum propagation.',
        counting_caveat='Formal binary optima may be faint. Gaussian diagnostics add an explicitly recorded isotropic covariance completion when the numerical covariance violates uncertainty; they describe a nearby Gaussian state, not an unnoticed modification of the original table.',
        method='Full discrete RK4IP adjoint rows; matrix-free tangent/adjoint action for refinements',
        reference=rows,convergence=convergence,checks=checks,sha256=hashes)
    brightness=RAW/'anom_N1_z0.75_R.brightness.json'
    if brightness.exists():result['conditional_brightness_example']=json.loads(brightness.read_text())
    (DEST/'summary.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result

def fmt(v):return '—' if v is None else f'{v:.6g}'

def tables(s):
    text=['---','agent: gpt-a','model: gpt-6-astra','family: gpt',f'run: {RUN}','---','',
        '# Numerical tables for the readout study','',
        f'All numbers below are from run `{RUN}`. Generated from its saved outputs by '
        '`scripts/readout_compile_reference.py`; the interpretation and limitations are in the reference note.','',
        '## Formal linearized hierarchy and binary optimization','',
        'The last column is coherent photons in the best mask. Faint masks are formal values, not measurable counting upper values. All gaps are $10\\log_{10}(F_{\\rm best}/B)$.','',
        '| Case | $\\lambda_{\\min}(V)$ | $\\lambda_{\\rm pass}$ | $\\lambda_{\\rm gen}$ | Best bound | Best binary | Gap bound / gen / field (dB) | Photons |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in s['reference']:
        values=[r[k] for k in ['lambda_min','lambda_pass','lambda_gen','best_bound','best_binary_F']]
        gaps=' / '.join(f'{r[k]:.4g}' for k in ['gap_bound_dB','gap_gen_dB','gap_min_dB'])
        text.append('| `'+r['label']+'` | '+' | '.join(map(fmt,values))+' | '+gaps+f" | {r['transmitted_photons']:.3g} |")
    text+=['','## Cheap certificates','',
        '| Case | Full Weyl | Amplitude Weyl | Conjugate uncertainty | Positivity bound | Binary eigenvector |',
        '|---|---:|---:|---:|---:|---:|']
    for r in s['reference']:
        c=r['cheap_certificates'];values=[c[k] for k in ['full_Weyl','amplitude_Weyl','amplitude_uncertainty','nonnegative_vector_bound']]+[r['binary_eigen_bound']]
        text.append('| `'+r['label']+'` | '+' | '.join(map(fmt,values))+' |')
    text+=['','## Matrix-free refinements','',
        'Eigenvalues here are converged Ritz estimates where residual flags pass, not rigorous lower eigenvalue enclosures. '
        'The binary value is a feasible mask searched in the stated bright core; it is an upper trial value for the full grid. '
        'A core-only relaxation is never reported as a global bound.','',
        '| Case | $\\lambda_{\\min}(V)$ | $\\lambda_{\\rm pass}$ | $\\lambda_{\\rm gen}$ | Core binary | Core bins | Largest reported eigen residual |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for c in s['convergence']:
        residual=max(c[k]['residuals'][0] for k in ['field_eigen','amplitude_eigen','passive_eigen'])
        text.append('| `'+c['config']['label']+'` | '+' | '.join(fmt(c[k]) for k in ['lambda_min','lambda_pass','lambda_gen','best_binary_F'])+f" | {c['core_bins']} | {residual:.2g} |")
    text+=['','## Gaussian counting diagnostic','',
        'These values include quadratic Gaussian photon-count moments. The recorded isotropic completion makes a nearby numerical covariance physical; '
        'they must not be silently substituted for the original covariance.','',
        '| Case | Completion $\\delta I$ | Original mask full-count F | Best Gaussian-count mask F | Its coherent photons |',
        '|---|---:|---:|---:|---:|']
    for r in s['reference']:
        g=r.get('gaussian_count_diagnostic')
        if not g:continue
        text.append('| `'+r['label']+'` | '+' | '.join(fmt(g[k]) for k in ['isotropic_covariance_completion','original_formal_mask_Gaussian_F','best_Gaussian_F','best_mask_coherent_photons'])+' |')
    (DEST/'tables.md').write_text('\n'.join(text)+'\n')

if __name__=='__main__':
    summary=collect();tables(summary)
    print(json.dumps(dict(completed=summary['completed_reference_points'],expected=summary['expected_reference_points'],convergence=len(summary['convergence']))))
