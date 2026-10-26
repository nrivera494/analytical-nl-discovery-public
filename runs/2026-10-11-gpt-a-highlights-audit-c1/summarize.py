"""Consolidate the three audit runs from saved results; gpt-a, gpt-6-astra, gpt."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
PROV=dict(agent='gpt-a',model='gpt-6-astra',family='gpt')
def load(c,name):return json.loads((ROOT/f'2026-10-11-gpt-a-highlights-audit-c{c}'/name).read_text())
def base(c):return dict(**PROV,run_id=f'2026-10-11-gpt-a-highlights-audit-c{c}',candidate=c,
    status='complete-bounded-audit',report='docs/review-2026-10-11-gpt-a-highlights-audit.md')
def save(c,out):
    out['outputs']=[p.name for p in sorted((ROOT/f'2026-10-11-gpt-a-highlights-audit-c{c}').glob('*.json')) if p.name!='summary.json']
    (ROOT/f'2026-10-11-gpt-a-highlights-audit-c{c}'/'summary.json').write_text(json.dumps(out,indent=2)+'\n')

out=base(1);rows=load(1,'refined.json')['rows'];out['scaling']=[]
for Z,ref in [(.5,1.570229157166407),(1.5,.3625049833090736)]:
    rr=[r for r in rows if r['Z']==Z and 'lambda_min' in r];nn=np.array([r['N'] for r in rr]);delta=np.array([r['lambda_min']*r['N']**2/ref-1 for r in rr])
    fit=lambda ix:float(np.polyfit(np.log(nn[ix]),np.log(abs(delta[ix])),1)[0])
    out['scaling'].append(dict(Z=Z,packet_Lambda_reference=ref,N=nn.tolist(),relative_errors=delta.tolist(),
      effective_c=(-delta*(nn*Z)**2).tolist(),error_exponent_all=fit(np.arange(len(nn))),error_exponent_N12_N20=fit(np.array([0,1])),
      independent_reduced=[r for r in rows if r['N']==192 and r['Z']==Z][0]))
small=[]
for Z in [.01,.02,.04,.08,.16]:
    a={r['N']:r for r in rows if r['Z']==Z};L=(4*a[800]['Lambda']-a[400]['Lambda'])/3;P=(4*a[800]['Pi']-a[400]['Pi'])/3
    small.append(dict(Z=Z,Lambda=L,Pi=P,Lambda_coefficient=(4*Z*Z*L-1)/Z,Pi_coefficient=(4*Z*Z*P-1)/Z))
out['small_Z_Richardson']=small
z=np.array([r['Z'] for r in small]);av=np.array([r['Lambda_coefficient'] for r in small]);pv=np.array([r['Pi_coefficient'] for r in small])
out['small_Z_quadratic_intercept']=dict(Lambda=float(np.polynomial.polynomial.polyfit(z,av,2)[0]),Pi=float(np.polynomial.polynomial.polyfit(z,pv,2)[0]),
    predicted_Lambda=float(2/np.sqrt(6)),predicted_Pi=float(np.sqrt(6)),
    Lambda_remainder_power=float(np.polyfit(np.log(z[:4]),np.log(z[:4]*abs(av[:4]-2/np.sqrt(6))),1)[0]))
cen=[r for r in load(1,'centroid.json')['rows'] if r.get('loss',0)==0]
conv=load(1,'convergence.json')['rows'];cen += [r for r in conv if 'F_centroid' in r]
out['centroid_max_relative_error_excluding_unphysical_loss_row']=max(abs(r['centroid_relative_error']) for r in cen)
r20=[r for r in rows if r['N']==20 and r['Z']==1.5][0];c20=[r for r in conv if r['N']==20][0]
out['Z1p5_N20_grid_step_relative_change']=c20['lambda_min']/r20['lambda_min']-1
r800=[r for r in rows if r['N']==800 and r['Z']==.01][0];c800=[r for r in conv if r['N']==800][0]
out['small_Z_grid_step_relative_change']=c800['Lambda']/r800['Lambda']-1
out['Raman']=load(1,'raman.json');out['Gaussian_Hamiltonian_small_Z']=load(1,'limits.json');save(1,out)

out=base(2);cl=load(2,'closed.json');out['closed']=cl
p8=load(2,'p8.json');linear=load(2,'p8_lin.json');sol=load(2,'p8_solver.json')
out['p8_compressed_timing_penalty']=(p8['compressed_input']+p8['compressed_ASE'])/(linear['compressed_input']+linear['compressed_ASE'])
out['p8_components']={k:p8[k] for k in ['compressed_input','compressed_ASE','energy_error','time_edge_fraction','frequency_edge_fraction']}
out['p8_solver_relative_difference']={}
for key,sk in [('C_in','C_in'),('C_ASE','C_ase')]:
    a=np.array(p8[key])[1:3,1:3];b=np.array(sol[sk])[:2,:2]*sol['N0']
    out['p8_solver_relative_difference'][key]=float(np.max(abs(a/b-1)))
out['fullfield']=[]
for r in load(2,'sweep.json')['rows']+load(2,'convergence.json')['rows']:
    C=np.array(r['C_in'])+np.array(r['C_ASE']);dd=np.sqrt(2/(2*np.arange(5)+1));ev=np.linalg.eigvalsh(C[4:,4:]*dd[:,None]*dd[None,:])
    rr={k:r[k] for k in ['case','eps','gL','edge','gbw','refine','compressed_input','compressed_ASE','energy_error']}
    rr.update(s1_ASE=r['C_ASE'][5][5],spectral_eigenvalue_ratio=float(ev[-2]/ev[-1]),phase_residual=float(1-C[0,3]**2/(C[0,0]*C[3,3])))
    if r['case']=='asym':
        U=r['gL'];freq=1+3*(1-np.exp(-U/3));comp=U*U/9+U*U/3-2*U+6*(1-np.exp(-U/3))
        rr['frequency_relative_error_to_leading']=C[2,2]/(2/(5*r['eps']**2)*freq)-1
        rr['compressed_relative_error_to_leading']=(r['compressed_input']+r['compressed_ASE'])/(comp/5)-1
    out['fullfield'].append(rr)
out['shape_RK4IP']=load(2,'shape.json');save(2,out)

out=base(3);rows=load(3,'dispersion.json')['rows'];out['completed_dispersion_rows']=len(rows);out['dispersion_fits']=[]
for shape in ['gaussian','quartic']:
 for Phi in [2,5,10,20]:
    rr=[r for r in rows if r['shape']==shape and r['Phi']==Phi and r['y']<=1e-4 and r['nt']==4096]
    power=float(np.polyfit(np.log([r['y'] for r in rr]),np.log([r['relative_excess'] for r in rr]),1)[0])
    out['dispersion_fits'].append(dict(shape=shape,Phi=Phi,power=power,range_y=[1e-6,1e-4],
      min_prefactor_ratio=min(r['prefactor_ratio'] for r in rr),max_prefactor_ratio=max(r['prefactor_ratio'] for r in rr)))
out['dispersion_convergence']=[]
for r in rows:
 if r['phase_step']==.0125:
    original=next(s for s in rows if s['shape']==r['shape'] and s['Phi']==r['Phi'] and s['y']==r['y'] and s['phase_step']==.025)
    out['dispersion_convergence'].append(dict(shape=r['shape'],Phi=r['Phi'],y=r['y'],relative_change=r['lambda_min']/original['lambda_min']-1))
al=load(3,'algebra.json');out['parity_Rayleigh']=al['parity_rayleigh'];out['physical_attenuator_Kerr_counterexample']=al['physical_attenuator_Kerr_counterexample']
out['maximum_polarization_relative_error']=max(abs(r['relative_error']) for r in al['polarization'])
out['maximum_arbitrary_shear_relative_error']=max(abs(r['relative_error']) for r in al['arbitrary_shear'])
out['raman_band']=load(3,'raman_band.json')['rows'];out['raman_convergence']=load(3,'raman_convergence.json')['rows'];out['Kerr_momentum']=load(3,'momentum.json');save(3,out)
print('Saved three completed bounded-audit summaries; failed rows remain separately preserved.')
