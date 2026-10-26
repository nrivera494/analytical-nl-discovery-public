#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt"""
import json
import numpy as np
import yaml
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from p002_nextorder_summarize import register,write,PREFIX,ROOT,RAW,MAT

def main():
    response,dest=register('radiation-onset-response','scripts/p002_radiation_onset.py','propagate','bf3a649')
    convergence,_=register('radiation-onset-convergence','scripts/p002_radiation_onset.py','convergence','bf3a649')
    pilot,pilotdest=register('radiation-onset-pilot','scripts/p002_radiation_pilot.jl','single exploratory case','bf3a649')
    base=next(x for x in response['cases'] if x['parameters']['delta']==.85)
    convergence['slope_changes']=[dict(label=x['label'],difference=x['measured_slope']-base['measured_slope']) for x in convergence['cases']]
    datasets=[('pilot',pilot)]
    refinement_raw=RAW/(PREFIX+'radiation-onset-pilot-convergence')
    if len(list(refinement_raw.glob('*.toml')))==2:
        refinement,_=register('radiation-onset-pilot-convergence','scripts/p002_radiation_pilot.jl','convergence','bff8ed3')
        datasets.append(('pilot-convergence',refinement))
    for suffix,case in [(suffix,x) for suffix,data in datasets for x in data['cases']]:
        ff=np.load(RAW/(PREFIX+'radiation-onset-'+suffix)/(case['label']+'.npz'))
        dt=ff['tau'][1]-ff['tau'][0];t=ff['tau'];r=case['r']
        for j,row in enumerate(case['rows']):
            field=ff['fields'][:,:,0,j]/np.sqrt(MAT['P0_W'])
            peak=t[np.argmax(abs(field[:,0]))]
            row['LP03_outside_radius15']=float(np.sum(abs(field[abs(t-peak)>15,2])**2)*dt)
            # Post-hoc diagnostic of the long pilot, not a frozen capture law.
            mask=abs(t-peak)<10;power=abs(field[:,0])**2
            norm=float(np.sum(power[mask])*dt);eta=norm/2
            center=float(np.sum(t[mask]*power[mask])*dt/norm)
            freq=2*np.pi*np.fft.fftfreq(len(t),dt)
            deriv=np.fft.ifft(1j*freq*np.fft.fft(field[:,0]))
            velocity=float(np.sum((field[:,0].conj()*deriv).imag[mask])*dt/norm)
            xx=t-center
            profile=2*np.exp(-abs(eta*xx))/(1+np.exp(-2*abs(eta*xx)))
            psi=np.sqrt(eta/2)*profile*np.exp(1j*(velocity-case['parameters']['delta'])*xx)
            row['posthoc_pump_tracker']=dict(center=center,frequency=velocity,eta=eta,
                minority_projection=float(abs(np.vdot(psi,field[:,1])*dt)**2/(2*r)))
            row['formal_algebraic_fraction']=base['parameters']['B0']/(1+r*base['parameters']['Gamma']/base['parameters']['B0']*row['zeta'])
        q=[row for row in case['rows'] if row['zeta']>=199.999]
        slope=float(np.polyfit([x['zeta'] for x in q],[x['LP03_outside_radius15']/r**2 for x in q],1)[0])
        case['outside_energy_slope_divided_by_r_squared']=slope
        case['frozen_source_Gamma']=base['parameters']['Gamma']
        case['relative_discrepancy_from_frozen_source']=slope/base['parameters']['Gamma']-1
        e0=sum(case['rows'][0]['energies'])
        case['max_total_energy_drift']=max(abs(sum(x['energies'])-e0) for x in case['rows'])
        case['max_temporal_edge_fraction']=max(x['temporal_edge_fraction'] for x in case['rows'])
        case['max_posthoc_tracker_minus_formal_fraction']=max(abs(x['posthoc_pump_tracker']['minority_projection']-x['formal_algebraic_fraction']) for x in case['rows'])
    write('radiation-onset-convergence',convergence);write('radiation-onset-pilot',pilot)
    if len(datasets)==2:
        ref=pilot['cases'][0];refinement['comparisons']=[]
        for case in refinement['cases']:
            row=case['rows'][-1];old=ref['rows'][-1]
            refinement['comparisons'].append(dict(label=case['label'],
                radiation_slope_difference=case['outside_energy_slope_divided_by_r_squared']-ref['outside_energy_slope_divided_by_r_squared'],
                fixed_projection_difference=row['reference_projection']-old['reference_projection'],
                moving_projection_difference=row['posthoc_pump_tracker']['minority_projection']-old['posthoc_pump_tracker']['minority_projection'],
                pump_center_difference=row['posthoc_pump_tracker']['center']-old['posthoc_pump_tracker']['center'],
                max_temporal_edge_fraction=case['max_temporal_edge_fraction'],max_total_energy_drift=case['max_total_energy_drift']))
        write('radiation-onset-pilot-convergence',refinement)
    for suffix in ['response','convergence']+[suffix for suffix,_ in datasets]:
        file=ROOT/'runs'/(PREFIX+'radiation-onset-'+suffix)/'meta.yaml';meta=yaml.safe_load(file.read_text())
        meta.update(claim=None,exploration='explorations/2026-10-04-gpt-a-radiative-boundary-lead.md',prediction_commit='bf3a649')
        file.write_text(yaml.safe_dump(meta,sort_keys=False))
    fig,axs=plt.subplots(1,3,figsize=(14,3.7))
    for case in response['cases']:
        z=np.array([x['zeta'] for x in case['rows']]);energy=np.array([x['continuum_energy'] for x in case['rows']])
        line,=axs[0].plot(z,energy,'o-',label=f"δ={case['parameters']['delta']:g}",markersize=3)
        # Intercept is anchored only for a slope comparison, never fitted into Gamma.
        zz=np.array([200.,400.]);idx=np.argmin(abs(z-200))
        axs[0].plot(zz,energy[idx]+case['parameters']['Gamma']*(zz-200),'--',color=line.get_color())
    case=pilot['cases'][0];q=case['rows'];r=case['r']
    axs[1].plot([x['zeta'] for x in q],[x['LP03_outside_radius15']/r**2 for x in q],'o-',label='Full nonlinear pilot')
    axs[1].plot([x['zeta'] for x in base['rows']],[x['continuum_energy'] for x in base['rows']],label='Frozen-source continuum')
    axs[0].set(xlabel='ζ',ylabel='LP03 continuum coefficient',title='Dashed: stationary prediction slope')
    axs[1].set(xlabel='ζ',ylabel='LP03 radiation energy / r²',title='Exploratory r=0.006, δ=0.85')
    axs[2].plot([x['zeta'] for x in q],[x['reference_projection'] for x in q],'o-',label='Fixed reference')
    axs[2].plot([x['zeta'] for x in q],[x['posthoc_pump_tracker']['minority_projection'] for x in q],'o',label='Post-hoc moving reference')
    axs[2].plot([x['zeta'] for x in q],[x['formal_algebraic_fraction'] for x in q],'--',label='Formal algebraic reduction')
    axs[2].set(xlabel='ζ',ylabel='Minority fraction',title='Motion and depletion are distinct')
    for ax in axs:ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(pilotdest/'radiation.png',dpi=170);plt.close(fig)
    print(json.dumps(dict(response=[{k:v for k,v in x.items() if k not in ('rows','agent','model','family')} for x in response['cases']],
        convergence=convergence['slope_changes'],pilot=[{k:v for k,v in x.items() if k!='rows'} for x in pilot['cases']]),indent=2))

if __name__=='__main__':main()
