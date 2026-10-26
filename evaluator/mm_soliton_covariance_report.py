#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.
Regenerate numerical reports and figures from retained raw runs.
"""
import hashlib
import argparse
import math
import json
import os
import platform
import subprocess
from pathlib import Path
import sys
import tomli
import yaml
import numpy as np
import scipy
from mm_soliton_covariance import IDENTITY,HBAR,KB,family,diffusion,readout,centre_phase_map,polynomial,dump
from mm_soliton_covariance_check import contraction

ROOT=Path(__file__).resolve().parents[1]
RAW=Path('~/analytical-nl-discovery-data')
PREFIX='2026-10-08-gpt-b-'
NOTE='explorations/2026-10-08-gpt-b-multimode-covariance.md'
TASK='T-20261008-gpt-b-01'
SCRIPTS=sorted(ROOT.glob('evaluator/mm_soliton_covariance*.*'))


def export(name,summary,config,solver_used=True):
    run_id=PREFIX+name;out=ROOT/'runs'/run_id;out.mkdir(parents=True,exist_ok=True)
    dump(out/'summary.json',summary)
    config={**IDENTITY,**config}
    (out/'config.yaml').write_text(yaml.safe_dump(config,sort_keys=False))
    commit=subprocess.check_output(['git','-C',str(ROOT/'solver'),'rev-parse','HEAD'],text=True).strip()
    dirty=bool(subprocess.check_output(['git','-C',str(ROOT/'solver'),'status','--porcelain'],text=True).strip())
    meta=dict(run_id=run_id,**IDENTITY,task=TASK,problem='P-20261004-claude-interactive-02',
        exploration=NOTE,solver_commit=commit,solver_dirty=dirty,solver_used=solver_used,
        raw_location=str(RAW/run_id),machine=platform.node(),hardware=platform.machine(),os=platform.platform(),
        python_version=platform.python_version(),julia_version='1.12.5',JULIA_NUM_THREADS=2,
        Julia_BLAS_threads=1,Julia_FFTW_threads=1,
        python_BLAS_threads='Not explicitly pinned in the original BVP/quadrature runs',
        numpy_version=np.__version__,scipy_version=scipy.__version__,wall_seconds=summary.get('elapsed_seconds'),
        timing_note='Where null, aggregate wall time was not separately captured; per-case timings remain in raw metadata.',
        reproduction_evaluator_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in SCRIPTS},
        scope=config.get('scope','Proposer calculation; not independent verification'))
    (out/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
    return out


def material():
    raw=RAW/(PREFIX+'covariance-material')
    s=tomli.loads((raw/'material.toml').read_text())
    errors={}
    for mode in ['grin','step']:
        a=np.load(raw/(mode+'_129.npz'));b=np.load(raw/(mode+'_257.npz'))
        errors[mode]=dict(S_max_relative_to_S0=float(np.max(np.abs(a['S']-b['S']))/b['S'][0,0,0,0]))
    s['grid_convergence']=errors
    extended=raw/'extended'/'material.toml'
    if extended.exists():s['extended_basis']=tomli.loads(extended.read_text())
    for mode,indices in [('grin02',[0,1]),('grin11',[0,2]),('step11',[0,1])]:
        ar=np.load(raw/('grin_257.npz' if mode.startswith('grin') else 'step_257.npz'))
        SS=ar['S'];over=np.array([[SS[m,m,n,n]/SS[0,0,0,0] for n in indices] for m in indices])
        s[mode+'_overlaps']=dict(s=over,C=2*over-np.diag(over.diagonal()))
        cal=s['grin_257' if mode.startswith('grin') else 'step_257']
        hbar=1.054571817e-34;t0=cal['T0_ps'];w0=cal['omega0_rad_ps']
        q=hbar*w0*1e12/(cal['P0_W']*t0*1e-12)
        b=np.asarray(cal['b'])[indices];d=np.asarray(cal['delta'])[indices]
        beta0=np.asarray(cal['beta0_per_m'])[indices]
        s[mode+'_normalization']=dict(q=q,photons_at_E2=2/q,
            energy_at_E2_pJ=2*cal['P0_W']*t0,
            compensated_frequency_offset_THz=d/b/t0/(2*np.pi),
            longitudinal_pair_beat_per_LD=abs(beta0[1]-beta0[0])*cal['LD_m'],
            balanced_gain_per_m_for_a_point1_nsp1=.1/cal['LD_m'],
            Raman_first_moment_ps=.18*2/.032/((1/.032)**2+(1/.0122)**2))
    export('covariance-material',s,dict(script='evaluator/mm_soliton_covariance_material.jl',
        command='JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_material.jl <raw_location>',
        wavelength_nm=1550.,T0_ps=.5,spatial_grids=[129,257],beta_order=5,
        dispersion_stencil_halfwidth_rad_ps=20.,dispersion_samples=13,
        grin=dict(core_radius_um=31.25,NA=.275),step=dict(V=3.3,NA=.03),
        scope='Analytic-profile silica material calibration; not measured commercial-fibre data'))


def comparison(sweep):
    cache={};scaled_cache={};out=[]
    for r in sweep['rows']:
        if r['name'].startswith('manakov'):continue
        p=r['p']
        if p not in cache:cache[p]=family(np.ones((2,2)),[2*(1-p),2*p])
        f=cache[p];X=readout(f,np.array(r['delta']));A=X@f['A']@np.linalg.inv(X)
        md=diffusion(f,np.array([[1.,.5],[.5,1.]]),np.array(r['delta']))
        refs={};rels={};nulls={};centre_refs={};centre_rels={};centre_actual={}
        for src in ['gain','raman']:
            ref=polynomial(A,X@md[src]@X.T);got=np.array(r['coefficients_over_q'][src])
            rat=np.divide(got,ref,out=np.zeros_like(got),where=np.abs(ref)>1e-12)-1
            rat=np.where(np.abs(ref)>1e-12,rat,np.nan)
            # JSON null labels a zero comparator, not an infinite relative error.
            rels[src]=[[[None if not np.isfinite(v) else float(v) for v in row] for row in mat] for mat in rat]
            refs[src]=ref;nulls[src]=np.where(np.abs(ref)<=1e-12,got,0.)
            Lf=centre_phase_map(r['N'],r['b'],r['delta'])
            Lm=centre_phase_map(f['N'],f['b'],r['delta'])
            actual=np.einsum('ia,kab,jb->kij',Lf,got,Lf)
            comparator=np.einsum('ia,kab,jb->kij',Lm,ref,Lm)
            rel=np.divide(actual,comparator,out=np.zeros_like(actual),where=abs(comparator)>1e-12)-1
            centre_refs[src]=comparator;centre_actual[src]=actual
            centre_rels[src]=[[[float(rel[k,i,j]) if abs(comparator[k,i,j])>1e-12 else None for j in range(6)] for i in range(6)] for k in range(3)]
        # A secondary comparator checks how much comes from the mean width.
        # Its common-sech variational width uses only the specified C,b,p;
        # no propagated covariance is used to choose kappa. Scaling the
        # isotropic Raman bath with kappa is an additional declared choice.
        fractions=np.asarray(r['N'])/sum(r['N'])
        kappa=float(fractions@np.asarray(r['C'])@fractions/(fractions@np.asarray(r['b'])))
        key=(p,kappa)
        if key not in scaled_cache:scaled_cache[key]=family(kappa*np.ones((2,2)),r['N'])
        sf=scaled_cache[key];SX=readout(sf,np.array(r['delta']));SA=SX@sf['A']@np.linalg.inv(SX)
        sd=diffusion(sf,kappa*np.array([[1.,.5],[.5,1.]]),np.array(r['delta']))
        sr={src:polynomial(SA,SX@sd[src]@SX.T) for src in ('gain','raman')}
        scaled=dict(kappa=kappa,reference_coefficients_over_q=sr,
            definition='C_mn=kappa; b_m=1; s11=s22=kappa, s12=kappa/2; same E,d,a,T0,T',
            kappa_choice='(p^T C p)/(sum p_m b_m), from the common-sech variational width',
            gain_timing_cubic_relative_difference=r['coefficients_over_q']['gain'][2][2][2]/sr['gain'][2,2,2]-1,
            Raman_timing_cubic_relative_difference=r['coefficients_over_q']['raman'][2][2][2]/sr['raman'][2,2,2]-1,
            Raman_carrier_phase_linear_relative_difference=r['coefficients_over_q']['raman'][0][5][5]/sr['raman'][0,5,5]-1,
            carrier_phase_cubic_reference_is_zero=True)
        out.append(dict(case=r['name'],p2=p,d=r['delta'],width_rescaled_Manakov=scaled,
            reference_coefficients=refs,relative_difference=rels,absolute_when_reference_zero=nulls,
            pulse_centre_phase_coefficients_over_q=centre_actual,
            pulse_centre_phase_reference_coefficients_over_q=centre_refs,
            pulse_centre_phase_relative_difference=centre_rels))
    return out


def base_runs():
    pilot=RAW/(PREFIX+'covariance-projection')/'summary.json'
    if pilot.exists():
        summary=json.loads(pilot.read_text())
        export('covariance-projection',summary,dict(script='evaluator/mm_soliton_covariance.py',
            command='python evaluator/mm_soliton_covariance.py <raw_location> --material <material_run> --quick',
            inputs=PREFIX+'covariance-material',nt=summary['nt'],window=summary['window'],
            scope='Retained initial four-case smoke calculation; superseded for claim coefficients by covariance-sweep'),solver_used=False)
    for name in ['covariance-sweep','covariance-limits','covariance-bath','covariance-prediction']:
        raw=RAW/(PREFIX+name);s=json.loads((raw/'summary.json').read_text())
        if name=='covariance-limits':
            if (raw/'extensions_algebra.json').exists():
                s['conditional_extensions_algebra']=json.loads((raw/'extensions_algebra.json').read_text())
                for row in s['conditional_extensions_algebra']['rows']:
                    row['quantum_gain_noise_bound_satisfied']=.1>=abs(row['Gamma'])/2
            cutoffs=[]
            for pair in ('grin02','grin11','step11'):
                fam=dict(np.load(RAW/(PREFIX+'covariance-sweep')/(pair+'_p0.2_physical.npz')))
                X=readout(fam,fam['d']);AY=X@fam['A']@np.linalg.inv(X)
                g=fam['g']*np.exp(-1j*fam['t'][:,None]*fam['d']/fam['b'])[:,:,None]
                F=fam['dt']*np.fft.fft(g,axis=0)
                white=X@diffusion(fam,fam['s'],fam['d'])['gain']@X.T
                full=polynomial(AY,white)
                for B in (4.,6.,8.,12.,20.,32.):
                    mask=abs(fam['k'])<=B
                    D=.1/2*np.real(np.einsum('kma,kmb,k->ab',F.conj(),F,mask))/(len(fam['t'])*fam['dt'])
                    coeff=polynomial(AY,X@D@X.T)
                    rel=np.divide(coeff-full,full,out=np.zeros_like(full),where=abs(full)>1e-12)
                    cv=np.einsum('k,kij->ij',4.**np.arange(1,4),coeff)
                    target=np.einsum('k,kij->ij',4.**np.arange(1,4),full)
                    cvscale=np.sqrt(target.diagonal()[:,None]*target.diagonal()[None,:])
                    cutoffs.append(dict(pair=pair,dimensionless_gain_half_bandwidth=B,
                        max_nonzero_coefficient_relative_error=float(np.max(abs(rel))),
                        relative_phase_linear_relative_error=rel[0,5,5],
                        relative_phase_cubic_relative_error=rel[2,5,5],
                        max_normalized_covariance_error_at_zeta4=float(np.max(abs(cv-target)/cvscale)),
                        background_mean_norm_over_q_at_zeta4=.1*(2*B/np.pi)*48.*4.))
            s['finite_gain_bandwidth']=cutoffs
        if name=='covariance-sweep':
            s['phase_reference']='Carrier phases at a fixed time origin; nominal fraction weights'
            s['manakov_comparisons']=comparison(s)
            if (raw/'stability.json').exists():s['stability']=json.loads((raw/'stability.json').read_text())
            bandwidth=[];balance=[]
            for row in s['rows']:
                if not (row['name'].endswith('physical') and row['p']==.2):continue
                pair=row['name'].split('_')[0]
                mat=np.load(RAW/(PREFIX+'covariance-material')/('grin_257.npz' if pair.startswith('grin') else 'step_257.npz'))
                fam=np.load(raw/(row['name']+'.npz'));indices=[0,2 if pair=='grin11' else 1]
                E=float(fam['N'].sum());delta_eff=float(fam['d'][1]/fam['b'][1]-fam['d'][0]/fam['b'][0])
                tr=.18*2/.032/((1/.032)**2+(1/.0122)**2)
                overlap_time=float(fam['dt']*np.sum(fam['f'][:,0]**2*fam['f'][:,1]**2))
                fp=-2*(tr/.5)*row['s'][0][1]*delta_eff*overlap_time/E
                predicted=2*KB*300*.5e-12/(HBAR*delta_eff*E)
                white_ratio=row['white_diffusion_over_q']['raman'][4][4]/abs(fp)
                exact_ratio=row['diffusion_over_q']['raman'][4][4]/abs(row['drift_raman'][4])
                mass=float(np.sum(fam['N']/fam['b']));rho_prime=2*fam['f']*fam['fp']
                product_prime=fam['fp'][:,0]*fam['f'][:,1]+fam['fp'][:,1]*fam['f'][:,0]
                bracket=float(fam['dt']*(np.einsum('tm,mn,tn->',rho_prime,fam['s'],rho_prime)
                    +2*fam['s'][0,1]*np.sum(product_prime**2)))
                fv=(tr/.5)*bracket/mass
                velocity_row=np.zeros(6);velocity_row[3]=E/mass;velocity_row[4]=delta_eff*E/mass
                velocity_ratio=2*KB*300*.5e-12/(HBAR*mass)
                white_velocity_ratio=(velocity_row@row['white_diffusion_over_q']['raman']@velocity_row)/fv
                exact_velocity_ratio=(velocity_row@row['diffusion_over_q']['raman']@velocity_row)/(velocity_row@row['drift_raman'])
                balance.append(dict(case=row['name'],delta_effective=delta_eff,first_moment_fraction_drift=fp,
                    thermal_ratio_prediction_over_q=predicted,white_ratio_over_q=white_ratio,
                    white_ratio_relative_error=white_ratio/predicted-1,
                    exact_spectrum_and_response_ratio_over_q=exact_ratio,
                    exact_ratio_relative_to_thermal_limit=exact_ratio/predicted-1,
                    first_moment_common_velocity_drift=fv,
                    thermal_velocity_ratio_prediction_over_q=velocity_ratio,
                    white_velocity_ratio_relative_error=white_velocity_ratio/velocity_ratio-1,
                    exact_velocity_ratio_over_q=exact_velocity_ratio,
                    exact_velocity_ratio_relative_to_thermal_limit=exact_velocity_ratio/velocity_ratio-1))
                field=fam['f']*np.exp(-1j*fam['t'][:,None]*fam['d']/fam['b'])
                spectral=abs(np.fft.fft(field,axis=0))**2;omega=abs(fam['k'])/.5
                order=np.argsort(omega);rows=[]
                for j,mode in enumerate(indices):
                    cumulative=np.cumsum(spectral[order,j])/spectral[:,j].sum()
                    cutoff=omega[order[np.searchsorted(cumulative,1-1e-6)]]
                    beta=mat['beta'][:,mode]
                    gvd=sum(abs(beta[n])*cutoff**(n-2)/math.factorial(n-2) for n in range(3,len(beta)))/abs(beta[2])
                    rows.append(dict(mode_index=mode,absolute_frequency_cutoff_rad_ps=cutoff,
                        excluded_spectral_energy_fraction=1e-6,
                        estimated_HOD_relative_GVD_bound=gvd,shock_bandwidth_ratio=cutoff/1215.2590756831312))
                bandwidth.append(dict(case=row['name'],modes=rows,
                    note='Triangle bound from fitted beta3 through beta5; omitted effects, not a propagated error estimate'))
            s['omitted_dispersion_and_shock_diagnostics']=bandwidth
            s['raman_exchange_balance']=balance
        if name=='covariance-prediction':
            L=centre_phase_map([s['energy']*(1-s['p2']),s['energy']*s['p2']],s['b'],s['d'])
            s['phase_reference']='Carrier phases at a fixed time origin; nominal fraction weights'
            s['pulse_centre_phase_coefficients_over_q']={k:np.einsum('ia,kab,jb->kij',L,v,L) for k,v in s['coefficients_over_q'].items()}
        config=dict(script={'covariance-sweep':'evaluator/mm_soliton_covariance.py',
            'covariance-limits':'evaluator/mm_soliton_covariance_limits.py',
            'covariance-bath':'evaluator/mm_soliton_covariance_sampler.py',
            'covariance-prediction':'evaluator/mm_soliton_covariance_prediction.py'}[name],
            inputs=s.get('profile',PREFIX+'covariance-material'),nt=s.get('nt',512),
            window=s.get('window',48.),T0_ps=s.get('T0_ps',.5),temperature_K=s.get('temperature_K',300.),
            seed=s.get('seed'),ntraj=s.get('ntraj'),
            scope=s.get('role','Stationary unequal-shape family and source quadratures; proposer calculation'))
        if name=='covariance-sweep':config.update(fractions=[.03,.1,.2,.4],energy=2.,gain_complex_psd_over_q=[.1,.1],
            mode_pairs=['grin02','grin11','step11','declared Manakov'],parameter_sets=['equal GVD, delta=1','actual modal GVD and walk-off'],
            secondary_Manakov_comparison='kappa=(p^T C p)/(sum p_m b_m); C_M=kappa, b_M=1, isotropic Raman Gram scaled by kappa',
            BVP_tolerance=2e-10,half_window=24.,max_BVP_nodes=30000,
            constrained_Hessian_cases='All three physical pairs at fractions 0.2 and 0.4')
        if name=='covariance-limits':config.update(weak_minority_fractions=[.002,.004,.008,.016,.032,.064],
            ideal_self_overlaps=[.5,.75],walkoff_values=[0.,1.,3.],
            quadrature_cases=[[256,48],[512,48],[1024,48],[1024,64],[8192,48]],
            walkoff_temperature_cases_K=[0.,77.,300.],gain_half_bandwidths=[4.,6.,8.,12.,20.,32.],
            extensions_script='evaluator/mm_soliton_covariance_extensions.py',
            conditional_gain_Gamma=[-.1,.03,.1,.3],conditional_gain_lengths=[.5,2.,4.],
            unequal_GVD_probe_fractions=[1e-4,1e-5,1e-6,1e-7],scaled_probe_sensitivities=True)
        if name=='covariance-bath':config.update(temperature_K=[0.,300.],
            beat_phase_distribution='uniform over [0,2pi)',temporal_noise='real Gaussian with coth spectrum',
            transverse_covariance='Gram of sampled phi01^2, phi02^2, phi01*phi02')
        if name=='covariance-prediction':config.update(p2=.35,energy=2.,gain_complex_psd_over_q=[.1,.1],
            zeta_targets=[.5,1.,2.,3.],propagated=False,secular_relative_tolerance=.002,
            freeze_commit='dc16c67')
        export(name,s,config,solver_used=False)
    raw=RAW/(PREFIX+'gain-calibration');s=tomli.loads((raw/'gain.toml').read_text())
    export('gain-calibration',s,dict(script='evaluator/mm_soliton_covariance_solver.jl',mode='gain',
        command='JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_solver.jl gain <raw_location>',
        seed=2026100802,ntraj=8192,nt=16,dt_ps=.25,dz_m=.125,length_m=1.,gain_per_m=.7,
        nsp=1.,noise_scale=.5,input_photons=1e6,
        scope='Unmodified scalar gain-noise backend versus a quantum-limited amplifier; no multimode ASE claim'))


def propagation(name):
    raw=RAW/(PREFIX+name);rows=[]
    for path in sorted(raw.rglob('*.toml')):
        m=tomli.loads(path.read_text());p=path.with_suffix('.npz')
        if not p.exists():continue
        r=contraction(m['profile'],p);r['solver_diagnostics']=m;rows.append(r)
        dump(path.with_name(path.stem+'_comparison.json'),{**IDENTITY,**r})
    powers={}
    growth=[r for r in rows if 'growth_z' in r['propagation']]
    if growth:
        for src,idx in [('gain',0),('raman',1)]:
            z=np.array([r['zeta'] for r in growth]);vals=np.array([r['covariance_over_q'][idx,5,5]-r['coefficients_over_q'][src][0,5,5]*r['zeta'] for r in growth])
            powers[src+'_relative_phase_cubic']=np.polyfit(np.log(z),np.log(vals),1)[0]
            vals=np.array([r['covariance_over_q'][idx,4,4] for r in growth]);powers[src+'_fraction']=np.polyfit(np.log(z),np.log(vals),1)[0]
        con=[r for r in rows if 'convergence_h' in r['propagation'] or 'growth_z4.0' in r['propagation']]
        step=np.array([r['solver_diagnostics']['dzeta'] for r in con]);err=np.array([r['max_normalized_error'] for r in con])
        powers['RK4IP_covariance_error']=np.polyfit(np.log(step),np.log(err),1)[0]
    comparisons=[]
    if name=='covariance-relaxed':
        def pick(pair,nm,step,raman=False,actual=False,nt=512):
            selected=[r for r in rows if r['solver_diagnostics'].get('pair')==pair
                and r['solver_diagnostics'].get('nm')==nm
                and abs(r['solver_diagnostics']['dzeta']-step)<1e-12
                and r['solver_diagnostics'].get('raman_mean',False)==raman
                and r['solver_diagnostics'].get('actual_energy_centroid_frequency_fraction_gradients',False)==actual
                and r['time_points']==nt]
            if len(selected)>1:raise ValueError('Ambiguous refinement selection')
            return selected[0] if selected else None
        def compare(label,coarse,fine):
            if coarse is None or fine is None:return
            expected=np.asarray(coarse['analytic_covariance_over_q'])
            diagonal=np.diagonal(expected,axis1=1,axis2=2)
            scale=np.sqrt(diagonal[:,:,None]*diagonal[:,None,:])
            difference=np.asarray(fine['covariance_over_q'])-np.asarray(coarse['covariance_over_q'])
            normalized=np.divide(difference,scale,out=np.zeros_like(difference),where=scale>1e-14)
            comparisons.append(dict(comparison=label,reference=coarse['propagation'],refined=fine['propagation'],
                max_normalized_covariance_difference=float(np.max(abs(normalized))),
                source_max_normalized_covariance_difference=np.max(abs(normalized),axis=(1,2)),
                normalized_covariance_difference=normalized,
                zero_scale_absolute_difference_over_q=np.where(scale<=1e-14,difference,0.)))
        for pair in ('grin02','grin11'):
            compare(pair+'_basis_6_to_11',pick(pair,6,.002),pick(pair,11,.002))
        compare('grin02_step_and_tensor_backend',pick('grin02',6,.002),pick('grin02',6,.001))
        for pair,nm in [('grin02',6),('grin11',6),('step11',3)]:
            compare(pair+'_nominal_to_actual_observable_gradients',pick(pair,nm,.002,True),pick(pair,nm,.002,True,True))
        compare('grin02_joint_temporal_and_step_refinement',pick('grin02',6,.002,True,True),pick('grin02',6,.001,True,True,1024))
    failure_path=raw/'launch_failures.json'
    failures=json.loads(failure_path.read_text()) if failure_path.exists() else []
    s=dict(**IDENTITY,task=TASK,rows=rows,measured_powers=powers,between_run_comparisons=comparisons,
           retained_launch_failures=failures,
           elapsed_seconds=sum(r['solver_diagnostics']['elapsed_seconds'] for r in rows))
    dump(raw/'summary.json',s)
    export(name,s,dict(script='evaluator/mm_soliton_covariance_timing.jl' if name=='covariance-timing' else 'evaluator/mm_soliton_covariance_solver.jl',
        contraction_script='evaluator/mm_soliton_covariance_check.py',
        profiles=PREFIX+'covariance-sweep',material=PREFIX+'covariance-material',
        adjoint_mode='discrete_rk4ip',no_shock=True,analytic_Raman_Fourier_kernel=True,
        task_local_model_adapter='CovarianceResponse: private dispatch for analytic Raman kernel and flat no-shock prefactor',
        solver_source_modified=False,temperature_K=300.,gain_complex_psd_over_q=.1,
        Raman_fraction=.18,Raman_tau1_ps=.0122,Raman_tau2_ps=.032,
        cases=[dict(time_points=int(r['time_points']),time_window=float(r['time_window']),
            **{k:r['solver_diagnostics'][k] for k in ('profile','pair','nm','zeta','dzeta','zspacing','raman_mean',
            'overlap_backend','actual_energy_centroid_frequency_fraction_gradients') if k in r['solver_diagnostics']}) for r in rows],
        scope='Full-field deterministic Jacobian contractions; source-specific leading weak-noise covariance'))


def figures():
    os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-b-matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter
    sweep=json.loads((ROOT/'runs'/(PREFIX+'covariance-sweep')/'summary.json').read_text())
    fig,axes=plt.subplots(2,2,figsize=(9,6.5),constrained_layout=True)
    names={'grin02':'GRIN LP01 + LP02','grin11':'GRIN LP01 + LP11a','step11':'Step-index LP01 + LP11a'}
    for pair,label in names.items():
        rr=[r for r in sweep['rows'] if r['name'].startswith(pair) and r['name'].endswith('physical')]
        cc=[r for r in sweep['manakov_comparisons'] if r['case'].startswith(pair) and r['case'].endswith('physical')]
        x=[r['p'] for r in rr]
        axes[0,0].plot(x,[100*r['relative_difference']['gain'][2][2][2] for r in cc],'o-',label=label)
        axes[0,1].plot(x,[100*r['relative_difference']['raman'][2][2][2] for r in cc],'o-')
        axes[1,0].plot(x,[100*r['relative_difference']['raman'][0][5][5] for r in cc],'o-')
        axes[1,1].plot(x,[r['coefficients_over_q']['raman'][2][5][5] for r in rr],'o-')
    for ax in axes.flat:ax.set_xlabel('Minority fraction p');ax.grid(alpha=.25)
    for ax in [axes[0,0],axes[0,1],axes[1,0]]:ax.axhline(0,color='k',lw=.7);ax.set_ylabel('Relative difference (%)')
    axes[0,0].set_title('Gain: timing cubic coefficient')
    axes[0,1].set_title('Raman: timing cubic coefficient')
    axes[1,0].set_title('Raman: carrier-referenced phase linear',fontsize=11)
    axes[1,1].set_title('Raman: carrier-referenced phase cubic',fontsize=11)
    axes[1,1].set_ylabel(r'$c_{\phi,3}/q$');axes[1,1].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
    axes[0,0].legend(fontsize=7.5)
    fig.suptitle('Same energy and fractions; actual modal GVD and walk-off\nDeclared Hermitian Raman bath, T₀ = 0.5 ps, 300 K',fontsize=10)
    fig.savefig(ROOT/'runs'/(PREFIX+'covariance-sweep')/'manakov_comparison.png',dpi=160);plt.close(fig)
    limits=json.loads((ROOT/'runs'/(PREFIX+'covariance-limits')/'summary.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(8,3.2),constrained_layout=True)
    for c,label in [(.5,'LP02'),(.75,'LP11a')]:
        rr=[r for r in limits['weak_minority'] if r['self_overlap']==c and r['delta']==1.]
        x=np.array([r['p'] for r in rr])
        for ax,src in zip(axes,['gain','raman']):
            yy=np.abs([r[src+'_relative_error'] for r in rr]);ax.loglog(x,yy,'o-',label=label)
            ax.loglog(x,yy[0]*x/x[0],'--',color='gray',alpha=.4)
            ax.set_title(src.capitalize()+': carrier-referenced phase cubic',fontsize=10);ax.set_xlabel('Minority fraction p');ax.set_ylabel('Relative asymptotic error');ax.grid(alpha=.2)
    axes[0].legend();fig.savefig(ROOT/'runs'/(PREFIX+'covariance-limits')/'weak_minority_error.png',dpi=160);plt.close(fig)
    adj=json.loads((ROOT/'runs'/(PREFIX+'covariance-adjoint')/'summary.json').read_text())
    rr=sorted([r for r in adj['rows'] if 'growth_z' in r['propagation']],key=lambda r:r['zeta'])
    fig,axes=plt.subplots(1,3,figsize=(10,3.2),constrained_layout=True)
    z=np.array([r['zeta'] for r in rr]);curve=np.geomspace(z.min(),z.max(),150)
    for ax,idx,power,title in [(axes[0],4,1,'Raman: fraction variance'),(axes[1],5,3,'Raman: phase cubic remainder')]:
        theory=rr[-1]['coefficients_over_q']['raman'][power-1][idx][idx]
        y=np.array([r['covariance_over_q'][1][idx][idx] for r in rr])
        if power==3:y-=np.array([r['coefficients_over_q']['raman'][0][idx][idx]*r['zeta'] for r in rr])
        ax.loglog(curve,theory*curve**power,label='BVP prediction')
        ax.loglog(z,y,'o',mfc='none',label='Discrete adjoint');ax.set_title(title,fontsize=10)
        ax.set_xlabel('Length ζ');ax.set_ylabel('Variance / q');ax.grid(alpha=.2)
    conv=sorted([r for r in adj['rows'] if 'convergence_h' in r['propagation'] or 'growth_z4.0' in r['propagation']],key=lambda r:r['solver_diagnostics']['dzeta'])
    h=np.array([r['solver_diagnostics']['dzeta'] for r in conv]);err=np.array([r['max_normalized_error'] for r in conv])
    axes[2].loglog(h,err,'o-',label='Covariance error');axes[2].loglog(h,err[0]*(h/h[0])**4,'--',label='Fourth power')
    axes[2].set_xlabel('RK4IP step');axes[2].set_ylabel('Normalized covariance error');axes[2].set_title('Propagation convergence',fontsize=10);axes[2].grid(alpha=.2)
    for ax in axes[:2]:
        ax.set_xticks([.5,1.,2.,4.],['0.5','1','2','4']);ax.xaxis.set_minor_formatter(NullFormatter())
    axes[2].set_xticks([.01,.02,.04],['0.01','0.02','0.04']);axes[2].xaxis.set_minor_formatter(NullFormatter())
    axes[0].legend(fontsize=8);axes[2].legend(fontsize=8)
    fig.savefig(ROOT/'runs'/(PREFIX+'covariance-adjoint')/'growth_and_convergence.png',dpi=160);plt.close(fig)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--raw-root',type=Path,default=RAW)
    ap.add_argument('--figures-only',action='store_true');args=ap.parse_args();RAW=args.raw_root
    if not args.figures_only:
        material();base_runs();propagation('covariance-adjoint');propagation('covariance-relaxed')
        if (RAW/(PREFIX+'covariance-timing')).exists():propagation('covariance-timing')
    figures()
    print('Figures regenerated.' if args.figures_only else 'Reports and figures regenerated from retained raw data.')
